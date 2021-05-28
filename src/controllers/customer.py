from flask import request
from flask_restplus import Resource
from src.server.server import server
from src.db_models.db_models import Customer as CustomerModel
from sqlalchemy import update, delete
from src.db_models.database import db_session
from src.utils.auth import auth_user
from src.utils.utils import return_dict
import json
from src.rest_models.customer_rest_models import customer_rest_model, \
    customer_email_rest_model, customer_response_rest_model

app = server.app
api = server.api

@api.route('/cliente')
class Customer(Resource):

    @api.doc(params={'customer_email': 'E-mail do cliente'})
    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error'
    })
    @api.response(200, 'Success', customer_response_rest_model)
    def get(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401

        customer_email = request.args.get("customer_email")

        if not customer_email:
            return return_dict('É necessário passar o parâmetro customer_email'), 400

        try:
            results = db_session.query(CustomerModel).filter_by(email=customer_email).first()
            if not results:
                return return_dict("Email not found"), 404

            results = str(results)
            results = json.loads(results)

            return results, 200
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
    @api.expect(customer_rest_model, validate=True)
    def post(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401


        customer_body = request.json

        customer_name = customer_body['customer_name']
        customer_email = customer_body['customer_email']

        try:
            email_already_exists = db_session.query(CustomerModel).filter_by(email=customer_email).first()
            if email_already_exists:
                return return_dict(f"Email '{customer_email}' já cadastrado"), 406

            customer_handler = CustomerModel(customer_name, customer_email)
            db_session.add(customer_handler)
            db_session.commit()
            return return_dict(f'Cliente {customer_name} cadastrado com sucesso'), 200
        except Exception as e:
            return return_dict(e), 500


    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(customer_rest_model, validate=True)
    def put(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401
        customer_body = request.json


        customer_name = customer_body['customer_name']
        customer_email = customer_body['customer_email']

        try:
            email_already_exists = db_session.query(CustomerModel).filter_by(email=customer_email).first()
            if not email_already_exists:
                return return_dict(f"Email '{customer_email}' não existe"), 404

            statement = update(CustomerModel).where(CustomerModel.email == customer_email).values(name=customer_name). \
                execution_options(synchronize_session="fetch")

            result = db_session.execute(statement)
            num_rows_matched = result.rowcount
            db_session.commit()

            if num_rows_matched == 0:
                return return_dict("Não foi possível atualizar o cliente"), 500

            return return_dict(f'Cliente com e-mail {customer_email} atualizado com sucesso'), 200
        except Exception as e:
            return return_dict(e), 500


    @api.doc(responses={
        401: 'Unauthenticated',
        400: 'Bad request',
        404: 'Not found',
        500: 'Internal server error',
        200: 'Success'
    })
    @api.expect(customer_email_rest_model, validate=True)
    def delete(self):
        if not auth_user(request):
            return return_dict("É necessário autenticar com usuário e senha validos"), 401

        customer_body = request.json
        customer_email = customer_body['customer_email']

        try:
            email_already_exists = db_session.query(CustomerModel).filter_by(email=customer_email).first()
            if not email_already_exists:
                return return_dict(f"Email '{customer_email}' não existe"), 404

            statement = delete(CustomerModel).where(CustomerModel.email == customer_email). \
                execution_options(synchronize_session="fetch")

            result = db_session.execute(statement)
            num_rows_matched = result.rowcount
            db_session.commit()

            if num_rows_matched == 0:
                return return_dict("Não foi possível deletar o cliente"), 500

            return return_dict(f'Cliente com e-mail: {customer_email} apagado com sucesso'), 200
        except Exception as e:
            return return_dict(e), 500


