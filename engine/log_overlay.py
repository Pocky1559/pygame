"""A scrollable log overlay for past dialogue."""

import pygame


class LogOverlay:
    """Displays a scrollable log of previous dialogue lines."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.active = False
        self.entries: list[tuple[str, str]] = []
        self.scroll_offset = 0
        self.font = pygame.font.Font(None, 26)
        self.background = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        self.background.fill((0, 0, 0, 220))

    def add_entry(self, speaker: str, text: str) -> None:
        self.entries.append((speaker, text))

    def open(self) -> None:
        self.active = True
        self.scroll_offset = 0

    def close(self) -> None:
        self.active = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.close()
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.scroll_offset = max(self.scroll_offset - 30, 0)
            elif event.key in (pygame.K_DOWN, pygame.K_s):
                self.scroll_offset += 30
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.close()
            elif event.button == 4:
                self.scroll_offset = max(self.scroll_offset - 30, 0)
            elif event.button == 5:
                self.scroll_offset += 30

    def update(self, dt: float) -> None:
        # Clamp scroll so it isn't too large
        max_offset = max(0, len(self.entries) * 30 - self.screen.get_height() + 80)
        self.scroll_offset = max(0, min(self.scroll_offset, max_offset))

    def render(self) -> None:
        self.screen.blit(self.background, (0, 0))
        y = 60 - self.scroll_offset
        for speaker, text in self.entries:
            prefix = f"{speaker}: " if speaker else ""
            line = prefix + text
            rendered = self.font.render(line, True, (220, 220, 255))
            self.screen.blit(rendered, (60, y))
            y += self.font.get_linesize() + 10
