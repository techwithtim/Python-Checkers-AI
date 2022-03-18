# Assets: https://techwithtim.net/wp-content/uploads/2020/09/assets.zip
import pygame
from checkers.constants import WIDTH, HEIGHT, SQUARE_SIZE, RED, WHITE
from checkers.game import Game
from minimax.algorithm import minimax
from montecarlo.algorithm import montecarlots

FPS = 60

RED = (255,0,0)
WHITE = (255, 255, 255)
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Checkers')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)

    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE :
            #print("White turn. Board is ", game.get_board())
            new_board = montecarlots(game.get_board(), WHITE)
            #value, new_board = minimax(game.get_board(), 2, WHITE, game)
            #print(value)
            game.ai_move(new_board)
            #print("White has made a move!\nNew board is now ", game.get_board())
            #pygame.time.delay(100)


        elif game.turn == RED:
            #print("Red turn. Board is ", game.get_board())
            new_board = montecarlots(game.get_board(), RED)
            #value, new_board = minimax(game.get_board(), 1, RED, game)
            if new_board == None :
                # Minimax return is none if there are no possible moves
                run = False

            else :
                game.ai_move(new_board)
                #print("Red has made a move!\nNew board is now ", game.get_board())
                #pygame.time.delay(100)

        if game.winner() != None:
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

        pygame.time.delay(1000)
        game.update()
    print("And the winner is : ", game.winner())
    #pygame.quit()

main()