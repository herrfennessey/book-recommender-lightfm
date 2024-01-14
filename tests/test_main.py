def test_root_path(client):
    response = client.get("/")
    assert b"Hello World!" in response.data
    assert response.status_code == 200


def test_health_path(client):
    response = client.get("/health")
    assert b"Healthy" in response.data
    assert response.status_code == 200


def test_model_info_path(client):
    response = client.get("/model-info")
    assert response.status_code == 200
    assert response.json == {
        "num_books": 24189,
        "num_reviews": 66038,
        "num_users": 341,
        "train_date": "Sat, 13 Jan 2024 12:53:17 GMT",
    }


def test_predict(client):
    response = client.post(
        "/predict", json={"user_id": "24697113", "genres": ["Fiction"], "limit": 5}
    )
    assert response.status_code == 200
    assert len(response.json) == 5
