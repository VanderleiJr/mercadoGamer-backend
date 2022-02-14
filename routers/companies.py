from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from backend.schemas import schemas
from backend.routers.utils import logged_company
from backend.infra.providers import hash, token
from backend.infra.sqlalchemy.config import database
from backend.infra.sqlalchemy.repository import company, product, order

router = APIRouter()

# Dados JSON que são recebidos do HTML/JavaScript estão na variável HTML_DATA
# Dados JSON que são recebidos do Banco de Dados estão na variável DB_DATA

# -- EMPRESA -- #
# Cadastrar uma Empresa - COMPLETO
@router.post('/signup', status_code=status.HTTP_201_CREATED)
def singup(html_data: schemas.Company, db_session: Session = Depends(database.get_db)):
    html_data.password = hash.make_hash(html_data.password)

    if company.ReposityCompany(db_session).search_cnpj(html_data.cnpj):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'CNPJ já cadastrado!')
    
    return company.ReposityCompany(db_session).create(html_data)


# Entrar com uma Empresa - COMPLETO
@router.post('/signin')
def singin(html_data: schemas.LoginCompany, db_session: Session = Depends(database.get_db)):
    db_data = company.ReposityCompany(db_session).search_cnpj(html_data.cnpj)

    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Empresa não cadastrado!')

    if not hash.verify_hash(html_data.password, db_data.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Senha Incorreta!')

    tk = token.make_token({'sub': db_data.cnpj})

    return schemas.LoggedCompany(company=db_data, access_token=tk)


# Home da Empresa - COMPLETO
@router.get('/home', response_model=schemas.DetailedCompany)
def home(db_data: schemas.Company = Depends(logged_company)):
    return db_data


# Deletar uma Empresa do Banco de Dados - PARCIALMENTE
@router.delete('/home')
def delete_company(db_data: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    
    company.ReposityCompany(db_session).remove(db_data.cnpj)
    return f'A empresa {db_data.name} ({db_data.cnpj}) foi removida com sucesso!'


# Editar uma Empresa do Banco de Dados - COMPLETO
@router.put('/edit')
def edit_company(html_data: schemas.CompanyNPNC, db_data: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    company.ReposityCompany(db_session).edit(db_data.cnpj, html_data)
    return f'A Empresa {html_data.name} foi atualizada com sucesso no Banco de Dados'


# Registar um produto para a Empresa - COMPLETO
@router.post('/products', status_code=status.HTTP_202_ACCEPTED)
def register_product_company(html_data: schemas.CompanyRegisterProduct,
                            db_data: schemas.Company = Depends(logged_company),
                            db_session: Session = Depends(database.get_db)):

    game = product.ReposityProduct(db_session).search_code(html_data.product_code)
    if not game:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um jogo com o código {html_data.product_code} registrado!')

    stock = company.ReposityCompany(db_session).registred_product_verify(schemas.AssociationPC(company_cnpj=db_data.cnpj, product_code=html_data.product_code, amount=html_data.amount))
    if stock:
        order.ReposityOrder(db_session).stock_edit(stock, html_data.amount)
        return f'O estoque do jogo {game.name} ({game.upc_ean}) foi atualizado com sucesso na {db_data.name}!'
    else:
        company.ReposityCompany(db_session).register_product(schemas.AssociationPC(company_cnpj=db_data.cnpj,
                                                                        amount=html_data.amount,
                                                                        product_code=html_data.product_code))
        return f'{game.name} ({game.upc_ean}) registrado com sucesso na empresa {db_data.name}!'


# Listar todos os produtos da Empresa - COMPLETO
@router.get('/products')
def register_product_company(db_data: schemas.Company = Depends(logged_company),
                            db_session: Session = Depends(database.get_db)):
    products = company.ReposityCompany(db_session).list_products(db_data)
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há produtos registrados!')
    return products


# Listar todos pedidos da Empresa - COMPLETO
@router.get('/orders', status_code=status.HTTP_202_ACCEPTED)
def user_orders(db_data: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db_session).search_orders_cnpj(db_data.cnpj)
    if not orders:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Você ainda não recebeu pedidos!')
    return orders


# -- PRODUTOS -- #
# Cadastrar um Produto Novo - COMPLETO
@router.post('/products/new', status_code=status.HTTP_201_CREATED)
def create_product(html_data: schemas.Product, db_data_company: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    if product.ReposityProduct(db_session).search_code(html_data.upc_ean):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'UPC/EAN já cadastrado!')
    db_data_product = product.ReposityProduct(db_session).create(html_data)
    return f'Produto {db_data_product.name} ({db_data_product.upc_ean}) cadastrado com sucesso no Banco de Dados pela empresa {db_data_company.name}'


# Exibir todos os Produtos do Banco de Dados - COMPLETO
@router.get('/products/all')
def expose_products(_: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    db_data = product.ReposityProduct(db_session).list_all()
    if not db_data:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há produtos registrados no Banco de Dados!')
    return db_data


# Pesquisar um Produto no Banco de Dados através de seu código - COMPLETO
@router.get('/products/{code}')
def search_product(code: int, _: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    db_data = product.ReposityProduct(db_session).search_code(code)
    if not db_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um produto no Banco de Dados com o código {code}')
    return db_data


# Atulizar um Produto - COMPLETO
@router.put('/products/{code}')
def edit_product(code: int, html_data: schemas.ProductEdit, db_data_company: schemas.Company = Depends(logged_company), db_session: Session = Depends(database.get_db)):
    db_data_product = product.ReposityProduct(db_session).search_code(code)
    if not db_data_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um produto no Banco de Dados com o código {code}')
    product.ReposityProduct(db_session).edit(code, html_data)
    return f'Produto {html_data.name} ({code}) atualizado com sucesso no Banco de Dados pela empresa {db_data_company.name}'

"""
# Exibir todas as Empresas
@router.get('/companies')
def expose_companies(db_session: Session = Depends(database.get_db)):
    companies = company.ReposityCompany(db_session).list_all()
    if not companies:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há lojas cadastradas!')
    return companies

# Pesquisar uma Empresa através de seu cnpj
@router.get('/companies/{cnpj}', status_code=status.HTTP_202_ACCEPTED)
def search_company(cnpj: int, db_session: Session = Depends(database.get_db)):
    companies = company.ReposityCompany(db_session).search_cnpj(cnpj)
    if not companies:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há loja com o CNPJ {cnpj}')
    return companies

# Desassociar um produto da Empresa
@router.delete('/companies/product/{code}')
def delete_product_company(code: int, db_session: Session = Depends(database.get_db)):
    company.ReposityCompany(db_session).remove(code)
    return {'msg': "O produto foi removido da loja com sucesso!"}
"""