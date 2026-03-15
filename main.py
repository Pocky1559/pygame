"""Entry point for the space-themed visual novel.

This file initializes Pygame, creates the main window, and runs the game loop.
"""

import pygame
from engine.scene_manager import SceneManager

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60


def main() -> None:
    pygame.init()
    pygame.display.set_caption("Space Visual Novel")
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    clock = pygame.time.Clock()

    scene_manager = SceneManager(screen)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                scene_manager.handle_event(event)

        scene_manager.update(dt)
        scene_manager.render()
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
