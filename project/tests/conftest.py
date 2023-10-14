import pytest
from project.src.database_model import db
from project import create_app

@pytest.fixture()
def app():
    
    app = create_app()
    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

