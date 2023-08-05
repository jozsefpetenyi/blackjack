from random import shuffle
from deck import Deck


class Shoe:
    def __init__(self, number_of_decks: int):
        self.number_of_decks = number_of_decks

        self.container = []

        for i in range(number_of_decks):
            self.container.extend(Deck().cards)

    def shuffle(self):
        shuffle(self.container)

    def draw(self):
        return self.container.pop()

    def get_number_of_remaining_cards(self):
        return len(self.container)

    def __str__(self):
        return str(self.container)
