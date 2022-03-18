from collections import defaultdict
from copy import deepcopy


RED = (255,0,0)
WHITE = (255, 255, 255)


def montecarlots(board, player):
    tree = MonteCarloTreeSearchNode(board, player)
    moves = tree._untried_actions

    return moves[0]




class MonteCarloTreeSearchNode():
    def __init__(self, state, color, parent=None, parent_action=None):
        """
        Class that modelizes a node as manipulated in a MCTS
        :param game:    Current game
        :param state:   Current board
        :param color:   Current player color
        :param parent:  Parent node, if any (none by default, for root)
        :param parent_action:   pas encore compris ce paramètre
        """
        self.state = state
        self.color = color
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._results[1] = 0
        self._results[-1] = 0
        self._untried_actions = None
        self._untried_actions = self.untried_actions()
        return

    def get_all_moves(self):
        """
            Function that returns all the possible outcoming boards from the current position when it is the turn of player "color"
            :param board: Current board
            :param color: Current player
            :return: List of boards corresponding to possible outcomes
        """
        moves = []
        for piece in self.state.get_all_pieces(self.color):
            valid_moves = self.state.get_valid_moves(piece)
            if len(valid_moves) != 0:
                for move, skip in valid_moves.items():
                    print(move)
                    temp_board = deepcopy(self.state)
                    temp_piece = temp_board.get_piece(piece.row, piece.col)
                    new_board = simulate_move(temp_piece, move, temp_board, skip)
                    moves.append(new_board)
        return moves


    def untried_actions(self):
        self._untried_actions = self.get_all_moves()
        return self._untried_actions

    def expand(self):
        next_state = self._untried_actions.pop()
        next_color = RED if self.color == WHITE else WHITE
        # TODO : faire en sorte que les actions soient différents des états.
        #   Action = mouvement de la piece (x1, y1) à la case (x2, y2).
        #   Etat : plateau après le mouvement
        child_node = MonteCarloTreeSearchNode(next_state, color=next_color, parent_action=next_state)
        self.children.append(child_node)
        return child_node

def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

