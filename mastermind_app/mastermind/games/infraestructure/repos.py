from .sql import EventStore
from mastermind.shared.model import UniqueID
from ..model import GameWriteRepository, Game


# One repository per aggregate

class EventSourcingGameRepository(GameWriteRepository):
    def __init__(self, event_store: EventStore):
        self._event_store = event_store

    def save(self, aggregate_root: Game) -> Game:
        self._event_store.save_events(
            aggregate_id=aggregate_root.game_id,
            events=aggregate_root.uncommitted_changes,
            expected_version=aggregate_root.version
        )
        aggregate_root.mark_changes_as_committed()
        return aggregate_root

    def get_by_id(self, aggregate_id: UniqueID) -> Game:
        event_stream = self._event_store.load_stream(aggregate_id)
        return Game(event_stream)
