import pygame
import logging

from scene import Scene, GameObject

logger = logging.getLogger("game")


class Game:
    running = True
    screen = None
    clock = None
    current_scene = None

    def __init__(self):
        pygame.init()
        self.current_scene = Scene("Main Menu")
        self.screen = pygame.display.set_mode((1920, 1080))
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

        while self.running:
            nr_events = self.handle_events()
            logger.debug(f"Handled {nr_events} events")
            self.update_simulation()
            self.render()

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

    def update_simulation(self):
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
    logger.setLevel(logging.DEBUG)
    game = Game()
    scene = Scene("Game Scene")
    width, height = pygame.display.get_surface().get_size()
    scene.add_object(GameObject(pygame.Vector2(width // 2, height // 2)))
    game.load_scene(scene)
    game.run()
