from sqlalchemy import select, delete
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

    def expose(self):
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