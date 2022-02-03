from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from backend.schemas import schemas
from backend.infra.sqlalchemy.config import database
from backend.infra.sqlalchemy.repository import product

router = APIRouter()

# -- PRODUTOS -- #
# Cadastrar um Produto
@router.post('/products', status_code=status.HTTP_201_CREATED)
def create_product(item: schemas.Product, db: Session = Depends(database.get_db)):
    new_product = product.ReposityProduct(db).create(item)
    if new_product == -1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f'UPC/EAN já cadastrado!')
    return new_product
"""
# Exibir todos os Produtos
@router.get('/products')
def expose_products(db: Session = Depends(database.get_db)):
    products = product.ReposityProduct(db).expose()
    if not products:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há produtos registrados!')
    return products

# Pesquisar um Produto através de seu código
@router.get('/products/{code}')
def search_product(code: int, db: Session = Depends(database.get_db)):
    item = product.ReposityProduct(db).search_code(code)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um jogo com o código {code}')
    return item

# Atulizar um Produto
@router.put('/products/{code}')
def edit_product(code: int, item: schemas.ProductEdit, db: Session = Depends(database.get_db)):
    item = product.ReposityProduct(db).edit(code, item)
    if item == -1:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'UPC/EAN não cadastrado!')
    return item

# Deletar um Produto do Banco de Dados
@router.delete('/products/{code}')
def delete_product(code: int, db: Session = Depends(database.get_db)):
    product.ReposityProduct(db).remove(code)
    return {'msg': "O jogo foi removido com sucesso!"}
    """