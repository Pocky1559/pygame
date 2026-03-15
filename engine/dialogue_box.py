"""Dialogue box UI component with word wrap and input handling."""

import pygame

from config import load_font


class DialogueBox:
    """Renders the dialogue UI and handles input for advancing text."""

    BOX_HEIGHT_RATIO = 0.25

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.rect = pygame.Rect(
            0,
            screen.get_height() - int(screen.get_height() * self.BOX_HEIGHT_RATIO),
            screen.get_width(),
            int(screen.get_height() * self.BOX_HEIGHT_RATIO),
        )

        self.font = load_font(28)
        self.name_font = load_font(24)

        self.speaker = ""
        self.text = ""
        self.lines: list[str] = []
        self.auto_mode = False

        # Button rects will be laid out based on the font size to adapt to different fonts.
        self.auto_button_rect = pygame.Rect(0, 0, 0, 0)
        self.log_button_rect = pygame.Rect(0, 0, 0, 0)

        self._prepare_surfaces()

    def _prepare_surfaces(self) -> None:
        self.background_surf = pygame.Surface(self.rect.size, pygame.SRCALPHA)
        self.background_surf.fill((10, 10, 20, 200))
        pygame.draw.rect(self.background_surf, (80, 160, 220, 200), self.background_surf.get_rect(), 2)

    def set_line(self, speaker: str, text: str) -> None:
        self.speaker = speaker
        self.text = text
        self._layout_buttons()

        # Ensure dialogue wraps before hitting the button region on the right.
        right_margin = max(self.auto_button_rect.width, self.log_button_rect.width) + 20
        max_text_width = self.rect.width - 40 - right_margin
        self.lines = self._wrap_text(text, self.font, max_text_width)

    def set_auto(self, enabled: bool) -> None:
        self.auto_mode = enabled

    def _wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list[str]:
        words = text.split(" ")
        lines: list[str] = []
        current = ""
        for word in words:
            test = current + (" " if current else "") + word
            if font.size(test)[0] <= max_width:
                current = test
            else:
                if current:
                    lines.append(current)
                current = word
        if current:
            lines.append(current)
        return lines

    def is_hovered(self, mouse_pos: tuple[int, int]) -> bool:
        return self.rect.collidepoint(mouse_pos)

    def handle_event(self, event: pygame.event.Event) -> None:
        # Reserved for future input needs
        pass

    def update(self, dt: float) -> None:
        # Keep UI layout updated (button positions, etc.)
        self._layout_buttons()

    def _layout_buttons(self) -> None:
        """Compute button rects based on font metrics so they fit any font."""
        padding_x = 16
        padding_y = 10

        auto_label = self.name_font.render("AUTO", True, (220, 220, 255))
        log_label = self.name_font.render("LOG", True, (220, 220, 255))

        auto_w = auto_label.get_width() + padding_x * 2
        auto_h = auto_label.get_height() + padding_y * 2
        log_w = log_label.get_width() + padding_x * 2
        log_h = log_label.get_height() + padding_y * 2

        # Position buttons in the top-right of the dialogue box, stacked vertically.
        self.auto_button_rect.size = (auto_w, auto_h)
        self.auto_button_rect.topleft = (self.rect.right - auto_w - 20, self.rect.top + 16)

        self.log_button_rect.size = (log_w, log_h)
        self.log_button_rect.topleft = (self.rect.right - log_w - 20, self.rect.top + 16 + auto_h + 12)

    def render(self) -> None:
        self.screen.blit(self.background_surf, self.rect.topleft)

        # Name plate
        if self.speaker:
            name_text = self.name_font.render(self.speaker, True, (230, 230, 255))
            plate_width = max(360, name_text.get_width() + 24)
            plate_rect = pygame.Rect(self.rect.left + 24, self.rect.top - 36, plate_width, 40)
            pygame.draw.rect(self.screen, (10, 10, 20, 220), plate_rect)
            pygame.draw.rect(self.screen, (80, 160, 220), plate_rect, 2)
            self.screen.blit(name_text, (plate_rect.left + 10, plate_rect.top + 8))

        # Dialogue text (top-aligned)
        text_y = self.rect.top + 20
        for line in self.lines:
            rendered = self.font.render(line, True, (240, 240, 255))
            self.screen.blit(rendered, (self.rect.left + 20, text_y))
            text_y += self.font.get_linesize() + 4

        # Buttons
        self._layout_buttons()
        self._render_button(self.auto_button_rect, "AUTO", self.auto_mode)
        self._render_button(self.log_button_rect, "LOG", False)

    def _render_button(self, rect: pygame.Rect, label: str, active: bool) -> None:
        color = (30, 40, 60)
        border = (120, 180, 255) if active else (80, 120, 160)
        pygame.draw.rect(self.screen, color, rect, border_radius=10)
        pygame.draw.rect(self.screen, border, rect, 2, border_radius=10)
        label_render = self.name_font.render(label, True, (220, 220, 255))
        label_pos = (rect.left + 12, rect.top + 6)
        self.screen.blit(label_render, label_pos)
