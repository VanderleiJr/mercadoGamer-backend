from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .infra.sqlalchemy.config import database

from .routers import users, companies, orders, market

# uvicorn mercadoGamer-backend.server:app --reload --reload-dir=mercadoGamer-backend

database.create_db()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

# ROUTERS
app.include_router(users.router, prefix='/user', tags=['users'])
app.include_router(orders.router, prefix='/order', tags=['orders'])
app.include_router(market.router, prefix='/market', tags=['market'])
app.include_router(companies.router, prefix='/company', tags=['companies'])


