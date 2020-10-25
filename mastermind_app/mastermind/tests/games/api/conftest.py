import pytest

from mastermind import create_app


@pytest.fixture
def app():
    app = create_app(use_test_config=True)
    return app

@pytest.fixture
def test_db(app):
    from mastermind.games.infraestructure import event_store_db
    event_store_db.init_app(app)
    event_store_db.drop_all()
    event_store_db.create_all()
    event_store_db.session.commit()

    yield event_store_db # This is where testing happens

    event_store_db.session.close()
    event_store_db.drop_all()
    event_store_db.session.commit()
