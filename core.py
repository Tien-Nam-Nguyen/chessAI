import pygame
import os
from Board import Board
from config import *


def evaluate(board: Board, playerColor):
    if playerColor == WHITE:
        return board.whiteScore - board.blackScore
    
    return board.blackScore - board.whiteScore


def minimax(board: Board, depth, alpha, beta, bot_turn, max_color): 
    # top state is given to bot to declare next state 
    
    if depth == 0 or board.gameover:
        return None, evaluate(board, max_color)
    
    moves = board.get_moves()   #[(src, dest), ...]
    max_eval = -99999999
    min_eval = max_eval * -1
    best_move = None


    for move in moves:
        board.make_move(move[0], move[1])
        current_eval = minimax(board, depth - 1, alpha, beta, not bot_turn, max_color)[1]
        board.unmake_move()
        if bot_turn:
            if current_eval > max_eval:
                max_eval = current_eval
                best_move = move

            alpha = max(alpha, current_eval)
            if alpha >= beta:
                break
        else:
            if current_eval < min_eval:
                min_eval = current_eval
                best_move = move
            beta = min(beta, current_eval)
            if alpha >= beta:
                break

    return best_move, max_eval if bot_turn else min_eval

    # best_move: (src, dest)