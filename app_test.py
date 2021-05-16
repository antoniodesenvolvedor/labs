import pytest
from app import app
import json
from base64 import b64encode



@pytest.fixture(scope="class")
def client():
    return app.test_client()

global_credentials = b64encode(b"labs:labs_123").decode('utf-8')


class TestCustomer:
    def _init_class(self, cli):
        self._headers = self._get_header()
        self._client = cli
        self._customer = {
            "customer_name": "email_de_teste_OOOOOO",
            "customer_email": "email_de_teste_OOOOOO"
        }
        self._new_customer_name = {
            "customer_name": "new_customer_name",
            "customer_email": "email_de_teste_OOOOOO"
        }
        self._non_existing_customer = {
            "customer_name": "non_existing_customer_000000000",
            "customer_email": "non_existing_customer_00000000"
        }


    def _get_header(self):
        return {
            "Authorization": f"Basic {global_credentials}",
            "Content-Type": "application/json"
        }

    def _test_get(self):
        response = self._client.get(f'/cliente?customer_email={self._customer["customer_email"]}')
        assert response.status_code == 403

        response = self._client.get(f'/cliente?customer_email={self._non_existing_customer["customer_email"]}'
                              , headers=self._headers)
        assert response.status_code == 404

        response = self._client.get(f'/cliente', headers=self._headers)
        assert response.status_code == 400


    def _test_post(self):
        response = self._client.post('/cliente', json=self._customer)
        assert response.status_code == 403

        response = self._client.post('/cliente', headers=self._headers)
        assert response.status_code == 400

        response = self._client.post('/cliente', json={"Wrong": "parameters"}, headers=self._headers)
        assert response.status_code == 400

        response = self._client.post('/cliente', json=self._customer, headers=self._headers)
        assert response.status_code == 200

        response = self._client.post('/cliente', json=self._customer, headers=self._headers)
        assert response.status_code == 406
        returned_message = json.loads(response.data)
        assert 'já cadastrado' in returned_message["message"]

        response = self._client.get(f'/cliente?customer_email={self._customer["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 200

        returned_message = json.loads(response.data)
        assert returned_message['name'] == self._customer['customer_name']
        assert returned_message['email'] == self._customer['customer_email']


    def _test_put(self):
        response = self._client.put('/cliente', json=self._new_customer_name)
        assert response.status_code == 403

        response = self._client.put('/cliente', headers=self._headers)
        assert response.status_code == 400

        response = self._client.put('/cliente', json={"Wrong": "parameters"}, headers=self._headers)
        assert response.status_code == 400

        response = self._client.put(f'/cliente', json=self._non_existing_customer, headers=self._headers)
        assert response.status_code == 404

        response = self._client.put('/cliente', json=self._new_customer_name, headers=self._headers)
        assert response.status_code == 200

        response = self._client.get(f'/cliente?customer_email={self._new_customer_name["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 200
        returned_message = json.loads(response.data)
        assert returned_message['name'] == self._new_customer_name['customer_name']
        assert returned_message['email'] == self._new_customer_name['customer_email']

    def _test_delete(self):
        response = self._client.delete(f'/cliente/{self._non_existing_customer["customer_email"]}')
        assert response.status_code == 403

        response = self._client.delete(f'/cliente/{self._non_existing_customer["customer_email"]}',
                                       headers=self._headers)
        assert response.status_code == 404

        response = self._client.delete(f'/cliente/{self._customer["customer_email"]}',
                                       headers=self._headers)
        assert response.status_code == 200

        response = self._client.get(f'/cliente?customer_email={self._customer["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 404

    def _delete_previous_data(self):
        self._client.delete(f'/cliente/{self._customer["customer_email"]}', headers=self._headers)
        self._client.delete(f'/cliente/{self._new_customer_name["customer_email"]}', headers=self._headers)
        self._client.delete(f'/cliente/{self._non_existing_customer["customer_email"]}', headers=self._headers)


    def test_customer(self, client):
        self._init_class(client)
        self._delete_previous_data()
        self._test_get()
        self._test_post()
        self._test_put()
        self._test_delete()




class TestFavoriteListItem:
    def _init_class(self, cli):
        self._headers = self._get_header()
        self._client = cli
        self._non_existing_product_id = {
            "customer_email": "email_testando_12345@@@",
            "product_id": "@@@0000@@@@"
        }
        self._non_existing_email= {
            "customer_email": "non_existing_email@@@@@",
            "product_id": "958ec015-cfcf-258d-c6df-1721de0ab6ea"
        }
        self._id_product_and_customer_email = {
            "customer_email": "email_de_teste_OOOOOO",
            "product_id": "958ec015-cfcf-258d-c6df-1721de0ab6ea"
        }
        self._customer = {
            "customer_name": "email_de_teste_OOOOOO",
            "customer_email": "email_de_teste_OOOOOO"
        }


    def _get_header(self):
        return {
            "Authorization": f"Basic {global_credentials}",
            "Content-Type": "application/json"
        }

    def _test_get(self):
        response = self._client.get('/lista_favoritos')
        assert response.status_code == 403

        response = self._client.get(f'/lista_favoritos', headers=self._headers)
        assert response.status_code == 400

        response = self._client.get(f'/lista_favoritos?customer_email={self._non_existing_email["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 404

        response = self._client.get(f'/lista_favoritos?customer_email={self._customer["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 404

    def _test_post(self):
        response = self._client.post('/lista_favoritos', json=self._id_product_and_customer_email)
        assert response.status_code == 403

        response = self._client.post('/lista_favoritos', headers=self._headers)
        assert response.status_code == 400

        response = self._client.post('/lista_favoritos', json=self._non_existing_email,
                                     headers=self._headers)
        assert response.status_code == 404

        response = self._client.post('/lista_favoritos', json=self._non_existing_product_id,
                                     headers=self._headers)
        assert response.status_code == 404

        response = self._client.post('/lista_favoritos', json=self._id_product_and_customer_email,
                                     headers=self._headers)
        assert response.status_code == 200

        response = self._client.post('/lista_favoritos', json=self._id_product_and_customer_email,
                                     headers=self._headers)
        assert response.status_code == 400

        response = self._client.get(
            f'/lista_favoritos?customer_email={self._id_product_and_customer_email["customer_email"]}',
                                    headers=self._headers)
        assert response.status_code == 200
        response_message = json.loads(response.data)
        assert response_message[0]['customer_email'] == self._id_product_and_customer_email["customer_email"]
        assert response_message[0]['product_id'] == self._id_product_and_customer_email["product_id"]

    def _test_delete(self):
        response = self._client.delete('/lista_favoritos', json=self._id_product_and_customer_email)
        assert response.status_code == 403

        response = self._client.delete('/lista_favoritos', headers=self._headers)
        assert response.status_code == 400

        response = self._client.post('/lista_favoritos', json=self._non_existing_email,
                                     headers=self._headers)
        assert response.status_code == 404

        response = self._client.delete('/lista_favoritos', json=self._non_existing_product_id,
                                     headers=self._headers)
        assert response.status_code == 404

        response = self._client.delete('/lista_favoritos', json=self._id_product_and_customer_email,
                                     headers=self._headers)
        assert response.status_code == 200

        response = self._client.delete('/lista_favoritos', json=self._id_product_and_customer_email,
                                     headers=self._headers)
        assert response.status_code == 404

        response = self._client.get(
            f'/lista_favoritos?customer_email={self._id_product_and_customer_email["customer_email"]}',
            headers=self._headers)
        assert response.status_code == 404

    def _delete_previous_data(self):
        self._client.delete('/lista_favoritos', json=self._id_product_and_customer_email,
                            headers=self._headers)


    def test_customer(self, client):
        self._init_class(client)
        self._delete_previous_data()
        self._client.post('/cliente', json=self._customer, headers=self._headers)

        self._test_get()
        self._test_post()
        self._test_delete()






