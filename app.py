from flask import Flask, request
import json
import traceback
from product_api import ProductAPI
from database import db_session, init_db
from models import Customer, FavoriteListItem
from sqlalchemy import update, delete

app = Flask(__name__)
init_db()


def return_message_json(message):
    return json.dumps({"message": message})


def auth_user(request):
    try:
        username = request.authorization.username
        password = request.authorization.password

        if username != 'labs' or password != 'labs_123':
            return False
        else:
            return True
    except Exception as e:
        return False


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


@app.route('/cliente', methods=['GET'])
def fetch_customer():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    customer_email = request.args.get("customer_email")

    if not customer_email:
        return return_message_json('É necessário passar o parâmetro customer_email'), 400

    try:
        results = db_session.query(Customer).filter_by(email=customer_email).first()
        if not results:
            return return_message_json("Email not found"), 404

        results = str(results)
        return results, 200
    except Exception as e:
        return return_message_json(e), 500


@app.route('/cliente', methods=['POST'])
def insert_customer():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    customer_body = request.json

    if not customer_body:
        return return_message_json('Corpo da requisição faltante'), 400
    if 'customer_name' not in customer_body:
        return return_message_json('É necessário informar a chave customer_name no corpo da requisição'), 400
    if 'customer_email' not in customer_body:
        return return_message_json('É necessário informar a chave customer_email no corpo da requisição'), 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        email_already_exists = db_session.query(Customer).filter_by(email=customer_email).first()
        if email_already_exists:
            return return_message_json(f"Email '{customer_email}' já cadastrado"), 406

        customer_handler = Customer(customer_name, customer_email)
        db_session.add(customer_handler)
        db_session.commit()
        return return_message_json(f'Cliente {customer_name} cadastrado com sucesso'), 200
    except Exception as e:
        return return_message_json(e), 500


@app.route('/cliente/<customer_email>', methods=['DELETE'])
def delete_customer(customer_email):
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    try:
        email_already_exists = db_session.query(Customer).filter_by(email=customer_email).first()
        if not email_already_exists:
            return return_message_json(f"Email '{customer_email}' não existe"), 404

        statement = delete(Customer).where(Customer.email == customer_email). \
            execution_options(synchronize_session="fetch")

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 0:
            return return_message_json("Não foi possível deletar o cliente"), 500

        return return_message_json(f'Cliente com e-mail: {customer_email} apagado com sucesso'), 200
    except Exception as e:
        return return_message_json(e), 500


@app.route('/cliente', methods=['PUT'])
def update_customer():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403
    customer_body = request.json

    if not customer_body:
        return return_message_json('Corpo da requisição faltante'), 400
    if 'customer_name' not in customer_body:
        return return_message_json('É necessário informar a chave customer_name no corpo da requisição'), 400
    if 'customer_email' not in customer_body:
        return return_message_json('É necessário informar a chave customer_email no corpo da requisição'), 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        email_already_exists = db_session.query(Customer).filter_by(email=customer_email).first()
        if not email_already_exists:
            return return_message_json(f"Email '{customer_email}' não existe"), 404

        statement = update(Customer).where(Customer.email == customer_email).values(name=customer_name). \
            execution_options(synchronize_session="fetch")

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 0:
            return return_message_json("Não foi possível atualizar o cliente"), 500

        return return_message_json(f'Cliente com e-mail {customer_email} atualizado com sucesso'), 200
    except Exception as e:
        return return_message_json(e), 500


@app.route('/lista_favoritos', methods=['GET'])
def fetch_favorite_list():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    customer_email = request.args.get("customer_email")

    if not customer_email:
        return return_message_json('É necessário passar o parâmetro customer_email'), 400

    try:
        email_already_exists = db_session.query(Customer).filter_by(email=customer_email).first()
        if not email_already_exists:
            return return_message_json(f"Email '{customer_email}' não existe"), 404

        query_result = db_session.query(FavoriteListItem, Customer) \
            .filter(Customer.customer_id == FavoriteListItem.customer_id) \
            .filter(Customer.email == customer_email) \
            .all()

        if not query_result:
            return return_message_json("Lista de favoritos não encontrada"), 404

        product_favorite_list = [{'customer_email': item[1].email, 'product_id': item[0].product_id}
                                 for item in query_result]

        product_favorite_list = json.dumps(product_favorite_list)
        return product_favorite_list, 200
    except Exception as e:
        return return_message_json(e), 500


