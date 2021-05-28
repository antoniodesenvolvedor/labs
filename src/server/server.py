from flask import Flask
from flask_restplus import Api
from src.db_models.database import init_db


authorizations = {
    'basic_auth': {
        'type': 'basic',
        'in': 'header',
        'name': 'Authorization'
    }
}


class Server():
    def __init__(self, ):
        self.app = Flask(__name__)
        self.api = Api(
            self.app,
            authorizations=authorizations,
            security= 'basic_auth',
            version='1.0',
            title='API cadastrar produtos favoritos',
            description="API responsável por cadastrar clientes e seus produtos favoritos",
            doc='/docs'
        )



    def run(self):
        init_db()
        self.app.run(host='0.0.0.0', port=5001, debug=True)

server = Server()