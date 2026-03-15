"""Global configuration for the visual novel game."""

import os
import pygame

# Path to the user font file, relative to the project root.
# Update this to point at a custom font inside assets/fonts/.
FONT_PATH = "assets/fonts/GoogleSans.ttf"


def load_font(size: int) -> pygame.font.Font:
    """Load a font by size, falling back to the default font if missing."""
    # Resolve relative paths in case game is started from a different working dir.
    absolute_path = os.path.join(os.path.dirname(__file__), FONT_PATH)

    try:
        return pygame.font.Font(absolute_path, size)
    except FileNotFoundError:
        print(f"Warning: Font not found at {absolute_path}, using default font.")
        return pygame.font.SysFont(None, size)
    except Exception:
        print(f"Warning: Failed to load font at {absolute_path}, using default font.")
        return pygame.font.SysFont(None, size)
