import os
from conftest import client


def test_create_unsuccessful_admin_user(run_database):
    password = "TestPasswordFooBarBaz1234"
    data_user = {
        "email": "testfoobarbaz2@gmail.com",
        "password": password,
        "key": "incorrect_key",
    }

    response_user = client.post("/user/", json=data_user)
    assert response_user.status_code == 401
    assert response_user.json().get("detail") == "Key is incorrect"


def test_create_successful_admin_user(run_database):
    password = "TestPasswordFooBarBaz1234"
    SECRET_KEY = os.environ["SECRET_KEY"]
    data_user = {
        "email": "testemail5@gmail.com",
        "password": password,
        "key": SECRET_KEY,
    }

    response_user = client.post("/user/", json=data_user)

    assert response_user.status_code == 200
    assert response_user.json().get("email") == data_user.get("email")
    assert response_user.json().get("hashed_password") != password
    assert response_user.json().get("key") == None
