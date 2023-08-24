import unittest

from deck import Deck
from game import Game
from shoe import Shoe
from strategies.basic_strategy import BasicStrategy
from strategies.strategy import Action, Outcome


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
        :param letters: list of strings e.g. '1', 'A', '4', '10'. The cards on the RIGHT of the list will be drawn first.
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
        self._setShoeToHaveTheFollowingCards(game.shoe, ['6'] * 100 + ['6', '8', '3', 'J', '4'])

        result = game.simulate()

        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 - BASE_BET)

    def testHitAction_oneHitActionOneStand_chipsIncreased_endedUpWithThreeCards(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['8', '5', '7', '7', 'J'])

        result = game.simulate()

        self.assertEqual(game.myself.actions, [Action.hit, Action.stand])
        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 + BASE_BET)
        self.assertEqual(game.myself.hand.get_number_of_cards(), 3)

    def testHitAction_twoHitActionOneStand_chipsDecreased_endedUpWithFourCards(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['4', '2', '2', 'Q', 'A', 'J'])

        result = game.simulate()

        self.assertEqual(game.myself.actions, [Action.hit, Action.hit, Action.stand])
        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 - BASE_BET)
        self.assertEqual(game.myself.hand.get_number_of_cards(), 4)

    def testDoubleAction(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['10', '3', '7', '8', 'A'])

        result = game.simulate()

    def testDealerHasABlackjack_lostWithOutcomeBlackjack_noAction_lostMoney_only2CardsInHand(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=1,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        self._setShoeToHaveTheFollowingCards(game.shoe, ['2', 'A', '2', 'J'])

        result = game.simulate()

        self.assertEqual(game.myself.outcome,  Outcome.lost_dealer_has_a_blackjack)
        self.assertEqual(game.myself.actions, [])
        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 - BASE_BET)
        self.assertEqual(game.myself.hand.get_number_of_cards(), 2)


    def testIhaveABlackjack_wonWithABlackJack_moneyIncreasedWithOneAndHalf_have2CardsInHand(self):
        BASE_BET = 2
        game = Game(number_of_decks=6,
                    number_of_players=2,
                    my_total_number_of_chips=10000,
                    number_of_rounds=1,
                    strategy=BasicStrategy(base_bet=BASE_BET))
        # dealer: 4, me: A, dummy: 4, dealer: 6, me: Q, dummy: 6
        self._setShoeToHaveTheFollowingCards(game.shoe, ['6'] * 10 + ['Q', '6', '4', 'A', '4'])

        result = game.simulate()

        self.assertEqual(game.myself.outcome, Outcome.won_with_a_blackjack)
        self.assertEqual(game.myself.actions, [Action.stand])
        self.assertEqual(result[0].total_number_of_chips, 10000)
        self.assertEqual(result[1].total_number_of_chips, 10000 + BASE_BET * 1.5)
        self.assertEqual(game.myself.hand.get_number_of_cards(), 2)
