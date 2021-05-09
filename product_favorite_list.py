import requests
import psycopg2
import json


class ProductFavoriteList:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="db_customers",
            user="postgres",
            password="labs"
        )

    def fetch_favorite_list_items(self, customer_email):
        cursor = self.conn.cursor()
        query = '''
            SELECT
                customer.customer_email,
                list_item.product_id
            FROM
                tb_customers customer
                INNER JOIN tb_favorite_list_item list_item 
                    on customer.customer_id = list_item.customer_id
            WHERE
                customer.customer_email = %s
              '''
        cursor.execute(query, (customer_email, ))
        records = cursor.fetchall()
        return records


    def add_favorite_list_item(self, customer_email, product_id):
        cursor = self.conn.cursor()
        query = f'''
                   INSERT INTO tb_favorite_list_item (customer_id, product_id,registration_date)		
                   values(
                        (select customer_id from tb_customers where customer_email = %s),
                        %s,
                        now()
                   ) 
                    RETURNING favorite_list_item_id
                '''

        cursor.execute(query, (customer_email, product_id))
        self.conn.commit()
        records = cursor.fetchall()
        if records:
            return True
        else:
            return False

    def delete_favorite_list_item(self, customer_email, product_id):
        cursor = self.conn.cursor()
        query = f'''
            delete from tb_favorite_list_item where 
                customer_id in (select customer_id from tb_customers where customer_email = %s)
                AND product_id = %s
            returning favorite_list_item_id'''

        cursor.execute(query, (customer_email, product_id))
        self.conn.commit()
        records = cursor.fetchall()
        if records:
            return True
        else:
            return False

    def get_favorite_list_item(self, customer_email, product_id):
        cursor = self.conn.cursor()
        query = '''
            SELECT 
                product_id 
            from 
                tb_favorite_list_item 
            where 
                customer_id in (select customer_id from tb_customers where customer_email = %s)
                AND product_id = %s
          '''
        cursor.execute(query, (customer_email, product_id))
        records = cursor.fetchall()

        return records







