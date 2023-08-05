import unittest

from deck import Deck
from hand import Hand, HandType


class CardArithmeticsTests(unittest.TestCase):
    def assertSumHelper(self, letters: list[str], expected: tuple[int, HandType]):
        cards = [Deck.get_card(l).turn_face_up() for l in letters]
        sum, type = Hand(cards=cards, bet=1).get_sum()
        expected_sum, expected_type = expected
        self.assertEqual(sum, expected_sum)
        self.assertEqual(type, expected_type)

    def testAddTwoCardsNoAces(self):
        self.assertSumHelper(['2', '3'], (5, HandType.hard))
        self.assertSumHelper(['6', '3'], (9, HandType.hard))
        self.assertSumHelper(['J', 'Q'], (20, HandType.hard))
        self.assertSumHelper(['J', '10'], (20, HandType.hard))
        self.assertSumHelper(['2', 'K'], (12, HandType.hard))
        self.assertSumHelper(['K', '2'], (12, HandType.hard))

    def testAddThreeCardsNoAces(self):
        self.assertSumHelper(['2', '2', '2'], (6, HandType.hard))
        self.assertSumHelper(['Q', '2', '2'], (14, HandType.hard))
        self.assertSumHelper(['5', '2', 'K'], (17, HandType.hard))
        self.assertSumHelper(['3', 'J', '9'], (22, HandType.hard))
        self.assertSumHelper(['8', '7', '3'], (18, HandType.hard))
        self.assertSumHelper(['Q', 'J', 'K'], (30, HandType.hard))
        self.assertSumHelper(['K', 'K', 'K'], (30, HandType.hard))

    def testAddTwoCardsOneAce(self):
        self.assertSumHelper(['2', 'A'], (13, HandType.soft))
        self.assertSumHelper(['A', '2'], (13, HandType.soft))
        self.assertSumHelper(['A', 'K'], (21, HandType.soft))
        self.assertSumHelper(['A', '9'], (20, HandType.soft))

    def testAddThreeCardsOneAce(self):
        self.assertSumHelper(['A', '10', '10'], (21, HandType.hard))
        self.assertSumHelper(['A', '2', '9'], (12, HandType.hard))
        self.assertSumHelper(['2', '9', 'A'], (12, HandType.hard))

    def testAddCardsEdgeCases(self):
        self.assertSumHelper(['A', 'A'], (12, HandType.pair))
        self.assertSumHelper(['A', 'A', 'A'], (13, HandType.soft))
        self.assertSumHelper(['A'] * 21, (21, HandType.hard))
        self.assertSumHelper(['A'] * 22, (22, HandType.hard))
        self.assertSumHelper(['2'] * 200, (400, HandType.hard))
        self.assertSumHelper(['A'] * 11, (21, HandType.soft))
        self.assertSumHelper(['A'], (11, HandType.soft))
        self.assertSumHelper([], (0, HandType.hard))

    def testAddCardsFaceDown(self):
        self.assertEqual(Hand(cards=[Deck.get_card('2'), Deck.get_card('8')], bet=1).get_sum(), (0, HandType.hard))
        self.assertEqual(Hand(cards=[Deck.get_card('2').turn_face_up(), Deck.get_card('8')], bet=1).get_sum(),
                         (2, HandType.hard))
        self.assertEqual(Hand(cards=[Deck.get_card('A').turn_face_up(), Deck.get_card('A')], bet=1).get_sum(),
                         (11, HandType.soft))
        self.assertEqual(
            Hand(cards=[Deck.get_card('A').turn_face_up(), Deck.get_card('A'), Deck.get_card('K').turn_face_up()],
                 bet=1).get_sum(), (21, HandType.soft))

    def testAddPairs(self):
        self.assertSumHelper(['A', 'A'], (12, HandType.pair))
        self.assertSumHelper(['2', '2'], (4, HandType.pair))
        self.assertSumHelper(['4', '4'], (8, HandType.pair))
        self.assertSumHelper(['K', 'K'], (20, HandType.pair))
        self.assertSumHelper(['Q', 'Q'], (20, HandType.pair))
        self.assertEqual(Hand(cards=[Deck.get_card('A').turn_face_up(), Deck.get_card('A')], bet=1).get_sum(),
                         (11, HandType.soft))
        self.assertEqual(Hand(cards=[Deck.get_card('2').turn_face_up(), Deck.get_card('2')], bet=1).get_sum(),
                         (2, HandType.hard))



if __name__ == '__main__':
    unittest.main()
