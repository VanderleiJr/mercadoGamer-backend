from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from backend.schemas import schemas
from backend.routers.utils import logged_company
from backend.infra.providers import hash, token
from backend.infra.sqlalchemy.config import database
from backend.infra.sqlalchemy.repository import company, product, order

router = APIRouter()

# -- EMPRESA -- #
# Cadastrar uma Empresa - COMPLETO
@router.post('/singup', status_code=status.HTTP_201_CREATED)
def singup(data: schemas.Company, db: Session = Depends(database.get_db)):
    data.password = hash.make_hash(data.password)

    if company.ReposityCompany(db).search_cnpj(data.cnpj):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={'msg': "CNPJ já cadastrado!"})
    
    return company.ReposityCompany(db).create(data)


# Entrar com uma Empresa - COMPLETO
@router.post('/singin')
def singin(data: schemas.LoginCompany, db: Session = Depends(database.get_db)):
    companydb = company.ReposityCompany(db).search_cnpj(data.cnpj)

    if not companydb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': "Empresa não cadastrado!"})

    if not hash.verify_hash(data.password, companydb.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': "Senha Incorreta!"})

    tk = token.make_token({'sub': companydb.cnpj})

    return schemas.LoggedCompany(company=companydb, access_token=tk)


# Home da Empresa - COMPLETO
@router.get('/home', response_model=schemas.DetailedCompany)
def home(data: schemas.Company = Depends(logged_company)):
    return data


# Deletar uma Empresa do Banco de Dados - PARCIALMENTE
@router.delete('/home')
def delete_company(data: schemas.Company = Depends(logged_company), db: Session = Depends(database.get_db)):
    
    company.ReposityCompany(db).remove(data.cnpj)
    return f'A Empresa {data.name} ({data.cnpj}) foi removida com sucesso!'


# Registar um produto para a Empresa - COMPLETO
@router.post('/products', status_code=status.HTTP_202_ACCEPTED)
def register_product_company(data: schemas.CompanyRegisterProduct,
                            companydb: schemas.Company = Depends(logged_company),
                            db: Session = Depends(database.get_db)):

    game = product.ReposityProduct(db).search_code(data.product_code)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um jogo com o código {data.product_code} registrado!')

    company.ReposityCompany(db).registerProduct(schemas.AssociationPC(company_cnpj=companydb.cnpj,
                                                                    amount=data.amount,
                                                                    product_code=data.product_code))
    return f'{game.name} ({game.upc_ean}) registrado com sucesso na empresa {companydb.name}!'


# Listar todos os produtos da Empresa - COMPLETO
@router.get('/products')
def register_product_company(companydb: schemas.Company = Depends(logged_company),
                            db: Session = Depends(database.get_db)):
    products = company.ReposityCompany(db).listProducts(companydb)
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há produtos registrados!')
    return products

# Listar todos pedidos da Empresa - COMPLETO
@router.get('/orders', status_code=status.HTTP_202_ACCEPTED)
def user_orders(data: schemas.Company = Depends(logged_company), db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).search_orders_cnpj(data.cnpj)
    if not orders:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Você ainda não recebeu pedidos!')
    return orders


"""
# Exibir todas as Empresas
@router.get('/companies')
def expose_companies(db: Session = Depends(database.get_db)):
    companies = company.ReposityCompany(db).expose()
    if not companies:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há lojas cadastradas!')
    return companies

# Pesquisar uma Empresa através de seu cnpj
@router.get('/companies/{cnpj}', status_code=status.HTTP_202_ACCEPTED)
def search_company(cnpj: int, db: Session = Depends(database.get_db)):
    companies = company.ReposityCompany(db).search_cnpj(cnpj)
    if not companies:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há loja com o CNPJ {cnpj}')
    return companies

# Desassociar um produto da Empresa
@router.delete('/companies/product/{code}')
def delete_product_company(code: int, db: Session = Depends(database.get_db)):
    company.ReposityCompany(db).remove(code)
    return {'msg': "O produto foi removido da loja com sucesso!"}
"""