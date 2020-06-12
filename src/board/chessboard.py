import chess
import enum
import numpy as np

# pieces as per FEN standard, ordered decreasing by value
pieces = "KQRBNPkqrbnp"
piece_indices = {x: i for i, x in enumerate(pieces)}
castle_rights = "KQkq"
castle_indices = {x: i for i, x in enumerate(castle_rights)}
files = "abcdefgh"
file_indices = {x: i for i, x in enumerate(files)}


class Chessboard:
    """
    Initialises the Chessboard environment with board-related attributes.

    Attributes:
    board -- (chess.Board) stores board state, python-chess object
    num_half_moves -- (int) counts number of half-moves for move threshold
    winner -- (str) winner of game, uses enum object
    resigned -- (boolean) whether loser resigned
    result -- (str) string encoding of result, ("1-0", "0-1", "1/2-1/2")
    """

    def __init__(self):
        self.board = None
        self.num_half_moves = 0
        self.winner = None
        self.resigned = False
        self.result = None

    def reset(self):
        self.board = chess.Board()
        self.num_half_moves = 0
        self.winner = None
        self.resigned = False
        self.result = None


def board_to_planes(board):
    """
    Returns stacked plane representation of piece locations

    Represents the positions of pieces (2x6) for both players. Outputs as numpy array with shape (12,8,8)

    Keyword arguments:
    board -- stores chess.Board object with current board state
    """

    # board prints conveniently as a string, so __str__ is called and saved. Could be done with FEN too
    board_str = board.__str__()
    board_arr = np.asarray([line.split(" ") for line in board_str.split("\n")])
    plane_repr = np.full((12, 8, 8,), 0)
    for i, piece in enumerate(pieces):
        plane_repr[i][board_arr == piece] = 1
    return plane_repr


def board_to_aux_planes(board):
    """
    Returns auxiliary planes with half-move no progress count, castling rights

    Planes filled with details of castling availability:
    - 1 for no-progress half-moves (max 100)
    - 4 for castling rights (KQkq)
    - 1 for whose move it is (0 for white 1 for black, also indicates if board will be flipped)
    No plane(s) track repetition count. This is hard to track effectively with MCTS. May be partially reflected in tree
    traversal by still causing terminal draw positions. May add plane for total moves to discourage very long games,
    but this is difficult because do not want to "reward" a losing player for stalling for a draw
    May not realistically need no-progress moves in policy/value evaluation, but the information is easily accessible

    Keyword arguments:
    board -- stores chess.Board object with current board state
    """
    # split at end for interpretability
    # example fen: 'rnbqkb1r/pppppppp/5n2/8/8/2N2N2/PPPPPPPP/R1BQKB1R b KQkq - 3 2'
    # split by space: piece positions, turn, castling rights, en passant position, no-progress half moves, full moves
    wb, castling, enpassant, halfmoves, fullmoves = board.fen().split(" ")[1:]
    plane_count = 0
    aux_planes = np.full((7, 8, 8), 0)

    if wb == "b":
        aux_planes[plane_count] = 1
    plane_count += 1

    for x in castle_rights:
        if x in castling:
            aux_planes[plane_count] = 1
        plane_count += 1

    if enpassant != "-":
        loc = pos_to_idx(enpassant)
        aux_planes[plane_count, loc[0], loc[1]] = 1
    plane_count += 1

    aux_planes[plane_count] = int(halfmoves)


def pos_to_idx(pos):
    """
    Turns position string in uci format into index aligning to 8x8 planes

    Turns position string in uci format into index aligning to 8x8 planes. e.g. b7 = (1, 6)

    Keyword arguments:
    pos -- 'str' in uci format
    """
    # recall that the 8x8 planes above have have 8th rank at index 0
    # idx is of the form row, col (pos is col, row)
    return 8 - int(pos[1]), file_indices[pos[0]]
