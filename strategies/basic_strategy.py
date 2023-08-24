from pathlib import Path

from hand import Hand, HandType
from strategies.strategy import Strategy, Action


class BasicStrategy(Strategy):
    def __init__(self, base_bet: int):
        super().__init__()

        folder = Path('strategies') / 'basic_strategy_tables'
        # enable this if you run unittests individually from the IDE
        # folder = Path.home() / 'Documents' / 'coding' / 'blackjack' / 'strategies' / 'basic_strategy_tables'
        self.hard_table_path = folder / 'hard.csv'
        self.soft_table_path = folder / 'soft.csv'
        self.pair_table_path = folder / 'pair.csv'

        self.base_bet = base_bet

        self.tables = {
            HandType.hard: self.read_table(self.hard_table_path),
            HandType.soft: self.read_table(self.soft_table_path),
            HandType.pair: self.read_table(self.pair_table_path),
        }

    def get_bet_amount(self, my_number_of_chips: int) -> int:
        return self.base_bet

    def get_action(self, my_hand: Hand, dealers_hand: Hand, other_players_hands: list[Hand],
                   my_number_of_chips: int) -> Action:

        my_sum, my_hand_type = my_hand.get_sum()
        dealers_sum, dealers_hand_type = dealers_hand.get_sum()
        return self.tables[my_hand_type][my_sum][dealers_sum]

    @staticmethod
    def read_table(path: Path):
        decision_map = {}
        char_to_action_map = {
            'h': Action.hit,
            's': Action.stand,
            'p': Action.split,
            'dh': Action.double_if_possible_otherwise_hit,
            'ds': Action.double_if_possible_otherwise_stand
        }

        with path.open('r') as f:
            lines = f.readlines()

        header = lines[0].strip().split(',')
        header = [int(c) for c in header[1:]]

        for line in lines[1:]:
            cells = line.strip().split(',')

            i = int(cells[0])
            decision_map[i] = {}
            for h, c in zip(header, cells[1:]):
                decision_map[i][h] = char_to_action_map[c]

        return decision_map
