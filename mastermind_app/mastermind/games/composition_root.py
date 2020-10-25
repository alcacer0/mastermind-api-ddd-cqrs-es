from contextlib import contextmanager

from .model import GameWriteRepository
from .infraestructure import EventSourcingGameRepository, PostgresEventStore, sql_session_scope


@contextmanager
def get_game_write_repo() -> GameWriteRepository:
    with sql_session_scope() as session:
        event_store = PostgresEventStore(session)
        yield EventSourcingGameRepository(event_store)
