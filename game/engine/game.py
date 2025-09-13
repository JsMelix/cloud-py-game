"""
Core Game Engine - Main game loop and initialization
"""

import pygame
import sys
from typing import Optional
from .state_manager import StateManager
from .constants import *

class Game:
    """Main game class handling initialization and game loop"""
    
    def __init__(self):
        """Initialize the game engine"""
        # Initialize Pygame
        pygame.init()
        pygame.mixer.init()
        
        # Set up display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Cloud Learning Game")
        
        # Game timing
        self.clock = pygame.time.Clock()
        self.running = True
        self.dt = 0
        
        # Initialize state manager
        self.state_manager = StateManager(self.screen)
        
        print("Cloud Learning Game initialized successfully!")
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            else:
                # Pass events to current state
                self.state_manager.handle_event(event)
    
    def update(self):
        """Update game logic"""
        self.state_manager.update(self.dt)
    
    def render(self):
        """Render the current frame"""
        # Clear screen
        self.screen.fill(BLACK)
        
        # Render current state
        self.state_manager.render(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        print("Starting game loop...")
        
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(TARGET_FPS) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update game state
            if self.running:
                self.update()
                self.render()
        
        print("Game loop ended.")
    
    def quit(self):
        """Gracefully quit the game"""
        self.running = False