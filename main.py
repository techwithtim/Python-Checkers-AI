# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from montecarlo.algorithm import montecarlots
import argparse

FPS = 60

RED = (255, 0, 0)
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def main():
    """
    One can run games of checkers between different types of bot
    and algorithms by giving as argument the variables above.
    """
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    parser = argparse.ArgumentParser(description="The Connect 4 game")
    parser.add_argument(
        "--player1",
        "--p1",
        "-1",
        type=str,
        help="Type of player for player 1",
        required=True,
        choices=("minimax", "mcts"),
        # choices=("minimax", "mcts", "random", "human"),
        default="minimax",
    )
    parser.add_argument(
        "--player2",
        "--p2",
        "-2",
        type=str,
        help="Type of player for player 2",
        required=True,
        choices=("minimax", "mcts"),
        # choices=("minimax", "mcts", "random"),
        default="mcts",
    )
    args = parser.parse_args()

    # p = [None, None]
    # if args.player1 == "minimax":
    #     p[0] = MINIMAX
    # else:
    # # elif args.player1 == "mcts":
    #     p[0] = MONTE_CARLO
    #
    # if args.player2 == "minimax":
    #     p[1] = MINIMAX
    # else:
    # # elif args.player2 == "mcts":
    #     p[1] = MONTE_CARLO

    p = [args.player1, args.player2]
    # p_str = [args.player1, args.player2]

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            print("Player 1 ({} AI) is thinking".format(p[0].upper()))
            if p[0] == "minimax":
                value, new_board = minimax(game.get_board(), 3, True, game)
                game.ai_move(new_board)
            elif p[0] == "mcts":
                new_board = montecarlots(game.get_board(), RED)
                if new_board is None:
                    run = False
                else:
                    game.ai_move(new_board)
            print("Player 1 ({} AI) has made its move".format(p[0].upper()))

        elif game.turn == RED:
            print("Player 2 ({} AI) is thinking".format(p[1].upper()))
            if p[1] == "minimax":
                value, new_board = minimax(game.get_board(), 3, True, game)
                game.ai_move(new_board)
            elif p[1] == "mcts":
                new_board = montecarlots(game.get_board(), RED)
                if new_board is None:
                    run = False
                else:
                    game.ai_move(new_board)
            print("Player 2 ({} AI) has made its move".format(p[1].upper()))

        if game.winner() is not None:
            run = False

        #        for event in pygame.event.get():
        #            if event.type == pygame.QUIT:
        #                run = False
        #
        #            if event.type == pygame.MOUSEBUTTONDOWN:
        #                move = montecarlots(game.get_board(), WHITE)
        #                pos = pygame.mouse.get_pos()
        #                row, col = get_row_col_from_mouse(pos)
        #                game.select(row, col)
        #                game.get_board().get_num()

        # pygame.time.delay(5000)
        game.update()
    print("And the winner is : ", game.winner())
    pygame.quit()


main()
