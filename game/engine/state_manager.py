"""
State Manager - Handles different game states and transitions
"""

import pygame
from typing import Dict, Optional
from .constants import GameState

class State:
    """Base class for game states"""
    
    def __init__(self, state_manager):
        self.state_manager = state_manager
    
    def enter(self):
        """Called when entering this state"""
        pass
    
    def exit(self):
        """Called when exiting this state"""
        pass
    
    def handle_event(self, event):
        """Handle pygame events"""
        pass
    
    def update(self, dt):
        """Update state logic"""
        pass
    
    def render(self, screen):
        """Render state graphics"""
        pass

class MenuState(State):
    """Main menu state"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 48)
        self.title_font = pygame.font.Font(None, 72)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                self.state_manager.change_state(GameState.GAMEPLAY)
    
    def render(self, screen):
        # Render title
        title_text = self.title_font.render("Cloud Learning Game", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(screen.get_width()//2, 200))
        screen.blit(title_text, title_rect)
        
        # Render instructions
        start_text = self.font.render("Press SPACE to Start", True, (200, 200, 200))
        start_rect = start_text.get_rect(center=(screen.get_width()//2, 400))
        screen.blit(start_text, start_rect)

class GameplayState(State):
    """Main gameplay state"""
    
    def __init__(self, state_manager):
        super().__init__(state_manager)
        self.font = pygame.font.Font(None, 24)
        
        # Import here to avoid circular imports
        from ..entities.player import Player
        from .input_handler import InputHandler
        from ..levels.level import LevelManager
        from ..systems.education import EducationSystem
        from ..systems.combat import CombatSystem
        from ..entities.enemy import EnemyManager
        
        # Initialize systems
        self.education_system = EducationSystem()
        self.level_manager = LevelManager()
        self.combat_system = CombatSystem()
        self.enemy_manager = EnemyManager()
        
        # Initialize player at spawn position
        self.player = Player(200, 200)  # Start in a safe area
        self.input_handler = InputHandler()
        
        # Connect ability manager to player
        from ..systems.abilities_simple import AbilityManager
        from ..systems.progress import ProgressTracker
        from ..systems.progression import LevelProgressionSystem
        from ..ui.hud import GameHUD
        from ..engine.constants import SCREEN_WIDTH, SCREEN_HEIGHT
        
        self.ability_manager = AbilityManager()
        self.progress_tracker = ProgressTracker()
        self.progression_system = LevelProgressionSystem()
        self.hud = GameHUD(SCREEN_WIDTH, SCREEN_HEIGHT)
        
        # Audio/Visual effects
        from ..systems.audio import AudioVisualManager
        self.av_manager = AudioVisualManager()
        
        self.player.ability_manager = self.ability_manager
        
        # Set up enemies for the current level
        self._setup_enemies()
        
        # Learning interface state
        self.learning_ui = None
        self.in_learning_mode = False
        
        # Simple learning stations (positions and concept IDs)
        self.learning_stations = [
            {'x': 10 * 32, 'y': 7 * 32, 'concept_id': 'ec2_basics', 'nearby': False},
            {'x': 30 * 32, 'y': 15 * 32, 'concept_id': 's3_storage', 'nearby': False},
            {'x': 15 * 32, 'y': 20 * 32, 'concept_id': 'vpc_networking', 'nearby': False}
        ]
    
    def _setup_enemies(self):
        """Set up enemy spawn points for the current level"""
        # Add enemy spawn points
        enemy_spawns = [
            (35 * 32, 25 * 32, ["latency_monster", "data_loss_demon"]),
            (8 * 32, 25 * 32, ["security_breach", "cost_overrun"]),
            (25 * 32, 10 * 32, ["latency_monster", "security_breach"])
        ]
        
        for x, y, enemy_types in enemy_spawns:
            self.enemy_manager.add_spawn_point(x, y, enemy_types)
        
        # Spawn initial enemies
        self.enemy_manager.spawn_enemy(35 * 32, 25 * 32, "latency_monster")
        self.enemy_manager.spawn_enemy(8 * 32, 25 * 32, "security_breach")
    
    def enter(self):
        """Called when entering gameplay state"""
        print("Entered gameplay - Use WASD or arrows to move, E to interact, ESC for menu")
    

    
    def handle_event(self, event):
        # Handle learning interface input first (highest priority)
        if self.in_learning_mode and self.learning_ui:
            if not self.learning_ui.handle_input(event):
                # Learning completed, get results
                completion_data = self.learning_ui.get_completion_data()
                concept = self.learning_ui.current_concept
                self._complete_learning(concept, completion_data)
            return
        
        # Handle combat input second priority
        if self.combat_system.handle_input(event):
            return
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.state_manager.change_state(GameState.MENU)
            elif event.key == pygame.K_e:
                # Handle learning station interaction
                self._handle_learning_interaction()
            elif event.key == pygame.K_TAB:
                # Toggle HUD elements
                self.hud.toggle_stats()
            elif event.key == pygame.K_m:
                # Toggle minimap
                self.hud.toggle_minimap()
        
        # Pass event to input handler
        self.input_handler.handle_event(event)
    
    def update(self, dt):
        """Update gameplay logic"""
        # Update combat system
        self.combat_system.update(dt)
        
        # If in combat or learning mode, don't update movement
        if self.combat_system.active or self.in_learning_mode:
            return
        
        # Update input handler
        self.input_handler.update()
        
        # Get movement input
        movement_direction = self.input_handler.get_movement_input()
        
        # Store previous position for collision handling
        from ..entities.player import Vector2
        previous_position = Vector2(self.player.position.x, self.player.position.y)
        
        # Move player
        self.player.move(movement_direction, dt)
        
        # Check level boundaries
        if self.level_manager.current_level:
            self.player.check_boundaries(
                self.level_manager.current_level.width,
                self.level_manager.current_level.height
            )
        
        # Get collision rectangles from level
        obstacles = self.level_manager.get_solid_rects()
        
        # Handle collisions with level obstacles
        self.player.handle_collision(obstacles, previous_position)
        
        # Update enemies
        player_center_x = int(self.player.position.x + self.player.sprite_size // 2)
        player_center_y = int(self.player.position.y + self.player.sprite_size // 2)
        
        self.enemy_manager.update(dt, player_center_x, player_center_y)
        
        # Check for combat initiation
        colliding_enemy = self.enemy_manager.check_player_collision(self.player.rect)
        if colliding_enemy and not self.combat_system.active:
            # Connect progress tracker to player for combat tracking
            self.player.progress_tracker = self.progress_tracker
            self.combat_system.ability_manager = self.ability_manager
            self.combat_system.start_combat(self.player, colliding_enemy)
        
        # Update camera to follow player
        self.level_manager.update_camera(player_center_x, player_center_y, dt)
        
        # Update learning stations
        self._update_learning_stations()
        
        # Update player animation
        self.player.update(dt)
        
        # Update HUD and effects
        self.hud.update(dt)
        self.av_manager.update(dt)
        
        # Update progress tracking
        self.progress_tracker.update_session_time(dt)
        
        # Track movement for exploration stats
        if movement_direction.x != 0 or movement_direction.y != 0:
            distance = (movement_direction.x ** 2 + movement_direction.y ** 2) ** 0.5 * self.player.speed * dt
            self.progress_tracker.track_movement(distance)
        
        # Update progression system
        progress_summary = self.progress_tracker.get_progress_summary()
        self.progression_system.update_player_progress(
            progress_summary['level'],
            set(self.player.learned_concepts),
            set(self.progress_tracker.unlocked_achievements),
            self.progress_tracker.combat_stats.enemies_defeated
        )
    
    def render(self, screen):
        """Render gameplay elements"""
        # Render level (background and tiles)
        self.level_manager.render(screen)
        
        # Render player with camera offset
        camera_x, camera_y = self.level_manager.get_camera_offset()
        self._render_player_with_camera(screen, camera_x, camera_y)
        
        # Render enemies
        self.enemy_manager.render(screen, camera_x, camera_y)
        
        # Render combat UI (if active)
        self.combat_system.render(screen)
        
        # Render learning interface (if active)
        if self.in_learning_mode and self.learning_ui:
            self.learning_ui.render(screen)
        else:
            # Only render HUD and other elements if not in learning mode
            # Render visual effects
            camera_x, camera_y = self.level_manager.get_camera_offset()
            self.av_manager.render(screen, camera_x, camera_y)
            
            # Render HUD
            self.hud.render(screen, self)
            
            # Draw additional UI elements
            self._render_interaction_prompts(screen)
    
    def _render_player_with_camera(self, screen, camera_x, camera_y):
        """Render player with camera offset"""
        # Create a temporary rect for rendering with camera offset
        render_rect = pygame.Rect(
            self.player.rect.x - camera_x,
            self.player.rect.y - camera_y,
            self.player.rect.width,
            self.player.rect.height
        )
        
        # Only render if player is visible on screen
        if (render_rect.right > 0 and render_rect.left < screen.get_width() and
            render_rect.bottom > 0 and render_rect.top < screen.get_height()):
            
            # Draw player sprite
            color = self.player.color
            if self.player.is_moving:
                color = (min(255, self.player.color[0] + 20), 
                        min(255, self.player.color[1] + 20), 
                        min(255, self.player.color[2] + 20))
            
            pygame.draw.rect(screen, color, render_rect)
            
            # Draw direction indicator
            center_x = render_rect.centerx
            center_y = render_rect.centery
            
            if self.player.facing_direction == "up":
                pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y - 8), 3)
            elif self.player.facing_direction == "down":
                pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y + 8), 3)
            elif self.player.facing_direction == "left":
                pygame.draw.circle(screen, (255, 255, 255), (center_x - 8, center_y), 3)
            elif self.player.facing_direction == "right":
                pygame.draw.circle(screen, (255, 255, 255), (center_x + 8, center_y), 3)
    

    
    def _update_learning_stations(self):
        """Update learning station proximity"""
        player_x = int(self.player.position.x + self.player.sprite_size // 2)
        player_y = int(self.player.position.y + self.player.sprite_size // 2)
        
        for station in self.learning_stations:
            distance = ((player_x - station['x']) ** 2 + (player_y - station['y']) ** 2) ** 0.5
            station['nearby'] = distance <= 48  # 1.5 tiles
    
    def _handle_learning_interaction(self):
        """Handle interaction with nearby learning stations"""
        for station in self.learning_stations:
            if station['nearby']:
                concept = self.education_system.get_concept(station['concept_id'])
                if concept:
                    # Check if already learned
                    if station['concept_id'] in self.player.learned_concepts:
                        self.hud.add_notification(f"Already mastered {concept.name}!", 3.0, (255, 200, 100))
                        continue
                    
                    # Start enhanced learning interface
                    self._start_enhanced_learning(concept)
                    break
    
    def _start_enhanced_learning(self, concept):
        """Start the enhanced learning interface"""
        from ..ui.learning_interface import InteractiveLearningUI
        
        self.learning_ui = InteractiveLearningUI()
        self.learning_ui.start_learning(concept)
        self.in_learning_mode = True
        
        print(f"Starting enhanced learning for: {concept.name}")
    
    def _complete_learning(self, concept, completion_data):
        """Complete the learning process with results"""
        if completion_data['passed']:
            # Learn the concept
            self.player.learn_concept(concept.id)
            
            # Calculate experience based on performance
            base_exp = 100
            quiz_bonus = int(completion_data['quiz_percentage'] * 0.5)  # Up to 50 bonus XP
            practical_bonus = 50 if completion_data['practical_completed'] else 0
            total_exp = base_exp + quiz_bonus + practical_bonus
            
            self.player.gain_experience(total_exp)
            
            # Track progress
            self.progress_tracker.learn_concept(concept.id)
            self.progress_tracker.gain_experience(total_exp, "learning")
            self.progress_tracker.complete_quiz(
                concept.id, 
                completion_data['quiz_percentage'], 
                1  # Attempts (simplified)
            )
            
            # Unlock abilities through ability manager
            if self.player.ability_manager:
                unlocked_abilities = self.player.ability_manager.unlock_ability(concept.id)
                for ability_name in unlocked_abilities:
                    print(f"Unlocked ability: {ability_name}")
                    # Auto-equip first few abilities
                    if len(self.player.ability_manager.equipped_abilities) < 4:
                        for ability_id, ability in self.player.ability_manager.all_abilities.items():
                            if ability.name == ability_name:
                                self.player.ability_manager.equip_ability(ability_id)
                                break
            
            # Legacy ability unlock
            if concept.unlock_ability:
                self.player.current_abilities.append(concept.unlock_ability)
            
            # Add HUD notifications
            self.hud.add_notification(f"Mastered: {concept.name}!", 4.0, (150, 255, 150))
            self.hud.add_notification(f"Gained {total_exp} XP!", 3.0, (100, 150, 255))
            
            if completion_data['quiz_percentage'] == 100:
                self.hud.add_notification("Perfect Score! 🏆", 4.0, (255, 215, 0))
            
            # Play learning effect
            self.av_manager.play_learning_effect(
                self.player.position.x + self.player.sprite_size // 2,
                self.player.position.y + self.player.sprite_size // 2
            )
            
            print(f"Mastered: {concept.name} - Gained {total_exp} XP!")
        else:
            # Failed to pass
            self.hud.add_notification("Study more and try again!", 3.0, (255, 150, 50))
            print(f"Need more study for {concept.name}. Try again later!")
        
        # Exit learning mode
        self.in_learning_mode = False
        self.learning_ui = None
    
    def _render_interaction_prompts(self, screen):
        """Render interaction prompts for nearby learning stations"""
        camera_x, camera_y = self.level_manager.get_camera_offset()
        
        for station in self.learning_stations:
            if station['nearby'] and station['concept_id'] not in self.player.learned_concepts:
                concept = self.education_system.get_concept(station['concept_id'])
                if concept:
                    # Calculate screen position
                    screen_x = station['x'] - camera_x
                    screen_y = station['y'] - camera_y - 40
                    
                    # Only render if on screen
                    if (0 <= screen_x <= screen.get_width() and 
                        0 <= screen_y <= screen.get_height()):
                        
                        # Create prompt
                        prompt_text = f"Press E to learn: {concept.name}"
                        prompt_surface = self.font.render(prompt_text, True, (255, 255, 0))
                        prompt_rect = prompt_surface.get_rect()
                        prompt_rect.centerx = screen_x
                        prompt_rect.y = screen_y
                        
                        # Background for better readability
                        bg_rect = prompt_rect.inflate(10, 5)
                        pygame.draw.rect(screen, (0, 0, 0), bg_rect)
                        pygame.draw.rect(screen, (255, 255, 0), bg_rect, 2)
                        
                        screen.blit(prompt_surface, prompt_rect)

class StateManager:
    """Manages game states and transitions"""
    
    def __init__(self, screen):
        self.screen = screen
        self.states: Dict[str, State] = {}
        self.current_state: Optional[State] = None
        self.current_state_name: Optional[str] = None
        
        # Initialize states
        self._initialize_states()
        
        # Start with menu state
        self.change_state(GameState.MENU)
    
    def _initialize_states(self):
        """Initialize all game states"""
        self.states[GameState.MENU] = MenuState(self)
        self.states[GameState.GAMEPLAY] = GameplayState(self)
    
    def change_state(self, new_state_name: str):
        """Change to a new state"""
        if new_state_name not in self.states:
            print(f"Warning: State '{new_state_name}' not found!")
            return
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
        
        # Change to new state
        self.current_state = self.states[new_state_name]
        self.current_state_name = new_state_name
        self.current_state.enter()
        
        print(f"Changed to state: {new_state_name}")
    
    def handle_event(self, event):
        """Pass events to current state"""
        if self.current_state:
            self.current_state.handle_event(event)
    
    def update(self, dt):
        """Update current state"""
        if self.current_state:
            self.current_state.update(dt)
    
    def render(self, screen):
        """Render current state"""
        if self.current_state:
            self.current_state.render(screen)