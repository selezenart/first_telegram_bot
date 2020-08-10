from enum import Enum
import numpy


class Color(Enum):
    WHITE = 0
    BLACK = 1
    NONE = 2


class Chessman(object):
    IMG = None
    color: Color
    X: int
    Y: int
    CALLBACK = None

    def __init__(self, color, x, y, number):
        self.color = color
        self.X = x
        self.Y = y
        self.CALLBACK += str(number)

    def __str__(self):
        # if self.color == Color.WHITE:
        #    return 0
        # else:
        #    return 1
        return self.IMG[0 if self.color == Color.WHITE else 1]


class Nothing(object):
    CALLBACK = "empty"
    Color = Color.NONE
    X: int
    Y: int

    def __init__(self, x, y):
        self.X = x
        self.Y = y
        self.CALLBACK += " " + str(x) + " " + str(y)

    def get_moves(self, board, x, y):
        raise Exception("Nothing has made a move!")

    def get_attacks(self, board, x, y):
        raise Exception("Nothing has attacked!")

    def __str__(self):
        return " "


class Pawn(Chessman):
    IMG = ("♙", "♟")
    CALLBACK = "pawn"

    def get_attacks(self):
        moves=[]
        if self.Y<7:
            if self.X==0:
                moves.append([self.X+1,self.Y+1])
            elif self.X==7:
                moves.append(([self.X-1,self.Y+1]))
            else:
                moves.append([self.X-1,self.Y+1])
                moves.append([self.X + 1, self.Y + 1])
        return moves


    def get_moves(self):
        moves = []
        if self.Y<7:
            moves.append([self.X, self.Y + 1])
        return moves



class King(Chessman):
    IMG = ("♔", "♚")
    CALLBACK = "king"


class Board(object):

    def __init__(self):
        # self.board = [[Nothing(x, y, Color.NONE) for x in range(8)] for y in range(8)]
        self.chessmen_list = []
        self.in_game_chessmen_list=[]
        self.board = numpy.empty(shape=(8, 8), dtype='object')
        for y in range(8):
            for x in range(8):
                self.board[y][x] = Nothing(y, x)

        pawn1 = Pawn(Color.WHITE, 0, 1, 1)
        pawn2 = Pawn(Color.WHITE, 1, 1, 2)
        pawn3 = Pawn(Color.WHITE, 2, 1, 3)
        pawn4 = Pawn(Color.WHITE, 3, 1, 4)
        pawn5 = Pawn(Color.WHITE, 4, 1, 5)
        pawn6 = Pawn(Color.WHITE, 5, 1, 6)
        pawn7 = Pawn(Color.WHITE, 6, 1, 7)
        pawn8 = Pawn(Color.WHITE, 7, 1, 8)
        king2 = King(Color.BLACK, 4, 6, 2)
        self.chessmen_list.append(king2)
        pawns = [pawn1, pawn2, pawn3, pawn4, pawn5, pawn6, pawn7, pawn8]
        for pawn in pawns:
            self.chessmen_list.append(pawn)
        for chess in self.chessmen_list:
            self.put_chessman(chess)
            self.in_game_chessmen_list.append(chess)


    def __str__(self):
        cells = [43, 45]
        res = ""
        i = 0
        for y in range(8):
            for x in range(8):
                res += self.set_color(cells[i]) + str(self.board[x][y]) + ' '
                i = 1 - i
            i = 1 - i
            res += self.set_color(0) + '\n'
        return res

    def redraw(self):
        for x in range(8):
            for y in range(8):
                self.board[x][y] = Nothing(x, y)
        for ch in self.in_game_chessmen_list:
            self.board[ch.X][ch.Y] = ch

    def put_chessman(self, chessman):
        for x in range(8):
            if x == chessman.Y:
                for y in range(8):
                    if y == chessman.X:
                        self.board[chessman.X][chessman.Y] = chessman

    def get_chessman(self, x, y):
        return self.board[x][y]

    def get_chessman_call(self, callback):
        for ch in self.chessmen_list:
            if callback.data == ch.CALLBACK:
                return ch
        #return Nothing(callback.data.split(' ')[1], callback.data.split(' ')[2])

    def move(self, chessman, new_x, new_y):
        new_x = int(new_x)
        new_y = int(new_y)
        print(self.board[new_x][new_y].CALLBACK)
        if not isinstance(self.board[new_x][new_y], Nothing):
            beaten_chessman = self.board[new_x][new_y]
            self.in_game_chessmen_list.remove(beaten_chessman)
        self.board[new_x][new_y] = chessman
        empty_cell = Nothing(chessman.X, chessman.Y)
        self.board[chessman.X][chessman.Y] = empty_cell
        chessman.X = new_x
        chessman.Y = new_y


    def get_color(self, x, y):
        return self.board[x][y].color

    def get_moves(self, x, y):
        return self.board[y][x].get_moves(self, x, y)

    def set_color(self, color):
        return "\033[%sm" % color
