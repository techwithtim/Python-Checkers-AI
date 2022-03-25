# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from montecarlo.algorithm import montecarlots
import argparse

FPS = 60

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')


def get_row_col_from_mouse(pos):
    """
    Returns the row and column numbers from mouse capture.
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def mcts_ai_move(game, run):
    """
    Executes a move on the board determined by the MCTS AI.
    """
    new_board = montecarlots(game.get_board(), RED)
    if new_board is None:
        run = False
    else:
        game.ai_move(new_board)
    return run


def minimax_ai_move(game):
    """
    Executes a move on the board determined by the Minimax AI.
    """
    value, new_board = minimax(game.get_board(), 3, True, game)
    game.ai_move(new_board)


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
        default="mcts",
    )
    args = parser.parse_args()

    p = [args.player1, args.player2]

    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            print("Player 1 ({} AI) is thinking".format(p[0].upper()))
            if p[0] == "minimax":
                minimax_ai_move(game)
            elif p[0] == "mcts":
                run = mcts_ai_move(game, run)
            print("Player 1 ({} AI) has made its move".format(p[0].upper()))

        elif game.turn == RED:
            print("Player 2 ({} AI) is thinking".format(p[1].upper()))
            if p[1] == "minimax":
                minimax_ai_move(game)
            elif p[1] == "mcts":
                run = mcts_ai_move(game, run)
            print("Player 2 ({} AI) has made its move".format(p[1].upper()))

        if game.winner() is not None:
            run = False
        game.update()
    print("And the winner is : ", game.winner())
    pygame.quit()


main()
