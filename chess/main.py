from models import Pawn, Board, King, Color

new_board = Board()
print(new_board)
new_board.board[1][2] = Pawn(Color.BLACK)
new_board.board[0][3] = King(Color.BLACK)
new_board.board[7][3] = King(Color.WHITE)
print(new_board)
next_move = new_board.get_moves(2, 1)
print(next_move)
new_board.move([2, 1], next_move[0])
print(new_board)
