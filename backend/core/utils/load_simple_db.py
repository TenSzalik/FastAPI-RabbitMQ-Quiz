from sqlalchemy.orm import Session
from core.models.models import User, Category, Answer, Question, Quiz, Result
from core.utils.get_hashed_password import get_hashed_password


def load_simple_db(database: Session):
    user = User(
        email="foobarbaz@gmail.com", password=get_hashed_password("FooBarBaz1234")
    )

    category_1 = Category(name="category1")
    category_2 = Category(name="category2")

    answer_1 = Answer(name="answer1", value=-2)
    answer_2 = Answer(name="answer2", value=-1)
    answer_3 = Answer(name="answer3", value=0)
    answer_4 = Answer(name="answer4", value=1)
    answer_5 = Answer(name="answer5", value=2)

    question_1 = Question(name="question1")
    question_2 = Question(name="question2")

    database.add_all(
        [
            user,
            category_1,
            category_2,
            answer_1,
            answer_2,
            answer_3,
            answer_4,
            answer_5,
            question_1,
            question_2,
        ]
    )
    database.commit()

    quiz_1 = Quiz(
        category=category_1,
        answer=[answer_1, answer_2, answer_3, answer_4, answer_5],
        question=question_1,
    )

    quiz_2 = Quiz(
        category=category_2,
        answer=[answer_1, answer_2, answer_3, answer_4, answer_5],
        question=question_2,
    )

    result = Result(age=24, sex="Male", quiz="{category_1: 2, category_2: 2}")

    database.add_all([quiz_1, quiz_2, result])
    database.commit()
