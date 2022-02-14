from sqlalchemy import select, delete, update
from sqlalchemy.orm import Session
from backend.schemas import schemas
from backend.infra.sqlalchemy.models import models

class ReposityUser():
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, user: schemas.User):
        db_user = models.User(cpf = user.cpf, email = user.email,
                              password = user.password, name = user.name,
                              telephone = user.telephone, sex = user.sex,
                              birth_date = user.birth_date)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def list_all(self):
        statement = select(models.User)
        users = self.db.execute(statement).scalars().all()
        return users

    def search_cpf(self, number: int) -> schemas.User:
        statement = select(models.User).where(models.User.cpf == number)
        user = self.db.execute(statement).scalars().first()
        return user

    def remove(self, number: int):
        statement = delete(models.User).where(models.User.cpf == number)
        self.db.execute(statement)
        self.db.commit()
    
    def edit(self, cpf: int, user: schemas.UserNPNC):
        statement = update(models.User).where(models.User.cpf == cpf).\
                    values(name = user.name, email = user.email,
                    telephone = user.telephone, birth_date = user.birth_date,
                    sex = user.sex)
        self.db.execute(statement)
        self.db.commit()