from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session

from ..models import models
from ....schemas import schemas


class ReposityProduct():
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, product: schemas.Product):
        db_product = models.Product(upc_ean = product.upc_ean, name = product.name,
                                    region = product.region, console = product.console,
                                    year = product.year, description = product.description,
                                    price = product.price)
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def list_all(self):
        statement = select(models.Product)
        products = self.db.execute(statement).scalars().all()
        return products

    def search_code(self, code: int):
        statement = select(models.Product).where(models.Product.upc_ean == code)
        game = self.db.execute(statement).scalars().first()
        return game

    def edit(self, code: int, product: schemas.Product):
        statement = update(models.Product).where(models.Product.upc_ean == code).\
                    values(name = product.name, region = product.region,
                    console = product.console, year = product.year,
                    description = product.description, price = product.price)
        self.db.execute(statement)
        self.db.commit()

    def remove(self, code: int):
        statement = delete(models.Product).where(models.Product.upc_ean == code)
        self.db.execute(statement)
        self.db.commit()

