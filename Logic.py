import Service
import random
from time import time


class GameEngine:
    objects = []
    map = None
    hero = None
    level = -1
    working = True
    subscribers = set()
    score = 0.
    game_process = True
    show_help = False
    show_small_map = True
    _time = 0

    def subscribe(self, obj):
        self.subscribers.add(obj)

    def unsubscribe(self, obj):
        if obj in self.subscribers:
            self.subscribers.remove(obj)

    def notify(self, message):
        for i in self.subscribers:
            i.update(message)

    # HERO
    def add_hero(self, hero):
        self.hero = hero
        self.hero.stats['stealth'] = True
        self._time = time()

    def interact(self):
        if self._time + 5 <= time() and self.hero.stats['stealth']:
            self.notify("You are now visible to enemies")
            self.hero.stats['stealth'] = False

        for obj in self.objects:
            if obj.type == 'Enemy':
                self.enemy_move(obj)
            if list(map(int, obj.position)) == list(map(int, self.hero.position)) and not self.hero.stats["stealth"]:
                self.delete_object(obj)
                obj.interact(self, self.hero)

    # MOVEMENT
    def move_up(self):
        self.score -= 0.02
        if self.hero.position[1] % 1 == 0 and self.hero.position[0] % 1 == 0:
            if self.map[int(self.hero.position[1]) - 1][int(self.hero.position[0])] == Service.wall:
                return
            self.hero.position[1] -= 1
            self.interact()

    def move_down(self):
        self.score -= 0.02
        if self.hero.position[1] % 1 == 0 and self.hero.position[0] % 1 == 0:
            if self.map[int(self.hero.position[1]) + 1][int(self.hero.position[0])] == Service.wall:
                return
            self.hero.position[1] += 1
            self.interact()

    def move_left(self):
        self.score -= 0.02
        if self.hero.position[1] % 1 == 0 and self.hero.position[0] % 1 == 0:
            if self.map[int(self.hero.position[1])][int(self.hero.position[0]) - 1] == Service.wall:
                return
            self.hero.position[0] -= 0.5
            if self.hero.direction != 'left':
                self.hero.transform = True
            self.hero.direction = 'left'
            self.interact()

    def move_right(self):
        self.score -= 0.02
        if self.hero.position[1] % 1 == 0 and self.hero.position[0] % 1 == 0:
            if self.map[int(self.hero.position[1])][int(self.hero.position[0]) + 1] == Service.wall:
                return
            self.hero.position[0] += 0.5
            if self.hero.direction != 'right':
                self.hero.transform = True
            self.hero.direction = 'right'
            self.interact()

    # MAP
    def load_map(self, game_map):
        self.map = game_map

    # OBJECTS
    def add_object(self, obj):
        self.objects.append(obj)

    def add_objects(self, objects):
        self.objects.extend(objects)

    def delete_object(self, obj):
        self.objects.remove(obj)

    def enemy_move(self, enemy):
        # случайно меняем направление
            if enemy.position[1] % 1 == 0 and enemy.position[0] % 1 == 0:
                rand = random.randint(0, 1)
                if rand == 0:
                    enemy.direction = random.choice(['left', 'right', 'up', 'down'])

            if enemy.direction == 'up':
                if enemy.position[1] % 1 == 0 and enemy.position[0] % 1 == 0:
                    if self.map[int(enemy.position[1] - 1)][int(enemy.position[0])] == Service.wall:
                        return
                enemy.position[1] -= 0.5
            if enemy.direction == 'down':
                if enemy.position[1] % 1 == 0 and enemy.position[0] % 1 == 0:
                    if self.map[int(enemy.position[1]) + 1][int(enemy.position[0])] == Service.wall:
                        return
                enemy.position[1] += 0.5
            if enemy.direction == 'left':
                if enemy.position[1] % 1 == 0 and enemy.position[0] % 1 == 0:
                    if self.map[int(enemy.position[1])][int(enemy.position[0]) - 1] == Service.wall:
                        return
                enemy.position[0] -= 0.5
            if enemy.direction == 'right':
                if enemy.position[1] % 1 == 0 and enemy.position[0] % 1 == 0:
                    if self.map[int(enemy.position[1])][int(enemy.position[0]) + 1] == Service.wall:
                        return
                enemy.position[0] += 0.5




