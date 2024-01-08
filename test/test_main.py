import os


def test_request_example(client):
    response = client.get("/")
    assert b"Hello World!" in response.data
    assert response.status_code == 200