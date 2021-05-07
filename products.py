import requests
import psycopg2
import json


class Products:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="labs"
        )


    @staticmethod
    def get_product_list_api(page):
        product_list = requests.get(f'http://challenge-api.luizalabs.com/api/product/?page={page}')

        if product_list.status_code != 200:
            return []

        return product_list.text

    @staticmethod
    def get_product_by_id_api(id):
        product = requests.get(f'http://challenge-api.luizalabs.com/api/product/{id}/')

        if product.status_code != 200:
            return []

        return product.text


    def fetch_favorite_list(self, customer_email):
        product_cursor = self.conn.cursor()
        query = '''
            SELECT
                list.customer_email,
                item.id_product,
                item.title,
                item.image,
                item.price,
                item.reviewScore,
                item.brand
            FROM
                tb_favorite_list list
                INNER JOIN tb_favorite_list_item item 
                    on item.favorite_list_id = list.favorite_list_id
            WHERE
                LIST.customer_email = %s

              '''
        product_cursor.execute(query, (customer_email, ))
        records = product_cursor.fetchall()
        return records

    def fetch_list_by_id(self, customer_email) -> int:
        product_cursor = self.conn.cursor()
        query = '''
             SELECT
                 list.favorite_list_id
             FROM
                 tb_favorite_list list
             WHERE
                 LIST.customer_email = %s
               '''
        product_cursor.execute(query, (customer_email,))
        records = product_cursor.fetchall()

        return records



    def add_items_to_favorite_list(self, customer_email, item):
        self._create_list_if_not_exists(customer_email)
        favorite_list_id = self.fetch_list_by_id(customer_email)[0][0]

        item_cursor = self.conn.cursor()
        query = f'''
                   INSERT INTO tb_favorite_list_item (favorite_list_id, registration_date,id_product,
                       title,image, price, reviewscore, brand)		
                   values(
                       %s,
                       now(),
                       %s,
                       %s,
                       %s,
                       %s,
                       %s,
                       %s
                   ) 
                    RETURNING favorite_list_id'''
        print(item)
        id_product = item['id'] if 'id' in item else None
        title = item['title'] if 'title' in item else None
        image = item['image'] if 'image' in item else None
        price = item['price'] if 'price' in item else None
        reviewscore = item['reviewscore'] if 'reviewscore' in item else None
        brand = item['brand'] if 'brand' in item else None

        insert_tuple = (favorite_list_id, id_product,
                        title, image, price, reviewscore, brand)

        print(query)
        print(insert_tuple)
        item_cursor.execute(query, insert_tuple)
        self.conn.commit()
        records = item_cursor.fetchall()
        if records:
            return True
        else:
            return False



    def _create_list_if_not_exists(self, customer_email):

        list_exists = self.fetch_list_by_id(customer_email)
        if list_exists:
            return

        list_cursor = self.conn.cursor()
        query = f'''
            insert into tb_favorite_list (customer_email,registration_date) values (
                '{customer_email}',
                now()
            ) '''
        list_cursor.execute(query, (customer_email,))
        self.conn.commit()

    def remote_item_from_list(self):
        pass

    def get_item_from_list(self):
        pass







