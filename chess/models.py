class Color(object):
    WHITE = 0
    BLACK = 1
    NONE = 2


class Nothing(object):
    color = Color.NONE

    def get_moves(self, board, x, y):
        raise Exception("Nothing has made a move!")

    def __str__(self):
        return "."


class ChessMan(object):
    IMG = None

    def __init__(self, color):
        self.color = color

    def __str__(self):
        # if self.color == Color.WHITE:
        #    return 0
        # else:
        #    return 1
        return self.IMG[0 if self.color == Color.WHITE else 1]


class Pawn(ChessMan):
    IMG = ("♙", "♟")

    def get_moves(self, board, x, y):
        moves = []
        if self.color == Color.BLACK and y < 7 and board.get_color(x, y) == Color.NONE:
            moves.append([x, y + 1])
        return moves


class King(ChessMan):
    IMG = ("♔", "♚")

    def get_moves(self, board, x, y):
        moves = []
        return moves


class Board(object):
    def __init__(self):
        self.board = [[Nothing()] * 8 for x in range(8)]

    def __str__(self):
        res = " "
        for x in range(8):
            res += " ".join(map(str, self.board[x])) + "\n"
        return res

    def get_color(self, x, y):
        return self.board[x][y].color

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def move(self, xy_from, xy_to):
        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Nothing()
