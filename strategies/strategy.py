from hand import Hand, HandType
from enum import Enum, auto


class Action(Enum):
    hit = auto()
    stand = auto()
    double = auto()
    split = auto()

    def __repr__(self):
        return self.name


class Strategy:
    def __init__(self):
        pass

    def get_bet_amount(self, my_number_of_chips: int) -> int:
        return 0

    def get_action(self, my_hand: Hand, dealers_hand: Hand, other_players_hands: list[Hand], my_number_of_chips: int) -> Action:
        return Action.stand



