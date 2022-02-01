from datetime import datetime, timedelta
from jose import jwt

# JOSE
SECRET_KEY = '2c7f621a96d3d4b23bd2aa4ad070c9de'
ALGORITHM = 'HS256'
EXPIRES_IN_MIN = 30

def make_token(item: dict):
    data = item.copy()
    expire = datetime.utcnow() + timedelta(minutes=EXPIRES_IN_MIN)

    data.update({'exp': expire})

    return jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)

def verify_token(tk: str):
    return jwt.decode(tk, SECRET_KEY, algorithms=[ALGORITHM], options={'verify_sub': False}).get('sub')