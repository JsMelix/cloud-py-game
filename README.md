# Cloud Learning Game

A pixel art educational video game that teaches cloud computing concepts through interactive gameplay.

## Features

- Learn cloud computing concepts through engaging gameplay
- Pixel art graphics and retro-style presentation
- Combat system using cloud knowledge as abilities
- Progressive difficulty with themed levels
- Achievement and progress tracking system

## Installation

1. Install Python 3.8 or higher
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

## Running the Game

```
python main.py
```

## Controls

- **WASD** or **Arrow Keys**: Move character
- **Space**: Start game (from menu)
- **Escape**: Return to menu

## Game Structure

- **Compute Valley**: Learn about EC2, Lambda, and serverless computing
- **Storage Caverns**: Explore S3, EBS, and database services
- **Network Nexus**: Master VPC, load balancers, and CDN concepts
- **Security Citadel**: Understand IAM, encryption, and compliance
- **DevOps Domain**: Practice CI/CD and infrastructure as code

## Development

The game is built with Python and Pygame, following a modular architecture:

- `game/engine/`: Core game engine and state management
- `game/entities/`: Player, enemies, and game objects
- `game/systems/`: Combat, learning, and progression systems
- `game/levels/`: Level definitions and management
- `game/ui/`: User interface components
- `assets/`: Graphics, sounds, and game data
- `tests/`: Unit and integration tests