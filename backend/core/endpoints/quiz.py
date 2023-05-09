from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from core.models.database import SessionLocal
from core.models.schemas import (
    QuizSchema,
    QuizCreateSchema,
    CategoryCreateSchema,
    QuestionCreateSchema,
    AnswerCreateSchema,
    ResultCreateSchema,
)
from core.models.models import Category, Answer, Question, Quiz, Result


router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Not found"}},
)


def get_database():
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


@router.get("/", response_model=list[QuizSchema])
def read_quiz(database: Session = Depends(get_database)):
    quiz_list = database.query(Quiz).all()
    return jsonable_encoder(quiz_list)


@router.post("/", response_model=QuizCreateSchema)
def create_quiz(quiz: QuizCreateSchema, database: Session = Depends(get_database)):
    category_obj = (
        database.query(Category).filter(Category.name == quiz.category).first()
    )
    answer_obj_list = [
        database.query(Answer).filter(Answer.name == x).first() for x in quiz.answer
    ]
    question_obj = (
        database.query(Question).filter(Question.name == quiz.question).first()
    )
    database_quiz = Quiz(
        category=category_obj, answer=answer_obj_list, question=question_obj
    )
    database.add(database_quiz)
    database.commit()
    return {
        "category": database_quiz.category.name,
        "answer": [x.name for x in database_quiz.answer],
        "question": database_quiz.question.name,
    }


@router.post("/category/", response_model=CategoryCreateSchema)
def create_category(
    category: CategoryCreateSchema, database: Session = Depends(get_database)
):
    category_obj = Category(name=category.name)
    database.add(category_obj)
    database.commit()
    return {"name": category_obj.name}


@router.post("/question/", response_model=QuestionCreateSchema)
def create_question(
    question: QuestionCreateSchema, database: Session = Depends(get_database)
):
    question_obj = Question(name=question.name)
    database.add(question_obj)
    database.commit()
    return {"name": question_obj.name}


@router.post("/answer/", response_model=AnswerCreateSchema)
def create_answer(
    answer: AnswerCreateSchema, database: Session = Depends(get_database)
):
    answer_obj = Answer(name=answer.name, value=answer.value)
    database.add(answer_obj)
    database.commit()
    return {"name": answer_obj.name, "value": answer_obj.value}


@router.post("/result/", response_model=ResultCreateSchema)
def save_result(result: ResultCreateSchema, database: Session = Depends(get_database)):
    result_model = Result(age=result.age, sex=result.sex, quiz=result.quiz)
    database.add(result_model)
    database.commit()
    return {"age": result_model.age, "sex": result_model.sex, "quiz": result_model.quiz}
