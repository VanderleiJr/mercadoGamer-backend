from fastapi import APIRouter
from fastapi import HTTPException, Depends, status

from sqlalchemy.orm import Session

from backend.schemas import schemas
from backend.routers.utils import logged_user
from backend.infra.providers import hash, token
from backend.infra.sqlalchemy.config import database
from backend.infra.sqlalchemy.repository import user, order


router = APIRouter()

# -- USUÁRIOS -- #
# Cadastrar o Usuário - COMPLETO
@router.post('/signup', status_code=status.HTTP_201_CREATED, response_model=schemas.SimpleUser)
def singup(data: schemas.User, db: Session = Depends(database.get_db)):
    data.password = hash.make_hash(data.password)
    
    if user.ReposityUser(db).search_cpf(data.cpf):
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail={'msg': "CPF já cadastrado!"})
    
    return user.ReposityUser(db).create(data)


# Entrar com um Usuário - COMPLETO
@router.post('/signin')
def singin(data: schemas.LoginUser, db: Session = Depends(database.get_db)):
    userdb = user.ReposityUser(db).search_cpf(data.cpf)

    if not userdb:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail={'msg': "Usuário não cadastrado!"})

    if not hash.verify_hash(data.password, userdb.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail={'msg': "Senha Incorreta!"})

    tk = token.make_token({'sub': userdb.cpf})

    return schemas.LoggedUser(user=userdb, access_token=tk)


# Home do Usuário - COMPLETO
@router.get('/home', response_model=schemas.UserNP)
def home(data: schemas.User = Depends(logged_user)):
    return data


# Listar todos pedidos do Usuários - COMPLETO
@router.get('/orders', status_code=status.HTTP_202_ACCEPTED)
def user_orders(data: schemas.User = Depends(logged_user), db: Session = Depends(database.get_db)):
    orders = order.ReposityOrder(db).search_orders_cpf(data.cpf)
    if not orders:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Você ainda não fez pedidos!')
    return orders


# Deletar um Usuário do Banco de Dados - PARCIALMENTE
@router.delete('/home')
def delete_user(data: int = Depends(logged_user), db: Session = Depends(database.get_db)):
    
    user.ReposityUser(db).remove(data.cpf)
    return f'O Usuário {data.name} ({data.cpf}) foi removido com sucesso!'


# Editar um Usuário do Banco de Dados - COMPLETO
@router.put('/edit', response_model=schemas.UserNP)
def edit_user(html_data: schemas.UserNPNC, db_data: schemas.User = Depends(logged_user), db_session: Session = Depends(database.get_db)):
    user.ReposityUser(db_session).edit(db_data.cpf, html_data)
    return db_data


"""
# Exibir todos os Usuários
@router.get('/users', status_code=status.HTTP_202_ACCEPTED)
def expose_users(db: Session = Depends(database.get_db)):
    users = user.ReposityUser(db).list_all()
    if not users:
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail=f'Não há usuários registrados!')
    return users

# Pesquisar um Usuário através de seu CPF
@router.get('/users/{cpf}')
def search_user(cpf: int, db: Session = Depends(database.get_db)):
    users = user.ReposityUser(db).search_cpf(cpf)
    if not users:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Não há um usuário com o CPF {cpf}')
    return users
"""