"""
Level System - Handles level data, tilemaps, and environment rendering
"""

import pygame
from typing import List, Dict, Tuple, Optional
from ..engine.constants import TILE_SIZE, SCREEN_WIDTH, SCREEN_HEIGHT

class Tile:
    """Represents a single tile in the level"""
    
    def __init__(self, tile_type: str, x: int, y: int, solid: bool = False):
        self.tile_type = tile_type
        self.x = x
        self.y = y
        self.solid = solid
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        
        # Tile colors for different types (will be replaced with sprites later)
        self.colors = {
            'grass': (34, 139, 34),
            'stone': (105, 105, 105),
            'water': (0, 100, 200),
            'wall': (139, 69, 19),
            'cloud_compute': (135, 206, 250),
            'cloud_storage': (255, 165, 0),
            'cloud_network': (50, 205, 50),
            'cloud_security': (255, 69, 0),
            'cloud_devops': (138, 43, 226),
            'learning_station': (255, 215, 0),
            'enemy_spawn': (220, 20, 60)
        }
    
    def get_color(self) -> Tuple[int, int, int]:
        """Get the color for this tile type"""
        return self.colors.get(self.tile_type, (128, 128, 128))
    
    def render(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Render the tile with camera offset"""
        render_rect = pygame.Rect(
            self.rect.x - camera_x,
            self.rect.y - camera_y,
            TILE_SIZE,
            TILE_SIZE
        )
        
        # Only render if visible on screen
        if (render_rect.right > 0 and render_rect.left < SCREEN_WIDTH and
            render_rect.bottom > 0 and render_rect.top < SCREEN_HEIGHT):
            
            pygame.draw.rect(screen, self.get_color(), render_rect)
            
            # Draw border for solid tiles
            if self.solid:
                pygame.draw.rect(screen, (0, 0, 0), render_rect, 2)

class Level:
    """Represents a game level with tilemap and entities"""
    
    def __init__(self, level_id: str, name: str, width: int, height: int):
        self.level_id = level_id
        self.name = name
        self.width = width
        self.height = height
        
        # Level data
        self.tiles: List[List[Optional[Tile]]] = []
        self.solid_tiles: List[pygame.Rect] = []
        self.learning_stations: List[Dict] = []
        self.enemy_spawns: List[Tuple[int, int]] = []
        
        # Level theme and background
        self.theme = "compute"  # compute, storage, network, security, devops
        self.background_color = (20, 30, 40)
        
        # Initialize empty tilemap
        self._initialize_tilemap()
    
    def _initialize_tilemap(self):
        """Initialize empty tilemap"""
        self.tiles = [[None for _ in range(self.width)] for _ in range(self.height)]
    
    def set_tile(self, x: int, y: int, tile_type: str, solid: bool = False):
        """Set a tile at the given coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            tile = Tile(tile_type, x, y, solid)
            self.tiles[y][x] = tile
            
            # Add to solid tiles list if solid
            if solid:
                self.solid_tiles.append(tile.rect)
            
            # Handle special tile types
            if tile_type == 'learning_station':
                self.learning_stations.append({
                    'x': x * TILE_SIZE,
                    'y': y * TILE_SIZE,
                    'concept': 'EC2 Basics',  # Will be customized per station
                    'activated': False
                })
            elif tile_type == 'enemy_spawn':
                self.enemy_spawns.append((x * TILE_SIZE, y * TILE_SIZE))
    
    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        """Get tile at coordinates"""
        if 0 <= x < self.width and 0 <= y < self.height:
            return self.tiles[y][x]
        return None
    
    def get_solid_rects(self) -> List[pygame.Rect]:
        """Get all solid collision rectangles"""
        return self.solid_tiles.copy()
    
    def render(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Render the level with camera offset"""
        # Clear background
        screen.fill(self.background_color)
        
        # Calculate visible tile range
        start_x = max(0, camera_x // TILE_SIZE - 1)
        end_x = min(self.width, (camera_x + SCREEN_WIDTH) // TILE_SIZE + 2)
        start_y = max(0, camera_y // TILE_SIZE - 1)
        end_y = min(self.height, (camera_y + SCREEN_HEIGHT) // TILE_SIZE + 2)
        
        # Render visible tiles
        for y in range(start_y, end_y):
            for x in range(start_x, end_x):
                tile = self.tiles[y][x]
                if tile:
                    tile.render(screen, camera_x, camera_y)
        
        # Render learning stations
        self._render_learning_stations(screen, camera_x, camera_y)
    
    def _render_learning_stations(self, screen: pygame.Surface, camera_x: int, camera_y: int):
        """Render learning stations with special effects"""
        for station in self.learning_stations:
            station_rect = pygame.Rect(
                station['x'] - camera_x,
                station['y'] - camera_y,
                TILE_SIZE,
                TILE_SIZE
            )
            
            # Only render if visible
            if (station_rect.right > 0 and station_rect.left < SCREEN_WIDTH and
                station_rect.bottom > 0 and station_rect.top < SCREEN_HEIGHT):
                
                # Animated glow effect
                import math
                import time
                glow_intensity = int(128 + 127 * math.sin(time.time() * 3))
                glow_color = (255, glow_intensity, 0)
                
                # Draw glowing learning station
                pygame.draw.rect(screen, glow_color, station_rect)
                pygame.draw.rect(screen, (255, 255, 255), station_rect, 3)

class Camera:
    """Camera system for following the player"""
    
    def __init__(self):
        self.x = 0
        self.y = 0
        self.target_x = 0
        self.target_y = 0
        self.follow_speed = 5.0
    
    def follow_target(self, target_x: int, target_y: int, level_width: int, level_height: int):
        """Follow a target (usually the player) with smooth movement"""
        # Calculate desired camera position (center target on screen)
        desired_x = target_x - SCREEN_WIDTH // 2
        desired_y = target_y - SCREEN_HEIGHT // 2
        
        # Clamp camera to level boundaries
        max_x = level_width * TILE_SIZE - SCREEN_WIDTH
        max_y = level_height * TILE_SIZE - SCREEN_HEIGHT
        
        desired_x = max(0, min(desired_x, max_x))
        desired_y = max(0, min(desired_y, max_y))
        
        # Smooth camera movement
        self.target_x = desired_x
        self.target_y = desired_y
    
    def update(self, dt: float):
        """Update camera position with smooth interpolation"""
        # Smooth interpolation towards target
        self.x += (self.target_x - self.x) * self.follow_speed * dt
        self.y += (self.target_y - self.y) * self.follow_speed * dt
    
    def get_offset(self) -> Tuple[int, int]:
        """Get camera offset for rendering"""
        return (int(self.x), int(self.y))

class LevelManager:
    """Manages level loading, transitions, and current level state"""
    
    def __init__(self):
        self.current_level: Optional[Level] = None
        self.levels: Dict[str, Level] = {}
        self.camera = Camera()
        
        # Initialize default levels
        self._create_default_levels()
    
    def _create_default_levels(self):
        """Create default levels for testing"""
        # Create Compute Valley level
        compute_level = self._create_compute_valley()
        self.levels["compute_valley"] = compute_level
        
        # Set as current level
        self.current_level = compute_level
    
    def _create_compute_valley(self) -> Level:
        """Create the Compute Valley level"""
        level = Level("compute_valley", "Compute Valley", 40, 30)
        level.theme = "compute"
        level.background_color = (25, 35, 50)
        
        # Create level layout
        # Borders
        for x in range(level.width):
            level.set_tile(x, 0, 'wall', solid=True)
            level.set_tile(x, level.height - 1, 'wall', solid=True)
        for y in range(level.height):
            level.set_tile(0, y, 'wall', solid=True)
            level.set_tile(level.width - 1, y, 'wall', solid=True)
        
        # Fill with grass
        for y in range(1, level.height - 1):
            for x in range(1, level.width - 1):
                level.set_tile(x, y, 'grass')
        
        # Add some cloud compute themed areas
        for x in range(5, 15):
            for y in range(5, 10):
                level.set_tile(x, y, 'cloud_compute')
        
        # Add obstacles and structures
        # Server room
        for x in range(20, 25):
            for y in range(8, 12):
                level.set_tile(x, y, 'stone', solid=True)
        
        # Learning stations
        level.set_tile(10, 7, 'learning_station')
        level.set_tile(30, 15, 'learning_station')
        level.set_tile(15, 20, 'learning_station')
        
        # Enemy spawns
        level.set_tile(35, 25, 'enemy_spawn')
        level.set_tile(8, 25, 'enemy_spawn')
        
        # Water feature
        for x in range(25, 35):
            for y in range(20, 25):
                level.set_tile(x, y, 'water', solid=True)
        
        return level
    
    def load_level(self, level_id: str) -> bool:
        """Load a specific level"""
        if level_id in self.levels:
            self.current_level = self.levels[level_id]
            print(f"Loaded level: {self.current_level.name}")
            return True
        else:
            print(f"Level '{level_id}' not found!")
            return False
    
    def get_solid_rects(self) -> List[pygame.Rect]:
        """Get collision rectangles from current level"""
        if self.current_level:
            return self.current_level.get_solid_rects()
        return []
    
    def update_camera(self, player_x: int, player_y: int, dt: float):
        """Update camera to follow player"""
        if self.current_level:
            self.camera.follow_target(player_x, player_y, 
                                    self.current_level.width, 
                                    self.current_level.height)
            self.camera.update(dt)
    
    def render(self, screen: pygame.Surface):
        """Render current level"""
        if self.current_level:
            camera_x, camera_y = self.camera.get_offset()
            self.current_level.render(screen, camera_x, camera_y)
    
    def get_camera_offset(self) -> Tuple[int, int]:
        """Get current camera offset"""
        return self.camera.get_offset()