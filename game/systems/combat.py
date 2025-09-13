"""
Combat System - Handles turn-based combat using cloud knowledge
"""

import pygame
import random
from typing import List, Optional, Dict, Tuple
from enum import Enum
from ..entities.enemy import CloudEnemy

class CombatState(Enum):
    """Combat states"""
    PLAYER_TURN = "player_turn"
    ENEMY_TURN = "enemy_turn"
    COMBAT_END = "combat_end"

class CloudAbility:
    """Represents a combat ability based on cloud concepts"""
    
    def __init__(self, name: str, concept_id: str, damage: int, description: str, 
                 cooldown: int = 0, special_effect: str = None):
        self.name = name
        self.concept_id = concept_id
        self.damage = damage
        self.description = description
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.special_effect = special_effect
    
    def can_use(self) -> bool:
        """Check if ability can be used (not on cooldown)"""
        return self.current_cooldown <= 0
    
    def use(self) -> int:
        """Use the ability and return damage dealt"""
        if self.can_use():
            self.current_cooldown = self.cooldown
            return self.damage
        return 0
    
    def update_cooldown(self):
        """Update cooldown (call each turn)"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

class CombatSystem:
    """Manages turn-based combat encounters"""
    
    def __init__(self):
        self.active = False
        self.state = CombatState.PLAYER_TURN
        self.current_enemy: Optional[CloudEnemy] = None
        self.player = None
        
        # Combat UI
        self.selected_ability = 0
        self.combat_log: List[str] = []
        self.turn_timer = 0
        self.auto_advance_time = 2.0  # Auto advance after enemy turn
        
        # Available abilities based on learned concepts
        self.available_abilities: List[CloudAbility] = []
        
        # Advanced ability system (will be set by gameplay state)
        self.ability_manager = None
        
        # Initialize default abilities
        self._initialize_abilities()
    
    def _initialize_abilities(self):
        """Initialize cloud-based combat abilities"""
        self.all_abilities = {
            "ec2_basics": CloudAbility(
                name="Auto Scaling",
                concept_id="ec2_basics",
                damage=25,
                description="Scales damage based on enemy health",
                cooldown=2,
                special_effect="scale_damage"
            ),
            "lambda_serverless": CloudAbility(
                name="Serverless Strike",
                concept_id="lambda_serverless",
                damage=30,
                description="Fast, efficient attack with no cooldown",
                cooldown=0,
                special_effect="no_cooldown"
            ),
            "s3_storage": CloudAbility(
                name="Data Backup",
                concept_id="s3_storage",
                damage=20,
                description="Restores health while dealing damage",
                cooldown=3,
                special_effect="heal_self"
            ),
            "vpc_networking": CloudAbility(
                name="Network Isolation",
                concept_id="vpc_networking",
                damage=15,
                description="Reduces enemy attack for next turn",
                cooldown=2,
                special_effect="debuff_enemy"
            ),
            "iam_security": CloudAbility(
                name="Access Control",
                concept_id="iam_security",
                damage=35,
                description="High damage against security threats",
                cooldown=3,
                special_effect="security_bonus"
            )
        }
    
    def start_combat(self, player, enemy: CloudEnemy):
        """Start combat encounter"""
        self.active = True
        self.player = player
        self.current_enemy = enemy
        self.state = CombatState.PLAYER_TURN
        self.selected_ability = 0
        self.combat_log.clear()
        
        # Update available abilities based on player's learned concepts
        self.available_abilities.clear()
        
        # Unlock abilities for learned concepts
        for concept_id in player.learned_concepts:
            unlocked = self.ability_manager.unlock_ability(concept_id)
            for ability_name in unlocked:
                print(f"Unlocked ability: {ability_name}")
        
        # Get equipped abilities for combat
        equipped_abilities = self.ability_manager.get_equipped_abilities()
        
        # Convert to old format for compatibility
        for advanced_ability in equipped_abilities:
            basic_ability = CloudAbility(
                name=advanced_ability.name,
                concept_id=advanced_ability.concept_id,
                damage=advanced_ability.effects[0].value if advanced_ability.effects else 20,
                description=f"Advanced {advanced_ability.ability_type.value} ability",
                cooldown=advanced_ability.cooldown
            )
            basic_ability.current_cooldown = 0  # Reset for new combat
            self.available_abilities.append(basic_ability)
        
        # Fallback to basic abilities if no equipped abilities
        if not self.available_abilities:
            for concept_id in player.learned_concepts:
                if concept_id in self.all_abilities:
                    ability = self.all_abilities[concept_id]
                    # Reset cooldown for new combat
                    ability.current_cooldown = 0
                    self.available_abilities.append(ability)
        
        # Add basic attack if no abilities available
        if not self.available_abilities:
            basic_attack = CloudAbility(
                name="Basic Attack",
                concept_id="basic",
                damage=15,
                description="A simple attack",
                cooldown=0
            )
            self.available_abilities.append(basic_attack)
        
        self.add_to_log(f"Combat started against {enemy.enemy_type}!")
        print(f"Combat started! Player vs {enemy.enemy_type}")
    
    def handle_input(self, event: pygame.event.Event) -> bool:
        """Handle combat input"""
        if not self.active or self.state != CombatState.PLAYER_TURN:
            return False
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_ability = (self.selected_ability - 1) % len(self.available_abilities)
                return True
            elif event.key == pygame.K_DOWN:
                self.selected_ability = (self.selected_ability + 1) % len(self.available_abilities)
                return True
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                self._execute_player_turn()
                return True
            elif event.key == pygame.K_ESCAPE:
                self._try_flee()
                return True
        
        return False
    
    def update(self, dt: float):
        """Update combat system"""
        if not self.active:
            return
        
        self.turn_timer += dt
        
        if self.state == CombatState.ENEMY_TURN:
            if self.turn_timer >= self.auto_advance_time:
                self._execute_enemy_turn()
        elif self.state == CombatState.COMBAT_END:
            if self.turn_timer >= self.auto_advance_time:
                self.end_combat()
    
    def _execute_player_turn(self):
        """Execute player's selected ability"""
        if not self.available_abilities:
            return
        
        ability = self.available_abilities[self.selected_ability]
        
        if not ability.can_use():
            self.add_to_log(f"{ability.name} is on cooldown!")
            return
        
        # Use ability
        base_damage = ability.use()
        
        # Apply special effects
        final_damage = self._apply_ability_effects(ability, base_damage)
        
        # Deal damage to enemy
        enemy_died = self.current_enemy.take_damage(final_damage, ability.concept_id)
        
        self.add_to_log(f"Used {ability.name} for {final_damage} damage!")
        
        # Update ability cooldowns
        for ab in self.available_abilities:
            ab.update_cooldown()
        
        # Check if enemy died
        if enemy_died:
            self._handle_victory()
        else:
            # Switch to enemy turn
            self.state = CombatState.ENEMY_TURN
            self.turn_timer = 0
    
    def _apply_ability_effects(self, ability: CloudAbility, base_damage: int) -> int:
        """Apply special effects of abilities"""
        final_damage = base_damage
        
        if ability.special_effect == "scale_damage":
            # Auto Scaling: More damage against wounded enemies
            enemy_health_percent = self.current_enemy.get_health_percentage()
            if enemy_health_percent < 50:
                final_damage = int(base_damage * 1.5)
                self.add_to_log("Auto Scaling activated! Bonus damage!")
        
        elif ability.special_effect == "heal_self":
            # Data Backup: Heal player
            heal_amount = 15
            self.player.heal(heal_amount)
            self.add_to_log(f"Restored {heal_amount} health!")
        
        elif ability.special_effect == "debuff_enemy":
            # Network Isolation: Reduce enemy damage next turn
            self.current_enemy.attack_damage = max(5, int(self.current_enemy.attack_damage * 0.7))
            self.add_to_log("Enemy attack reduced!")
        
        elif ability.special_effect == "security_bonus":
            # Access Control: Extra damage against security threats
            if "security" in self.current_enemy.enemy_type:
                final_damage = int(base_damage * 1.8)
                self.add_to_log("Security expertise! Massive damage!")
        
        return final_damage
    
    def _execute_enemy_turn(self):
        """Execute enemy's turn"""
        if not self.current_enemy or not self.current_enemy.is_alive():
            return
        
        # Enemy attacks
        damage = self.current_enemy.attack_player()
        
        if damage > 0:
            player_died = self.player.take_damage(damage)
            self.add_to_log(f"{self.current_enemy.enemy_type} attacks for {damage} damage!")
            
            if player_died:
                self._handle_defeat()
                return
        else:
            self.add_to_log(f"{self.current_enemy.enemy_type} is preparing to attack...")
        
        # Switch back to player turn
        self.state = CombatState.PLAYER_TURN
        self.turn_timer = 0
    
    def _handle_victory(self):
        """Handle player victory"""
        exp_reward = 50 + (self.current_enemy.max_health // 10)
        self.player.gain_experience(exp_reward)
        
        # Track victory in progress system (if available)
        if hasattr(self.player, 'progress_tracker') and self.player.progress_tracker:
            abilities_used = [ability.name for ability in self.available_abilities if ability.times_used > 0]
            self.player.progress_tracker.win_battle(
                self.current_enemy.enemy_type,
                sum(ability.total_damage_dealt for ability in self.available_abilities),
                self.player.max_health - self.player.health,
                abilities_used
            )
        
        self.add_to_log(f"Victory! Gained {exp_reward} experience!")
        self.state = CombatState.COMBAT_END
        self.turn_timer = 0
    
    def _handle_defeat(self):
        """Handle player defeat"""
        self.add_to_log("Defeat! You have been overwhelmed...")
        self.state = CombatState.COMBAT_END
        self.turn_timer = 0
    
    def _try_flee(self):
        """Attempt to flee from combat"""
        flee_chance = 0.7  # 70% chance to flee
        if random.random() < flee_chance:
            self.add_to_log("Successfully fled from combat!")
            self.end_combat()
        else:
            self.add_to_log("Failed to flee!")
            # Enemy gets a free attack
            self.state = CombatState.ENEMY_TURN
            self.turn_timer = 0
    
    def add_to_log(self, message: str):
        """Add message to combat log"""
        self.combat_log.append(message)
        if len(self.combat_log) > 8:  # Keep only last 8 messages
            self.combat_log.pop(0)
    
    def end_combat(self):
        """End combat and return to normal gameplay"""
        self.active = False
        self.current_enemy = None
        self.player = None
        self.combat_log.clear()
        print("Combat ended")
    
    def render(self, screen: pygame.Surface):
        """Render combat UI"""
        if not self.active:
            return
        
        # Semi-transparent overlay
        overlay = pygame.Surface((screen.get_width(), screen.get_height()))
        overlay.set_alpha(180)
        overlay.fill((20, 20, 40))
        screen.blit(overlay, (0, 0))
        
        # Combat panel
        panel_width = 600
        panel_height = 400
        panel_x = (screen.get_width() - panel_width) // 2
        panel_y = (screen.get_height() - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(screen, (40, 40, 60), panel_rect)
        pygame.draw.rect(screen, (255, 255, 255), panel_rect, 3)
        
        # Fonts
        font_title = pygame.font.Font(None, 28)
        font_text = pygame.font.Font(None, 24)
        font_small = pygame.font.Font(None, 20)
        
        # Title
        title_text = font_title.render("Combat", True, (255, 255, 255))
        screen.blit(title_text, (panel_x + 20, panel_y + 10))
        
        # Enemy info
        if self.current_enemy:
            enemy_text = font_text.render(f"Enemy: {self.current_enemy.enemy_type}", True, (255, 200, 200))
            screen.blit(enemy_text, (panel_x + 20, panel_y + 40))
            
            enemy_health = font_text.render(f"Health: {self.current_enemy.health}/{self.current_enemy.max_health}", True, (255, 200, 200))
            screen.blit(enemy_health, (panel_x + 20, panel_y + 65))
        
        # Player info
        player_health = font_text.render(f"Your Health: {self.player.health}/{self.player.max_health}", True, (200, 255, 200))
        screen.blit(player_health, (panel_x + 300, panel_y + 40))
        
        # Abilities (if player turn)
        if self.state == CombatState.PLAYER_TURN:
            abilities_title = font_text.render("Abilities:", True, (255, 255, 255))
            screen.blit(abilities_title, (panel_x + 20, panel_y + 100))
            
            for i, ability in enumerate(self.available_abilities):
                y_pos = panel_y + 130 + (i * 25)
                
                # Highlight selected ability
                color = (255, 255, 100) if i == self.selected_ability else (255, 255, 255)
                if not ability.can_use():
                    color = (150, 150, 150)
                
                ability_text = f"{ability.name} - {ability.damage} dmg"
                if ability.current_cooldown > 0:
                    ability_text += f" (Cooldown: {ability.current_cooldown})"
                
                ability_surface = font_small.render(ability_text, True, color)
                screen.blit(ability_surface, (panel_x + 40, y_pos))
        
        # Combat log
        log_title = font_text.render("Combat Log:", True, (255, 255, 255))
        screen.blit(log_title, (panel_x + 300, panel_y + 100))
        
        for i, message in enumerate(self.combat_log[-6:]):  # Show last 6 messages
            log_y = panel_y + 130 + (i * 20)
            log_surface = font_small.render(message, True, (200, 200, 200))
            screen.blit(log_surface, (panel_x + 300, log_y))
        
        # Instructions
        if self.state == CombatState.PLAYER_TURN:
            instructions = "UP/DOWN: Select ability | ENTER: Use | ESC: Flee"
        else:
            instructions = "Enemy turn..."
        
        instruction_surface = font_small.render(instructions, True, (255, 255, 255))
        instruction_rect = instruction_surface.get_rect(centerx=panel_rect.centerx, y=panel_y + panel_height - 30)
        screen.blit(instruction_surface, instruction_rect)