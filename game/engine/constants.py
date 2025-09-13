"""
Game Constants and Configuration
"""

# Import pygame for key constants
import pygame

# Display settings
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
TARGET_FPS = 60

# Colors (RGB)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 200)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
GRAY = (128, 128, 128)

# Tile and sprite settings
TILE_SIZE = 32
PLAYER_SPEED = 200  # pixels per second

# Game states
class GameState:
    MENU = "menu"
    GAMEPLAY = "gameplay"
    COMBAT = "combat"
    LEARNING = "learning"
    PAUSE = "pause"

# Input keys
MOVEMENT_KEYS = {
    'up': [pygame.K_w, pygame.K_UP],
    'down': [pygame.K_s, pygame.K_DOWN],
    'left': [pygame.K_a, pygame.K_LEFT],
    'right': [pygame.K_d, pygame.K_RIGHT]
}