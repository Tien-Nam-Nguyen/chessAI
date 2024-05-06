from Board import Board
import time
from core import minimax
from config import *
from math import inf

board = Board(playerColor=WHITE)
board.visualize_board()

# luu y: goc toa do (0, 0) nam o goc tren ben trai cua ban co
while not board.gameover:
    if board.playerTurn:
        x_src = int(input('Nhap vao hoanh do x quan can di: '))
        y_src = int(input('Nhap vao tung do y quan can di: '))

        x_dest = int(input('Nhap vao hoanh do x dich den: '))
        y_dest = int(input('Nhap vao tung do y dich den: '))

        piece = board.tiles[y_src][x_src]
        if piece is not None and (x_dest, y_dest) in piece.valid_moves(board) and not board.checked_after_move((x_src, y_src), (x_dest, y_dest), board.playerColor):
            board.make_move((x_src, y_src), (x_dest, y_dest))
        else:
            print('Invalid move!! Try again')
            continue
                        
    else:
        start = time.time()
        best_move, max_eval = minimax(board, MEDIUM, -inf, inf, True, board.botColor)

        board.make_move(best_move[0], best_move[1])
        print(f'Bot thuc hien nuoc di {best_move[0]} den {best_move[1]} trong {time.time() - start} giay')
    
    board.history_board.append(board.copy())
    board.visualize_board()

print(board.game_result)
                
