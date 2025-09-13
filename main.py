#!/usr/bin/env python3
"""
Cloud Learning Game - Main Entry Point
A pixel art educational game teaching cloud computing concepts
"""

import pygame
import sys
from game.engine.game import Game

def main():
    """Main entry point for the Cloud Learning Game"""
    try:
        # Initialize the game
        game = Game()
        
        # Run the game loop
        game.run()
        
    except Exception as e:
        print(f"Error starting game: {e}")
        sys.exit(1)
    
    finally:
        pygame.quit()
        sys.exit(0)

if __name__ == "__main__":
    main()