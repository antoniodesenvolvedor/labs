import psycopg2

class Customer:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="db_customers",
            user="postgres",
            password="labs"
        )


    def fetch_customer(self, customer_email):

        cursor = self.conn.cursor()
        query = '''
            select customer_id, customer_email, customer_name from tb_customers where customer_email = %s
        '''
        cursor.execute(query, (customer_email, ))
        records = cursor.fetchall()
        return records

    def update_customer(self, customer_email, customer_name):
        cursor = self.conn.cursor()
        query = '''
            update tb_customers set customer_name = %s where customer_email = %s
            RETURNING customer_id
       '''
        cursor.execute(query, (customer_name, customer_email))
        self.conn.commit()
        records = cursor.fetchall()
        if records:
            return True
        else:
            return False

    def insert_customer(self, customer_email, customer_name):
        cursor = self.conn.cursor()
        query = '''
             insert into tb_customers (customer_email, customer_name, registration_date)
             values (%s, %s, now())
             RETURNING customer_id
        '''
        cursor.execute(query, (customer_email, customer_name))
        self.conn.commit()
        records = cursor.fetchall()
        if records:
            return True
        else:
            return False

    def delete_customer(self, customer_email):
        cursor = self.conn.cursor()
        query = '''
            delete from tb_customers where customer_email = %s
            RETURNING customer_id
        '''
        cursor.execute(query, (customer_email, ))
        self.conn.commit()
        records = cursor.fetchall()

        if records:
            return True
        else:
            return False






