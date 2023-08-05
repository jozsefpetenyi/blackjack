from enum import Enum
from typing import Union

import constants

class Suite(Enum):
    hearts = '♥️'
    spades = '♠️'
    diamonds = '♦️'
    clubs = '♣️'

    def __str__(self):
        return str(self.value)


class Card:
    def __init__(self, suite: Suite, letter: str, value: int):
        self.suite = suite
        self.letter = letter
        self.value = value
        self.face_up = False

    def turn_face_up(self):
        self.face_up = True
        return self
    def turn_face_down(self):
        self.face_up = False
        return self


    def __str__(self):
        return f'{self.suite}{self.letter}' + ('' if self.face_up else '(face down)')

    def __repr__(self):
        return str(self)


