from copy import deepcopy

from checkers.piece import Piece


class Move:
    def __init__(self, origin_state, color, origin_piece, destination_loc, skip):
        self.origin_state = origin_state
        self.color = color
        self.piece = origin_piece
        self.loc = destination_loc
        self.skip = skip
        self.value = "Not yet computed"
        self.final_state = self.origin_state

        # We do not assign a value to the move yet, we will do it only when necessary
        # self.value = self.eval_move()

    def get_piece(self):
        return self.piece

    def get_loc(self):
        return self.loc[0], self.loc[1]

    def get_skip(self):
        return self.skip

    def compute_value(self):
        self.value = self.eval_move()
        return

    def eval_move(self):
        # TODO : improve with heuristic taking into account the movement (taking a piece, reaching the other side)
        #  Currently : does a comparison after-before. So it's a "+1" if normal move, "+2" if takes a piece
        origin_eval = self.origin_state.eval(self.color)
        self.compute_final_state()
        final_eval = self.final_state.eval(self.color)
        return final_eval - origin_eval + len(self.skip)

    def compute_final_state(self):
        col, row = self.get_loc()
        skip = self.skip
        temp_board = deepcopy(self.origin_state)
        temp_piece = temp_board.get_piece(self.piece.row, self.piece.col)
        self.final_state = temp_board.simulate_move(temp_piece, (col, row), skip)
        return

    def __repr__(self):
        return("From board {} move piece {} to {} ({} piece taken). Value = {}".format(self.origin_state, self.piece, self.loc, len(self.skip), self.value ))

    def is_equivalent_to(self, other_move):
        # TODO ajouter comparaison entre les states (les board)
        piece_test = self.piece.color == other_move.piece.color
        piece_test *= self.piece.row == other_move.piece.row
        piece_test *= self.piece.col == other_move.piece.col

        dest_test = self.loc == other_move.loc

        return piece_test*dest_test
