import pygame as pg
from engine import Game
from engine.game_objects import Sprite

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

sprites = {path: pg.image.load(path) for path in ASSET_PATHS}
game_objects = [Sprite(sprite, name=path) for path, sprite in sprites.items()]
game = Game(GAME_SIZE, caption="Sprite Renderer Example")

for index, game_object in enumerate(game_objects):
    game_object.transform.position = (
        index * GAME_SIZE[0] // len(game_objects),
        index * GAME_SIZE[1] // len(game_objects),
    )
    game.add_game_object(game_object)


game.run()
