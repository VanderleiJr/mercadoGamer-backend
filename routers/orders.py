from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from ..schemas import schemas
from ..routers.utils import logged_user
from ..infra.sqlalchemy.config import database
from ..infra.sqlalchemy.repository import order, user, product, company
from ..infra.sqlalchemy.models.models import AssociationPC

router = APIRouter()

# -- PEDIDO -- #
# Cadastrar um Pedido - COMPLETO
@router.get('/{company_cnpj}/{product_code}/{amount}', status_code=status.HTTP_201_CREATED)
def create_order(company_cnpj: int, product_code: int, amount: int, 
                data: schemas.User = Depends(logged_user),
                db: Session = Depends(database.get_db)):

    if not product.ReposityProduct(db).search_code(product_code):    
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Jogo não cadastrado!'})
    elif not company.ReposityCompany(db).search_cnpj(company_cnpj):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Empresa não cadastrado!'})
    elif not user.ReposityUser(db).search_cpf(data.cpf):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Usuário não cadastrado!'})

    stockdb = order.ReposityOrder(db).stock_verify(AssociationPC(company_cnpj=company_cnpj, product_code=product_code, amount=amount))
    if stockdb:
        order.ReposityOrder(db).stock_edit(stockdb, (-1)*amount)
        return order.ReposityOrder(db).create(schemas.Order(customer_cpf=data.cpf, market_cnpj=company_cnpj,
                                                        game_code=product_code, amount=amount))
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'error': 'Produto sem Estoque!'})








"""

# Exibir todos os Pedidos
@router.get('/orders')
def expose_orders(db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).list_all()
    if not orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Não há pedidos realizados!'})
    return orders

# Exibir todos os Pedidos de um Usuário
@router.get('/orders/user/{cpf}', status_code=status.HTTP_202_ACCEPTED)
def search_orders_cpf(cpf: int, db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).search_orders_cpf(cpf)
    if not orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Não há pedidos deste Usuário'})
    return orders

# Exibir todos os Pedidos de uma Empresa
@router.get('/orders/company/{cnpj}', status_code=status.HTTP_202_ACCEPTED)
def search_orders_cnpj(cnpj: int, db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).search_orders_cnpj(cnpj)
    if not orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Não há pedidos para esta Empresa'})
    return orders

# Exibir todos os Pedidos de um Produto
@router.get('/orders/product/{code}', status_code=status.HTTP_202_ACCEPTED)
def search_orders_code(code: int, db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).search_orders_code(code)
    if not orders:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'error': 'Não há pedidos deste Jogo'})
    return orders
    
"""