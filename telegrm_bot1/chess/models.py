class Color(object):
    WHITE = 0
    BLACK = 1
    NONE = 2


class Nothing(object):
    color = Color.NONE
    CALLBACK = "empty"

    def get_moves(self, board, x, y):
        raise Exception("Nothing has made a move!")

    def __str__(self):
        return " "


class ChessMan(object):
    IMG = None
    X = 0
    Y = 0
    CALLBACK = None

    def __init__(self, color,x,y):
        self.color = color
        self.X = x
        self.Y = y

    def __str__(self):
        # if self.color == Color.WHITE:
        #    return 0
        # else:
        #    return 1
        return self.IMG[0 if self.color == Color.WHITE else 1]


class Pawn(ChessMan):
    IMG = ("♙", "♟")
    CALLBACK = "pawn"

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
        pawn1 = Pawn(Color.WHITE, 0, 1)
        pawn2 = Pawn(Color.WHITE, 1, 1)
        pawn3 = Pawn(Color.WHITE, 2, 1)
        pawn4 = Pawn(Color.WHITE, 3, 1)
        pawn5 = Pawn(Color.WHITE, 4, 1)
        pawn6 = Pawn(Color.WHITE, 5, 1)
        pawn7 = Pawn(Color.WHITE, 6, 1)
        pawn8 = Pawn(Color.WHITE, 7, 1)
        pawns = [pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8]
        for pawn in pawns:
                    self.put_chessman(pawn)

    def __str__(self):
        cells = [43, 45]
        res = ""
        i = 0
        for x in range(8):
            for y in range(8):
                res += self.set_color(cells[i]) + str(self.board[x][y]) + ' '
                i = 1 - i
            i = 1 - i
            res += self.set_color(0) + '\n'
        return res

    def put_chessman(self,chessman):
        for i in range(8):
            if i == chessman.X:
                for j in range(8):
                    if j == chessman.Y:
                        self.board[chessman.Y][chessman.X] = chessman




    def get_color(self, x, y):
        return self.board[x][y].color

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def move(self, xy_from, xy_to):
        self.board[xy_to[1]][xy_to[0]] = self.board[xy_from[1]][xy_from[0]]
        self.board[xy_from[1]][xy_from[0]] = Nothing()

    def set_color(self,color):
        return "\033[%sm" % color

