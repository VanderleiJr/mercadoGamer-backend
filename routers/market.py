from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from ..schemas import schemas
from ..routers.utils import logged_user
from ..infra.providers import hash, token
from ..infra.sqlalchemy.config import database
from ..infra.sqlalchemy.repository import market, company, product, order

router = APIRouter()

# -- MARKET -- #
# Exibe todos os produtos registrados por empresas - COMPLETO
@router.get('/')
def market_all_itens(db: Session = Depends(database.get_db)):
    products = market.ReposityMarket(db).all_items()
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há produtos nesse site!')
    return products

# Exibir detalhes de um produto específico e todo mundo que vende aquele produto - COMPLETO
@router.get('/code/{code}')
def item_and_companies(code: int, db: Session = Depends(database.get_db)):
    if not product.ReposityProduct(db).search_code(code):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': "Código não cadastrado!"})
    return market.ReposityMarket(db).item_and_all_companies(code)

# Exibir detalhes de uma empresa específica e tudo que ela vende - COMPLETO
@router.get('/cnpj/{cnpj}')
def company_and_items(cnpj: int, db: Session = Depends(database.get_db)):
    if not company.ReposityCompany(db).search_cnpj(cnpj):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': "CNPJ não cadastrado!"})
    return market.ReposityMarket(db).company_and_all_items(cnpj)