from typing import Callable
from functools import reduce
import pygame as pg
import time
from math import inf
from random import seed, randint

from engine import Game
from engine.game_objects import SpriteButton, Rectangle, Label, LabelButton
from engine.game_components.label_renderer import LabelRenderConfig
from engine.game_objects.SpriteButton import SpriteButtonConfig
from engine.game_objects.LabelButton import LabelButtonConfig
from engine.game_components.button import ButtonEvents, Button as ButtonComponent

import Piece as BackendPiece
from Board import Board
import config as BoardConfig
from core import minimax

PLAYER_FIRST = True
SEED = 0
MINIMAX_DEPTH = BoardConfig.EASY

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

PIECE_OBJECT_RMAP = {piece: sprite for sprite, piece in PIECE_OBJECT_MAP.items()}

PIECE_COUNT = {
    "b": 8,
    "k": 8,
    "n": 8,
    "p": 8,
    "q": 8,
    "r": 8,
}

PIECES = [f"{color}{piece}" for piece in PIECE_TYPES for color in ["b", "w"]]
GAME_SIZE = (BoardConfig.SCREEN_WIDTH, BoardConfig.SCREEN_HEIGHT)
ASSET_PATHS = {piece: f"assets/pieces/{piece}.png" for piece in PIECES}

ODD_COLOR = (113, 149, 88)
EVEN_COLOR = (235, 236, 210)
ODD_SELECTED_COLOR = (70, 110, 40)
EVEN_SELECTED_COLOR = (170, 170, 170)

PLAYER_COLOR = BoardConfig.WHITE if PLAYER_FIRST else BoardConfig.BLACK


