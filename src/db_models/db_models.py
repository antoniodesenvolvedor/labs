from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint
from src.db_models.database import Base
from sqlalchemy.types import DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

class Customer(Base):
    __tablename__ = 'customers'
    customer_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    registration_date = Column(DateTime, default=datetime.now)

    def __init__(self, name=None, email=None):
        self.name = name
        self.email = email



    def __repr__(self):
        return f'{{"customer_id": {self.customer_id}, "name":"{self.name}", "email":"{self.email}"}}'


class FavoriteListItem(Base):
    __tablename__ = 'favorite_list_items'
    favorite_list_item_id = Column(Integer, primary_key=True)
    customer_id = Column(Integer, ForeignKey('customers.customer_id'), nullable=False)
    customer = relationship("Customer", lazy=False)
    product_id = Column(String(120), nullable=False)
    registration_date = Column(DateTime, default=datetime.utcnow)
    UniqueConstraint(customer_id, product_id)

    def __init__(self, customer_id=None, product_id=None):
        self.customer_id = customer_id
        self.product_id = product_id


    def __repr__(self):
        return f'{{"favorite_list_item_id": {self.favorite_list_item_id},' \
               f' "customer_id":{self.customer_id}, "product_id":"{self.product_id}"}}'
