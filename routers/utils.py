from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.exceptions import HTTPException
from fastapi.param_functions import Depends

from jose import JWTError
from sqlalchemy.orm import Session

from ..infra.providers import token
from ..infra.sqlalchemy.config import database
from ..infra.sqlalchemy.repository import user, company

oauth2_schema = OAuth2PasswordBearer(tokenUrl='token')

def logged_user(tk: str = Depends(oauth2_schema), session: Session = Depends(database.get_db)):
    INVALID_TOKEN = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Token Inválido'})

    try:
        data = token.verify_token(tk)
    except JWTError:
        raise INVALID_TOKEN

    if not data:
        raise INVALID_TOKEN

    userdb = user.ReposityUser(session).search_cpf(data)

    if not userdb:
        raise INVALID_TOKEN

    return userdb

def logged_company(tk: str = Depends(oauth2_schema), session: Session = Depends(database.get_db)):
    INVALID_TOKEN = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail={'error': 'Token Inválido'})

    try:
        data = token.verify_token(tk)
    except JWTError:
        raise INVALID_TOKEN

    if not data:
        raise INVALID_TOKEN

    companydb = company.ReposityCompany(session).search_cnpj(data)

    if not companydb:
        raise INVALID_TOKEN

    return companydb