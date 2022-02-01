from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.infra.sqlalchemy.config import database

from backend.routers import users, products, companies, orders, market

# uvicorn backend.server:app --reload --reload-dir=backend

database.create_db()
app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'])

# ROUTERS
app.include_router(users.router, prefix='/user', tags=['users'])
app.include_router(orders.router, prefix='/order', tags=['orders'])
app.include_router(market.router, prefix='/market', tags=['market'])
app.include_router(products.router)
app.include_router(companies.router, prefix='/company', tags=['companies'])


