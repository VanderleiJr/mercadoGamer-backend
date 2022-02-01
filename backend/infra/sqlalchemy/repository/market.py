from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from backend.schemas import schemas
from backend.infra.sqlalchemy.models import models
from backend.infra.sqlalchemy.repository import user, product, company

class ReposityMarket():
    def __init__(self, db: Session) -> None:
        self.db = db
    
    def all_items(self):
        statement = select(models.AssociationPC).order_by(models.AssociationPC.register_date)
        items = self.db.execute(statement).scalars().all()
        return items
    
    def item_and_all_companies(self, code: int):
        statement = select(models.Product).where(models.Product.upc_ean==code)
        item = self.db.execute(statement).scalars().first()

        statement = select(models.AssociationPC).where(models.AssociationPC.product_code==code)
        companies = self.db.execute(statement).scalars().all()

        return schemas.ProductsAndCompanies(name=item.name,
                                            list=companies)
        
    def company_and_all_items(self, code: int):
        statement = select(models.Company).where(models.Company.cnpj==code)
        company = self.db.execute(statement).scalars().first()

        statement = select(models.AssociationPC).where(models.AssociationPC.company_cnpj==code)
        items = self.db.execute(statement).scalars().all()

        return schemas.ProductsAndCompanies(name=company.name,
                                            list=items)