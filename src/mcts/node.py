class Node:
    def __init__(self):
        self.parent = None
        self.children = None

    def is_leaf(self):
        return len(self.children) == 0

class ChessNode(Node):
    def __init__(self):
        Node.__init__(self)
        self.board = None
        self.moves = None
        self.is_terminal = False

        # state value from neural network value head
        self.q_ = 0
        # number of times state has been reached from root
        self.N_ = 0
        # prior probability of making move to reach this state (note we are not tracking edges explicitly)
        self.p_ = 0
        # total value of child states
        self.w_ = 0

    def has_moves(self):
        return self.board.legal_moves.count > 0


class Tree:
    def __init__(self):
        self.root = None