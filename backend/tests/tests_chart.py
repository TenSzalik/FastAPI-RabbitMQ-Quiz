from conftest import client


def test_chart():
    data = {
        "queue_smooth_data": {
            "category1": 1,
            "category2": 2,
            "very_unique_name_foobarbaz": 3,
        }
    }
    response = client.post("/chart/", json=data)
    assert response.status_code == 200
    assert "category1" in response.read().decode()
    assert "category2" in response.read().decode()
    assert "very_unique_name_foobarbaz" in response.read().decode()
    assert "category4" not in response.read().decode()
    assert response.read()[1:6].decode() == "<div>"
