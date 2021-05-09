create database db_customers

CREATE TABLE tb_customers (
customer_email varchar(255) not null  primary key,
customer_name varchar(255),
registration_date timestamp
)


CREATE TABLE tb_favorite_list(
favorite_list_id serial not null primary key,
customer_email varchar(255) unique references tb_customers(customer_email),
registration_date timestamp
)

CREATE TABLE tb_favorite_list_item(
favorite_list_item_id serial not null primary key,
favorite_list_id int references tb_favorite_list(favorite_list_id) not null,
registration_date timestamp,
product_id varchar(100) not null,
unique(favorite_list_id, product_id)
)

CREATE  INDEX tb_favorite_list_item_favorite_list_id ON tb_favorite_list_item (favorite_list_id);
CREATE  INDEX tb_favorite_list_item_id_product ON tb_favorite_list_item (product_id);

