from Piece import *
from config import *

class Board:
    
    def __init__(self, playerColor=WHITE):
        self.whiteScore = 10 * 8 + 30 * 4 + 50 * 2 + 90 + 1000
        self.blackScore = 10 * 8 + 30 * 4 + 50 * 2 + 90 + 1000
        self.playerColor = playerColor
        self.botColor = BLACK
        if self.playerColor == BLACK:
            self.botColor = WHITE

        self.gameover = False
        self.game_result = None
        self.tiles = []
        self.history = []
        self.history_board = []
        self.turnColor = WHITE
        self.playerTurn = True if self.turnColor == self.playerColor else False


        # init bot
        row = []
        row.append(Rook(0, 0, self.botColor))        
        row.append(Knight(1, 0, self.botColor))
        row.append(Bishop(2, 0, self.botColor))
        row.append(Queen(3, 0, self.botColor))
        row.append(King(4, 0, self.botColor))
        row.append(Bishop(5, 0, self.botColor))
        row.append(Knight(6, 0, self.botColor))
        row.append(Rook(7, 0, self.botColor))
        self.tiles.append(row)

        row = []
        for i in range(8):
            row.append(Pawn(i, 1, self.botColor))
        self.tiles.append(row)


        for i in range(4):
            self.tiles.append([None, None, None, None, None, None, None, None])


        row = []
        for i in range(8):
            row.append(Pawn(i, 6, self.playerColor))
        self.tiles.append(row)

        row = []
        row.append(Rook(0, 7, self.playerColor))        
        row.append(Knight(1, 7, self.playerColor))
        row.append(Bishop(2, 7, self.playerColor))
        row.append(Queen(3, 7, self.playerColor))
        row.append(King(4, 7, self.playerColor))
        row.append(Bishop(5, 7, self.playerColor))
        row.append(Knight(6, 7, self.playerColor))
        row.append(Rook(7, 7, self.playerColor))
        self.tiles.append(row)

        self.whiteKing = (4, 7) if self.playerColor == WHITE else (4, 0)
        self.blackKing = (4, 0) if self.whiteKing == (4, 7) else (4, 7)


        
    def make_move(self, src, dest):         # src co dang x, y
        src_piece = self.tiles[src[1]][src[0]]
        dest_piece = self.tiles[dest[1]][dest[0]]

        previous_state = {
            "blackScore": self.blackScore,
            "whiteScore": self.whiteScore,
            "blackKing": self.blackKing,
            "whiteKing": self.whiteKing,
            "gameover": self.gameover,
            "src": (src, src_piece.copy()),
            "dest": (dest, dest_piece.copy() if dest_piece is not None else None)
        }

        self.history.append(previous_state)

        if dest_piece is not None:
            if self.turnColor == WHITE:
                self.blackScore -= dest_piece.weight
            else:
                self.whiteScore -= dest_piece.weight


        src_piece.move(dest[0], dest[1])
        dest_piece = src_piece
        dest_piece.firstMove = False
        
        # replace piece in tiles
        self.tiles[dest[1]][dest[0]] = dest_piece
        self.tiles[src[1]][src[0]] = None
        
        if type(dest_piece) is Pawn:
            if (self.playerTurn and dest[1] == 0) or (not self.playerTurn and dest[1] == 7):
                self.tiles[dest[1]][dest[0]] = Queen(dest[0], dest[1], dest_piece.color)

        if type(dest_piece) is King:
            if dest_piece.color == WHITE:
                self.whiteKing = (dest[0], dest[1])
            else:
                self.blackKing = (dest[0], dest[1])

        src_piece = None
        self.next_turn()
        # TODO: check win condition
        self.get_over_state()




    def unmake_move(self):
        previous_state = self.history.pop()
        self.blackScore = previous_state['blackScore']
        self.whiteScore = previous_state['whiteScore']
        self.whiteKing = previous_state['whiteKing']
        self.blackKing = previous_state['blackKing']
        self.gameover = previous_state['gameover']

        x = previous_state['src'][0][0]
        y = previous_state['src'][0][1]
        self.tiles[y][x] = previous_state['src'][1]
        x = previous_state['dest'][0][0]
        y = previous_state['dest'][0][1]
        self.tiles[y][x] = previous_state['dest'][1]

        self.next_turn()
        del previous_state
    


    def next_turn(self):
        if self.turnColor == WHITE:
            self.turnColor = BLACK
        else:
            self.turnColor = WHITE

        self.playerTurn = not self.playerTurn




    def valid_move(self, coor, color):
        if self.is_valid_coords(coor) and (not self.piece_at_coords(coor) or self.enemy_at_coords(coor, color)):
            return True
        
        return False


    def piece_at_coords(self, coords):
        if not self.is_valid_coords(coords) or self.tiles[coords[1]][coords[0]] is None:
            return False
        
        return True


    def enemy_at_coords(self, coords, color):
        if self.piece_at_coords(coords) and color != self.tiles[coords[1]][coords[0]].color:
            return True
        
        return False
    

    def sort_by_weight(self, move):
        if self.tiles[move[1][1]][move[1][0]] is None:
            return -1
        
        return self.tiles[move[1][1]][move[1][0]].weight




    def get_moves(self):        # [(src, dest), ...]
        moves = []
        enemy_king = self.blackKing if self.turnColor == WHITE else self.whiteKing

        for y in range(8):
            for x in range(8):
                if self.piece_at_coords((x, y)) and self.turnColor == self.tiles[y][x].color:
                    for move in self.tiles[y][x].valid_moves(self):
                        if not self.checked_after_move((x,y), move, self.turnColor):
                            tmp_board = self.copy()
                            tmp_board.tiles[move[1]][move[0]] = self.tiles[y][x]
                            tmp_board.tiles[y][x] = None
                            if tmp_board not in self.history_board:
                                moves.append(((x, y), move))
                                del tmp_board

        moves = sorted(moves, key=self.sort_by_weight, reverse=True)
        return moves
    


    def is_valid_coords(self, coords):
        if coords[0] < 0 or coords[0] >= 8 or coords[1] < 0 or coords[1] >= 8:
            return False
        
        return True
    


    def checked_after_move(self, src, dest, color):
        res = False
        # self.make_move(src, dest)
        src_piece = self.tiles[src[1]][src[0]]
        dest_piece = self.tiles[dest[1]][dest[0]]
        tmp_dest = dest_piece.copy() if dest_piece is not None else None
        tmp_src = src_piece.copy()


        if type(dest_piece) is Pawn:
            if (self.playerTurn and dest[1] == 0) or (not self.playerTurn and dest[1] == 7):
                src_piece = Queen(src[0], src[1], src_piece.color)

        src_piece.move(dest[0], dest[1])
        dest_piece = src_piece

        self.tiles[src[1]][src[0]] = None
        self.tiles[dest[1]][dest[0]] = dest_piece
        
        if type(dest_piece) is Pawn:
            if (self.playerTurn and dest[1] == 0) or (not self.playerTurn and dest[1] == 7):
                self.tiles[dest[1]][dest[0]] = Queen(dest[0], dest[1], dest_piece.color)

        king = None
        if type(dest_piece) is King:
            if dest_piece.color == WHITE:
                king = self.whiteKing
                self.whiteKing = (dest[0], dest[1])
            else:
                king = self.blackKing
                self.blackKing = (dest[0], dest[1])
        src_piece = None
        self.next_turn()

        if self.is_checked(color):
            res = True

        # restore tiles

        self.tiles[src[1]][src[0]] = tmp_src
        self.tiles[dest[1]][dest[0]] = tmp_dest
        # self.tiles[src[1]][src[0]].move(src[0], src[1])

        if type(dest_piece) is King:
            if dest_piece.color == WHITE:
                self.whiteKing = king
            else:
                self.blackKing = king

        self.next_turn() 
        # self.unmake_move()
        return res


    def is_checked(self, color):
        king_coords = self.whiteKing if color == WHITE else self.blackKing
        
        for y in range(8):
            for x in range(8):
                if self.enemy_at_coords((x,y), color):
                    for move in self.tiles[y][x].valid_moves(self):
                        if king_coords[0] == move[0] and king_coords[1] == move[1]:
                            return True
                        
        return False
    

    def get_over_state(self):
        out_of_move = True
        
        for y in range(8):
            for x in range(8):
                if self.piece_at_coords((x, y)) and self.turnColor == self.tiles[y][x].color:
                    moves = self.tiles[y][x].valid_moves(self)
                    for move in moves:
                        if not self.checked_after_move((x, y), move, self.turnColor):
                            out_of_move = False
                            break
            
            if not out_of_move:
                break
                        

        if out_of_move:
            self.gameover = True
            if not self.is_checked(self.turnColor):
                self.game_result = (None, 'draw')
                return
            
            else:
                self.game_result = (self.turnColor, 'lose')
                return 
        
        self.gameover = False
        return None
    

    def copy(self):
        copy = Board(self.playerColor)
        for y in range(8):
            for x in range(8):
                if self.tiles[y][x] is not None:
                    copy.tiles[y][x] = self.tiles[y][x].copy()
                else:
                    copy.tiles[y][x] = None

        return copy
    

    def __eq__(self, value: object) -> bool:
        for y in range(8):
            for x in range(8):
                if type(self.tiles[y][x]) != type(value.tiles[y][x]):
                    return False
                
        return True

                        

    def visualize_board(self):
        for y in range(8):
            row = []
            for x in range(8):
                if self.tiles[y][x] is None:
                    row.append(None)
                else:
                    color = self.tiles[y][x].color
                    if color == WHITE:
                        color = 'w_'
                    else:
                        color = 'b_'
                    row.append(color + type(self.tiles[y][x]).__name__)
            
            print(row)




        