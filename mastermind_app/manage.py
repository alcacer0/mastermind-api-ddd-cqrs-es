from flask import current_app
from flask.cli import FlaskGroup, with_appcontext

from mastermind.games.infraestructure import event_store_db
from mastermind import create_app


cli = FlaskGroup(create_app=create_app)


@cli.command('create_games_db')
@with_appcontext
def create_games_db():
    event_store_db.init_app(current_app)
    event_store_db.drop_all()
    event_store_db.create_all()
    event_store_db.session.commit()


if __name__ == "__main__":
    cli()
