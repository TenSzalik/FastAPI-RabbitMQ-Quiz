from typing import Annotated
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from core.models.database import get_database
from core.models.schemas import (
    QuizSchema,
    QuizCreateSchema,
    CategoryCreateSchema,
    QuestionCreateSchema,
    AnswerCreateSchema,
    ResultCreateSchema,
    UserSchema,
)
from core.models.models import Category, Answer, Question, Quiz, Result
from core.managers.token_manager import TokenManager
from core.managers.database_manager import DatabaseManager, PDatabase


router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=list[QuizSchema])
def read_quiz(database: Session = Depends(get_database)):
    quiz: PDatabase = DatabaseManager(database)
    return quiz.read(Quiz)


@router.post("/")
def create_quiz(
    current_user: Annotated[  # pylint: disable=unused-argument
        UserSchema, Depends(TokenManager.oauth2_scheme)
    ],
    quiz: QuizCreateSchema,
    database: Session = Depends(get_database),
):
    category_obj = (
        database.query(Category).filter(Category.name == quiz.category).first()
    )
    answer_obj_list = [
        database.query(Answer).filter(Answer.name == x).first() for x in quiz.answer
    ]
    question_obj = (
        database.query(Question).filter(Question.name == quiz.question).first()
    )

    quiz_json: PDatabase = DatabaseManager(database).create(
        Quiz,
        {"category": category_obj, "answer": answer_obj_list, "question": question_obj},
    )
    return {
        "category": quiz_json.get("category").name,
        "answer": [x.name for x in quiz_json.get("answer")],
        "question": quiz_json.get("question").name,
    }


@router.post("/category/", response_model=CategoryCreateSchema)
def create_category(
    current_user: Annotated[  # pylint: disable=unused-argument
        UserSchema, Depends(TokenManager.oauth2_scheme)
    ],
    category: CategoryCreateSchema,
    database: Session = Depends(get_database),
):
    quiz: PDatabase = DatabaseManager(database)
    return quiz.create(Category, {"name": category.name})


@router.post("/question/", response_model=QuestionCreateSchema)
def create_question(
    current_user: Annotated[  # pylint: disable=unused-argument
        UserSchema, Depends(TokenManager.oauth2_scheme)
    ],
    question: QuestionCreateSchema,
    database: Session = Depends(get_database),
):
    quiz: PDatabase = DatabaseManager(database)
    return quiz.create(Question, {"name": question.name})


@router.post("/answer/", response_model=AnswerCreateSchema)
def create_answer(
    current_user: Annotated[  # pylint: disable=unused-argument
        UserSchema, Depends(TokenManager.oauth2_scheme)
    ],
    answer: AnswerCreateSchema,
    database: Session = Depends(get_database),
):
    quiz: PDatabase = DatabaseManager(database)
    return quiz.create(Answer, {"name": answer.name, "value": answer.value})


@router.post("/result/", response_model=ResultCreateSchema)
def save_result(result: ResultCreateSchema, database: Session = Depends(get_database)):
    quiz: PDatabase = DatabaseManager(database)
    return quiz.create(
        Result, {"age": result.age, "sex": result.sex, "quiz": result.quiz}
    )
