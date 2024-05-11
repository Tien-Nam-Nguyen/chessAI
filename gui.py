import math
import pygame as pg
from engine import Game
from engine.game_objects import Sprite, SpriteButton
from engine.game_objects.SpriteButton import SpriteButtonConfig

PIECE_TYPES = [
    "b",
    "k",
    "n",
    "p",
    "q",
    "r",
]

PIECE_SIZE = (150, 150)

PIECES = [f"{color}{piece}" for piece in PIECE_TYPES for color in ["b", "w"]]
GAME_SIZE = (500, 500)
ASSET_PATHS = [f"assets/pieces/{piece}.png" for piece in PIECES]


class Chess(Game):
    def __init__(self):
        sprites = {path: pg.image.load(path) for path in ASSET_PATHS}
        game_objects = [
            # Sprite(sprite, name=path, active=False)
            # for path, sprite in sprites.items()
            SpriteButton(SpriteButtonConfig(sprite), name=path, active=False)
            for path, sprite in sprites.items()
        ]

        super().__init__(
            GAME_SIZE, caption="Sprite Renderer Example", game_objects=game_objects
        )

        # test relative position
        self.chess_piece_a = game_objects[0]
        self.chess_piece_b = game_objects[1]

        self.chess_piece_a.active = True
        self.chess_piece_b.active = True

        self.chess_piece_a.transform.x = 150
        self.chess_piece_a.transform.y = 150

        self.chess_piece_a.add_child(self.chess_piece_b)
        self.chess_piece_b.transform.x = 100


chess = Chess()
chess.run()
