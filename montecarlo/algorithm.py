from copy import deepcopy

def montecarlots(board, player) :
    moves = get_all_moves(board, player)
    if len(moves) != 0 :
        return moves[0]

    return None


def get_all_moves(board, color):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        if len(valid_moves) !=0 :
            #print("Piece ", piece, " of player ", color, " can do the following moves ")
            #print("\tIn short : ")
            for move, skip in valid_moves.items():
                #print("\t", move, ", resulting in ", len(skip), " pieces of the other color captured")
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_board = simulate_move(temp_piece, move, temp_board, skip)
                moves.append(new_board)

    return moves


def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

