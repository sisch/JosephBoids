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
    def __init__(self, position: pygame.Vector2 = None):
        self.position = position or pygame.Vector2(0, 0)

    def render(self, screen: pygame.Surface):
        draw.rect(screen, (255, 255, 255), (self.position.x, self.position.y, 10, 10))
