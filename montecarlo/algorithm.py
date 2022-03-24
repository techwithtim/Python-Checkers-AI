import copy
import random
from collections import defaultdict
from copy import deepcopy
from checkers.move import Move

RED = (255, 0, 0)
WHITE = (255, 255, 255)


def montecarlots(board, player):
    tree = MCNode(board, player)
    chosen_node = tree.monte_carlo_tree_search()
    chosen_node_board = chosen_node.state
    return chosen_node_board


class MonteCarloTreeSearchNode():
    def __init__(self, state, color, parent=None, max_it=10):
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
        self.adv_color
        self.reward = 0.0
        self.visits = 1  # On passera toujours par le node qu'on vient de créer
        self.parent = parent
        self.children = []
        self.children_moves = []
        self.max_it = max_it
        return

    def monte_carlo_tree_search(self):
        for i in range(self.max_it):
            # TODO
            self.select()

        return self.best_child()

    def select(self):
        """
        This function defines the selection policy. If the current node is still not fully explored,
        it expands the node and selects the newly created child. If the node is fully explored, we
        move down in the tree, selecting the best child until the node is terminal or not fully explored

        :return: The selected node according to the policy.
        """
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.fully_explored():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node

    def expand(self):
        """
        Expansion of the current node. We try to create a child node by chosing a move that has not been chosen before
        for this node.
        :return: The newly created node
        """
        # the function returns a list of possible moves (objects of the class Move)
        possible_moves = self.get_all_moves()

        # Loop variables (to avoid the use of "break")
        res = True
        i = 0
        while res and i < len(possible_moves):
            move = possible_moves[i]
            if self.not_in_children_moves(move):
                # print("Node expanded with move ", move)

                # When we found a movement that was not tried before, we capture the information to simulate it
                # (origin piece, final destination, and if a piece was captured)
                piece = move.get_piece()
                final_loc = move.get_loc()
                skip = move.get_skip()

                # Copy of the board, to avoid simulation from influencing the board
                new_board = deepcopy(self.state)

                # Need to make a deep copy of piece to avoid simulation from influencing the board
                temp_piece = new_board.get_piece(piece.row, piece.col)

                new_state = simulate_move(temp_piece, final_loc, new_board, skip)

                # See definition of the function.
                self.add_child(new_state, move)
                res = False
            i += 1
        # Returns the newly created child (node)
        return self.children[-1]

    def best_child(self):
        # TODO : implement selection of the best node, and handle case where no possible moves
        #  Currently :
        if len(self.children) == 0 :
            return None
        return self.children[random.randint(0,len(self.children)-1)]

    def is_terminal_node(self):
        """
        Function that tests if a node is terminal. By definition, a node is terminal when there are no possible moves.
        :return: Boolean
        """
        return len(self.get_all_moves()) == 0

    def fully_explored(self):
        """
        Returns a boolean value telling wether the node has been fully explored or not. A node is fully explored when
        all his possible moves are in his children
        :return: Boolean
        """
        possible_moves = self.get_all_moves()
        return len(possible_moves) == len(self.children)

    def get_all_moves(self):
        """
            Function that returns all the possible outcoming boards from the current position when it is the turn of player "color"
            :param board: Current board
            :param color: Current player
            :return: List of Moves corresponding to possible outcomes
        """
        moves = []
        for piece in self.state.get_all_pieces(self.color):
            valid_moves = self.state.get_valid_moves(piece)[1] # index 0 is the piece itself
            if len(valid_moves) != 0:
                for final_dest, skip in valid_moves.items():
                    move = Move(piece, final_dest, skip)
                    # print(move)
                    moves.append(move)
        return moves


    def add_child(self, state, move):
        """
        Function that modifies the current node by adding a new child node, and adding a move to his list of moves.
        :param state:   Current board
        :param move:    move to add
        :return:        None
        """
        child_node = MCNode(state, parent=self, color=self.adv_color)
        self.children.append(child_node)
        self.children_moves.append(move)

    def not_in_children_moves(self, move):
        for child_move in self.children_moves :
            if child_move.is_equivalent_to(move) :
                return False
        return True

    def simulate(self, last_node):
        """

        :param last_node: Initial MCNode for the simulation.
        :return: Reward value (0 or 1)
        """

        new_state = deepcopy(last_node.state) # To avoid working on existing new_state

        possible_moves = last_node.get_all_moves()

        new_child = last_node

        while not len(possible_moves) == 0:
            rand_move = possible_moves[random.randint(0, len(self.children) - 1)]
            row, col = rand_move.get_loc()
            new_state.move(rand_move.piece, row, col)

            new_color = RED if last_node.color == WHITE else WHITE
            new_child = MCNode(new_state, new_color)
            possible_moves = new_child.get_all_moves()

        winner_color = new_child.state.winner()
        return 1 if winner_color == last_node.color else 0

    def backpropagate(self, reward, node):
        # +=1 visits pour tout et +reward aux nodes avec la couleur du node de départ, +reward%2 aux autres.
        if node.parent == None:
            #We got to the root.
            return

        node.visits += 1 # Same for every node we visited

        if node.color == self.color:
            node.reward += reward
        else:
            node.reward += (reward+1)%2 # The reward is adapted according to the color of the node.

        self.backpropagate(reward, node.parent)




def simulate_move(piece, move, board, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board