@app.route('/lista_favoritos', methods=['POST'])
def insert_favorite_item():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    product_body = request.json

    if not product_body:
        return return_message_json('Corpo da requisição faltante'), 400
    if 'customer_email' not in product_body:
        return return_message_json('É necessário informar a chave customer_email no corpo da requisição'), 400
    if 'product_id' not in product_body:
        return return_message_json('É necessário informar a chave product_id no corpo da requisição'), 400

    customer_email = product_body['customer_email']
    product_id = product_body['product_id']

    try:
        customer = db_session.query(Customer).filter_by(email=customer_email).first()
        if not customer:
            return return_message_json(f"Email '{customer_email}' inexistente"), 404

        status_code, product_response = ProductAPI.get_product_by_id_api(product_id)

        if status_code == 404:
            return return_message_json(f'ID produto inexistente {product_id}'), 404
        elif status_code != 200:
            return \
                return_message_json(f'Erro ao consultar produto na api de produtos, {product_response}'),\
                status_code

        product = json.loads(product_response)
        product_id = product['id'] if 'id' in product else None

        if not product_id:
            return \
            return_message_json(f'Erro ao consultar produto na api de produtos, {product_response}'),\
            status_code

        product_already_in_list = db_session.query(FavoriteListItem, Customer) \
            .filter(FavoriteListItem.customer_id == Customer.customer_id) \
            .filter(Customer.email == customer_email) \
            .filter(FavoriteListItem.product_id == product_id) \
            .first()

        if product_already_in_list:
            return return_message_json(f'Produto já cadastrado na lista do cliente {customer_email}'), 400

        favorite_list_item_handler = FavoriteListItem(
            customer_id=customer.customer_id,
            product_id=product_id
        )

        db_session.add(favorite_list_item_handler)
        db_session.commit()

        return return_message_json("Item adicionado com sucesso"), 200

    except Exception as e:
        return return_message_json(e), 500


@app.route('/lista_favoritos', methods=['DELETE'])
def delete_favorite_item():
    if not auth_user(request):
        return return_message_json("É necessário autenticar com usuário e senha validos"), 403

    product_body = request.json

    if not product_body:
        return return_message_json('Corpo da requisição faltante'), 400
    if 'customer_email' not in product_body:
        return return_message_json('É necessário informar a chave customer_email no corpo da requisição'), 400
    if 'product_id' not in product_body:
        return return_message_json('É necessário informar a chave product_id no corpo da requisição'), 400

    customer_email = product_body['customer_email']
    product_id = product_body['product_id']

    try:
        customer = db_session.query(Customer).filter_by(email=customer_email).first()
        if not customer:
            return return_message_json(f"Email '{customer_email}' inexistente"), 404

        favorite_list_item = db_session.query(Customer, FavoriteListItem) \
            .filter(Customer.customer_id == FavoriteListItem.customer_id) \
            .filter(FavoriteListItem.product_id == product_id) \
            .filter(Customer.email == customer_email) \
            .first()

        if not favorite_list_item:
            return return_message_json(f"Item inexistente na lista do cliente {customer_email}"), 404

        favorite_list_item_id = favorite_list_item[1].favorite_list_item_id

        statement = delete(FavoriteListItem).where(FavoriteListItem.favorite_list_item_id == favorite_list_item_id) \
            .execution_options(synchronize_session='fetch')

        result = db_session.execute(statement)
        num_rows_matched = result.rowcount
        db_session.commit()

        if num_rows_matched == 1:
            return return_message_json("Item deletado com sucesso"), 200
        else:
            return return_message_json("Houve algum erro ao deletar o item"), 500
    except Exception as e:
        return return_message_json(e), 500


if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', port=5000, debug=False)
