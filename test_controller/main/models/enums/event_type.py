from enum import Enum, auto


class EventType(Enum):

    ADDED = "ADDED"
    DELETED = "DELETED"
    MODIFIED = "MODIFIED"