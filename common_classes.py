from typing import List

import pygame
from pygame import draw


class Scene:
    def __init__(self, name, position: pygame.Vector2 = None):
        self.name = name
        self.position = position or pygame.Vector2(0, 0)
        self.objects: List[GameObject] = []

    def render(self, screen: pygame.Surface):
        for obj in self.objects:
            obj.render(screen)

    def add_object(self, game_object: 'GameObject'):
        self.objects.append(game_object)


class GameObject:
    id: int

    def __init__(self, position: pygame.Vector2 | tuple = None):
        if isinstance(position, tuple):
            position = pygame.Vector2(position)
        self.position = position or pygame.Vector2(0, 0)

    def render(self, screen: pygame.Surface):
        draw.rect(screen, (255, 255, 255), (self.position.x - 5, self.position.y - 5, 10, 10))


class PhysicsMixin:
    velocity: pygame.Vector2 | tuple[int, int]

    def update(self, dt, time):
        ...
