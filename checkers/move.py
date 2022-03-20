class Move:
    def __init__(self, origin_piece, destination_loc, skip):
        self.piece = origin_piece
        self.loc = destination_loc
        self.skip = skip

    def get_piece(self):
        return self.piece

    def get_loc(self):
        return self.loc

    def get_skip(self):
        return self.skip

    def __repr__(self):
        return("Move piece {} to {} ({} piece taken)".format(self.piece, self.loc, len(self.skip) ))

    def is_equivalent_to(self, other_move):
        piece_test = self.piece.color == other_move.piece.color
        piece_test *= self.piece.row == other_move.piece.row
        piece_test *= self.piece.col == other_move.piece.col

        dest_test = self.loc == other_move.loc

        return piece_test*dest_test