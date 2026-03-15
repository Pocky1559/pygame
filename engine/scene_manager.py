"""Manages scenes, dialogue progression, and global UI state."""

import json
import os
import pygame

from engine.background import BackgroundRenderer
from engine.character import CharacterManager
from engine.dialogue_box import DialogueBox
from engine.end_screen import EndScreen
from engine.log_overlay import LogOverlay
from engine.name_input import NameInputScreen

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "story.json")


class SceneManager:
    """Loads story data and advances through scenes and dialogue."""

    def __init__(self, screen: pygame.Surface) -> None:
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.background = BackgroundRenderer(screen)
        self.characters = CharacterManager(screen)
        self.dialogue_box = DialogueBox(screen)
        self.log_overlay = LogOverlay(screen)

        self.name_input = NameInputScreen(screen)
        self.player_name: str | None = None

        self.auto_mode = False
        self.auto_timer = 0.0
        self.auto_delay = 2.5  # seconds per line in auto mode

        self.story = self.load_story(DATA_PATH)
        self.current_scene_index = 0
        self.current_line_index = 0

        self.game_over = False
        self.end_screen = EndScreen(screen)

    def load_story(self, path: str) -> dict:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)

    @property
    def current_scene(self) -> dict:
        scenes = self.story.get("scenes", [])
        if self.current_scene_index < 0 or self.current_scene_index >= len(scenes):
            return {}
        return scenes[self.current_scene_index]

    def advance_line(self) -> None:
        """Advance to the next dialogue line or scene."""
        scene = self.current_scene
        if not scene:
            return

        dialogue = scene.get("dialogue", [])
        if self.current_line_index >= len(dialogue):
            # Move to next scene
            self.current_scene_index += 1
            self.current_line_index = 0
            if self.current_scene_index >= len(self.story.get("scenes", [])):
                # End of story
                self.game_over = True
                return
            scene = self.current_scene
            dialogue = scene.get("dialogue", [])
            self.load_scene(scene)
        elif self.current_line_index == 0:
            # First line in scene: load scene assets
            self.load_scene(scene)

        if not dialogue:
            return

        line = dialogue[self.current_line_index]

        # If the line defines characters explicitly, apply them.
        # Otherwise, retain current character state.
        if "characters" in line:
            self.characters.set_characters(line.get("characters", []))

        speaker = line.get("speaker", "")
        text = line.get("text", "")
        speaker = self._format_player_name(speaker)
        text = self._format_player_name(text)

        self.dialogue_box.set_line(speaker, text)
        self.log_overlay.add_entry(speaker, text)

        self.current_line_index += 1
        self.auto_timer = 0.0

    def _format_player_name(self, raw: str) -> str:
        if not self.player_name:
            return raw
        return raw.replace("{player}", self.player_name)

    def load_scene(self, scene: dict) -> None:
        """Load scene assets: background and characters."""
        bg_file = scene.get("background", "")
        self.background.set_background(bg_file)

        characters = scene.get("characters", [])
        self.characters.set_characters(characters)

    def handle_event(self, event: pygame.event.Event) -> None:
        # If the name input screen is active, let it handle events first.
        if not self.player_name:
            self.name_input.handle_event(event)
            if self.name_input.is_done():
                self.player_name = self.name_input.get_name()
                self.advance_line()
            return

        if self.game_over:
            self.end_screen.handle_event(event)
            return

        if self.log_overlay.active:
            self.log_overlay.handle_event(event)
            return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.log_overlay.open()
            elif event.key == pygame.K_SPACE:
                self.advance_line()
            elif event.key == pygame.K_l:
                self.log_overlay.open()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                # Prioritize UI buttons before advancing dialogue via click
                if self.dialogue_box.auto_button_rect.collidepoint(event.pos):
                    self.toggle_auto()
                elif self.dialogue_box.log_button_rect.collidepoint(event.pos):
                    self.log_overlay.open()
                elif self.dialogue_box.is_hovered(event.pos):
                    self.advance_line()

        self.dialogue_box.handle_event(event)

    def toggle_auto(self) -> None:
        self.auto_mode = not self.auto_mode
        self.dialogue_box.set_auto(self.auto_mode)

    def update(self, dt: float) -> None:
        if not self.player_name:
            self.name_input.update(dt)
            return

        if self.game_over:
            self.end_screen.update(dt)
            return

        if self.log_overlay.active:
            # Only update overlay when it's open
            self.log_overlay.update(dt)
            return

        self.dialogue_box.update(dt)
        self.characters.update(dt)

        if self.auto_mode:
            self.auto_timer += dt
            if self.auto_timer >= self.auto_delay:
                self.advance_line()

    def render(self) -> None:
        if not self.player_name:
            self.name_input.render()
            return

        if self.game_over:
            self.end_screen.render()
            return

        self.background.render()
        self.characters.render()
        self.dialogue_box.render()
        if self.log_overlay.active:
            self.log_overlay.render()
