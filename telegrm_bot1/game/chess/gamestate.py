from dataclasses import dataclass
from enum import Enum

from game.chess.models import Color, Board


@dataclass
class GameState:
    chat_id: int
    turn: Color
    holding_chessman = None
    board: Board

    def __init__(self, message, some_board):
        self.chat_id = message.chat.id
        self.turn = Color.WHITE
        self.board = some_board

    def change_turn(self):
        self.holding_chessman = None
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        elif self.turn == Color.BLACK:
            self.turn = Color.WHITE
        else:
            raise Exception("Color Error")

    def capture_chessman(self, chessman):
        self.holding_chessman = chessman

    def is_holding(self, chessman):
        for ch in self.board.chessmen_list:
            if ch.CALLBACK == chessman.CALLBACK:
                return True
        return False

    def leave_chessman(self):
        if self.holding_chessman is not None:
            self.holding_chessman = None

    def allow_turn(self, chessman_call):#allows to take a turn
        if self.board.get_chessman_call(chessman_call).color == self.turn:
            return True
        else:
            return False

    def allow_attack(self, chessman_call, x, y):#allows to make an attack on x,y cell
        chessman = self.board.get_chessman_call(chessman_call)
        if self.check_attack(int(x), int(y), chessman) and self.check_move_color(chessman, int(x), int(y)):
            return True
        else:
            return False

    def allow_move(self, x, y, chessman_call):#allow to make a move on x,y cell, without eating other chessman
        if self.check_move(int(x), int(y), chessman_call):
            return True
        else:
             return False

    def check_move_color(self, chessman, x, y):#name! checks if attacked x,y cell is not under your control
        if chessman.color != self.holding_chessman.color:
            return True
        else:
            return False

    def check_move(self, x, y, chessman):#checks, uf selected chessman can make move on x,y cell
        if chessman.get_moves().count([x,y]):
            return True
        else:
            return False

    def check_attack(self,x,y,chessman):#checks, if selected chessman can make such an attack(this function is made specially for pawns, becouse their attack moves are different from regular moves)
        if self.holding_chessman.get_attacks().count([x,y]):
            return True
        else:
            return False