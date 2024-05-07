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

    def run(self):
        self.running = True

        while self.running:
            self.clock.tick(60)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.quit()

            self.screen.fill(self.background)

            for game_object in self.game_objects:
                game_object.core_update()

            pg.display.flip()
            pg.display.update()

        pg.quit()

    def quit(self):
        self.running = False

    def add_game_object(self, game_object: "GameObject"):
        game_object.game = self
        self.game_objects.append(game_object)

    def remove_game_object(self, game_object: "GameObject"):
        self.game_objects.remove(game_object)
        game_object.game = None
