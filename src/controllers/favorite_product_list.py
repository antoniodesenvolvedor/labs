from flask import request
from flask_restplus import Resource
from src.db_models.db_models import Customer, FavoriteListItem
from sqlalchemy import delete
from src.db_models.database import db_session
from src.server.server import server
from src.integration.product_api import ProductAPI
import json
from src.utils.auth import auth_user
from src.utils.utils import return_dict
from src.rest_models.favorite_product_list_models import customer_product_rest_model

app = server.app
api = server.api

@api.route('/lista_favoritos')
class FavoriteProductList(Resource):

    @api.doc(params={'customer_email': 'E-mail do cliente'})
    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error'
    })
    @api.response(200, 'Success', customer_product_rest_model)
    def get(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401

        customer_email = request.args.get("customer_email")

        if not customer_email:
            return return_dict('É necessário passar o parâmetro customer_email'), 400

        try:
            email_already_exists = db_session.query(Customer).filter_by(email=customer_email).first()
            if not email_already_exists:
                return return_dict(f"Email '{customer_email}' não existe"), 404

            query_result = db_session.query(FavoriteListItem, Customer) \
                .filter(Customer.customer_id == FavoriteListItem.customer_id) \
                .filter(Customer.email == customer_email) \
                .all()

            if not query_result:
                return return_dict("Lista de favoritos não encontrada"), 404

            product_favorite_list = [{'customer_email': item[1].email, 'product_id': item[0].product_id}
                                     for item in query_result]

            return product_favorite_list, 200
        except Exception as e:
            return return_dict(e), 500

    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        406: 'Not allowed',
        200: 'Success'
    })
    @api.expect(customer_product_rest_model, validate=True)
    def post(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401

        product_body = request.json

        customer_email = product_body['customer_email']
        product_id = product_body['product_id']

        try:
            customer = db_session.query(Customer).filter_by(email=customer_email).first()
            if not customer:
                return return_dict(f"Email '{customer_email}' inexistente"), 404

            status_code, product_response = ProductAPI.get_product_by_id_api(product_id)

            if status_code == 404:
                return return_dict(f'ID produto inexistente {product_id}'), 404
            elif status_code != 200:
                return \
                    return_dict(f'Erro ao consultar produto na api de produtos, {product_response}'), \
                    status_code

            product = json.loads(product_response)
            product_id = product['id'] if 'id' in product else None

            if not product_id:
                return \
                    return_dict(f'Erro ao consultar produto na api de produtos, {product_response}'), \
                    status_code

            product_already_in_list = db_session.query(FavoriteListItem, Customer) \
                .filter(FavoriteListItem.customer_id == Customer.customer_id) \
                .filter(Customer.email == customer_email) \
                .filter(FavoriteListItem.product_id == product_id) \
                .first()

            if product_already_in_list:
                return return_dict(f'Produto já cadastrado na lista do cliente {customer_email}'), 406

            favorite_list_item_handler = FavoriteListItem(
                customer_id=customer.customer_id,
                product_id=product_id
            )

            db_session.add(favorite_list_item_handler)
            db_session.commit()

            return return_dict("Item adicionado com sucesso"), 200

        except Exception as e:
            return return_dict(e), 500


    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(customer_product_rest_model, validate=True)
    def delete(self, ):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401

        product_body = request.json

        customer_email = product_body['customer_email']
        product_id = product_body['product_id']

        try:
            customer = db_session.query(Customer).filter_by(email=customer_email).first()
            if not customer:
                return return_dict(f"Email '{customer_email}' inexistente"), 404

            favorite_list_item = db_session.query(Customer, FavoriteListItem) \
                .filter(Customer.customer_id == FavoriteListItem.customer_id) \
                .filter(FavoriteListItem.product_id == product_id) \
                .filter(Customer.email == customer_email) \
                .first()

            if not favorite_list_item:
                return return_dict(f"Item inexistente na lista do cliente {customer_email}"), 404

            favorite_list_item_id = favorite_list_item[1].favorite_list_item_id

            statement = delete(FavoriteListItem).where(FavoriteListItem.favorite_list_item_id == favorite_list_item_id) \
                .execution_options(synchronize_session='fetch')

            result = db_session.execute(statement)
            num_rows_matched = result.rowcount
            db_session.commit()

            if num_rows_matched == 1:
                return return_dict("Item deletado com sucesso"), 200
            else:
                return return_dict("Houve algum erro ao deletar o item"), 500
        except Exception as e:
            return return_dict(e), 500
