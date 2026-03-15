"""Background renderer for the visual novel."""

import os
import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
BACKGROUND_DIR = os.path.join(ASSETS_DIR, "backgrounds")


class BackgroundRenderer:
    """Draws a full-screen background image."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.image = None
        self.rect = self.screen.get_rect()

    def set_background(self, filename: str) -> None:
        if not filename:
            self.image = None
            return

        path = os.path.join(BACKGROUND_DIR, filename)
        if not os.path.isfile(path):
            self._create_placeholder(path)

        try:
            img = pygame.image.load(path).convert()
            self.image = pygame.transform.scale(img, self.rect.size)
        except Exception:
            self.image = None

    def render(self) -> None:
        if self.image:
            self.screen.blit(self.image, (0, 0))
        else:
            self.screen.fill((10, 10, 20))

    def _create_placeholder(self, path: str) -> None:
        """Create a placeholder background image when none exists."""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        surface = pygame.Surface((1280, 720))
        surface.fill((15, 15, 40))
        pygame.draw.circle(surface, (60, 100, 170), (640, 360), 260, 8)
        pygame.draw.rect(surface, (30, 30, 60), pygame.Rect(0, 0, 1280, 720), 6)
        pygame.image.save(surface, path)
