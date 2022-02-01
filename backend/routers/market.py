from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from backend.schemas import schemas
from backend.routers.utils import logged_user
from backend.infra.providers import hash, token
from backend.infra.sqlalchemy.config import database
from backend.infra.sqlalchemy.repository import market, company, product, order

router = APIRouter()

# -- MARKET -- #
# Exibe todos os produtos registrados por empresas - COMPLETO
@router.get('/')
def market_all_itens(db: Session = Depends(database.get_db)):
    return market.ReposityMarket(db).all_itens()

# Exibir detalhes de um produto específico e todo mundo que vende aquele produto - COMPLETO
@router.get('/code/{code}')
def item_and_companies(code: int, db: Session = Depends(database.get_db)):
    return market.ReposityMarket(db).item_and_all_companies(code)

# Exibir detalhes de uma empresa específica e tudo que ela vende - COMPLETO
@router.get('/cnpj/{cnpj}')
def company_and_items(cnpj: int, db: Session = Depends(database.get_db)):
    return market.ReposityMarket(db).company_and_all_items(cnpj)