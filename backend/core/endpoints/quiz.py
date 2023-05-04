from fastapi import Depends
from sqlalchemy.orm import Session
from core.models.database import SessionLocal
import core.schemas.schemas as schemas, core.models.models as models
from fastapi.encoders import jsonable_encoder
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/quiz",
    tags=["quiz"],
    responses={404: {"description": "Not found"}},
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[schemas.QuizSchema])
def read_quiz(db: Session = Depends(get_db)):
    quiz = db.query(models.Quiz).all()
    return jsonable_encoder(quiz)


@router.post("/", response_model=schemas.QuizCreateSchema)
def create_quiz(question: schemas.QuizCreateSchema, db: Session = Depends(get_db)):
    cat = (
        db.query(models.Category)
        .filter(models.Category.id == question.category)
        .first()
    )
    ans = db.query(models.Answer).all()
    que = (
        db.query(models.Question)
        .filter(models.Question.id == question.question)
        .first()
    )
    db_answer = models.Quiz(category=cat, answer=ans, question=que)
    db.add(db_answer)
    db.commit()
    db.refresh(db_answer)
    return {
        "category": db_answer.category.id,
        "answer": [x.id for x in db_answer.answer],
        "question": db_answer.question.id,
    }


@router.post("/category/", response_model=schemas.CategoryCreateSchema)
def create_category(
    category: schemas.CategoryCreateSchema, db: Session = Depends(get_db)
):
    category_model = models.Category(name=category.name)
    db.add(category_model)
    db.commit()
    db.refresh(category_model)
    return {"name": category_model.name}


@router.post("/question/", response_model=schemas.QuestionCreateSchema)
def create_question(
    question: schemas.QuestionCreateSchema, db: Session = Depends(get_db)
):
    question_model = models.Question(name=question.name)
    db.add(question_model)
    db.commit()
    db.refresh(question_model)
    return {"name": question_model.name}


@router.post("/answer/", response_model=schemas.AnswerCreateSchema)
def create_answer(answer: schemas.AnswerCreateSchema, db: Session = Depends(get_db)):
    answer_model = models.Answer(name=answer.name, value=answer.value)
    db.add(answer_model)
    db.commit()
    db.refresh(answer_model)
    return {"name": answer_model.name, "value": answer_model.value}


@router.post("/result/", response_model=schemas.ResultCreateSchema)
def save_result(result: schemas.ResultCreateSchema, db: Session = Depends(get_db)):
    result_model = models.Result(age=result.age, sex=result.sex, quiz=result.quiz)
    db.add(result_model)
    db.commit()
    db.refresh(result_model)
    return {"age": result_model.age, "sex": result_model.sex, "quiz": result_model.quiz}
