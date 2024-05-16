import logging

import pygame

from boid2 import Boid, Flock
from common_classes import Scene, GameObject, PhysicsMixin
from config import SIZE, logger

class Game:
    running = True
    screen = None
    clock = None
    current_scene = None

    def __init__(self, size: tuple[int, int] = (1920, 1080)):
        pygame.init()
        self.current_scene = Scene("Main Menu")
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Game")

    def handle_events(self):
        count = 0
        for event in pygame.event.get():
            count += 1
            if event.type == pygame.QUIT:
                self.running = False
            if event.type in (pygame.KEYDOWN, pygame.KEYUP):
                action = self.handle_input(event)
                logger.debug(f"Action: {action}")
                action()
        return count

    def run(self):
        self.clock = pygame.time.Clock()
        delta_time = 0
        start_time = pygame.time.get_ticks()
        last_time = start_time
        while self.running:

            nr_events = self.handle_events()
            #logger.debug(f"Handled {nr_events} events")
            self.update_simulation(delta_time, pygame.time.get_ticks() - start_time)
            self.render()

            pygame.display.flip()
            self.clock.tick(60)
            delta_time = (pygame.time.get_ticks() - last_time) / 1000
            last_time = pygame.time.get_ticks()

        pygame.quit()

    def update_simulation(self, dt, time):
        for obj in self.current_scene.objects:
            if not isinstance(obj, PhysicsMixin):
                continue
            obj.update(dt, time)
        pass

    def render(self):
        self.screen.fill((0, 0, 0))
        self.current_scene.render(self.screen)

    def handle_input(self, event) -> callable:
        if event.key == pygame.K_ESCAPE:
            return self.quit_game
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            return lambda: print("Left")
        return lambda: None

    def quit_game(self):
        self.running = False

    def load_scene(self, scene: Scene):
        self.current_scene = scene
        self.render()


if __name__ == '__main__':
    logger.addHandler(logging.FileHandler("log.txt", "w"))
    logger.debug("Starting game")
    game = Game(SIZE)
    scene = Scene("Game Scene")
    width, height = pygame.display.get_surface().get_size()
    flock = Flock()
    for i in range(4):
        #b = Boid((width // 2 + i*10, height // 2 + (i*15) % 25), 10*pygame.Vector2(0, -15), 10*pygame.Vector2(0, -5))
        b = Boid((width // 2 + i * 10, height // 2 + (i * 15) % 25), 50, pygame.Vector2(0, -1).rotate(i * 65))
        b.id = i + 1
        scene.add_object(b)
        flock.add_boid(b)
    game.load_scene(scene)
    game.run()
