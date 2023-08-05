from dataclasses import dataclass
from typing import Optional

import constants
from constants import pp
from exceptions import IRunOutOfChipsException, LogicError
from player import Player
from shoe import Shoe
from strategies.basic_strategy import BasicStrategy
from strategies.dealers_strategy import DealersStrategy
from strategies.strategy import Action, Strategy


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

        self.shoe: Optional[Shoe] = None
        self.reshuffle_shoe()

        self.myself = Player(name="Myself", strategy=BasicStrategy(base_bet=2),
                             total_number_of_chips=self.my_total_number_of_chips)
        self.other_players = [
            Player(name=f"Dummy player {i}", strategy=Strategy(), total_number_of_chips=0)
            for i in range(self.number_of_players - 1)]
        self.dealer = Player(name="Dealer", strategy=DealersStrategy(), total_number_of_chips=0)

    def reshuffle_shoe(self):
        self.shoe = Shoe(number_of_decks=self.number_of_decks)
        self.shoe.shuffle()

    # todo right now the rules are not explicitly enforced! Raise errors every time the player wants to do something
    #  they are not supposed to

    def reset_player_hands(self):
        self.myself.hand.clear_bet()
        self.myself.hand.clear_cards()
        for player in self.other_players:
            player.hand.clear_bet()
            player.hand.clear_cards()
        self.dealer.hand.clear_bet()
        self.dealer.hand.clear_cards()

    def place_bets(self):
        self.myself.bet(amount=self.myself.strategy.get_bet_amount(
            my_number_of_chips=self.myself.total_number_of_chips))

    def deal_cards(self):
        self.dealer.hand.add_card(self.shoe.draw().turn_face_up())
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())

        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

        self.dealer.hand.add_card(self.shoe.draw())  # it is face down
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())
        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

    def check_if_dealer_has_blackjack(self):
        self.dealer.hand.list_of_cards[-1].turn_face_up()
        dealers_sum, _ = self.dealer.hand.get_sum()
        self.dealer.hand.list_of_cards[-1].turn_face_down()
        return dealers_sum == constants.BLACKJACK

    def execute_actions(self, player):
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
            if action == Action.double_if_possible_otherwise_stand:
                if player.hand.get_number_of_cards() == 2:
                    action = Action.double
                else:
                    action = Action.stand
            elif action == Action.double_if_possible_otherwise_hit:
                if player.hand.get_number_of_cards() == 2:
                    action = Action.double
                else:
                    action = Action.hit

            if action == Action.stand:
                break
            elif action == Action.hit:
                player.hand.add_card(self.shoe.draw().turn_face_up())
            elif action == Action.double:
                # todo: is this implemented correctly? I found this:
                #  Another option open to the player is doubling their bet when the original two cards dealt
                #  total 9, 10, or 11. This would mean it only applies if the sum is 9, 10, or 11?
                player.bet(amount=player.hand.bet)
                player.hand.add_card(self.shoe.draw().turn_face_up())
                break
            elif action == Action.split:
                extra_card = player.hand.list_of_cards.pop()
                current_bet = player.hand.bet
                self.execute_actions(player)
                player.hand.clear_cards()
                player.hand.add_card(extra_card)
                player.hand.place_bet(amount=current_bet)
                self.execute_actions(player)
            else:
                raise LogicError(
                    'If the game is implemented correctly, then you should never see this message. '
                    'If you do, then there is a major bug in the game implementation.')

            current_sum, _ = player.hand.get_sum()
            if current_sum >= constants.BLACKJACK:
                break

        if player == self.dealer:
            self.check_who_won_and_distribute_chips()

    def check_who_won_and_distribute_chips(self):
        my_sum, _ = self.myself.hand.get_sum()
        dealers_sum, _ = self.dealer.hand.get_sum()
        if my_sum == constants.BLACKJACK:
            self.myself.won_bet(self.myself.hand.bet * 2.5)
        elif my_sum > dealers_sum:
            self.myself.won_bet(self.myself.hand.bet * 2)  # dealer matches my amount
        elif my_sum == dealers_sum:
            self.myself.won_bet(self.myself.hand.bet * 1)
        else:
            # we lost
            pass

    def reshuffle_cards_if_there_are_too_few_cards_in_the_shoe(self):
        # todo: check value for CUT in casinos
        if self.shoe.get_number_of_remaining_cards() < constants.CUT:
            self.reshuffle_shoe()

    def play(self, round: int) -> GameStatus:
        pp(f'Round {round} starts')
        self.reset_player_hands()
        self.place_bets()
        self.deal_cards()

        if self.check_if_dealer_has_blackjack():
            pp('Dealer won, they have a blackjack')
            pp(self.dealer)
            # todo what if I have a blackjack as well?

            return GameStatus(round=round, total_number_of_chips=self.myself.total_number_of_chips)

        pp(self.dealer)
        for player in [self.myself] + self.other_players + [self.dealer]:
            self.execute_actions(player)

        self.reshuffle_cards_if_there_are_too_few_cards_in_the_shoe()
        return GameStatus(round=round, total_number_of_chips=self.myself.total_number_of_chips)

    def simulate(self):
        result = [GameStatus(round=-1, total_number_of_chips=self.myself.total_number_of_chips)]
        for i in range(self.number_of_rounds):
            try:
                result.append(self.play(round=i))
            except IRunOutOfChipsException:
                print('Stopped simulation early because we run out of chips')
                break
        return result
