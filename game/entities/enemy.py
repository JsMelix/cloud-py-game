"""
Enemy Entity - Cloud challenge enemies with AI behavior
"""

import pygame
import random
import math
from typing import List, Optional, Dict
from ..engine.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class CloudEnemy:
    """Base class for cloud challenge enemies"""
    
    def __init__(self, x: float, y: float, enemy_type: str):
        # Position and movement
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.enemy_type = enemy_type
        
        # Combat stats
        self.max_health = 100
        self.health = self.max_health
        self.attack_damage = 20
        self.defense = 0
        
        # Movement and AI
        self.speed = 50  # pixels per second
        self.detection_range = 150
        self.attack_range = 40
        self.patrol_range = 100
        
        # State management
        self.state = "patrol"  # patrol, chase, attack, stunned
        self.target_player = None
        self.last_attack_time = 0
        self.attack_cooldown = 2.0  # seconds
        
        # Animation and rendering
        self.sprite_size = TILE_SIZE
        self.rect = pygame.Rect(x, y, self.sprite_size, self.sprite_size)
        self.facing_direction = "down"
        self.animation_timer = 0
        
        # Patrol behavior
        self.patrol_target_x = x
        self.patrol_target_y = y
        self.patrol_timer = 0
        
        # Cloud-specific properties
        self.weakness_concepts: List[str] = []  # Concepts that deal extra damage
        self.immune_concepts: List[str] = []    # Concepts that deal no damage
        
        # Set enemy-specific properties
        self._initialize_enemy_type()
    
    def _initialize_enemy_type(self):
        """Initialize enemy properties based on type"""
        if self.enemy_type == "latency_monster":
            self.max_health = 80
            self.health = self.max_health
            self.attack_damage = 15
            self.speed = 30
            self.weakness_concepts = ["vpc_networking", "lambda_serverless"]
            self.color = (200, 100, 100)
            
        elif self.enemy_type == "security_breach":
            self.max_health = 120
            self.health = self.max_health
            self.attack_damage = 25
            self.speed = 40
            self.weakness_concepts = ["iam_security"]
            self.immune_concepts = ["ec2_basics"]
            self.color = (150, 50, 200)
            
        elif self.enemy_type == "data_loss_demon":
            self.max_health = 100
            self.health = self.max_health
            self.attack_damage = 30
            self.speed = 35
            self.weakness_concepts = ["s3_storage"]
            self.color = (200, 150, 50)
            
        elif self.enemy_type == "cost_overrun":
            self.max_health = 150
            self.health = self.max_health
            self.attack_damage = 20
            self.speed = 25
            self.weakness_concepts = ["lambda_serverless", "ec2_basics"]
            self.color = (100, 200, 100)
            
        else:  # generic cloud bug
            self.max_health = 60
            self.health = self.max_health
            self.attack_damage = 10
            self.speed = 45
            self.color = (150, 150, 150)
    
    def update(self, dt: float, player_x: float, player_y: float):
        """Update enemy AI and behavior"""
        # Calculate distance to player
        distance_to_player = math.sqrt((player_x - self.x) ** 2 + (player_y - self.y) ** 2)
        
        # Update timers
        self.last_attack_time += dt
        self.patrol_timer += dt
        self.animation_timer += dt
        
        # State machine
        if self.state == "patrol":
            self._update_patrol(dt)
            
            # Check if player is in detection range
            if distance_to_player <= self.detection_range:
                self.state = "chase"
                
        elif self.state == "chase":
            self._update_chase(dt, player_x, player_y, distance_to_player)
            
            # Check if player is in attack range
            if distance_to_player <= self.attack_range:
                self.state = "attack"
            # Check if player escaped
            elif distance_to_player > self.detection_range * 1.5:
                self.state = "patrol"
                
        elif self.state == "attack":
            self._update_attack(dt, player_x, player_y, distance_to_player)
            
            # Check if player moved out of attack range
            if distance_to_player > self.attack_range:
                self.state = "chase"
        
        # Update rect position
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
    
    def _update_patrol(self, dt: float):
        """Update patrol behavior"""
        # Choose new patrol target periodically
        if self.patrol_timer >= 3.0:
            angle = random.uniform(0, 2 * math.pi)
            distance = random.uniform(20, self.patrol_range)
            self.patrol_target_x = self.start_x + math.cos(angle) * distance
            self.patrol_target_y = self.start_y + math.sin(angle) * distance
            self.patrol_timer = 0
        
        # Move towards patrol target
        self._move_towards(self.patrol_target_x, self.patrol_target_y, dt, self.speed * 0.5)
    
    def _update_chase(self, dt: float, player_x: float, player_y: float, distance: float):
        """Update chase behavior"""
        self._move_towards(player_x, player_y, dt, self.speed)
    
    def _update_attack(self, dt: float, player_x: float, player_y: float, distance: float):
        """Update attack behavior"""
        # Face the player but don't move
        if player_x > self.x:
            self.facing_direction = "right"
        elif player_x < self.x:
            self.facing_direction = "left"
        elif player_y > self.y:
            self.facing_direction = "down"
        else:
            self.facing_direction = "up"
    
    def _move_towards(self, target_x: float, target_y: float, dt: float, speed: float):
        """Move towards a target position"""
        dx = target_x - self.x
        dy = target_y - self.y
        distance = math.sqrt(dx * dx + dy * dy)
        
        if distance > 5:  # Don't move if very close
            # Normalize direction
            dx /= distance
            dy /= distance
            
            # Move
            self.x += dx * speed * dt
            self.y += dy * speed * dt
            
            # Update facing direction
            if abs(dx) > abs(dy):
                self.facing_direction = "right" if dx > 0 else "left"
            else:
                self.facing_direction = "down" if dy > 0 else "up"
    
    def can_attack(self) -> bool:
        """Check if enemy can attack (cooldown finished)"""
        return self.last_attack_time >= self.attack_cooldown
    
    def attack_player(self) -> int:
        """Perform attack and return damage dealt"""
        if self.can_attack():
            self.last_attack_time = 0
            return self.attack_damage
        return 0
    
    def take_damage(self, damage: int, concept_used: str = None) -> bool:
        """Take damage and return True if enemy died"""
        # Apply concept-based damage modifiers
        if concept_used:
            if concept_used in self.immune_concepts:
                damage = 0
                print(f"{self.enemy_type} is immune to {concept_used}!")
            elif concept_used in self.weakness_concepts:
                damage = int(damage * 1.5)
                print(f"{self.enemy_type} is weak to {concept_used}! Extra damage!")
        
        self.health = max(0, self.health - damage)
        
        # Brief stun when taking damage
        if damage > 0:
            self.state = "stunned"
            # Will return to previous state after a brief moment
        
        return self.health <= 0
    
    def is_alive(self) -> bool:
        """Check if enemy is still alive"""
        return self.health > 0
    
    def get_health_percentage(self) -> float:
        """Get health as percentage"""
        return (self.health / self.max_health) * 100
    
    def render(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render the enemy sprite"""
        # Calculate screen position
        screen_x = self.rect.x - camera_x
        screen_y = self.rect.y - camera_y
        
        # Only render if visible on screen
        if (screen_x + self.sprite_size > 0 and screen_x < SCREEN_WIDTH and
            screen_y + self.sprite_size > 0 and screen_y < SCREEN_HEIGHT):
            
            render_rect = pygame.Rect(screen_x, screen_y, self.sprite_size, self.sprite_size)
            
            # Enemy color based on state
            color = self.color
            if self.state == "attack":
                color = tuple(min(255, c + 50) for c in self.color)  # Brighter when attacking
            elif self.state == "stunned":
                color = tuple(max(0, c - 50) for c in self.color)   # Darker when stunned
            
            # Draw enemy body
            pygame.draw.rect(screen, color, render_rect)
            pygame.draw.rect(screen, (0, 0, 0), render_rect, 2)
            
            # Draw facing direction indicator
            center_x = render_rect.centerx
            center_y = render_rect.centery
            
            if self.facing_direction == "up":
                pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y - 8), 3)
            elif self.facing_direction == "down":
                pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y + 8), 3)
            elif self.facing_direction == "left":
                pygame.draw.circle(screen, (255, 0, 0), (center_x - 8, center_y), 3)
            elif self.facing_direction == "right":
                pygame.draw.circle(screen, (255, 0, 0), (center_x + 8, center_y), 3)
            
            # Draw health bar
            self._render_health_bar(screen, render_rect)
    
    def _render_health_bar(self, screen: pygame.Surface, render_rect: pygame.Rect):
        """Render enemy health bar"""
        if self.health < self.max_health:  # Only show when damaged
            bar_width = self.sprite_size
            bar_height = 6
            bar_x = render_rect.x
            bar_y = render_rect.y - 10
            
            # Background
            bg_rect = pygame.Rect(bar_x, bar_y, bar_width, bar_height)
            pygame.draw.rect(screen, (100, 0, 0), bg_rect)
            
            # Health
            health_percentage = self.health / self.max_health
            health_width = int(bar_width * health_percentage)
            if health_width > 0:
                health_rect = pygame.Rect(bar_x, bar_y, health_width, bar_height)
                pygame.draw.rect(screen, (0, 200, 0), health_rect)
            
            # Border
            pygame.draw.rect(screen, (255, 255, 255), bg_rect, 1)

class EnemyManager:
    """Manages all enemies in the current level"""
    
    def __init__(self):
        self.enemies: List[CloudEnemy] = []
        self.spawn_points: List[Dict] = []
        self.last_spawn_time = 0
        self.spawn_cooldown = 10.0  # seconds between spawns
    
    def add_spawn_point(self, x: float, y: float, enemy_types: List[str]):
        """Add an enemy spawn point"""
        self.spawn_points.append({
            'x': x,
            'y': y,
            'enemy_types': enemy_types,
            'last_spawn': 0
        })
    
    def spawn_enemy(self, x: float, y: float, enemy_type: str):
        """Spawn a specific enemy at coordinates"""
        enemy = CloudEnemy(x, y, enemy_type)
        self.enemies.append(enemy)
        return enemy
    
    def update(self, dt: float, player_x: float, player_y: float):
        """Update all enemies"""
        # Update existing enemies
        for enemy in self.enemies[:]:  # Copy list to allow removal during iteration
            if enemy.is_alive():
                enemy.update(dt, player_x, player_y)
            else:
                self.enemies.remove(enemy)
        
        # Handle spawning
        self.last_spawn_time += dt
        if self.last_spawn_time >= self.spawn_cooldown and len(self.enemies) < 5:  # Max 5 enemies
            self._try_spawn_enemy()
    
    def _try_spawn_enemy(self):
        """Try to spawn an enemy at a random spawn point"""
        if self.spawn_points:
            spawn_point = random.choice(self.spawn_points)
            enemy_type = random.choice(spawn_point['enemy_types'])
            
            self.spawn_enemy(spawn_point['x'], spawn_point['y'], enemy_type)
            self.last_spawn_time = 0
    
    def get_enemies_near_player(self, player_x: float, player_y: float, range_distance: float) -> List[CloudEnemy]:
        """Get enemies within range of player"""
        nearby_enemies = []
        for enemy in self.enemies:
            distance = math.sqrt((player_x - enemy.x) ** 2 + (player_y - enemy.y) ** 2)
            if distance <= range_distance:
                nearby_enemies.append(enemy)
        return nearby_enemies
    
    def check_player_collision(self, player_rect: pygame.Rect) -> Optional[CloudEnemy]:
        """Check if player collides with any enemy"""
        for enemy in self.enemies:
            if enemy.is_alive() and player_rect.colliderect(enemy.rect):
                return enemy
        return None
    
    def render(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render all enemies"""
        for enemy in self.enemies:
            if enemy.is_alive():
                enemy.render(screen, camera_x, camera_y)
    
    def clear_all_enemies(self):
        """Remove all enemies"""
        self.enemies.clear()