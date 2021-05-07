from flask import Flask, request
import json
from customer import Customer
import traceback
from products import Products




app = Flask(__name__)

@app.route('/cliente', methods=['GET'])
def fetch_customer():

    customer_email = request.args.get("customer_email")

    if not customer_email:
        return 'É necessário passar o parâmetro customer_email', 400

    try:
        customer_handler = Customer()
        customer_result = customer_handler.fetch_customers(customer_email)

        if not customer_result:
            return "Email not found", 404


        customer_name = customer_result[0][0]
        customer_email = customer_result[0][1]

        customer_result = {
            'customer_name':customer_name,
            'customer_email':customer_email
        }

        customer_result = json.dumps(customer_result)
        return customer_result, 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente', methods=['POST'])
def insert_customer():
    customer_body = request.json
    if 'customer_name' not in customer_body:
        return 'É necessário informar a chave customer_name no corpo da requisição', 400
    if 'customer_email' not in customer_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        customer_handler = Customer()

        email_already_exists = customer_handler.fetch_customers(customer_email)
        if email_already_exists:
            return f'Email "{customer_email}" já cadastrado', 406

        sucessful_operation = customer_handler.insert_customer(customer_email, customer_name)
        if not sucessful_operation:
            return "Não foi possível inserir o cliente", 500

        return f'Cliente {customer_name} cadastrado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente/<customer_email>', methods=['DELETE'])
def delete_customer(customer_email):
    try:
        customer_handler = Customer()

        email_already_exists = customer_handler.fetch_customers(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        sucessful_operation = customer_handler.delete_customer(customer_email)
        if not sucessful_operation:
            return "Não foi possível deletar o cliente", 500

        return f'Cliente com e-mail: {customer_email} apagado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/cliente/', methods=['PUT'])
def update_customer():
    customer_body = request.json
    if 'customer_name' not in customer_body:
        return 'É necessário informar a chave customer_name no corpo da requisição', 400
    if 'customer_email' not in customer_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400

    customer_name = customer_body['customer_name']
    customer_email = customer_body['customer_email']

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customers(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        sucessful_operation = customer_handler.update_customers(customer_email, customer_name)
        if not sucessful_operation:
            return "Não foi possível atualizar o cliente", 500

        return f'Cliente com e-mail {customer_email} atualizado com sucesso', 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/lista_favoritos', methods=['GET'])
def fetch_favorite_list():
    customer_email = request.args.get("customer_email")

    if not customer_email:
        return 'É necessário passar o parâmetro customer_email', 400

    try:
        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customers(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        product_handler = Products()
        product_list = product_handler.fetch_favorite_list(customer_email)

        if not product_list:
            return "Lista não encontrada", 404

        product_list = json.dumps(product_list)
        return product_list, 200
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500



@app.route('/lista_favoritos', methods=['POST'])
def insert_favorite_item():
    product_body = request.json

    if 'customer_email' not in product_body:
        return 'É necessário informar a chave customer_email no corpo da requisição', 400
    if 'product_id' not in product_body:
        return 'É necessário informar a chave product_id no corpo da requisição', 400

    customer_email = product_body['customer_email']
    product_id = product_body['product_id']

    try:

        customer_handler = Customer()
        email_already_exists = customer_handler.fetch_customers(customer_email)
        if not email_already_exists:
            return f'Email "{customer_email}" não existe', 404

        product = Products.get_product_by_id_api(product_id)
        product = json.loads(product)
        if not product:
            return f'ID produto não inexistente {product_id}', 404

        product_handler = Products()
        was_item_added = product_handler.add_items_to_favorite_list(customer_email, product )

        if was_item_added:
            return "Item adicionado com sucesso", 200
        else:
            return "Houve algum erro ao adicionar o item", 500
    except:
        error_message = traceback.print_exc()
        print(error_message)
        return error_message, 500




if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)