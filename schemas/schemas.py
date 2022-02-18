from datetime import date
from pydantic import BaseModel
from typing import Optional, List

## Usuário Padrão
class User(BaseModel):
    cpf: int
    email: str
    password: str
    name: str
    telephone: str
    sex: str
    birth_date: date
    class Config:
        orm_mode = True

## Usuário Padrão, sem PASSWORD
class UserNP(BaseModel):
    cpf: int
    email: str
    name: str
    telephone: str
    sex: str
    birth_date: date
    class Config:
        orm_mode = True

## Usuário para Edição, sem PASSWORD, sem CPF
class UserNPNC(BaseModel):
    email: str
    name: str
    telephone: str
    sex: str
    birth_date: date
    class Config:
        orm_mode = True

# Produto Padrão
class Product(BaseModel):
    upc_ean: int
    name: str
    region: str = 'Worldwide'
    console: str
    year: int
    description: str
    price: float
    class Config:
        orm_mode = True

# Produto para edição, sem UPC_EAN
class ProductEdit(BaseModel):
    name: Optional[str]
    region: Optional[str]
    console: Optional[str]
    year: Optional[int]
    description: Optional[str]
    price: Optional[float]
    class Config:
        orm_mode = True

# Compania Padrão
class Company(BaseModel):
    cnpj: int
    email: str
    password: str
    name: str
    description: Optional[str] = None
    class Config:
        orm_mode = True

# Compania para Edição, sem CNPJ, sem PASSWORD
class CompanyNPNC(BaseModel):
    email: str
    name: str
    description: Optional[str] = None
    class Config:
        orm_mode = True

# Associação entre Produto e Compania
class AssociationPC(BaseModel):
    company_cnpj: int
    amount: int
    product_code: int
    register_date: Optional[date] = date.today()
    class Config:
        orm_mode = True

# Associação entre Produto e Compania, para registro de produtos
class CompanyRegisterProduct(BaseModel):
    product_code: int
    amount: int
    class Config:
        orm_mode = True

# Pedidos Padrão
class Order(BaseModel):
    id: Optional[int] = None
    customer_cpf: int
    market_cnpj: int
    game_code: int
    amount: int
    order_date: Optional[date] = date.today()
    class Config:
        orm_mode = True

class SimpleUser(BaseModel):
    name: str
    email: str
    class Config:
        orm_mode = True

class LoggedUser(BaseModel):
    user: SimpleUser
    access_token: str

class SimpleCompany(BaseModel):
    name: str
    description: str

class DetailedCompany(BaseModel):
    name: str
    cnpj: int
    email: str
    description: Optional[str]
    class Config:
        orm_mode = True

class LoggedCompany(BaseModel):
    company: SimpleUser
    access_token: str

class LoginUser(BaseModel):
    cpf: int
    password: str

class LoginCompany(BaseModel):
    cnpj: int
    password: str

class ProductsAndCompanies(BaseModel):
    name: str
    list: List[AssociationPC]
    class Config:
        orm_mode = True
    