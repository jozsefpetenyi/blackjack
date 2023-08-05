from random import choice

from card import Card, Suite
from exceptions import DidNotFindCardException


class Deck:
    def __init__(self):
        self.cards: list[Card] = []
        self._initiate()

    def _initiate(self):
        suites = (s for s in Suite)

        for suite in suites:
            for i in range(2, 11):
                self.cards.append(Card(suite=suite, letter=f'{i}', value=i))

            for letter in ['J', 'Q', 'K']:
                self.cards.append(Card(suite=suite, letter=letter, value=10))

            # note that A could be worth 1, but it's not stored here but handled in the Hand.get_sum method
            self.cards.append(Card(suite=suite, letter="A", value=11))

    @staticmethod
    def get_random_card():
        return choice(Deck().cards)

    @staticmethod
    def get_card(letter: str):
        try:
            return next(filter(lambda x: x.letter == letter, Deck().cards))
        except StopIteration:
            raise DidNotFindCardException('Wrong letter provided')

    def __str__(self):
        return str(self.cards)

    def __repr__(self):
        return str(self)
