create database db_customers

CREATE TABLE tb_customers (
customer_id serial not null primary key,
customer_email varchar(255) not null  unique,
customer_name varchar(255),
registration_date timestamp
)

CREATE TABLE tb_favorite_list_item(
favorite_list_item_id serial not null primary key,
customer_id int  not null references tb_customers(customer_id),
product_id varchar(255) not null,
registration_date timestamp,
unique(customer_id, product_id)
)

CREATE  INDEX tb_favorite_list_item_customer_id ON tb_favorite_list_item (customer_id);
CREATE  INDEX tb_favorite_list_item_id_product ON tb_favorite_list_item (product_id);

