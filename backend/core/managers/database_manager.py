from typing import Protocol
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.models.models import Category, Answer, Question, Quiz, Result


class PDatabase(Protocol):
    def __init__(self, database: Session):
        ...

    def read(self, model: Category | Answer | Question | Quiz | Result) -> dict:
        ...

    def create(
        self, model: Category | Answer | Question | Quiz | Result, data: dict
    ) -> dict:
        ...


class DatabaseManager:
    def __init__(self, database):
        self.database = database

    def read(self, model):
        json = self.database.query(model).all()
        return jsonable_encoder(json)

    def create(self, model, data):
        self.database.add(model(**data))
        self.database.commit()
        return data
