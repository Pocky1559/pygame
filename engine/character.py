"""Character display system for a visual novel."""

import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import pygame

ASSETS_DIR = os.path.join(os.path.dirname(__file__), "..", "assets")
CHAR_DIR = os.path.join(ASSETS_DIR, "characters")

POSITIONS = {
    "left": 220,
    "center": 640,
    "right": 1060,
}


@dataclass
class CharacterData:
    name: str
    position: str
    expression: Optional[str]


class CharacterSprite:
    """Represents a rendered character sprite with position and optional fade transition."""

    def __init__(self, data: CharacterData, screen: pygame.Surface):
        self.screen = screen
        self.data = data
        self.image = self._load_image() or self._placeholder_surface()
        self.rect = self.image.get_rect()
        self.rect.midbottom = (POSITIONS.get(data.position, 640), screen.get_height() - 40)
        self.alpha = 255
        self.image.set_alpha(self.alpha)

    def _load_image(self) -> Optional[pygame.Surface]:
        if not self.data.name:
            return None

        filename = self.data.name
        if self.data.expression:
            filename = f"{filename}_{self.data.expression}"
        filename = f"{filename}.png"

        path = os.path.join(CHAR_DIR, filename)
        if not os.path.isfile(path):
            self._create_placeholder(path)

        try:
            img = pygame.image.load(path).convert_alpha()
            scale = 0.6
            size = (int(img.get_width() * scale), int(img.get_height() * scale))
            return pygame.transform.smoothscale(img, size)
        except Exception:
            return None

    def _placeholder_surface(self) -> pygame.Surface:
        surf = pygame.Surface((400, 600), pygame.SRCALPHA)
        surf.fill((0, 0, 0, 0))
        pygame.draw.rect(surf, (60, 120, 180), surf.get_rect(), border_radius=16)
        pygame.draw.rect(surf, (180, 220, 255), surf.get_rect(), 4, border_radius=16)
        font = pygame.font.Font(None, 32)
        text = font.render(self.data.name or "?", True, (230, 230, 255))
        surf.blit(text, (20, 20))
        return surf

    def _create_placeholder(self, path: str) -> None:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        surf = self._placeholder_surface()
        pygame.image.save(surf, path)

    def render(self) -> None:
        self.screen.blit(self.image, self.rect)


class CharacterManager:
    """Manages character sprites and transitions."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.sprites: Dict[str, CharacterSprite] = {}

    def set_characters(self, data: List[dict]) -> None:
        """Set current characters for the scene."""
        next_sprites: Dict[str, CharacterSprite] = {}
        for char in data:
            name = char.get("name", "")
            pos = char.get("position", "center")
            expr = char.get("expression")
            key = pos
            next_sprites[key] = CharacterSprite(CharacterData(name, pos, expr), self.screen)

        self.sprites = next_sprites

    def update(self, dt: float) -> None:
        # Place for future transitions
        pass

    def render(self) -> None:
        for sprite in self.sprites.values():
            sprite.render()
