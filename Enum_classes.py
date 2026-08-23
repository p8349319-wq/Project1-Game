from enum import Enum
from Player import Player


class special_event(Enum):
    ATTACK = "Massive Attack"
    DEFENSE = "Unbreakable Wall"
    SPEED = "Fast Acceleration"
    EXTRA_Attack = "Extra Attack"
    NO_EVENT = "No Event"


class player_status(Enum):
    WIN = "Win"
    LOSE = "Lose"
    IN_MATCH = "Player in the match"


weights = {
    special_event.ATTACK: 10,
    special_event.DEFENSE: 20,
    special_event.SPEED: 25,
    special_event.NO_EVENT: 45,
}


def calculate_special_events_weight(weights: dict, player: Player):
    if player.luck != 0:
        final_weights = {
            event: weight * (1 + (player.luck / 100))
            for event, weight in weights.items()
        }
    else:
        final_weights = weights
    return final_weights
