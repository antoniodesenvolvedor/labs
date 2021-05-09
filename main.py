from flask import Flask, request
import json
import traceback
from customer import Customer
from product_api import ProductAPI
from product_favorite_list import ProductFavoriteList


app = Flask(__name__)



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



@app.route('/cliente', methods=['GET'])
def fetch_customer():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    customer_email = request.args.get("customer_email")

    if not customer_email:
        return 'É necessário passar o parâmetro customer_email', 400

    try:
        customer_handler = Customer()
        customer_result = customer_handler.fetch_customer(customer_email)

        if not customer_result:
            return "Email not found", 404

        customer_name = customer_result[0][0]
        customer_email = customer_result[0][1]

        customer_result = {
            'customer_name': customer_name,
            'customer_email': customer_email
        }

        customer_result = json.dumps(customer_result)
        return customer_result, 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente', methods=['POST'])
def insert_customer():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    customer_body = request.json

    if not customer_body:
        return 'Corpo da requisição faltante', 400
    if 'customer_name' not in customer_body:
        return 'É necessário informar a chave customer_name no corpo da requisição', 400
    if 'customer_email' not in customer_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customer(customer_email)
        if email_already_exists:
            return f'Email "{customer_email}" já cadastrado', 406

        successful_operation = customer_handler.insert_customer(customer_email, customer_name)
        if not successful_operation:
            return "Não foi possível inserir o cliente", 500

        return f'Cliente {customer_name} cadastrado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente/<customer_email>', methods=['DELETE'])
def delete_customer(customer_email):
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    try:
        customer_handler = Customer()

        email_already_exists = customer_handler.fetch_customer(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        successful_operation = customer_handler.delete_customer(customer_email)
        if not successful_operation:
            return "Não foi possível deletar o cliente", 500

        return f'Cliente com e-mail: {customer_email} apagado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente/', methods=['PUT'])
def update_customer():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403
    customer_body = request.json

    if not customer_body:
        return 'Corpo da requisição faltante', 400
    if 'customer_name' not in customer_body:
        return 'É necessário informar a chave customer_name no corpo da requisição', 400
    if 'customer_email' not in customer_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customer(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        successful_operation = customer_handler.update_customer(customer_email, customer_name)
        if not successful_operation:
            return "Não foi possível atualizar o cliente", 500

        return f'Cliente com e-mail {customer_email} atualizado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/lista_favoritos', methods=['GET'])
def fetch_favorite_list():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    customer_email = request.args.get("customer_email")

    if not customer_email:
        return 'É necessário passar o parâmetro customer_email', 400

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customer(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" inexistente', 404

        product_favorite_list_handler = ProductFavoriteList()
        product_favorite_list = product_favorite_list_handler.fetch_favorite_list_items(customer_email)

        if not product_favorite_list:
            return "Lista de favoritos não encontrada", 404

        print(product_favorite_list)
        product_favorite_list = [{'customer_email': item[0], 'product_id': item[1]}
                                 for item in product_favorite_list]
        # product_favorite_list =  [item[0] for item in product_favorite_list]


        product_favorite_list = json.dumps(product_favorite_list)
        return product_favorite_list, 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/lista_favoritos', methods=['POST'])
def insert_favorite_item():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    product_body = request.json

    if not product_body:
        return 'Corpo da requisição faltante', 400
    if 'customer_email' not in product_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400
    if 'product_id' not in product_body:
        return 'É necessário informar a chave product_id no corpo da requisição', 400

    customer_email = product_body['customer_email']
    product_id = product_body['product_id']

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customer(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" inexistente', 404

        status_code, product_response = ProductAPI.get_product_by_id_api(product_id)

        if status_code == 404:
            return f'ID produto inexistente {product_id}', 404
        elif status_code != 200:
            return f'Erro ao consultar produto na api de produtos, response {product_response}', status_code

        product = json.loads(product_response)
        product_id = product['id'] if 'id' in product else None

        if not product_id:
            return f'Erro ao consultar produto na api de produtos, resposne {product_response}', status_code



        product_favorite_list_handler = ProductFavoriteList()
        product_already_in_list = product_favorite_list_handler.get_favorite_list_item(customer_email, product_id)

        if product_already_in_list:
            return f'Produto já cadastrado na lista do cliente {customer_email}', 400

        was_item_added = product_favorite_list_handler.add_favorite_list_item(customer_email, product_id)

        if was_item_added:
            return "Item adicionado com sucesso", 200
        else:
            return "Houve algum erro ao adicionar o item", 500
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/lista_favoritos', methods=['DELETE'])
def delete_favorite_item():
    if not auth_user(request):
        return "É necessário autenticar com usuário e senha validos", 403

    product_body = request.json

    if not product_body:
        return 'Corpo da requisição faltante', 400
    if 'customer_email' not in product_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400
    if 'product_id' not in product_body:
        return 'É necessário informar a chave product_id no corpo da requisição', 400

    customer_email = product_body['customer_email']
    product_id = product_body['product_id']

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customer(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" inexistente', 404

        product_favorite_list_handler = ProductFavoriteList()
        product_already_in_list = product_favorite_list_handler.get_favorite_list_item(customer_email, product_id)
        if not product_already_in_list:
            return f'Produto não encontrado na lista do cliente {customer_email}', 404

        was_item_deleted = product_favorite_list_handler.delete_favorite_list_item(customer_email, product_id)

        if was_item_deleted:
            return "Item deletado com sucesso", 200
        else:
            return "Houve algum erro ao deletar o item", 500
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)