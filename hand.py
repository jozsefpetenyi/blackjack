from enum import Enum, auto

import constants
from card import Card


class HandType(Enum):
    soft = auto()
    hard = auto()
    pair = auto()

    def __str__(self):
        return self.name

    def __repr__(self):
        return str(self)



class Hand:
    def __init__(self, cards: list[Card], bet: int):
        self.list_of_cards = cards
        self.bet = bet

    def place_bet(self, amount):
        self.bet = amount

    def clear_bet(self):
        self.bet = 0

    def add_card(self, card: Card):
        self.list_of_cards.append(card)

    def clear_cards(self):
        self.list_of_cards = []

    def get_number_of_cards(self):
        return len(self.list_of_cards)

    def get_sum(self) -> tuple[int, HandType]:
        """
        Getting the sum and the type (soft/hard) of the hand.
        The implementation probably could be simplified.
        For correctness pls check the unit tests.
        Note, that face down cards are not counted towards the sum.
        :return: tuple of the sum and type(soft/hard)
        """
        face_up_cards = []
        for card in self.list_of_cards:
            if card.face_up:
                face_up_cards.append(card)

        if len(face_up_cards) == 2:
            if face_up_cards[0].letter == face_up_cards[1].letter:
                if face_up_cards[0].letter == 'A':
                    return 12, HandType.pair
                else:
                    return face_up_cards[0].value * 2, HandType.pair

        sum = 0
        number_of_aces_that_is_worth_11 = 0
        for card in face_up_cards:
            sum += card.value
            if card.letter == 'A':
                number_of_aces_that_is_worth_11 += 1

        if number_of_aces_that_is_worth_11 == 0:
            return sum, HandType.hard

        if sum <= constants.BLACKJACK:
            return sum, HandType.soft

        while number_of_aces_that_is_worth_11 > 0:

            if sum <= constants.BLACKJACK:
                return sum, HandType.soft

            sum -= 10  # note that aces are worth 11 or 1 (difference is 10)
            number_of_aces_that_is_worth_11 -= 1

        return sum, HandType.hard

    def split(self):
        if len(self.list_of_cards) != 2:
            raise ValueError('You cannot split because you dont have exactly 2 cards in your hand')

        return Hand([self.list_of_cards[0]], self.bet), Hand([self.list_of_cards[1]], self.bet)

    def __str__(self):
        sum, type = self.get_sum()
        return f'cards: {self.list_of_cards} (sum: {sum}, type: {type}), bet: {self.bet}'
