from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from backend.schemas import schemas
from backend.infra.sqlalchemy.models import models


class ReposityOrder():
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def create(self, order: schemas.Order):
        db_order = models.Order(customer_cpf=order.customer_cpf, market_cnpj=order.market_cnpj,
                                game_code=order.game_code, amount=order.amount, order_date=order.order_date)
        self.db.add(db_order)
        self.db.commit()
        self.db.refresh(db_order)
        return db_order

    def expose(self):
        statement = select(models.Order)
        orders = self.db.execute(statement).scalars().all()
        return orders

    def search_orders_cpf(self, cpf: int):
        statement = select(models.Order).where(models.Order.customer_cpf == cpf)
        orders = self.db.execute(statement).scalars().all()
        return orders

    def search_orders_cnpj(self, cnpj: int):
        statement = select(models.Order).where(models.Order.market_cnpj == cnpj)
        orders = self.db.execute(statement).scalars().all()
        return orders

    def search_orders_code(self, code: int):
        statement = select(models.Order).where(models.Order.game_code == code)
        orders = self.db.execute(statement).scalars().all()
        return orders