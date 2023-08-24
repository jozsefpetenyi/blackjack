from typing import Optional
from hand import Hand
from strategies.basic_strategy import BasicStrategy
from strategies.strategy import Strategy, Action, Outcome
from exceptions import IRunOutOfChipsException
from constants import log


class Player:
    def __init__(self, name:str, strategy: Strategy, total_number_of_chips: int):
        self.name = name
        self.total_number_of_chips = total_number_of_chips
        self.hand = Hand(cards=[], bet=0)
        self.strategy = strategy
        self.actions: list[Action] = []
        self.outcome: Optional[Outcome] = None

    def bet(self, amount: int):
        log_statement = f'bet({self.name}: {amount}, from {self.total_number_of_chips} to '
        if self.total_number_of_chips <= 0:
            raise IRunOutOfChipsException('There is no more chips left')

        if amount > self.total_number_of_chips:
            self.hand.place_bet(self.total_number_of_chips)
            self.total_number_of_chips = 0

        self.total_number_of_chips -= amount
        self.hand.place_bet(amount)
        log.debug(f'{log_statement} {self.total_number_of_chips})')

    def won_bet(self, amount: int):
        self.total_number_of_chips += amount

    def clear_actions(self):
        self.actions = []

    def add_action(self, action: Action):
        self.actions.append(action)

    def __str__(self):
        return f'{self.name}: {self.hand}, chips: {self.total_number_of_chips}'
