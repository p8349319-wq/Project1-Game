from enum import Enum

class special_event(Enum):
    ATTACK = "Massive Attack"
    DEFENSE = "Unbreakable Wall"
    SPEED = "Fast Acceleration"
    EXTRA_Attack = "Extra Attack"
    NO_EVENT = "No Event"

weights = {
    special_event.ATTACK : 15,
    special_event.DEFENSE : 20,
    special_event.SPEED : 25,
    special_event.NO_EVENT : 40
}