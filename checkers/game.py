import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS
from checkers.board import Board
from .move import Move


class Game:
    def __init__(self, win=None):
        self._init(display=win is not None)
        self.win = win
        self.king_moved = 0

    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self, display: bool):
        self.selected = None
        self.board = Board(display=False)
        self.turn = WHITE
        self.valid_moves = {}

    def winner(self):
        if self.king_moved >= 20:
            return "BOTH"
        return self.board.winner()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected:
            # il faut que ça soit selected pour pouvoir faire move
            result = self._move(row, col)
            # il faut que le move soit accepté pour qu'il se passe quelque chose, sinon on annule le move et on recommence
            if not result:
                self.selected = None
                self.select(row, col)

        piece = self.board.get_piece(row, col)
        # Piece vaut 0 si la case n'est pas occupée, (255,0,0) si c'est rouge, et (255,255,255) si c'est blanc

        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True

        return False

    def _move(self, row, col):
        piece = self.board.get_piece(row, col)  # La place à occuper ensuite.
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row,
                            col)  # A ce moment là, on bouge une pièce, il faut regarder si c'est un king ou pas.
            if self.selected.king:
                # Il faut compter chaque fois qu'une dame bouge.
                # print("Une dame a été jouée")
                self.king_moved += 1
            else:
                # print("Ce n'est pas une dame qui a joué")
                self.king_moved = 0
            skipped = self.valid_moves[(row, col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
        else:
            return False

        return True

    def draw_valid_moves(self, moves):
        for move in moves:
            row, col = move
            pygame.draw.circle(self.win, BLUE,
                               (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self) -> Board:
        return self.board

    def ai_move(self, board, parent_action: Move):
        # Change here the counting of king_moved
        self.analyze_move(parent_action)
        self.board = board
        self.change_turn()

    def analyze_move(self, move: Move):
        # Need to check if this was a king move and if there was a capture.
        piece_moved = move.get_piece()
        if piece_moved.is_king():
            # print("Dame jouée")  # DEBUG
            self.king_moved += 1
            # If no capture, we do nothing. If capture, count is back to zero.
            if move.get_skip() is not None and len(move.get_skip()) != 0:
                # print("Capture!")  # DEBUG
                self.king_moved = 0
        else:
            # print("Pion joué")  # DEBUG
            self.king_moved = 0
