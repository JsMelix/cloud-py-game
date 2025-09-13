"""
HUD (Heads-Up Display) System - Game UI elements
"""

import pygame
from typing import Dict, List, Optional, Tuple
from enum import Enum

class UIPanel:
    """Base class for UI panels"""
    
    def __init__(self, x: int, y: int, width: int, height: int, 
                 background_color: Tuple[int, int, int] = (40, 40, 60),
                 border_color: Tuple[int, int, int] = (255, 255, 255),
                 alpha: int = 200):
        self.rect = pygame.Rect(x, y, width, height)
        self.background_color = background_color
        self.border_color = border_color
        self.alpha = alpha
        self.visible = True
    
    def render_background(self, screen: pygame.Surface):
        """Render panel background"""
        if not self.visible:
            return
        
        # Create surface with alpha
        panel_surface = pygame.Surface((self.rect.width, self.rect.height))
        panel_surface.set_alpha(self.alpha)
        panel_surface.fill(self.background_color)
        
        # Draw background
        screen.blit(panel_surface, self.rect)
        
        # Draw border
        pygame.draw.rect(screen, self.border_color, self.rect, 2)
    
    def render(self, screen: pygame.Surface):
        """Override in subclasses"""
        self.render_background(screen)

class HealthBar(UIPanel):
    """Health bar UI element"""
    
    def __init__(self, x: int, y: int, width: int = 200, height: int = 20):
        super().__init__(x, y, width, height, (60, 20, 20), (255, 255, 255), 150)
        self.font = pygame.font.Font(None, 18)
    
    def render(self, screen: pygame.Surface, current_health: int, max_health: int):
        """Render health bar"""
        if not self.visible:
            return
        
        # Background
        self.render_background(screen)
        
        # Health fill
        health_percentage = current_health / max_health if max_health > 0 else 0
        fill_width = int((self.rect.width - 4) * health_percentage)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, fill_width, self.rect.height - 4)
            
            # Color based on health percentage
            if health_percentage > 0.6:
                color = (0, 200, 0)  # Green
            elif health_percentage > 0.3:
                color = (255, 255, 0)  # Yellow
            else:
                color = (255, 0, 0)  # Red
            
            pygame.draw.rect(screen, color, fill_rect)
        
        # Health text
        health_text = f"{current_health}/{max_health}"
        text_surface = self.font.render(health_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class ExperienceBar(UIPanel):
    """Experience bar UI element"""
    
    def __init__(self, x: int, y: int, width: int = 300, height: int = 15):
        super().__init__(x, y, width, height, (20, 20, 60), (255, 255, 255), 150)
        self.font = pygame.font.Font(None, 16)
    
    def render(self, screen: pygame.Surface, current_exp: int, exp_to_next: int, level: int):
        """Render experience bar"""
        if not self.visible:
            return
        
        # Background
        self.render_background(screen)
        
        # Experience fill
        exp_percentage = current_exp / exp_to_next if exp_to_next > 0 else 0
        fill_width = int((self.rect.width - 4) * exp_percentage)
        
        if fill_width > 0:
            fill_rect = pygame.Rect(self.rect.x + 2, self.rect.y + 2, fill_width, self.rect.height - 4)
            pygame.draw.rect(screen, (100, 150, 255), fill_rect)
        
        # Level and XP text
        exp_text = f"Level {level} - {current_exp}/{exp_to_next} XP"
        text_surface = self.font.render(exp_text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

class MinimapPanel(UIPanel):
    """Minimap showing player position and nearby elements"""
    
    def __init__(self, x: int, y: int, size: int = 150):
        super().__init__(x, y, size, size, (20, 30, 40), (255, 255, 255), 180)
        self.scale = 0.1  # Scale factor for minimap
    
    def render(self, screen: pygame.Surface, player_x: int, player_y: int, 
               level_width: int, level_height: int, enemies: List = None, 
               learning_stations: List = None):
        """Render minimap"""
        if not self.visible:
            return
        
        # Background
        self.render_background(screen)
        
        # Calculate minimap bounds
        map_rect = pygame.Rect(self.rect.x + 5, self.rect.y + 5, 
                              self.rect.width - 10, self.rect.height - 10)
        
        # Scale factors
        scale_x = map_rect.width / (level_width * 32)  # 32 = TILE_SIZE
        scale_y = map_rect.height / (level_height * 32)
        
        # Draw player
        player_map_x = int(map_rect.x + player_x * scale_x)
        player_map_y = int(map_rect.y + player_y * scale_y)
        pygame.draw.circle(screen, (0, 255, 0), (player_map_x, player_map_y), 3)
        
        # Draw enemies
        if enemies:
            for enemy in enemies:
                enemy_map_x = int(map_rect.x + enemy.x * scale_x)
                enemy_map_y = int(map_rect.y + enemy.y * scale_y)
                pygame.draw.circle(screen, (255, 0, 0), (enemy_map_x, enemy_map_y), 2)
        
        # Draw learning stations
        if learning_stations:
            for station in learning_stations:
                station_map_x = int(map_rect.x + station['x'] * scale_x)
                station_map_y = int(map_rect.y + station['y'] * scale_y)
                pygame.draw.circle(screen, (255, 255, 0), (station_map_x, station_map_y), 2)

class AbilityPanel(UIPanel):
    """Panel showing equipped abilities"""
    
    def __init__(self, x: int, y: int, width: int = 200, height: int = 120):
        super().__init__(x, y, width, height, (30, 30, 50), (255, 255, 255), 180)
        self.font = pygame.font.Font(None, 18)
        self.small_font = pygame.font.Font(None, 14)
    
    def render(self, screen: pygame.Surface, abilities: List = None):
        """Render ability panel"""
        if not self.visible:
            return
        
        # Background
        self.render_background(screen)
        
        # Title
        title_text = self.font.render("Abilities", True, (255, 255, 255))
        screen.blit(title_text, (self.rect.x + 10, self.rect.y + 5))
        
        # Abilities
        if abilities:
            for i, ability in enumerate(abilities[:4]):  # Show max 4 abilities
                y_pos = self.rect.y + 25 + (i * 20)
                
                # Ability name
                ability_name = ability.name if hasattr(ability, 'name') else str(ability)
                name_surface = self.small_font.render(ability_name, True, (200, 200, 255))
                screen.blit(name_surface, (self.rect.x + 10, y_pos))
                
                # Cooldown indicator
                if hasattr(ability, 'current_cooldown') and ability.current_cooldown > 0:
                    cooldown_text = f"({ability.current_cooldown})"
                    cooldown_surface = self.small_font.render(cooldown_text, True, (255, 100, 100))
                    screen.blit(cooldown_surface, (self.rect.x + 150, y_pos))

class NotificationPanel:
    """Panel for showing temporary notifications"""
    
    def __init__(self, x: int, y: int, width: int = 400):
        self.x = x
        self.y = y
        self.width = width
        self.font = pygame.font.Font(None, 24)
        self.notifications: List[Dict] = []
        self.max_notifications = 5
    
    def add_notification(self, message: str, duration: float = 3.0, 
                        color: Tuple[int, int, int] = (255, 255, 255)):
        """Add a notification"""
        notification = {
            'message': message,
            'duration': duration,
            'color': color,
            'alpha': 255
        }
        
        self.notifications.append(notification)
        
        # Remove old notifications if too many
        if len(self.notifications) > self.max_notifications:
            self.notifications.pop(0)
    
    def update(self, dt: float):
        """Update notifications"""
        for notification in self.notifications[:]:
            notification['duration'] -= dt
            
            # Fade out in last second
            if notification['duration'] < 1.0:
                notification['alpha'] = int(255 * notification['duration'])
            
            # Remove expired notifications
            if notification['duration'] <= 0:
                self.notifications.remove(notification)
    
    def render(self, screen: pygame.Surface):
        """Render notifications"""
        for i, notification in enumerate(self.notifications):
            y_pos = self.y + (i * 30)
            
            # Create surface with alpha
            text_surface = self.font.render(notification['message'], True, notification['color'])
            text_surface.set_alpha(notification['alpha'])
            
            # Background
            bg_rect = pygame.Rect(self.x - 5, y_pos - 2, self.width, 26)
            bg_surface = pygame.Surface((bg_rect.width, bg_rect.height))
            bg_surface.set_alpha(notification['alpha'] // 3)
            bg_surface.fill((0, 0, 0))
            screen.blit(bg_surface, bg_rect)
            
            # Text
            screen.blit(text_surface, (self.x, y_pos))

class GameHUD:
    """Main HUD system managing all UI elements"""
    
    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # UI Elements
        self.health_bar = HealthBar(10, 10)
        self.experience_bar = ExperienceBar(10, 40)
        self.minimap = MinimapPanel(screen_width - 160, 10)
        self.ability_panel = AbilityPanel(screen_width - 210, 170)
        self.notifications = NotificationPanel(10, screen_height - 200)
        
        # Stats panel
        self.stats_panel = UIPanel(10, 70, 300, 100, (20, 40, 20), (255, 255, 255), 150)
        self.font = pygame.font.Font(None, 20)
        self.small_font = pygame.font.Font(None, 16)
        
        # Toggle states
        self.show_minimap = True
        self.show_abilities = True
        self.show_stats = True
    
    def update(self, dt: float):
        """Update HUD elements"""
        self.notifications.update(dt)
    
    def render(self, screen: pygame.Surface, game_state):
        """Render all HUD elements"""
        # Health bar
        if hasattr(game_state, 'player'):
            player = game_state.player
            self.health_bar.render(screen, player.health, player.max_health)
            
            # Experience bar
            progress_summary = game_state.progress_tracker.get_progress_summary()
            self.experience_bar.render(screen, 
                                     progress_summary['experience'],
                                     progress_summary['exp_to_next'],
                                     progress_summary['level'])
            
            # Stats panel
            if self.show_stats:
                self._render_stats_panel(screen, game_state, progress_summary)
            
            # Minimap
            if self.show_minimap:
                enemies = game_state.enemy_manager.enemies if hasattr(game_state, 'enemy_manager') else []
                learning_stations = game_state.learning_stations if hasattr(game_state, 'learning_stations') else []
                level = game_state.level_manager.current_level if hasattr(game_state, 'level_manager') else None
                
                if level:
                    self.minimap.render(screen, 
                                      int(player.position.x), int(player.position.y),
                                      level.width, level.height,
                                      enemies, learning_stations)
            
            # Ability panel
            if self.show_abilities and hasattr(player, 'ability_manager'):
                equipped_abilities = player.ability_manager.get_equipped_abilities()
                self.ability_panel.render(screen, equipped_abilities)
        
        # Notifications
        self.notifications.render(screen)
    
    def _render_stats_panel(self, screen: pygame.Surface, game_state, progress_summary):
        """Render stats panel"""
        self.stats_panel.render_background(screen)
        
        y_offset = self.stats_panel.rect.y + 10
        
        # Concepts learned
        concepts_text = f"Concepts: {progress_summary['concepts_learned']}"
        concepts_surface = self.small_font.render(concepts_text, True, (150, 255, 150))
        screen.blit(concepts_surface, (self.stats_panel.rect.x + 10, y_offset))
        
        # Battles won
        battles_text = f"Battles: {progress_summary['battles_won']}"
        battles_surface = self.small_font.render(battles_text, True, (255, 150, 150))
        screen.blit(battles_surface, (self.stats_panel.rect.x + 150, y_offset))
        
        y_offset += 20
        
        # Achievements
        achievements_text = f"Achievements: {progress_summary['achievements_unlocked']}/{progress_summary['total_achievements']}"
        achievements_surface = self.small_font.render(achievements_text, True, (255, 215, 0))
        screen.blit(achievements_surface, (self.stats_panel.rect.x + 10, y_offset))
        
        y_offset += 20
        
        # Time played
        time_minutes = int(progress_summary['time_played'] / 60)
        time_text = f"Time: {time_minutes}m"
        time_surface = self.small_font.render(time_text, True, (200, 200, 255))
        screen.blit(time_surface, (self.stats_panel.rect.x + 10, y_offset))
        
        # Combat status
        if hasattr(game_state, 'combat_system') and game_state.combat_system.active:
            combat_text = "IN COMBAT"
            combat_surface = self.small_font.render(combat_text, True, (255, 100, 100))
            screen.blit(combat_surface, (self.stats_panel.rect.x + 150, y_offset))
    
    def add_notification(self, message: str, duration: float = 3.0, 
                        color: Tuple[int, int, int] = (255, 255, 255)):
        """Add a notification to the HUD"""
        self.notifications.add_notification(message, duration, color)
    
    def toggle_minimap(self):
        """Toggle minimap visibility"""
        self.show_minimap = not self.show_minimap
    
    def toggle_abilities(self):
        """Toggle ability panel visibility"""
        self.show_abilities = not self.show_abilities
    
    def toggle_stats(self):
        """Toggle stats panel visibility"""
        self.show_stats = not self.show_stats