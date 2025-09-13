"""
Input Handler - Processes keyboard input for player movement and actions
"""

import pygame
from typing import Dict, List
from .constants import MOVEMENT_KEYS
from ..entities.player import Vector2

class InputHandler:
    """Handles keyboard input and converts to game actions"""
    
    def __init__(self):
        self.keys_pressed: Dict[int, bool] = {}
        self.keys_just_pressed: Dict[int, bool] = {}
        self.keys_just_released: Dict[int, bool] = {}
    
    def update(self):
        """Update input state - call once per frame"""
        # Get current key states
        current_keys = pygame.key.get_pressed()
        
        # Update just pressed/released states
        self.keys_just_pressed.clear()
        self.keys_just_released.clear()
        
        for key in range(len(current_keys)):
            was_pressed = self.keys_pressed.get(key, False)
            is_pressed = current_keys[key]
            
            if is_pressed and not was_pressed:
                self.keys_just_pressed[key] = True
            elif not is_pressed and was_pressed:
                self.keys_just_released[key] = True
            
            self.keys_pressed[key] = is_pressed
    
    def is_key_pressed(self, key: int) -> bool:
        """Check if key is currently pressed"""
        return self.keys_pressed.get(key, False)
    
    def is_key_just_pressed(self, key: int) -> bool:
        """Check if key was just pressed this frame"""
        return self.keys_just_pressed.get(key, False)
    
    def is_key_just_released(self, key: int) -> bool:
        """Check if key was just released this frame"""
        return self.keys_just_released.get(key, False)
    
    def get_movement_input(self) -> Vector2:
        """Get movement direction based on input"""
        direction = Vector2(0, 0)
        
        # Check each movement direction
        for move_dir, keys in MOVEMENT_KEYS.items():
            for key in keys:
                if self.is_key_pressed(key):
                    if move_dir == 'up':
                        direction.y -= 1
                    elif move_dir == 'down':
                        direction.y += 1
                    elif move_dir == 'left':
                        direction.x -= 1
                    elif move_dir == 'right':
                        direction.x += 1
                    break  # Only need one key per direction
        
        return direction
    
    def handle_event(self, event: pygame.event.Event):
        """Handle pygame events for immediate responses"""
        # This method can be used for events that need immediate response
        # rather than continuous checking (like menu selections)
        pass