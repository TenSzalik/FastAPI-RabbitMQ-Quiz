# pylint: disable=no-name-in-module
from pydantic import BaseModel


class BaseSchema(BaseModel):
    name: str


class CategoryCreateSchema(BaseSchema):
    pass


class CategorySchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class AnswerCreateSchema(BaseSchema):
    value: int


class AnswerSchema(AnswerCreateSchema):
    id: int

    class Config:
        orm_mode = True


class QuestionCreateSchema(BaseSchema):
    pass


class QuestionSchema(BaseSchema):
    id: int

    class Config:
        orm_mode = True


class QuizCreateSchema(BaseModel):
    category: str
    answer: list[str]
    question: str

    class Config:
        orm_mode = True


class QuizSchema(BaseModel):
    id: int
    category: CategorySchema
    answer: list[AnswerSchema]
    question: QuestionSchema

    class Config:
        orm_mode = True


class QueueCreateSchema(BaseModel):
    queue: str

    class Config:
        orm_mode = True


class QueueSchema(QueueCreateSchema):
    category: str
    answer: int

    class Config:
        orm_mode = True


class ResultCreateSchema(BaseModel):
    age: int
    sex: str
    quiz: str

    class Config:
        orm_mode = True


class ChartSchema(BaseModel):
    queue_smooth_data: dict
