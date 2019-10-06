from abc import ABC, abstractmethod
import pygame
import random


def create_sprite(img, sprite_size):
    icon = pygame.image.load(img).convert_alpha()
    icon = pygame.transform.scale(icon, (sprite_size, sprite_size))
    sprite = pygame.Surface((sprite_size, sprite_size), pygame.HWSURFACE)
    sprite.blit(icon, (0, 0))
    return sprite


# FIXME
# add classes
class AbstractObject(ABC):
    def __init__(self):
        self.position = None
        self.type = None

    def draw(self, display):

        if self.transform == True:
            self.sprite = pygame.transform.flip(self.sprite, 1, 0)
            self.sprite2 = pygame.transform.flip(self.sprite2, 1, 0)
            self.transform = False

        display.draw_object(self.sprite, self.position)

        if display.game_engine.hero.direction == 'right':
            if self.position[0] % 1 != 0:
                display.draw_object(self.sprite2, self.position)
                self.position[0] += 0.25

        if display.game_engine.hero.direction == 'left':
            if self.position[0] % 1 != 0:
                display.draw_object(self.sprite2, self.position)
                self.position[0] -= 0.25


class Interactive(ABC):

    @abstractmethod
    def interact(self, engine, hero):
        pass


class Ally(AbstractObject, Interactive):

    def __init__(self, icon, action, position):
        self.sprite = icon
        self.action = action
        self.position = position
        self.type = 'Ally'

    def interact(self, engine, hero):
        self.action(engine, hero)




class Creature(AbstractObject):

    def __init__(self, icon, stats, position):
        self.sprite = icon
        self.sprite2 = None
        self.transform = False
        self.stats = stats
        self.position = position
        self.direction = 'right'
        self.calc_max_HP()
        self.hp = self.max_hp

    def calc_max_HP(self):
        self.max_hp = 5 + self.stats["endurance"] * 2
        if self.hp > self.max_hp:
            self.hp = self.max_hp



        # FIXME class Enemy
class Enemy(Creature, Interactive):
    def __init__(self, icon, stats, xp, position):
        self.sprite = icon
        self.sprite2 = [pygame.transform.flip(self.sprite[0], 1, 0)]
        self.stats = stats
        self.xp = xp
        self.position = position
        self.type = 'Enemy'
        self.direction = random.choice(['left', 'right', 'up', 'down'])

    def interact(self, engine, hero):
        self.action(engine, hero)
        for msg in hero.level_up():
            engine.notify(msg)

    def action(self, engine, hero):
        hero.hp -= self.stats['strength']
        hero.exp += self.stats['strength']
        if hero.hp <= 0:
            hero.hp = 0
            engine.game_process = False
        engine.notify("you were attacked by the enemy")


class Hero(Creature):

    def __init__(self, stats, icon):
        pos = [1, 1]
        self.level = 1
        self.exp = 0
        self.gold = 0
        self.type = 'Hero'
        self.hp = 0

        super().__init__(icon, stats, pos)

    def level_up(self):
        while self.exp >= 100 * (2 ** (self.level - 1)):
            yield "level up!"
            self.level += 1
            self.stats["strength"] += 2
            self.stats["endurance"] += 2
            self.calc_max_HP()
            self.hp = self.max_hp


class Effect(Hero):

    def __init__(self, base):
        self.base = base
        self.stats = self.base.stats.copy()
        self.apply_effect()

    @property
    def position(self):
        return self.base.position

    @position.setter
    def position(self, value):
        self.base.position = value

    @property
    def level(self):
        return self.base.level

    @level.setter
    def level(self, value):
        self.base.level = value

    @property
    def gold(self):
        return self.base.gold

    @gold.setter
    def gold(self, value):
        self.base.gold = value

    @property
    def hp(self):
        return self.base.hp

    @hp.setter
    def hp(self, value):
        self.base.hp = value

    @property
    def max_hp(self):
        return self.base.max_hp

    @max_hp.setter
    def max_hp(self, value):
        self.base.max_hp = value

    @property
    def exp(self):
        return self.base.exp

    @exp.setter
    def exp(self, value):
        self.base.exp = value

    @property
    def sprite(self):
        return self.base.sprite

    @sprite.setter
    def sprite(self, value):
        self.base.sprite = value

    @property
    def sprite2(self):
        return self.base.sprite2

    @sprite2.setter
    def sprite2(self, value):
        self.base.sprite2 = value

    @property
    def transform(self):
        return self.base.transform

    @transform.setter
    def transform(self, value):
        self.base.transform = value

    @property
    def direction(self):
        return self.base.direction

    @direction.setter
    def direction(self, value):
        self.base.direction = value

    @abstractmethod
    def apply_effect(self):
        pass


class Berserk(Effect):
    def apply_effect(self):
        self.max_hp += 20
        self.hp += 20


class Blessing(Effect):
    def apply_effect(self):
        self.stats["strength"] += 4
        self.stats["luck"] += 4
        self.stats["endurance"] += 4


class Weakness(Effect):
    def apply_effect(self):
        self.stats["strength"] -= 5
        self.stats["endurance"] -= 5


class Stealth(Effect):
    def apply_effect(self):
        self.stats.stealth = True
