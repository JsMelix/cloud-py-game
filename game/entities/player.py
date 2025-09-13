"""
Player Entity - Main character with movement and basic properties
"""

import pygame
from typing import List, Tuple
from ..engine.constants import PLAYER_SPEED, TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Vector2:
    """Simple 2D vector class for position and movement"""
    
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
    
    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)
    
    def __mul__(self, scalar: float):
        return Vector2(self.x * scalar, self.y * scalar)
    
    def normalize(self):
        """Return normalized vector"""
        length = (self.x ** 2 + self.y ** 2) ** 0.5
        if length == 0:
            return Vector2(0, 0)
        return Vector2(self.x / length, self.y / length)
    
    def to_tuple(self) -> Tuple[int, int]:
        """Convert to integer tuple for pygame"""
        return (int(self.x), int(self.y))

class Player:
    """Player character with movement, health, and learning progress"""
    
    def __init__(self, x: float = 100, y: float = 100):
        # Position and movement
        self.position = Vector2(x, y)
        self.velocity = Vector2(0, 0)
        self.speed = PLAYER_SPEED
        
        # Player stats
        self.health = 100
        self.max_health = 100
        self.experience = 0
        self.level = 1
        
        # Learning progress
        self.learned_concepts: List[str] = []
        self.current_abilities: List[str] = []
        
        # Advanced ability system
        self.ability_manager = None  # Will be set by gameplay state
        
        # Sprite and animation
        self.sprite_size = TILE_SIZE
        self.color = (0, 150, 255)  # Blue player color
        self.rect = pygame.Rect(self.position.x, self.position.y, self.sprite_size, self.sprite_size)
        
        # Animation state
        self.is_moving = False
        self.facing_direction = "down"
        self.animation_timer = 0
        self.animation_frame = 0
    
    def move(self, direction: Vector2, dt: float):
        """Move player in given direction with delta time"""
        if direction.x != 0 or direction.y != 0:
            # Normalize diagonal movement
            normalized_direction = direction.normalize()
            
            # Calculate new position
            movement = normalized_direction * (self.speed * dt)
            new_position = self.position + movement
            
            # Update position and rect
            self.position = new_position
            self.rect.x = int(self.position.x)
            self.rect.y = int(self.position.y)
            
            # Update animation state
            self.is_moving = True
            self._update_facing_direction(normalized_direction)
        else:
            self.is_moving = False
    
    def _update_facing_direction(self, direction: Vector2):
        """Update which direction the player is facing"""
        if abs(direction.x) > abs(direction.y):
            self.facing_direction = "right" if direction.x > 0 else "left"
        else:
            self.facing_direction = "down" if direction.y > 0 else "up"
    
    def check_boundaries(self, level_width: int = None, level_height: int = None):
        """Keep player within level boundaries"""
        if level_width is None:
            level_width = SCREEN_WIDTH
        if level_height is None:
            level_height = SCREEN_HEIGHT
        
        # Convert level size from tiles to pixels
        max_x = level_width * TILE_SIZE
        max_y = level_height * TILE_SIZE
        
        if self.rect.left < 0:
            self.rect.left = 0
            self.position.x = self.rect.x
        elif self.rect.right > max_x:
            self.rect.right = max_x
            self.position.x = self.rect.x
        
        if self.rect.top < 0:
            self.rect.top = 0
            self.position.y = self.rect.y
        elif self.rect.bottom > max_y:
            self.rect.bottom = max_y
            self.position.y = self.rect.y
    
    def check_collision(self, obstacles: List[pygame.Rect]) -> bool:
        """Check collision with solid objects"""
        for obstacle in obstacles:
            if self.rect.colliderect(obstacle):
                return True
        return False
    
    def handle_collision(self, obstacles: List[pygame.Rect], previous_position: Vector2):
        """Handle collision by reverting to previous position"""
        if self.check_collision(obstacles):
            self.position = previous_position
            self.rect.x = int(self.position.x)
            self.rect.y = int(self.position.y)
    
    def take_damage(self, amount: int):
        """Take damage and update health"""
        self.health = max(0, self.health - amount)
        return self.health <= 0  # Return True if player died
    
    def heal(self, amount: int):
        """Heal player"""
        self.health = min(self.max_health, self.health + amount)
    
    def gain_experience(self, amount: int):
        """Gain experience points"""
        self.experience += amount
        # Simple leveling system
        required_exp = self.level * 100
        if self.experience >= required_exp:
            self.level += 1
            self.experience -= required_exp
            self.max_health += 10
            self.health = self.max_health  # Full heal on level up
    
    def learn_concept(self, concept: str):
        """Learn a new cloud concept"""
        if concept not in self.learned_concepts:
            self.learned_concepts.append(concept)
            print(f"Learned new concept: {concept}")
    
    def update(self, dt: float):
        """Update player animation and state"""
        if self.is_moving:
            self.animation_timer += dt
            if self.animation_timer >= 0.2:  # Animation frame every 0.2 seconds
                self.animation_frame = (self.animation_frame + 1) % 4
                self.animation_timer = 0
        else:
            self.animation_frame = 0
    
    def render(self, screen: pygame.Surface):
        """Render the player sprite"""
        # Simple colored rectangle for now (will be replaced with pixel art)
        color = self.color
        
        # Slightly different color when moving for animation feedback
        if self.is_moving:
            color = (min(255, self.color[0] + 20), 
                    min(255, self.color[1] + 20), 
                    min(255, self.color[2] + 20))
        
        pygame.draw.rect(screen, color, self.rect)
        
        # Draw a simple direction indicator
        center_x = self.rect.centerx
        center_y = self.rect.centery
        
        if self.facing_direction == "up":
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y - 8), 3)
        elif self.facing_direction == "down":
            pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y + 8), 3)
        elif self.facing_direction == "left":
            pygame.draw.circle(screen, (255, 255, 255), (center_x - 8, center_y), 3)
        elif self.facing_direction == "right":
            pygame.draw.circle(screen, (255, 255, 255), (center_x + 8, center_y), 3)