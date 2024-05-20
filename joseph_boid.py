import pygame

from boid2 import Boid


class JosephBoid(Boid):
    speed = 150
    turn_speed = 480
    avoid_radius = 30

    def render(self, screen):
        sprite = pygame.image.load("assets/the_pack.png")
        sprite = pygame.transform.rotate(sprite, -self.heading +90)
        screen.blit(sprite, self.position - pygame.Vector2(16, 16))
