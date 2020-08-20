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

    # function changes turn by setting GameState class's attribute turn into other Color
    def change_turn(self):
        self.holding_chessman = None
        if self.turn == Color.WHITE:
            self.turn = Color.BLACK
        elif self.turn == Color.BLACK:
            self.turn = Color.WHITE
        else:
            raise Exception("Color Error")

    # function captures chessman by changing class's attribute and saves there captured chessman. Captured chessman
    # is able to make a move.
    def capture_chessman(self, chessman):
        self.holding_chessman = chessman

    # function check if GameState has a captured_chessman
    def is_holding(self, chessman):
        for ch in self.board.chessmen_list:
            if ch.CALLBACK == chessman.CALLBACK:
                return True
        return False

    # function makes GameState by changing attribute captured_chessman to "free" chessman if there is one
    def leave_chessman(self):
        if self.holding_chessman is not None:
            self.holding_chessman = None

    # function checks if chessman, which was captured, has the same color as GameState.turn
    def allow_turn(self, chessman_call):
        if self.board.get_chessman_call(chessman_call).color == self.turn:
            return True
        else:
            return False

    # function checks if captured_chessman can attack on x,y cell and if x,y cell is not taken yet by same color
    # chessman.
    def allow_attack(self, chessman_call, x, y):
        chessman = self.board.get_chessman_call(chessman_call)
        if self.check_attack(int(x), int(y)) and self.check_move_color(chessman):
            return True
        else:
            return False

    # function checks if captured_chessman can make a move on x,y cell. (Throws exception message in __main__.py)
    def allow_move(self, x, y, chessman_call):
        if self.check_move(int(x), int(y), chessman_call):
            return True
        else:
            return False

    # name! checks if attacked x,y cell is not the same color, as captured_chessman
    def check_move_color(self, chessman):
        if chessman.color != self.holding_chessman.color:
            return True
        else:
            return False

    # function checks, if selected chessman can make move on x,y cell
    def check_move(self, x, y, chessman):
        if chessman.get_moves().count([x, y]):
            return True
        else:
            return False

    # function checks, if selected chessman can make such an attack(this function is made specially for pawns,
    # because their attack moves are different from regular moves)
    def check_attack(self, x, y,):
        if self.holding_chessman.get_attacks().count([x, y]):
            return True
        else:
            return False
