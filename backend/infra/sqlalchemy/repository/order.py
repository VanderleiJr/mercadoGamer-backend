from sqlalchemy import and_, select, delete, update
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

    def list_all(self):
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
    
    def stock_verify(self, association: schemas.AssociationPC):
        statement = select(models.AssociationPC).where(models.AssociationPC.company_cnpj == association.company_cnpj,
                                                    models.AssociationPC.product_code == association.product_code,
                                                    models.AssociationPC.amount >= association.amount)
        return self.db.execute(statement).scalars().first()

    def stock_edit(self, association: schemas.AssociationPC, item_amount: int):
        statement = update(models.AssociationPC).\
                    where(and_(models.AssociationPC.company_cnpj == association.company_cnpj, models.AssociationPC.product_code == association.product_code)).\
                    values(amount = (association.amount + item_amount))
        self.db.execute(statement)
        self.db.commit()
