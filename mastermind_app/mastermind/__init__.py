from flask import Flask


def create_app(use_test_config=False):
    app = Flask(__name__)

    if use_test_config:
        app.config.from_object('mastermind.config.TestConfig')
    else:
        app.config.from_object('mastermind.config.Config')

    from mastermind.games.infraestructure import event_store_db
    event_store_db.init_app(app)

    from mastermind.games.api.game import mastermind_games_api
    mastermind_games_api.init_app(app)

    return app
