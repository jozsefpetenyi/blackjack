from dataclasses import dataclass

import constants
from constants import pp
from player import Player
from shoe import Shoe
from strategies.basic_strategy import BasicStrategy
from strategies.dealers_strategy import DealersStrategy
from strategies.strategy import Action, Strategy
from exceptions import IRunOutOfChipsException

@dataclass
class GameStatus:
    round: int
    total_number_of_chips: int


class Game:
    def __init__(self, number_of_decks: int, number_of_players: int, my_total_number_of_chips: int,
                 number_of_rounds: int):
        self.number_of_decks = number_of_decks
        self.number_of_players = number_of_players  # including myself
        self.my_total_number_of_chips = my_total_number_of_chips
        self.number_of_rounds = number_of_rounds

        self.reshuffle_shoe()

        self.myself = Player(name="Myself", strategy=BasicStrategy(),
                             total_number_of_chips=self.my_total_number_of_chips)
        self.other_players = [
            Player(name=f"Dummy player {i}", strategy=Strategy(), total_number_of_chips=0)
            for i in range(self.number_of_players - 1)]
        self.dealer = Player(name="Dealer", strategy=DealersStrategy(), total_number_of_chips=0)

    def reshuffle_shoe(self):
        self.shoe = Shoe(number_of_decks=self.number_of_decks)
        self.shoe.shuffle()

    def play(self, round:int) -> GameStatus:
        pp('Rounds starts')
        self.myself.hand.clear_bet()
        self.myself.hand.clear_cards()
        for player in self.other_players:
            player.hand.clear_bet()
            player.hand.clear_cards()
        self.dealer.hand.clear_bet()
        self.dealer.hand.clear_cards()

        self.myself.bet(amount=self.myself.strategy.get_bet_amount(
            my_number_of_chips=self.myself.total_number_of_chips))

        self.dealer.hand.add_card(self.shoe.draw().turn_face_up())
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())

        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

        self.dealer.hand.add_card(self.shoe.draw())  # it is face down
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())
        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

        self.dealer.hand.list_of_cards[-1].turn_face_up()
        dealers_sum, _ = self.dealer.hand.get_sum()
        self.dealer.hand.list_of_cards[-1].turn_face_down()
        if dealers_sum == constants.BLACKJACK:
            pp('Dealer won, they have a blackjack')
            pp(self.dealer)
            self.myself.hand.clear_bet()
            self.myself.hand.clear_cards()
            # todo what if I have a blackjack as well?

            return GameStatus(round=round, total_number_of_chips=self.myself.total_number_of_chips)


        for player in [self.myself] + self.other_players + [self.dealer]:
            if player == self.dealer:
                self.dealer.hand.list_of_cards[-1].turn_face_up()

            while True:
                pp(player)
                action = player.strategy.get_action(
                    my_hand=player.hand,
                    dealers_hand=self.dealer.hand,
                    other_players_hands=[p.hand for p in self.other_players],
                    my_number_of_chips=player.total_number_of_chips
                )
                if action == Action.stand:
                    break
                elif action == Action.hit:
                    player.hand.add_card(self.shoe.draw().turn_face_up())
                # todo implament other actions
                else:
                    player.hand.add_card(self.shoe.draw().turn_face_up())

        my_sum, _ = self.myself.hand.get_sum()
        dealers_sum, _ = self.dealer.hand.get_sum()
        if my_sum == constants.BLACKJACK:
            self.myself.won_bet(self.myself.hand.bet * 2.5)
        elif my_sum > dealers_sum:
            self.myself.won_bet(self.myself.hand.bet * 2)  # dealer matches my amount
        elif my_sum == dealers_sum:
            self.myself.won_bet(self.myself.hand.bet * 1)
        else:
            pass

        if self.shoe.get_number_of_remaining_cards() < constants.CUT:
            self.reshuffle_shoe()

        return GameStatus(round=round, total_number_of_chips=self.myself.total_number_of_chips)

    def simulate(self):
        result = []
        for i in range(self.number_of_rounds):
            try:
                result.append(self.play(round=i))
            except IRunOutOfChipsException:
                print('Stopped simulation early because we run out of chips')
                break
        return result
