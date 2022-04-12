import pygame
from .constants import RED, WHITE, BLUE, SQUARE_SIZE, ROWS, COLS
from checkers.board import Board

class Game:
    def __init__(self, win):
        self._init()
        self.win = win
        self.king_moved = 0
    
    def update(self):
        self.board.draw(self.win)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()

    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = WHITE
        self.valid_moves = {}

    def winner(self):
        if self.king_moved >= 26:
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
        piece = self.board.get_piece(row, col) # La place à occuper ensuite.
        if self.selected and piece == 0 and (row, col) in self.valid_moves:
            self.board.move(self.selected, row, col) # A ce moment là, on bouge une pièce, il faut regarder si c'est un king ou pas.
            if self.selected.king:
                # Il faut compter chaque fois qu'une dame bouge.
                print("Une dame a été jouée")
                self.king_moved += 1
            else:
                print("Ce n'est pas une dame qui a joué")
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
            pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), 15)

    def change_turn(self):
        self.valid_moves = {}
        if self.turn == RED:
            self.turn = WHITE
        else:
            self.turn = RED

    def get_board(self) -> Board:
        return self.board

    def ai_move(self, board):
        # Change here the counting of king_moved
        self.compare_boards(board)
        self.board = board
        self.change_turn()

    def compare_boards(self, new_board):
        # On doit comparer les deux pour savoir quelle pièce a été jouée
        print("Yo")
        for i in range(ROWS):
            for j in range(COLS):
                if self.board.get_piece(i, j) == 0 and new_board.get_piece(i, j) != 0:
                    if new_board.get_piece(i,j).king:
                        print("Une dame a bougé")
                        self.king_moved += 1
                    else:
                        print("La dame n'a pas bougé")
                        self.king_moved = 0
                    return
