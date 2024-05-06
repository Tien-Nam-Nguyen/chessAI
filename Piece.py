import os
from config import *
import pygame

# king_black = pygame.image.load(os.path.join('images', 'king-black.png'))
# queen_black = pygame.image.load(os.path.join('images', 'queen-black.png'))
# bishop_black = pygame.image.load(os.path.join('images', 'bishop-black.png'))
# knight_black = pygame.image.load(os.path.join('images', 'knight-black.png'))
# rook_black = pygame.image.load(os.path.join('images', 'rook-black.png'))
# pawn_black = pygame.image.load(os.path.join('images', 'pawn-black.png'))


# king_white = pygame.image.load(os.path.join('images', 'king-white.png'))
# queen_white = pygame.image.load(os.path.join('images', 'queen-white.png'))
# bishop_white = pygame.image.load(os.path.join('images', 'bishop-white.png'))
# knight_white = pygame.image.load(os.path.join('images', 'knight-white.png'))
# rook_white = pygame.image.load(os.path.join('images', 'rook-white.png'))
# pawn_white = pygame.image.load(os.path.join('images', 'pawn-white.png'))


# IMAGES = [
#     pygame.transform.scale(king_white, IMG_SCALE),
#     pygame.transform.scale(king_black, IMG_SCALE),
#     pygame.transform.scale(queen_white, IMG_SCALE),
#     pygame.transform.scale(queen_black, IMG_SCALE),
#     pygame.transform.scale(bishop_white, IMG_SCALE),
#     pygame.transform.scale(bishop_black, IMG_SCALE),
#     pygame.transform.scale(knight_white, IMG_SCALE),
#     pygame.transform.scale(knight_black, IMG_SCALE),
#     pygame.transform.scale(rook_white, IMG_SCALE),
#     pygame.transform.scale(rook_black, IMG_SCALE),
#     pygame.transform.scale(pawn_white, IMG_SCALE),
#     pygame.transform.scale(pawn_black, IMG_SCALE)
# ]

class Piece:

    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.image = None
        self.firstMove = True
        self.weight = 0

    
    def draw(self):
        if self.color == WHITE:
            # SCREEN.blit(IMAGES[self.image], to_coords(self.x, self.y))
        # else:
            # SCREEN.blit(IMAGES[self.image + 1], to_coords(self.x, self.y))
            pass

    
    def move(self, x, y):
        self.x = x
        self.y = y


    def copy(self):
        copy = type(self)(self.x, self.y, self.color)
        copy.image = self.image
        copy.firstMove = self.firstMove

        return copy


class King(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 0
        self.weight = 1000

    
    def valid_moves(self, board):
        moves = []
        for x in range(self.x - 1, self.x + 2):
            for y in range(self.y - 1, self.y + 2):
                if board.valid_move((x, y), self.color):
                    moves.append((x, y))

        # castle
        

        return moves
    

class Queen(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 2
        self.weight = 90

    
    def valid_moves(self, board):
        moves = Rook.valid_moves(self, board) + Bishop.valid_moves(self, board)

        return moves



class Bishop(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 4
        self.weight = 30

    
    def valid_moves(self, board):
        moves = []
        x, y = self.x, self.y
        while board.valid_move((x - 1, y - 1), self.color):
            moves.append((x - 1, y - 1))
            if board.piece_at_coords((x - 1, y - 1)):
                break

            x -= 1
            y -= 1

        x, y = self.x, self.y
        while board.valid_move((x + 1, y - 1), self.color):
            moves.append((x + 1, y - 1))
            if board.piece_at_coords((x + 1, y - 1)):
                break

            x += 1
            y -= 1

        x, y = self.x, self.y
        while board.valid_move((x - 1, y + 1), self.color):
            moves.append((x - 1, y + 1))
            if board.piece_at_coords((x - 1, y + 1)):
                break

            x -= 1
            y += 1
        
        x, y = self.x, self.y
        while board.valid_move((x + 1, y + 1), self.color):
            moves.append((x + 1, y + 1))
            if board.piece_at_coords((x + 1, y + 1)):
                break

            x += 1
            y += 1

        return moves
    

class Knight(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 6
        self.weight = 30

    
    def valid_moves(self, board):
        moves = []
        # x = 6;  y = 7
        # up right
        coor1 = (self.x + 1, self.y - 2)
        coor2 = (self.x + 2, self.y - 1)
        coor3 = (self.x + 1, self.y + 2)
        coor4 = (self.x + 2, self.y + 1)
        coor5 = (self.x - 1, self.y + 2)
        coor6 = (self.x - 2, self.y + 1)
        coor7 = (self.x - 1, self.y - 2)
        coor8 = (self.x - 2, self.y - 1)
        coors = [coor1, coor2, coor3, coor4, coor5, coor6, coor7, coor8]
        
        for coor in coors:
            if board.valid_move(coor, self.color):    
                moves.append(coor)

        return moves
    

class Rook(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y, color)
        self.image = 8
        self.weight = 50

    
    def valid_moves(self, board):
        moves = []

        for y in range(self.y - 1, -1, -1):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        for y in range(self.y + 1, 8):
            if board.valid_move((self.x, y), self.color):
                moves.append((self.x, y))
            if board.piece_at_coords((self.x, y)):
                break

        for x in range(self.x - 1, -1, -1):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        for x in range(self.x + 1, 8):
            if board.valid_move((x, self.y), self.color):
                moves.append((x, self.y))
            if board.piece_at_coords((x, self.y)):
                break

        return moves
    

class Pawn(Piece):

    def __init__(self, x, y, color):
        super().__init__(x, y , color)
        self.image = 10
        self.weight = 10

    
    def valid_moves(self, board):
        moves = []

        if board.playerTurn:
            if board.valid_move((self.x, self.y - 1), self.color) and not board.piece_at_coords((self.x, self.y - 1)):
                moves.append((self.x, self.y - 1))

                if board.valid_move((self.x, self.y - 2), self.color) and not board.piece_at_coords((self.x, self.y - 2)) and self.firstMove:
                    moves.append((self.x, self.y - 2))

            # capture
            if board.valid_move((self.x - 1, self.y - 1), self.color) and board.enemy_at_coords((self.x - 1, self.y - 1), self.color):
                moves.append((self.x - 1, self.y - 1))

            if board.valid_move((self.x + 1, self.y - 1), self.color) and board.enemy_at_coords((self.x + 1, self.y - 1), self.color):
                moves.append((self.x + 1, self.y - 1))

        else:

            if board.valid_move((self.x, self.y + 1), self.color) and not board.piece_at_coords((self.x, self.y + 1)):
                moves.append((self.x, self.y + 1))
            
                if board.valid_move((self.x, self.y + 2), self.color) and not board.piece_at_coords((self.x, self.y + 2)) and self.firstMove:
                    moves.append((self.x, self.y + 2))
            
            if board.valid_move((self.x + 1, self.y + 1), self.color) and board.enemy_at_coords((self.x + 1, self.y + 1), self.color):
                moves.append((self.x + 1, self.y + 1))

            if board.valid_move((self.x - 1, self.y + 1), self.color) and board.enemy_at_coords((self.x - 1, self.y + 1), self.color):
                moves.append((self.x - 1, self.y + 1))


        return moves
