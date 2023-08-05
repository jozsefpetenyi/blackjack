from hand import Hand
from strategies.strategy import Strategy, Action


class DealersStrategy(Strategy):
    def __init__(self):
        super().__init__()

    def get_action(self, my_hand: Hand,
                   dealers_hand: Hand,
                   other_players_hands: list[Hand],
                   my_number_of_chips: int) -> Action:

        #todo there is an edge case with soft 17, look that up and implement it
        while True:
            sum, type = dealers_hand.get_sum()
            if sum >= 17:
                return Action.stand
            else:
                return Action.hit

