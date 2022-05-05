import pytest
from requests import request
from app import create_app
from app import db
from flask.signals import request_finished
from app.models.cats import Cat

@pytest.fixture
def app():
    app = create_app({"Testing":True})

    @request_finished.connect_via(app)
    def expire_session(sender,response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app 
    
    with app.app_context():
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def seven_cats(app):
    jazz = Cat(id = 1, name = 'Jazz', color = 'black', age = 8)
    cosmo = Cat(id = 2, name = 'Cosmo', color = 'tuxedo', age = 8)
    lily = Cat(id = 3, name = 'Lily', color = 'brown and black', age = 6)
    ellis = Cat(id = 4, name = 'Ellis', color = 'orange', age = 2)
    monster = Cat(id = 5, name = 'Monster', color = 'grey', age = 14)
    simba = Cat(id = 6, name = 'Simba', color = 'orange', age = 8)
    jenkins = Cat(id = 7, name = 'Jenkins', color = 'tuxedo', age = 4)

    db.session.add_all([jazz, cosmo, lily, ellis, monster, simba, jenkins])
    db.session.commit()
