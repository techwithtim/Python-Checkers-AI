# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame

from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from montecarlo.algorithm import montecarlots, MCNode
import random
import argparse

FPS = 60
random.seed(15)


def get_row_col_from_mouse(pos):
    """
    Returns the row and column numbers from mouse capture.
    """
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col


def mcts_ai_move(game, run, tree):
    """
    Executes a move on the board determined by the MCTS AI.
    """
    new_board, new_tree, best_move = montecarlots(game.board,game.turn, game, tree)
    if new_board is None or best_move is None:
        # print("end of game?")  # DEBUG
        run = False
    else:
        game.ai_move(new_board, best_move)
    return run, new_tree, best_move


def minimax_ai_move(game, tree):
    """
    Executes a move on the board determined by the Minimax AI.
    :param game: Game instance
    :param tree: MCTS tree
    """
    if game.get_board().winner() is not None:
        print("Error : Calling minimax_ai_move while there's already a winner ")
        exit()
    value, chosen_move = minimax(game.get_board(), 3, game)
    chosen_move.compute_final_state()
    new_board = chosen_move.final_state
    if tree:
        tree = tree.get_child(new_board)
    # If no moves left
    if new_board is None:
        # When no moves left, actually it is possible to loop, so we have to put a limit of turns or decide that the game is over
        # print("Player {} had no moves left".format(game.turn))  # DEBUG
        new_board = game.board
    game.ai_move(new_board, chosen_move)
    return tree


def human_move(game):
    """
    Executes a move on the board determined by the player.
    """
    value, chosen_move = minimax(game.get_board(), 3, game) # TODO pourquoi c'est un minimax ?
    chosen_move.compute_final_state()

    game.ai_move(chosen_move.final_state)
    # FIXME: implement the correct function, currently is a copy of minimax_ai_move


def make_move(game, p, n, run, tree):
    """
    Executes a move on the board determined by the arguments chosen at game launch.
    """
    if p[n] == "human":
        human_move(game)
    else:
        run, tree = make_ai_move(game, n, p, run, tree)
    return run, tree


def make_ai_move(game, n, p, run, tree):
    # print("Player {} ({} AI) is thinking".format(n + 1, p[n].upper()))
    if p[n] == "minimax":
        tree = minimax_ai_move(game, tree)
    elif p[n] == "mcts":
        run, tree, best_move = mcts_ai_move(game, run, tree)
    # print("Player {} ({} AI) has made its move".format(n + 1, p[n].upper()))
    return run, tree


def main():
    """
    One can run games of checkers between different types of bot
    and algorithms by giving as argument the variables above.
    """
    WIN = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Checkers')

    clock = pygame.time.Clock()
    game = Game(WIN)

    parser = argparse.ArgumentParser(description="Checkers game")
    parser.add_argument(
        "--player1",
        "--p1",
        "-1",
        type=str,
        help="Type of player for player 1",
        required=True,
        choices=("minimax", "mcts", "human"),
        default="minimax",
    )
    parser.add_argument(
        "--player2",
        "--p2",
        "-2",
        type=str,
        help="Type of player for player 2",
        required=True,
        choices=("minimax", "mcts", "human"),
        default="mcts",
    )
    args = parser.parse_args()

    p = [args.player1, args.player2]
    most_recent_tree = None

    winner = ''
    run = True
    while run:
        clock.tick(FPS)

        if game.turn == WHITE:
            run, most_recent_tree = make_move(game, p, 0, run, most_recent_tree)
            if not run:
                winner = "RED"
        elif game.turn == RED:
            run, most_recent_tree = make_move(game, p, 1, run, most_recent_tree)
            if not run:
                winner = "WHITE"

        if game.winner() is not None:
            run = False
            winner = game.winner()
        game.update()
        # input("[next move]")
        pygame.time.wait(500)
    print("And the winner is : ", winner)
    pygame.quit()


if __name__ == '__main__':
    main()
