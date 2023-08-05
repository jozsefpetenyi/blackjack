import matplotlib.pyplot as plt

from game import Game

if __name__ == '__main__':
    game = Game(number_of_decks=6,
                number_of_players=4,
                my_total_number_of_chips=10000,
                number_of_rounds=10000)

    result = game.simulate()

    print(f'Started with: {result[0].total_number_of_chips} chips')
    print(f'Remaining: {result[-1].total_number_of_chips} chips')

    # todo how is this defined?
    edge = (result[-1].total_number_of_chips - result[0].total_number_of_chips) / result[-1].round
    print(f'Edge: {edge * 100:.3f} %')

    # fig, ax = plt.subplots(1, 1, figsize=(8, 5))
    # ax.plot([l.round for l in result], [l.total_number_of_chips for l in result])
    # ax.plot([result[0].round, result[-1].round], [result[0].total_number_of_chips, result[-1].total_number_of_chips])
    # plt.show()
