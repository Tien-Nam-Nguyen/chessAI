from functools import reduce
import pygame as pg
from engine import Game
from engine.game_objects import SpriteButton, Rectangle, Label
from engine.game_components.label_renderer import LabelRenderConfig
from engine.game_objects.SpriteButton import SpriteButtonConfig
from engine.game_components.button import ButtonEvents, Button as ButtonComponent

import Piece as BackendPiece
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
    "b": BackendPiece.Bishop,
    "k": BackendPiece.King,
    "n": BackendPiece.Knight,
    "p": BackendPiece.Pawn,
    "q": BackendPiece.Queen,
    "r": BackendPiece.Rook,
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

ODD_COLOR = (113, 149, 88)
EVEN_COLOR = (235, 236, 210)
ODD_SELECTED_COLOR = (70, 110, 40)
EVEN_SELECTED_COLOR = (170, 170, 170)

PLAYER_FIRST = True
PLAYER_COLOR = BoardConfig.WHITE if PLAYER_FIRST else BoardConfig.BLACK


class Piece(SpriteButton):
    def __init__(
        self,
        coord_x: int,
        coord_y: int,
        config: SpriteButtonConfig,
        name="Piece",
        active=True,
    ):
        super().__init__(config, name, active)
        self.coord_x = coord_x
        self.coord_y = coord_y


class Tile(Rectangle):
    def __init__(
        self,
        x: float,
        y: float,
        coord_x: int,
        coord_y: int,
        width: float,
        height: float,
        color: pg.color.Color,
        name: str = "Tile",
        active: bool = True,
    ):
        super().__init__(x, y, width, height, color, name, active)
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.button_component = ButtonComponent(self.rect)
        self.add_component(self.button_component)


class Chess(Game):
    def __init__(self):
        self.sprites = {
            piece: pg.image.load(path) for piece, path in ASSET_PATHS.items()
        }

        scale = self.calc_pieces_size()

        self.pieces = {
            piece: [
                Piece(
                    0,
                    0,
                    SpriteButtonConfig(
                        sprite,
                        rest_scale=scale,
                        hover_scale=scale * 1.2,
                        pressed_scale=scale * 1.3,
                    ),
                    name=f"{piece}{index}",
                    active=False,
                )
                for index in range(PIECE_COUNT[piece[1]])
            ]
            for piece, sprite in self.sprites.items()
        }

        self.tiles = {
            (x, y): Tile(
                *self.calc_piece_game_coords(x, y),
                x,
                y,
                BoardConfig.TILE_SIZE,
                BoardConfig.TILE_SIZE,
                color=(x + y) % 2 and ODD_COLOR or EVEN_COLOR,
                name=f"Tile{x}{y}",
            )
            for x in range(8)
            for y in range(8)
        }

        tile_game_objs = [tile for tile in self.tiles.values()]
        piece_game_objs = [piece for pieces in self.pieces.values() for piece in pieces]

        game_pieces = [
            *tile_game_objs,
            *piece_game_objs,
        ]

        super().__init__(
            GAME_SIZE, caption="Sprite Renderer Example", game_objects=game_pieces
        )

        self.board = Board(playerColor=PLAYER_COLOR)
        self.pieces_by_coords = self.sync_pieces()
        self.listen_pieces_click()
        self.listen_tiles_click()

        self.available_moves: list[tuple[tuple[int, int], tuple[int, int]]] = (
            self.board.get_moves()
        )

        self.potential_moves: list[tuple[tuple[int, int], tuple[int, int]]] = []

        self.turn_indicator_font = pg.font.Font(None, 36)
        self.turn_indicator = self.place_turn_indicator()
        self.add_game_objects(self.turn_indicator)

    def place_turn_indicator(self):
        self.is_players_turn = PLAYER_FIRST

        text = "Player's turn on " if self.is_players_turn else "AI's turn on "
        text += "White" if self.board.turnColor == BoardConfig.WHITE else "Black"

        indicator = Label(
            self.turn_indicator_font,
            text,
            LabelRenderConfig(BoardConfig.BLACK),
            name="TurnIndicator",
        )

        center_x = GAME_SIZE[0] // 2
        top = 60

        indicator.transform.x = center_x
        indicator.transform.y = top

        return indicator

    def calc_pieces_size(self):
        max_size = max(
            max(sprite.get_width(), sprite.get_height())
            for sprite in self.sprites.values()
        )

        scale = BoardConfig.TILE_SIZE / max_size
        return scale

    def sync_pieces(self):
        unassigned_pieces = {
            piece: pieces.copy() for piece, pieces in self.pieces.items()
        }

        reversed_map = {piece: sprite for sprite, piece in PIECE_OBJECT_MAP.items()}

        pieces_by_coords = {}

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
                piece.coord_x = backend_piece.x
                piece.coord_y = backend_piece.y
                piece.transform.x = coords[0]
                piece.transform.y = coords[1]

                pieces_by_coords[(backend_piece.x, backend_piece.y)] = piece

        return pieces_by_coords

    def listen_pieces_click(self):
        for pieces in self.pieces.values():
            for piece in pieces:
                piece.button_component.on(
                    ButtonEvents.CLICK,
                    lambda button: self.on_click_piece(button.game_object),
                )

    def listen_tiles_click(self):
        for tile in self.tiles.values():
            tile.button_component.on(
                ButtonEvents.CLICK,
                lambda button: self.on_click_tile(button.game_object),
            )

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

    def on_click_piece(self, piece: Piece):
        moves: list[tuple[tuple[int, int], tuple[int, int]]] = reduce(
            lambda acc, move: (
                acc + [move] if move[0] == (piece.coord_x, piece.coord_y) else acc
            ),
            self.available_moves,
            [],
        )

        if len(moves) == 0:
            self.potential_moves = []
            self.recolor_tiles([])
            return

        self.potential_moves = moves
        self.recolor_tiles([move[1] for move in moves])

    def on_click_tile(self, tile: Tile):
        if len(self.potential_moves) == 0:
            return

        dests = reduce(
            lambda acc, move: (
                acc + [move] if move[1] == (tile.coord_x, tile.coord_y) else acc
            ),
            self.potential_moves,
            [],
        )

        if len(dests) == 0:
            return

        print(dests)

    def recolor_tiles(self, selected_tiles: list[tuple[int, int]]):
        for x in range(8):
            for y in range(8):
                color = (x + y) % 2 and ODD_COLOR or EVEN_COLOR
                self.tiles[(x, y)].color = color

        for tile in selected_tiles:
            color = (
                (tile[0] + tile[1]) % 2 and ODD_SELECTED_COLOR or EVEN_SELECTED_COLOR
            )
            self.tiles[tile].color = color

    def update(self):
        if self.board.playerTurn != self.is_players_turn:
            self.is_players_turn = self.board.playerTurn
            text = "Player's turn on" if self.is_players_turn else "AI's turn on"
            text += "White" if self.board.turnColor == BoardConfig.WHITE else "Black"
            self.turn_indicator.text = text


chess = Chess()
chess.run()
