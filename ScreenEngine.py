import pygame
import collections
import Service

colors = {
    "black": (0, 0, 0, 255),
    "white": (255, 255, 255, 255),
    "red": (255, 0, 0, 255),
    "green": (0, 255, 0, 255),
    "blue": (0, 0, 255, 255),
    "wooden": (153, 92, 0, 255),
    "gray": (128, 128, 128, 128)
}


class ScreenHandle(pygame.Surface):

    def __init__(self, *args, **kwargs):
        self.game_engine = None
        if len(args) > 1:
            self.successor = args[-1]
            self.next_coord = args[-2]
            args = args[:-2]
        else:
            self.successor = None
            self.next_coord = (0, 0)
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        if self.successor is not None:
            canvas.blit(self.successor, self.next_coord)
            self.successor.draw(canvas)

    def connect_engine(self, engine):
        self.game_engine = engine
        if self.successor is not None:
            self.successor.connect_engine(engine)


class GameSurface(ScreenHandle):

    def draw_hero(self, sprite):
        self.game_engine.hero.draw(sprite)

    def draw_map(self):

        min_x, min_y = self.calculate()

        if self.game_engine.map:
            for i in range(len(self.game_engine.map[0]) - min_x):
                for j in range(len(self.game_engine.map) - min_y):
                    self.blit(self.game_engine.map[min_y + j][min_x + i][
                              0], (i * self.game_engine.sprite_size, j * self.game_engine.sprite_size))
        else:
            self.fill(colors["white"])

    def draw_object(self, sprite, coord):
        min_x, min_y = self.calculate()

        if self.game_engine.hero.stats['stealth']:
            # pygame.draw.rect(sprite, (255, 255, 255),
            #                                (int(coord[0] + 10), int(coord[1]), 30, 60), 1)
            pygame.draw.ellipse(self, colors["white"], (int((coord[0] - min_x) * self.game_engine.sprite_size)-10,
                                                        int((coord[1] - min_y) * self.game_engine.sprite_size)-10, 70, 80), 1)
            Service.shield = True

        self.blit(sprite, ((coord[0] - min_x) * self.game_engine.sprite_size,
                           (coord[1] - min_y) * self.game_engine.sprite_size))

    def draw(self, canvas):
        min_x, min_y = self.calculate()

        self.draw_map()
        for obj in self.game_engine.objects:
            sprite = obj.sprite[0]
            if obj.type == 'Enemy':
                if obj.direction == 'left':
                    sprite = obj.sprite2[0]

            self.blit(sprite, ((obj.position[0] - min_x) * self.game_engine.sprite_size,
                                       (obj.position[1] - min_y) * self.game_engine.sprite_size))

        self.draw_hero(self)
        super().draw(canvas)

    def calculate(self):
        display_size = list(self.get_size())
        display_size[0] /= self.game_engine.sprite_size
        display_size[1] /= self.game_engine.sprite_size
        hero_pos = self.game_engine.hero.position
        min_x = int(max(0, hero_pos[0] - display_size[0] + 7))
        min_y = int(max(0, hero_pos[1] - display_size[1] + 7))

        return (min_x, min_y)


class ProgressBar(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        alpha = 10
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 16)
        font2 = pygame.font.SysFont("serif", 16, 5)

        pygame.draw.rect(self, colors["white"], (20, 5, 200, 20), 2)
        pygame.draw.rect(self, colors["white"], (250, 5, 200, 20), 2)

        if self.game_engine:
            pygame.draw.rect(self, colors[
                             "red"], (20, 5, 200 * self.game_engine.hero.hp / self.game_engine.hero.max_hp, 20))

            pygame.draw.rect(self, colors["white"], (250, 5, 200, 20))
            pygame.draw.rect(self, colors["green"], (250, 5,
                                                     200 * self.game_engine.hero.exp / (100 * (2**(self.game_engine.hero.level - 1))), 20))

            self.blit(font1.render(f'HP', True, colors["black"]),
                      (30, 5))

            self.blit(font1.render(f'{self.game_engine.hero.hp}/{self.game_engine.hero.max_hp}', True, colors["black"]),
                      (80, 5))

            self.blit(font1.render(f'Level', True, colors["black"]),
                      (300, 5))
            self.blit(font2.render(f'Gold', True, colors["white"]),
                      (560, 5))

            self.blit(font1.render(f'{self.game_engine.hero.level}', True, colors["black"]),
                      (360, 5))
            self.blit(font2.render(f'{self.game_engine.hero.gold}', True, colors["white"]),
                      (610, 5))

            self.blit(font2.render(f'Str', True, colors["white"]),
                      (480, 5))
            self.blit(font2.render(f'Luck', True, colors["white"]),
                      (650, 5))

            self.blit(font2.render(f'{self.game_engine.hero.stats["strength"]}', True, colors["white"]),
                      (520, 5))
            self.blit(font2.render(f'{self.game_engine.hero.stats["luck"]}', True, colors["white"]),
                      (700, 5))

        super().draw(canvas)


class InfoWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)

    def connect_engine(self, engine):
        engine.subscribe(self)
        super().connect_engine(engine)

    def update(self, value):
        self.data.append(f"> {str(value)}")

    def draw(self, canvas):
        self.fill((0, 0, 0, 0))
        # self.fill(colors["wooden"])

        font = pygame.font.SysFont("comicsansms", 16, 5)
        for i, text in enumerate(reversed(self.data)):
            self.blit(font.render(text, True, colors["white"]),
                      (10, 500 + 18 * i))
        super().draw(canvas)


class HelpWindow(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.len = 30
        clear = []
        self.data = collections.deque(clear, maxlen=self.len)
        self.data.append([" →", "Move Right"])
        self.data.append([" ←", "Move Left"])
        self.data.append([" ↑ ", "Move Top"])
        self.data.append([" ↓ ", "Move Bottom"])
        self.data.append([" H ", "Show Help"])
        self.data.append(["Num+", "Zoom +"])
        self.data.append(["Num-", "Zoom -"])
        self.data.append([" M ", "Show Small Map"])
        self.data.append([" R ", "Restart Game"])

    def draw(self, canvas):
        alpha = 0
        if self.game_engine.show_help:
            alpha = 128
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 24)
        font2 = pygame.font.SysFont("serif", 24)
        if self.game_engine.show_help:
            pygame.draw.lines(self, (255, 0, 0, 255), True, [
                              (0, 0), (700, 0), (700, 500), (0, 500)], 5)
            for i, text in enumerate(self.data):
                self.blit(font1.render(text[0], True, ((128, 128, 255))),
                          (50, 50 + 30 * i))
                self.blit(font2.render(text[1], True, ((128, 128, 255))),
                          (150, 50 + 30 * i))

        super().draw(canvas)


class GameOver(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill(colors["wooden"])

    def draw(self, canvas):
        alpha = 10
        self.fill((0, 0, 0, alpha))
        font1 = pygame.font.SysFont("courier", 32, 20)

        if not self.game_engine.game_process:
            self.blit(font1.render(f'GAME OVER !', True, colors["white"]),
                      (300, 300))
        super().draw(canvas)


class SmallMap(ScreenHandle):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def draw_rect(self, coord, color):
        x, y = 635+(coord[0] * 4), 435+(coord[1] * 4)
        pygame.draw.rect(self, color, (x, y, 4, 4))

    def draw(self, canvas):
        self.fill((0, 0, 0, 0))
        if self.game_engine.show_small_map:
            if self.game_engine.map:
                if self.game_engine.map:
                    for i in range(len(self.game_engine.map)):
                        for j in range(len(self.game_engine.map[0])):
                            if self.game_engine.map[j][i] == Service.wall:
                                color = colors["gray"]
                            else:
                                color = colors["black"]
                            self.draw_rect((i, j), color)

            if self.game_engine.hero:
                self.draw_rect(self.game_engine.hero.position, colors["blue"])

            for obj in self.game_engine.objects:
                if obj.type == 'Enemy':
                    self.draw_rect(obj.position, colors["red"])
                else:
                    self.draw_rect(obj.position, colors["green"])

        super().draw(canvas)
