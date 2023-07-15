from conftest import client


def test_create_token(run_database, load_database):
    jwt_header = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9"
    form_data = {"username": "foobarbaz@gmail.com", "password": "FooBarBaz1234"}

    response_token = client.post("/token/", data=form_data)

    assert response_token.status_code == 200
    assert response_token.json().get("access_token").split(".")[0] == jwt_header
