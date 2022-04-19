# Let's gooooo
from checkers.board import Board
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
import random
import pygame

from checkers.game import Game
from main import make_move
from montecarlo.algorithm import MCNode

FPS = 60
random.seed(15)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')
POP_SIZE = 3

def init_population():
    population = []
    for i in range(POP_SIZE):
        it = random.randint(5, 40)
        safe_heuri = random.uniform(0, 1)
        exploit = random.uniform(0, 1)
        population.append((it, safe_heuri, exploit))
    return population


def main():
    clock = pygame.time.Clock()



    p = ["minimax", "mcts"]

    optimal = False
    population = init_population()
    while not optimal:
        for villager in population:
            set_parameters(villager[0], villager[1], villager[2])
            reward = 0
            for i in range(3):
                reward += play_game(clock, p)
            print(reward)
    pygame.quit()


def play_game(clock, p):
    game = Game(WIN)
    winner = 0
    most_recent_tree = None
    running = True

    while running:
        clock.tick(FPS)

        if game.turn == WHITE:
            running, most_recent_tree = make_move(game, p, 0, running, most_recent_tree)
            if not running:
                print("Blanc a gagné")
                winner = "RED"
        elif game.turn == RED:
            running, most_recent_tree = make_move(game, p, 1, running, most_recent_tree)
            if not running:
                print("Rouge a gagné")
                print(running)
                winner = "WHITE"

        if game.winner() is not None:
            running = False
            winner = game.winner()
        game.update()
        # pygame.time.wait(100)
        print(running)

    if winner == "RED":
        return 1
    elif winner == "WHITE":
        return 0
    else:
        return 0.5


def set_parameters(iterations, safe_heuristic, exploitation):
    Board.set_safe_heuri_param(safe_heuristic)
    MCNode.set_exploit(exploitation)
    MCNode.set_max_it(iterations)


if __name__ == '__main__':
    main()
