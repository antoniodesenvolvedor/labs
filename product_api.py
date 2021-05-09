import requests

class ProductAPI:

    @staticmethod
    def get_product_list_api(page):
        response = requests.get(f'http://challenge-api.luizalabs.com/api/product/?page={page}')

        if response.status_code != 200:
            return []

        return response.text

    @staticmethod
    def get_product_by_id_api(id):
        response = requests.get(f'http://challenge-api.luizalabs.com/api/product/{id}/')

        return response.status_code, response.text