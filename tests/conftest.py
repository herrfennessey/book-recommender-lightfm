import pytest

from src.main import create_app


@pytest.fixture
def client():
    # Setup the app with testing config
    app = create_app(True)

    # Use the test client provided by Flask
    with app.test_client() as client:
        yield client
