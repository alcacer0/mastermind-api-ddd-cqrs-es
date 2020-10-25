import attr
import datetime
from typing import List
from dataclasses import dataclass, field

# Note:
# When dealing with the events we use the `attr` package for the following reasons:
#  - ATM `dataclasses` does not support a keyword only feature, we need it because of the following reason
#  - when using dataclass on a parent class that has default argument (such as version), it will throw error
#    that there is non default parameters after default parameter.


def generate_utc_timestamp() -> float:
    return datetime.datetime.now(datetime.timezone.utc).timestamp()


@attr.s(kw_only=True, frozen=True)
class BaseEvent:
    operation_id: str = attr.ib()
    version: int = attr.ib(default=1)
    timestamp: float = attr.field(factory=generate_utc_timestamp)


@dataclass(frozen=True)
class EventStream:
    events: List[BaseEvent]
    version: int = field(default=-1)

