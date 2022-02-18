from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session


from ..models import models
from ....schemas import schemas

class ReposityCompany():
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, company: schemas.Company):
        db_company = models.Company(cnpj = company.cnpj, email = company.email,
                                    password = company.password, name = company.name,
                                    description = company.description)
        self.db.add(db_company)
        self.db.commit()
        self.db.refresh(db_company)
        return db_company

    def list_all(self):
        statement = select(models.Company)
        company = self.db.execute(statement).scalars().all()
        return company

    def search_cnpj(self, number: int) -> schemas.Company:
        statement = select(models.Company).where(models.Company.cnpj == number)
        company = self.db.execute(statement).scalars().first()
        return company

    def remove(self, number: int):
        statement = delete(models.Company).where(models.Company.cnpj == number)
        self.db.execute(statement)
        self.db.commit()

    def register_product(self, association: schemas.AssociationPC):
        db_association = models.AssociationPC(company_cnpj = association.company_cnpj, amount = association.amount,
                                            product_code = association.product_code, register_date = association.register_date)
        self.db.add(db_association)
        self.db.commit()
        self.db.refresh(db_association)

    def registred_product_verify(self, association: schemas.AssociationPC):
        statement = select(models.AssociationPC).where(models.AssociationPC.company_cnpj == association.company_cnpj,
                                                    models.AssociationPC.product_code == association.product_code)
        return self.db.execute(statement).scalars().first()

    def list_products(self, company: schemas.Company):
        statement = select(models.AssociationPC).where(models.AssociationPC.company_cnpj == company.cnpj)
        products = self.db.execute(statement).scalars().all()
        return products

    def remove_product(self, code:int):
        statement = delete(models.AssociationPC).where(models.AssociationPC.product_code == code)
        self.db.execute(statement)
        self.db.commit()

    def edit(self, cnpj: int, company: schemas.CompanyNPNC):
        statement = update(models.Company).where(models.Company.cnpj == cnpj).\
                    values(name = company.name, email = company.email,
                    description = company.description)
        self.db.execute(statement)
        self.db.commit()