# pylint: disable=unused-argument
from conftest import client


def test_read_quiz(run_database, load_database):
    data_quiz = [
        {
            "id": 1,
            "category": {"name": "category1", "id": 1},
            "answer": [
                {"name": "answer1", "value": -2, "id": 1},
                {"name": "answer2", "value": -1, "id": 2},
                {"name": "answer3", "value": 0, "id": 3},
                {"name": "answer4", "value": 1, "id": 4},
                {"name": "answer5", "value": 2, "id": 5},
            ],
            "question": {"name": "question1", "id": 1},
        },
        {
            "id": 2,
            "category": {"name": "category2", "id": 2},
            "answer": [
                {"name": "answer1", "value": -2, "id": 1},
                {"name": "answer2", "value": -1, "id": 2},
                {"name": "answer3", "value": 0, "id": 3},
                {"name": "answer4", "value": 1, "id": 4},
                {"name": "answer5", "value": 2, "id": 5},
            ],
            "question": {"name": "question2", "id": 2},
        },
    ]
    response_quiz = client.get("/quiz/")
    assert response_quiz.status_code == 200
    assert response_quiz.json() == data_quiz


def test_create_quiz(run_database, load_database, token_header):
    data_quiz = {
        "category": "category1",
        "answer": ["answer1", "answer2"],
        "question": "question2",
    }

    response_quiz = client.post("/quiz/", json=data_quiz, headers=token_header)
    assert response_quiz.status_code == 200
    assert response_quiz.json() == data_quiz


def test_create_category(run_database, token_header):
    data_category = {"name": "foo"}
    response_category = client.post(
        "/quiz/category/", json=data_category, headers=token_header
    )
    assert response_category.status_code == 200
    assert response_category.json() == data_category


def test_create_question(run_database, token_header):
    data_question = {"name": "bar"}
    response_question = client.post(
        "/quiz/question/", json=data_question, headers=token_header
    )
    assert response_question.status_code == 200
    assert response_question.json() == data_question


def test_create_answers(run_database, token_header):
    data_answer_1 = {"name": "baz", "value": 2}
    data_answer_2 = {"name": "bay", "value": 1}
    response_answer_1 = client.post(
        "/quiz/answer/", json=data_answer_1, headers=token_header
    )
    response_answer_2 = client.post(
        "/quiz/answer/", json=data_answer_2, headers=token_header
    )
    assert response_answer_1.status_code == 200
    assert response_answer_2.status_code == 200
    assert response_answer_1.json() == data_answer_1
    assert response_answer_2.json() == data_answer_2


def test_create_result(run_database):
    data_result = {"age": 24, "sex": "male", "quiz": "{'category': 11}"}
    response_result = client.post("/quiz/result/", json=data_result)
    assert response_result.status_code == 200
    assert response_result.json() == data_result