class Piece(SpriteButton):
    def __init__(
        self,
        coord_x: int,
        coord_y: int,
        color: pg.color.Color,
        config: SpriteButtonConfig,
        name="Piece",
        active=True,
    ):
        super().__init__(config, name, active)
        self.coord_x = coord_x
        self.coord_y = coord_y
        self.color = color


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
        seed(SEED)
        self.sprites = {
            piece: pg.image.load(path) for piece, path in ASSET_PATHS.items()
        }

        scale = self.calc_pieces_size()

        self.pieces = {
            piece: [
                Piece(
                    -1,
                    -1,
                    BoardConfig.WHITE if piece[0] == "w" else BoardConfig.BLACK,
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

        self.heading_font = pg.font.Font(None, 36)
        self.body_font = pg.font.Font(None, 24)

        self.turn_indicator = self.place_turn_indicator()
        self.add_game_objects(self.turn_indicator)

        self.button_section = self.place_button_heading()
        self.add_game_objects(self.button_section)

        self.buttons = self.place_buttons()
        self.add_game_objects(*self.buttons.values())

    def place_buttons(self):
        random_move_button = self.place_random_move_button()
        minimax_move_button = self.place_minimax_move_button()

        return {
            random_move_button.name: random_move_button,
            minimax_move_button.name: minimax_move_button,
        }

    def place_random_move_button(self):
        button = LabelButton(
            self.body_font,
            "Make Random Move",
            LabelButtonConfig(
                LabelRenderConfig(BoardConfig.BLACK),
                rest_scale=1.0,
                hover_scale=1.2,
                pressed_scale=1.3,
            ),
            name="RandomMoveButton",
        )

        button.transform.x = 135
        button.transform.y = 100

        button.button_component.on(
            ButtonEvents.CLICK,
            lambda button: self.on_click_random_move_button(button.game_object),
        )

        return button

    def place_minimax_move_button(self):
        button = LabelButton(
            self.body_font,
            "Make Minimax Move",
            LabelButtonConfig(
                LabelRenderConfig(BoardConfig.BLACK),
                rest_scale=1.0,
                hover_scale=1.2,
                pressed_scale=1.3,
            ),
            name="MinimaxMoveButton",
        )

        button.transform.x = 135
        button.transform.y = 130

        button.button_component.on(
            ButtonEvents.CLICK,
            lambda button: self.on_click_minimax_move_button(button.game_object),
        )

        return button

    def on_click_random_move_button(self, button):
        if len(self.available_moves) == 0:
            return

        move = self.available_moves[randint(0, len(self.available_moves) - 1)]
        self.make_move(move)

    def on_click_minimax_move_button(self, button):
        if len(self.available_moves) == 0:
            return

        is_bot_turn = not self.board.playerTurn
        bot_color = self.board.botColor

        start = time.time()
        move, eval_score = minimax(
            self.board, MINIMAX_DEPTH, -inf, inf, is_bot_turn, bot_color
        )
        end = time.time()

        print(
            f"Made move {move} in {end - start} seconds with minimax score {eval_score}."
        )
        self.make_move(move)

    def place_turn_indicator(self):
        indicator = Label(
            self.heading_font,
            self.get_turn_indicator_text(),
            LabelRenderConfig(BoardConfig.BLACK),
            name="TurnIndicator",
        )

        center_x = GAME_SIZE[0] // 2
        top = 60

        indicator.transform.x = center_x
        indicator.transform.y = top

        return indicator

    def place_button_heading(self):
        label = Label(
            self.heading_font,
            "Buttons",
            LabelRenderConfig(BoardConfig.BLACK),
            name="ButtonSectionLabel",
        )

        left_x = 100
        top_y = 60

        label.transform.x = left_x
        label.transform.y = top_y

        return label

    def calc_pieces_size(self):
        max_size = max(
            max(sprite.get_width(), sprite.get_height())
            for sprite in self.sprites.values()
        )

        scale = BoardConfig.TILE_SIZE / max_size
        return scale

    def reset_pieces(self):
        for pieces in self.pieces.values():
            for piece in pieces:
                piece.button_component.active = False
                piece.active = False
                piece.coord_x = -1
                piece.coord_y = -1

    def find_unassigned_pieces(self, name: str):
        for piece in self.pieces[name]:
            if not piece.active:
                return piece

    def sync_pieces(self):
        def for_each_backend_piece(callback: Callable[[BackendPiece.Piece], None]):
            for row in self.board.tiles:
                for backend_piece in row:
                    if backend_piece is None:
                        continue

                    callback(backend_piece)

        pieces_by_coords = {}
        turn_color = self.board.turnColor

        def sync_piece_with_backend(backend_piece: BackendPiece.Piece):
            piece_type: str = PIECE_OBJECT_RMAP.get(type(backend_piece))
            is_white = backend_piece.color == BoardConfig.WHITE
            is_same_as_turn_color = backend_piece.color == turn_color

            piece_name = f"{is_white and 'w' or 'b'}{piece_type}"
            piece = self.find_unassigned_pieces(piece_name)

            coords = self.calc_piece_game_coords(backend_piece.x, backend_piece.y)

            piece.active = True
            piece.button_component.active = is_same_as_turn_color
            piece.coord_x = backend_piece.x
            piece.coord_y = backend_piece.y
            piece.transform.x = coords[0]
            piece.transform.y = coords[1]

            pieces_by_coords[(backend_piece.x, backend_piece.y)] = piece

        self.reset_pieces()
        for_each_backend_piece(sync_piece_with_backend)

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

        for move in self.potential_moves:
            if move[1] == (tile.coord_x, tile.coord_y):
                self.make_move(move)
                break

    def make_move(self, move: tuple[tuple[int, int], tuple[int, int]]):
        self.board.make_move(*move)
        self.pieces_by_coords = self.sync_pieces()
        self.available_moves = self.board.get_moves()
        self.potential_moves = []
        self.recolor_tiles([])
        self.update_turn_indicator()

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

    def update_turn_indicator(self):
        self.turn_indicator.label_componenet.label = self.get_turn_indicator_text()

    def get_turn_indicator_text(self):
        if self.board.gameover:
            is_draw = self.board.game_result[1] == "draw"
            text = "Game Over!"
            text += (
                "Draw"
                if is_draw
                else f"{self.board.game_result[0]} {self.board.game_result[1]}"
            )
            return text

        text = "Player's turn on " if self.board.playerTurn else "AI's turn on "
        text += "White" if self.board.turnColor == BoardConfig.WHITE else "Black"
        return text


chess = Chess()
chess.run()
