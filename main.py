from game import Game
from strategies.basic_strategy import BasicStrategy


if __name__ == '__main__':
    game = Game(number_of_decks=6,
                number_of_players=4,
                my_total_number_of_chips=10000,
                number_of_rounds=10000,
                strategy=BasicStrategy(base_bet=2))

    result = game.simulate()

    print(f'Started with: {result[0].total_number_of_chips} chips')
    print(f'Remaining: {result[-1].total_number_of_chips} chips')

    # todo how is this defined?
    total_number_of_rounds = (result[-1].round - result[0].round)  # because it can end early
    number_of_chips_gained = (result[-1].total_number_of_chips - result[0].total_number_of_chips)
    gain_per_round = number_of_chips_gained / total_number_of_rounds
    print(f'rounds: {total_number_of_rounds}')
    print(f'gain: {number_of_chips_gained} chips')
    print(f'gain/round: {gain_per_round:.5f} chips/round')
    print(f'base bet: {game.myself.strategy.base_bet} chips')

    # todo: I suspect that the basic strategy (or something else) is not implemented correctly, because based on the
    #  simulation we're losing 0.49 chips/round when we have 2 chips as a bet per round

    # fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    # ax.plot([l.round for l in result], [l.total_number_of_chips for l in result])
    # ax.plot([result[0].round, result[-1].round], [result[0].total_number_of_chips, result[-1].total_number_of_chips])
    # plt.show()
