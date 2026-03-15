"""Name input screen shown at game start."""

import pygame

from config import load_font


class NameInputScreen:
    """Handles player name entry before the story begins."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.font = load_font(40)
        self.prompt_font = load_font(36)
        self.error_font = load_font(24)

        self.input_text = ""
        self.error_text = ""
        self.confirmed_name: str | None = None

        self.box_rect = pygame.Rect(240, 320, 800, 60)
        self.confirm_rect = pygame.Rect(0, 0, 0, 0)

        self._layout()

    def _layout(self) -> None:
        """Layout UI elements to work well with the loaded font size."""
        # Confirm button size depends on the font metrics
        confirm_surf = self.font.render("Confirm", True, (220, 220, 255))
        padding_x = 24
        padding_y = 16
        width = confirm_surf.get_width() + padding_x * 2
        height = confirm_surf.get_height() + padding_y

        self.confirm_rect.size = (width, height)
        self.confirm_rect.topleft = (
            self.box_rect.centerx - width // 2,
            self.box_rect.bottom + 16,
        )

    def handle_event(self, event: pygame.event.Event) -> None:
        # Ensure layout is up-to-date in case fonts changed or screen resized
        self._layout()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.input_text = self.input_text[:-1]
            elif event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                self._try_confirm()
            else:
                if event.unicode.isprintable() and len(self.input_text) < 24:
                    self.input_text += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.confirm_rect.collidepoint(event.pos):
                self._try_confirm()

    def _try_confirm(self) -> None:
        name = self.input_text.strip()
        if not name:
            self.error_text = "Please enter a name before continuing."
            return
        self.error_text = ""
        self.confirmed_name = name

    def update(self, dt: float) -> None:
        # Ensure button layout adapts when fonts or resolution may change.
        self._layout()

    def is_done(self) -> bool:
        return self.confirmed_name is not None

    def get_name(self) -> str:
        return self.confirmed_name or ""

    def render(self) -> None:
        # Background
        self.screen.fill((10, 10, 20))

        # Prompt
        prompt = "Enter your name to begin your mission:" 
        prompt_surf = self.prompt_font.render(prompt, True, (220, 220, 255))
        self.screen.blit(prompt_surf, (self.box_rect.left, self.box_rect.top - 60))

        # Input box
        pygame.draw.rect(self.screen, (20, 30, 50), self.box_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 180, 230), self.box_rect, 2, border_radius=12)

        input_display = self.input_text or "..."
        input_surf = self.font.render(input_display, True, (240, 240, 255))
        self.screen.blit(input_surf, (self.box_rect.left + 14, self.box_rect.top + 12))

        # Confirm button
        pygame.draw.rect(self.screen, (30, 40, 60), self.confirm_rect, border_radius=12)
        pygame.draw.rect(self.screen, (80, 180, 230), self.confirm_rect, 2, border_radius=12)
        confirm_surf = self.font.render("Confirm", True, (220, 220, 255))
        confirm_pos = (
            self.confirm_rect.left + (self.confirm_rect.width - confirm_surf.get_width()) // 2,
            self.confirm_rect.top + (self.confirm_rect.height - confirm_surf.get_height()) // 2,
        )
        self.screen.blit(confirm_surf, confirm_pos)

        # Error
        if self.error_text:
            err_surf = self.error_font.render(self.error_text, True, (240, 120, 120))
            self.screen.blit(err_surf, (self.box_rect.left, self.box_rect.bottom + 14))
