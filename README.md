# Cloud Learning Game

A pixel art educational video game that teaches cloud computing concepts through interactive gameplay.

## Features

- **Enhanced Interactive Learning**: Multi-phase educational system with detailed content, interactive demos, quizzes, and practical exercises
- **Comprehensive Cloud Education**: Learn EC2, Lambda, S3, VPC, and IAM with real-world scenarios and hands-on practice
- **Engaging Combat System**: Use cloud knowledge as combat abilities with strategic depth
- **Rich Visual Experience**: Pixel art graphics with particle effects, screen shake, and visual feedback
- **Progress Tracking**: Detailed statistics, achievements, and performance analytics
- **Adaptive Learning**: Personalized experience based on quiz performance and practical completion

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

**Movement & Basic Actions:**
- **WASD** or **Arrow Keys**: Move character
- **E**: Interact with learning stations
- **Space**: Start game (from menu)
- **Escape**: Return to menu / Exit learning

**Enhanced Learning Interface:**
- **Space/→**: Next page/phase in learning
- **←**: Previous page/phase  
- **↑↓**: Select options in quizzes/exercises
- **Enter**: Confirm selection
- **Escape**: Exit learning session

**HUD Controls:**
- **TAB**: Toggle stats panel
- **M**: Toggle minimap

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