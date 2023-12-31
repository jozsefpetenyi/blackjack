from dataclasses import dataclass
from typing import Optional

import constants
from constants import log
from exceptions import IRunOutOfChipsException, LogicError, ActionIsAgainstTheRulesError
from hand import Hand
from player import Player
from shoe import Shoe
from strategies.dealers_strategy import DealersStrategy
from strategies.strategy import Action, Strategy, Outcome


@dataclass
class GameStatus:
    round: int
    total_number_of_chips: int


class Game:
    def __init__(self, number_of_decks: int, number_of_players: int, my_total_number_of_chips: int,
                 number_of_rounds: int, strategy: Strategy):
        self.number_of_decks = number_of_decks
        self.number_of_players = number_of_players  # including myself
        self.my_total_number_of_chips = my_total_number_of_chips
        self.number_of_rounds = number_of_rounds
        self.strategy = strategy

        self.shoe: Optional[Shoe] = None
        self.reshuffle_shoe()

        self.myself = Player(name="Me",
                             strategy=strategy,
                             total_number_of_chips=self.my_total_number_of_chips)
        self.other_players = [
            Player(name=f"Dummy player {i}", strategy=Strategy(), total_number_of_chips=0)
            for i in range(self.number_of_players - 1)]
        self.dealer = Player(name="Dealer", strategy=DealersStrategy(), total_number_of_chips=0)

    @staticmethod
    def is_blackjack(hand: Hand):
        is_2_cards = hand.get_number_of_cards() == 2
        sum, hand_type = hand.get_sum()
        is_sum_21 = sum == constants.BLACKJACK
        return is_2_cards and is_sum_21

    def reshuffle_shoe(self):
        self.shoe = Shoe(number_of_decks=self.number_of_decks)
        self.shoe.shuffle()

    # todo right now the rules are not explicitly enforced! Raise errors every time the player wants to do something
    #  they are not supposed to

    def reset_player_hands(self):
        log.debug("Resetting player hands...")
        self.myself.hand.clear_bet()
        self.myself.hand.clear_cards()
        self.myself.clear_actions()
        for player in self.other_players:
            player.hand.clear_bet()
            player.hand.clear_cards()
            player.clear_actions()
        self.dealer.hand.clear_bet()
        self.dealer.hand.clear_cards()
        self.dealer.clear_actions()

    def place_bets(self):
        log.debug("")
        log.debug("Placing bets...")
        self.myself.bet(amount=self.myself.strategy.get_bet_amount(
            my_number_of_chips=self.myself.total_number_of_chips))

    def deal_cards(self):
        log.debug("")
        log.debug("Dealing cards...")
        self.dealer.hand.add_card(self.shoe.draw().turn_face_up())
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())

        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

        self.dealer.hand.add_card(self.shoe.draw())  # it is face down
        self.myself.hand.add_card(self.shoe.draw().turn_face_up())
        for player in self.other_players:
            player.hand.add_card(self.shoe.draw().turn_face_up())

        log.debug(self.myself)
        log.debug(self.dealer)
        for player in self.other_players:
            log.debug(player)

    def check_if_dealer_has_blackjack(self):
        self.dealer.hand.list_of_cards[-1].turn_face_up()
        dealers_sum, _ = self.dealer.hand.get_sum()
        self.dealer.hand.list_of_cards[-1].turn_face_down()
        return dealers_sum == constants.BLACKJACK

    def execute_actions(self, player):
        log.debug("")
        log.debug(f'Executing actions for player "{player.name}"...')
        if player == self.dealer:
            self.dealer.hand.list_of_cards[-1].turn_face_up()

        while True:
            action = player.strategy.get_action(
                my_hand=player.hand,
                dealers_hand=self.dealer.hand,
                other_players_hands=[p.hand for p in self.other_players],
                my_number_of_chips=player.total_number_of_chips
            )
            log.debug(f'Action: {action}\t({player.hand})')

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

            if player.hand.get_number_of_cards() != 2 and action in [Action.double, Action.split]:
                raise ActionIsAgainstTheRulesError(
                    f'Action {action} is not permitted when player has {player.hand.get_number_of_cards()} cards.')

            # logging action
            player.add_action(action)

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

        log.debug(f'Executed actions: {player.actions}')
        log.debug(f'Final hand: {player.hand}')

        if player == self.dealer:
            self.check_who_won_and_distribute_chips()

    def check_who_won_and_distribute_chips(self):
        log.debug('')
        log.debug('Evaluating hands...')
        self.dealer.hand.list_of_cards[-1].turn_face_up()

        log.debug(f'My hand: {self.myself.hand}')
        log.debug(f'Dealer\'s hand: {self.dealer.hand}')

        my_sum, _ = self.myself.hand.get_sum()
        dealers_sum, _ = self.dealer.hand.get_sum()

        if self.is_blackjack(self.myself.hand) and self.is_blackjack(self.dealer.hand):
            self.myself.outcome = Outcome.push_2_blackjacks
            self.myself.won_bet(self.myself.hand.bet * 1)

        elif self.is_blackjack(self.dealer.hand):
            self.myself.outcome = Outcome.lost_dealer_has_a_blackjack
            pass

        elif self.is_blackjack(self.myself.hand):
            self.myself.outcome = Outcome.won_with_a_blackjack
            self.myself.won_bet(self.myself.hand.bet * 2.5)

        elif my_sum > constants.BLACKJACK:
            self.myself.outcome = Outcome.lost_bust
            pass

        elif dealers_sum > constants.BLACKJACK:
            self.myself.outcome = Outcome.won_dealer_busts
            self.myself.won_bet(self.myself.hand.bet * 2)

        elif my_sum > dealers_sum:
            self.myself.outcome = Outcome.won_higher_sum
            self.myself.won_bet(self.myself.hand.bet * 2)  # dealer matches my amount

        elif my_sum == dealers_sum:
            self.myself.outcome = Outcome.push_equal_sum
            self.myself.won_bet(self.myself.hand.bet * 1)

        else:
            self.myself.outcome = Outcome.lost_lower_sum
            pass

        log.debug(f'{self.myself.outcome}')

    def reshuffle_cards_if_there_are_too_few_cards_in_the_shoe(self):
        # todo: check value for CUT in casinos
        if self.shoe.get_number_of_remaining_cards() < constants.CUT:
            log.debug(
                f'Reshuffling cards (number of cards ({self.shoe.get_number_of_remaining_cards()}) '
                f'is lower than cut value ({constants.CUT}))')
            self.reshuffle_shoe()

    def play(self, round: int) -> GameStatus:
        log.debug(f'===== Round {round} starts =====')
        self.reset_player_hands()
        self.place_bets()
        self.deal_cards()

        if self.check_if_dealer_has_blackjack():
            log.debug('Dealer has a blackjack, ending turn...')
            self.check_who_won_and_distribute_chips()

        else:
            for player in [self.myself] + self.other_players + [self.dealer]:
                self.execute_actions(player)

        self.reshuffle_cards_if_there_are_too_few_cards_in_the_shoe()
        log.debug(f'===== Round {round} ends =====')

        return GameStatus(round=round, total_number_of_chips=self.myself.total_number_of_chips)

    def simulate(self):
        log.debug(f'===== Simulation starts, there will be {self.number_of_rounds} round(s) =====')
        result = [GameStatus(round=-1, total_number_of_chips=self.myself.total_number_of_chips)]
        for i in range(self.number_of_rounds):
            try:
                result.append(self.play(round=i))
            except IRunOutOfChipsException:
                log.debug('Simulation stopped early because we run out of chips')
                break
        return result
