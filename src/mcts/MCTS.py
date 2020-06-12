import numpy as np

def traverse(root):
    moves = root.moves
    if root.isLeaf() and root.has_moves():
        pass
    children_q_scores = [child.q_ for child in root.children]

# move to own class later
def board_to_state(board):
    return

# move to own class later
def nn_output(state):
    return