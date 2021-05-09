import psycopg2

class Customer:
    def __init__(self):
        self.conn = psycopg2.connect(
            host="localhost",
            database="db_customers",
            user="postgres",
            password="labs"
        )


    def fetch_customers(self, customer_email):

        customer_cursor = self.conn.cursor()
        query = '''
            select customer_email, customer_name from tb_customers where customer_email = %s
        '''
        customer_cursor.execute(query, (customer_email, ))
        records = customer_cursor.fetchall()
        return records

    def update_customers(self, customer_email, customer_name):
        customer_cursor = self.conn.cursor()
        query = '''
            update tb_customers set customer_name = %s where customer_email = %s
            RETURNING customer_name
       '''
        customer_cursor.execute(query, (customer_name, customer_email))
        self.conn.commit()
        records = customer_cursor.fetchall()
        if records:
            return True
        else:
            return False

    def insert_customer(self, customer_email, customer_name):
        customer_cursor = self.conn.cursor()
        query = '''
             insert into tb_customers (customer_name, customer_email, registration_date)
             values (%s, %s, now())
             RETURNING customer_email
        '''
        customer_cursor.execute(query, (customer_name, customer_email))
        self.conn.commit()
        records = customer_cursor.fetchall()
        if records:
            return True
        else:
            return False

    def delete_customer(self, customer_email):
        customer_cursor = self.conn.cursor()
        query = '''
            delete from tb_customers where customer_email = %s
            RETURNING customer_email
        '''
        customer_cursor.execute(query, (customer_email, ))
        self.conn.commit()
        records = customer_cursor.fetchall()

        if records:
            return True
        else:
            return False






