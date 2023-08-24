from enum import Enum, auto

from hand import Hand


class Action(Enum):
    hit = auto()
    stand = auto()
    double_if_possible_otherwise_hit = auto()
    double_if_possible_otherwise_stand = auto()
    split = auto()
    double = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)


class Strategy:
    def __init__(self):
        pass

    def get_bet_amount(self, my_number_of_chips: int) -> int:
        return 0

    def get_action(self, my_hand: Hand, dealers_hand: Hand, other_players_hands: list[Hand],
                   my_number_of_chips: int) -> Action:
        return Action.stand


class Outcome(Enum):
    push_2_blackjacks = 'Push (both me and the dealer have blackjacks)'
    lost_dealer_has_a_blackjack = 'Lost (dealer has a blackjack)'
    won_with_a_blackjack = 'Won (blackjack)'
    won_higher_sum = 'Won (sum is higher than dealer\'s)'
    push_equal_sum = 'Push (sum is equal to dealer\'s)'
    lost_lower_sum = 'Lost (sum is lower than dealer\'s)'
    lost_bust = 'Lost (sum is over 21)'
    won_dealer_busts = 'Won (dealer has a sum over 21)'

    def __str__(self):
        return f'Outcome: {self.value}'

    def __repr__(self):
        return str(self)
