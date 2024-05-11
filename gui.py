import pygame as pg
from engine import Game
from engine.game_objects import Sprite, SpriteButton
from engine.game_objects.SpriteButton import SpriteButtonConfig
import Piece
from Board import Board
import config as BoardConfig

PIECE_TYPES = [
    "b",
    "k",
    "n",
    "p",
    "q",
    "r",
]

PIECE_OBJECT_MAP = {
    "b": Piece.Bishop,
    "k": Piece.King,
    "n": Piece.Knight,
    "p": Piece.Pawn,
    "q": Piece.Queen,
    "r": Piece.Rook,
}

PIECE_COUNT = {
    "b": 2,
    "k": 1,
    "n": 2,
    "p": 8,
    "q": 1,
    "r": 2,
}

PIECES = [f"{color}{piece}" for piece in PIECE_TYPES for color in ["b", "w"]]
GAME_SIZE = (BoardConfig.SCREEN_WIDTH, BoardConfig.SCREEN_HEIGHT)
ASSET_PATHS = {piece: f"assets/pieces/{piece}.png" for piece in PIECES}


class Chess(Game):
    def __init__(self):
        self.sprites = {
            piece: pg.image.load(path) for piece, path in ASSET_PATHS.items()
        }

        self.pieces = {
            piece: [
                SpriteButton(
                    SpriteButtonConfig(sprite), name=f"{piece}{index}", active=False
                )
                for index in range(PIECE_COUNT[piece[1]])
            ]
            for piece, sprite in self.sprites.items()
        }

        game_pieces = [piece for pieces in self.pieces.values() for piece in pieces]

        super().__init__(
            GAME_SIZE, caption="Sprite Renderer Example", game_objects=game_pieces
        )

        self.update_pieces_size()
        self.board = Board(playerColor=BoardConfig.WHITE)
        self.sync_pieces()

    def update_pieces_size(self):
        max_size = max(
            max(sprite.get_width(), sprite.get_height())
            for sprite in self.sprites.values()
        )

        scale = BoardConfig.TILE_SIZE / max_size

        for piece in self.pieces.values():
            for sprite in piece:
                sprite.config = SpriteButtonConfig(
                    sprite.config.image,
                    rest_scale=scale,
                    hover_scale=scale * 1.1,
                    pressed_scale=scale * 1.2,
                )

    def sync_pieces(self):
        unassigned_pieces = self.pieces.copy()
        reversed_map = {piece: sprite for sprite, piece in PIECE_OBJECT_MAP.items()}

        for row in self.board.tiles:
            for backend_piece in row:
                if backend_piece is None:
                    continue

                piece_type: str = reversed_map.get(type(backend_piece))
                is_white = backend_piece.color == BoardConfig.WHITE

                piece_name = f"{is_white and 'w' or 'b'}{piece_type}"
                piece = unassigned_pieces[piece_name].pop()

                coords = self.calc_piece_game_coords(backend_piece.x, backend_piece.y)

                piece.active = True
                piece.transform.x = coords[0]
                piece.transform.y = coords[1]

    def calc_piece_game_coords(self, x: int, y: int):

        board_size = BoardConfig.TILE_SIZE * 8

        # center the board based on board_size instead of the values inside config, sprites are centered so we need to also account for the size of the tile in our calculations
        coords = (
            (GAME_SIZE[0] - board_size) // 2
            + BoardConfig.TILE_SIZE * x
            + BoardConfig.TILE_SIZE // 2,
            (GAME_SIZE[1] - board_size) // 2
            + BoardConfig.TILE_SIZE * y
            + BoardConfig.TILE_SIZE // 2,
        )

        return coords


chess = Chess()
chess.run()
