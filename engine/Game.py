from typing import TYPE_CHECKING
import pygame as pg

if TYPE_CHECKING:
    from .GameObject import GameObject


class Game:
    def __init__(
        self,
        screen_size: tuple[int, int],
        caption: str,
        background=pg.Color(255, 255, 255),
        game_objects: list["GameObject"] = [],
    ) -> None:
        if not pg.font:
            raise ImportError("pg.font not available")

        if not pg.mixer:
            raise ImportError("pg.mixer not available")

        pg.font.init()
        pg.mixer.init()

        pg.display.set_caption(caption)

        self.background = background
        self.screen = pg.display.set_mode(screen_size)
        self.clock = pg.time.Clock()
        self.game_objects: list["GameObject"] = []
        self.running = False

        self.add_game_objects(*game_objects)

    def run(self):
        self.running = True

        self.start_tick()

        while self.running:
            self.tick()

        pg.quit()

    def start_tick(self):
        self.clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

        self.screen.fill(self.background)

        for game_object in self.game_objects:
            game_object.core_start()

        pg.display.flip()
        pg.display.update()

    def tick(self):
        self.clock.tick(60)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.quit()

        self.screen.fill(self.background)

        for game_object in self.game_objects:
            game_object.core_update()

        pg.display.flip()
        pg.display.update()

    def quit(self):
        self.running = False

    def add_game_objects(self, *game_objects: "GameObject"):
        for game_object in game_objects:
            if game_object.game is not None:
                game_object.game.remove_game_objects(game_object)

            game_object.game = self
            self.game_objects.append(game_object)

    def remove_game_objects(self, *game_objects: "GameObject"):
        for game_object in game_objects:
            self.game_objects.remove(game_object)
            game_object.game = None
