from copy import deepcopy
from typing import List

import pygame

from checkers.board import Board
from checkers.move import Move

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def minimax(position: Board, depth, game) -> (float, Move):
    """
    Computes the best move on a given position using a minimax algorithm up to given depth
    :param position:
    :param depth:
    :param game:
    :return: evaluation and best move
    """
    # Need to know if the current player is player MAX or player MIN
    max_player = game.turn == WHITE

    if depth == 0 or position.winner() is not None:
        return position.evaluate(), position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE, game):
            move.compute_final_state()
            evaluation = minimax(move.final_state, depth-1, game)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move

        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED, game):
            move.compute_final_state()
            evaluation = minimax(move.final_state, depth-1, game)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move

        return minEval, best_move


def get_all_moves(board, color, game) -> List[Move]:
    """
    Get every move from a given board and a given player
    :param board:
    :param color:
    :param game:
    :return:
    """
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)[1]
        for destination, skip in valid_moves.items():
            #draw_moves(game, board, piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_move = Move(temp_board, color, temp_piece, destination, skip)
            moves.append(new_move)
    return moves
# test
def draw_moves(game, board, piece):
    valid_moves = board.get_valid_moves(piece)[1]
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    #pygame.time.delay(100)

