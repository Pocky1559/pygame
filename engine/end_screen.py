"""End screen shown after the story ends."""

import pygame

from config import load_font


class EndScreen:
    """Displays a thank-you message and a Quit button."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.title_font = load_font(48)
        self.button_font = load_font(28)

        self.button_rect = pygame.Rect(0, 0, 0, 0)
        self._layout_buttons()

        self.request_quit = False

    def _layout_buttons(self) -> None:
        label = self.button_font.render("Quit", True, (220, 220, 255))
        padding_x = 28
        padding_y = 16
        width = label.get_width() + padding_x * 2
        height = label.get_height() + padding_y
        self.button_rect.size = (width, height)
        self.button_rect.center = (self.screen.get_width() // 2, self.screen.get_height() // 2 + 120)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.request_quit = True

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.button_rect.collidepoint(event.pos):
                self.request_quit = True

    def update(self, dt: float) -> None:
        # Support dynamic layout on resize
        self._layout_buttons()

    def render(self) -> None:
        self.screen.fill((8, 8, 16))

        title = "Thank you for playing"
        title_surf = self.title_font.render(title, True, (240, 240, 255))
        title_pos = title_surf.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2 - 80))
        self.screen.blit(title_surf, title_pos)

        # Quit button
        pygame.draw.rect(self.screen, (30, 40, 60), self.button_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 180, 230), self.button_rect, 2, border_radius=12)
        label = self.button_font.render("Quit", True, (220, 220, 255))
        label_pos = label.get_rect(center=self.button_rect.center)
        self.screen.blit(label, label_pos)
