from sqlalchemy import Column, Integer, Float, String, Date, ForeignKey
from sqlalchemy.orm import relationship, backref
from backend.infra.sqlalchemy.config.database import Base

class AssociationPC(Base):
    __tablename__ = "associationPC"
    company_cnpj = Column(Integer, ForeignKey('companies.cnpj'), primary_key=True)
    amount = Column(Integer)
    product_code = Column(Integer, ForeignKey('products.upc_ean'), primary_key=True)
    register_date = Column(Date)
    product = relationship("Product", back_populates="companies")
    company = relationship("Company", back_populates="products")
    
class Product(Base):
    __tablename__ = "products"
    upc_ean = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    region = Column(String)
    console = Column(String)
    year = Column(Integer)
    description = Column(String)
    price = Column(Float)
    companies = relationship("AssociationPC", back_populates="product")
    
class User(Base):
    __tablename__ = "users"
    cpf = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password =  Column(String)
    name = Column(String)
    telephone = Column(String)
    sex = Column(String)
    birth_date = Column(Date)

class Company(Base):
    __tablename__ = "companies"
    cnpj = Column(Integer, primary_key=True, index=True)
    email = Column(String)
    password =  Column(String)
    name = Column(String)
    description = Column(String)
    products = relationship("AssociationPC", back_populates="company")

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_cpf = Column(Integer, ForeignKey('users.cpf', name='fk_user'))
    market_cnpj = Column(Integer, ForeignKey('companies.cnpj', name='fk_market'))
    game_code = Column(Integer, ForeignKey('products.upc_ean', name='fk_game'))
    amount = Column(Integer)
    order_date = Column(Date)
    
    user = relationship('User')
    product = relationship('Product')
    company = relationship('Company')