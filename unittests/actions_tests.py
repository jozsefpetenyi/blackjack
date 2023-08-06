import unittest

from deck import Deck
from game import Game
from shoe import Shoe
from strategies.basic_strategy import BasicStrategy


# todo add much more unit tests to make sure actions and chip distribution work as expected
class ActionsTests(unittest.TestCase):

    # def testSplitAction(self):
    #     game = Game(number_of_decks=6,
    #                 number_of_players=1,
    #                 my_total_number_of_chips=10000,
    #                 number_of_rounds=1)
    #
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #     game.shoe.container.append(Deck.get_card('6'))
    #
    #     game.shoe.container.append(Deck.get_card('2'))  # will be mine
    #     game.shoe.container.append(Deck.get_card('3'))  # will be dealer's
    #     game.shoe.container.append(Deck.get_card('2'))  # will be mine
    #     game.shoe.container.append(Deck.get_card('4'))  # will be dealer's
    #
    #     print(game.myself.total_number_of_chips)
    #     result = game.simulate()
    #     print(game.myself.total_number_of_chips)

    @staticmethod
    def _setShoeToHaveTheFollowingCards(shoe: Shoe, letters: list[str]):
        """
        Helper method for unit testing. This sets the cards in the shoe to the list provided.
        :param shoe: Shoe object that needs to be filled
        :param letters: list of strings e.g. '1', 'A', '4', '10'. The cards on the left of the list will be drawn first.
        :return: None
        """

        shoe.clear()
        for letter in letters:
            shoe.container.append(Deck.get_card(letter))

    def testStandAction_won_chipsIncreased(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['6'] * 100 + ['Q', '3', 'J', '4'])

        result = game.simulate()

        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 + BASE_BET)

    def testStandAction_lost_chipsDecreased(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['6'] * 100 + ['8', '3', 'J', '4'])

        result = game.simulate()

        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 - BASE_BET)

    def testHitAction_oneHitActionOneStand_chipsIncreased(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['8'] * 100 + ['5', '7', '7', 'J'])

        result = game.simulate()

        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 + BASE_BET)
