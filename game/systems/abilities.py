"""
Cloud Ability System - Advanced abilities based on cloud concepts
"""

import pygame
import random
from typing import Dict, List, Optional, Tuple
from enum import Enum
from dataclasses import dataclass

class AbilityType(Enum):
    """Types of abilities"""
    OFFENSIVE = "offensive"
    DEFENSIVE = "defensive"
    UTILITY = "utility"
    PASSIVE = "passive"

class AbilityTarget(Enum):
    """Ability targeting"""
    SELF = "self"
    ENEMY = "enemy"
    ALL_ENEMIES = "all_enemies"
    AREA = "area"

@dataclass
class AbilityEffect:
    """Represents an ability effect"""
    effect_type: str
    value: int
    duration: int = 0  # 0 for instant effects
    description: str = ""

class CloudAbilityAdvanced:
    """Advanced cloud ability with complex effects"""
    
    def __init__(self, name: str, concept_id: str, ability_type: AbilityType, 
                 target: AbilityTarget, effects: List[AbilityEffect], 
                 cooldown: int = 0, cost: int = 0):
        self.name = name
        self.concept_id = concept_id
        self.ability_type = ability_type
        self.target = target
        self.effects = effects
        self.cooldown = cooldown
        self.current_cooldown = 0
        self.cost = cost  # Could be mana, energy, etc.
        
        # Usage statistics
        self.times_used = 0
        self.total_damage_dealt = 0
        self.total_healing_done = 0
    
    def can_use(self, player) -> bool:
        """Check if ability can be used"""
        return self.current_cooldown <= 0 and self._has_sufficient_resources(player)
    
    def _has_sufficient_resources(self, player) -> bool:
        """Check if player has sufficient resources (could be extended for mana/energy)"""
        return True  # For now, no resource cost
    
    def use(self, user, target=None) -> List[str]:
        """Use the ability and return list of result messages"""
        if not self.can_use(user):
            return ["Ability not ready!"]
        
        results = []
        self.current_cooldown = self.cooldown
        self.times_used += 1
        
        for effect in self.effects:
            result = self._apply_effect(effect, user, target)
            if result:
                results.append(result)
        
        return results
    
    def _apply_effect(self, effect: AbilityEffect, user, target) -> str:
        """Apply a specific effect"""
        if effect.effect_type == "damage":
            if target and hasattr(target, 'take_damage'):
                actual_damage = target.take_damage(effect.value, self.concept_id)
                self.total_damage_dealt += effect.value
                return f"Dealt {effect.value} damage!"
        
        elif effect.effect_type == "heal":
            if hasattr(user, 'heal'):
                user.heal(effect.value)
                self.total_healing_done += effect.value
                return f"Restored {effect.value} health!"
        
        elif effect.effect_type == "buff_damage":
            # Temporary damage boost (would need status effect system)
            return f"Damage increased by {effect.value}!"
        
        elif effect.effect_type == "debuff_enemy":
            if target and hasattr(target, 'attack_damage'):
                target.attack_damage = max(5, target.attack_damage - effect.value)
                return f"Enemy attack reduced by {effect.value}!"
        
        elif effect.effect_type == "shield":
            # Temporary damage reduction (would need status effect system)
            return f"Shield activated! Reduces incoming damage by {effect.value}!"
        
        return effect.description
    
    def update_cooldown(self):
        """Update cooldown (call each turn)"""
        if self.current_cooldown > 0:
            self.current_cooldown -= 1

class AbilityManager:
    """Manages player abilities and unlocking system"""
    
    def __init__(self):
        self.all_abilities: Dict[str, CloudAbilityAdvanced] = {}
        self.unlocked_abilities: List[str] = []
        self.equipped_abilities: List[str] = []  # Max 4 equipped at once
        self.max_equipped = 4
        
        self._initialize_abilities()
    
    def _initialize_abilities(self):
        """Initialize all cloud abilities"""
        
        # EC2 Abilities
        self.all_abilities["auto_scaling"] = CloudAbilityAdvanced(
            name="Auto Scaling",
            concept_id="ec2_basics",
            ability_type=AbilityType.OFFENSIVE,
            target=AbilityTarget.ENEMY,
            effects=[
                AbilityEffect("damage", 25, description="Scales damage based on enemy health"),
                AbilityEffect("buff_damage", 10, duration=2, description="Increases next attack")
            ],
            cooldown=2
        )
        
        self.all_abilities["load_balancing"] = CloudAbilityAdvanced(
            name="Load Balancing",
            concept_id="ec2_basics",
            ability_type=AbilityType.DEFENSIVE,
            target=AbilityTarget.SELF,
            effects=[
                AbilityEffect("shield", 15, duration=3, description="Distributes incoming damage"),
                AbilityEffect("heal", 10, description="Optimizes resource usage")
            ],
            cooldown=3
        )
        
        # Lambda Abilities
        self.all_abilities["serverless_burst"] = CloudAbilityAdvanced(
            name="Serverless Burst",
            concept_id="lambda_serverless",
            ability_type=AbilityType.OFFENSIVE,
            target=AbilityTarget.ALL_ENEMIES,
            effects=[
                AbilityEffect("damage", 20, description="Instant execution against all enemies")
            ],
            cooldown=0  # No cooldown, true to serverless nature
        )
        
        self.all_abilities["event_driven"] = CloudAbilityAdvanced(
            name="Event-Driven Response",
            concept_id="lambda_serverless",
            ability_type=AbilityType.UTILITY,
            target=AbilityTarget.SELF,
            effects=[
                AbilityEffect("buff_damage", 20, duration=1, description="Reactive damage boost")
            ],
            cooldown=1
        )
        
        # S3 Abilities
        self.all_abilities["data_replication"] = CloudAbilityAdvanced(
            name="Data Replication",
            concept_id="s3_storage",
            ability_type=AbilityType.DEFENSIVE,
            target=AbilityTarget.SELF,
            effects=[
                AbilityEffect("heal", 25, description="Restores from backup"),
                AbilityEffect("shield", 10, duration=2, description="Redundant protection")
            ],
            cooldown=4
        )
        
        self.all_abilities["lifecycle_management"] = CloudAbilityAdvanced(
            name="Lifecycle Management",
            concept_id="s3_storage",
            ability_type=AbilityType.UTILITY,
            target=AbilityTarget.ENEMY,
            effects=[
                AbilityEffect("debuff_enemy", 15, duration=3, description="Optimizes enemy resources away")
            ],
            cooldown=2
        )
        
        # VPC Abilities
        self.all_abilities["network_segmentation"] = CloudAbilityAdvanced(
            name="Network Segmentation",
            concept_id="vpc_networking",
            ability_type=AbilityType.DEFENSIVE,
            target=AbilityTarget.SELF,
            effects=[
                AbilityEffect("shield", 20, duration=4, description="Isolates from attacks")
            ],
            cooldown=3
        )
        
        self.all_abilities["traffic_routing"] = CloudAbilityAdvanced(
            name="Traffic Routing",
            concept_id="vpc_networking",
            ability_type=AbilityType.UTILITY,
            target=AbilityTarget.AREA,
            effects=[
                AbilityEffect("damage", 15, description="Redirects attacks back to enemies")
            ],
            cooldown=2
        )
        
        # IAM Abilities
        self.all_abilities["access_control"] = CloudAbilityAdvanced(
            name="Access Control",
            concept_id="iam_security",
            ability_type=AbilityType.OFFENSIVE,
            target=AbilityTarget.ENEMY,
            effects=[
                AbilityEffect("damage", 35, description="Denies enemy access to resources")
            ],
            cooldown=3
        )
        
        self.all_abilities["principle_least_privilege"] = CloudAbilityAdvanced(
            name="Principle of Least Privilege",
            concept_id="iam_security",
            ability_type=AbilityType.DEFENSIVE,
            target=AbilityTarget.SELF,
            effects=[
                AbilityEffect("debuff_enemy", 25, duration=2, description="Minimizes enemy capabilities")
            ],
            cooldown=4
        )
    
    def unlock_ability(self, concept_id: str) -> List[str]:
        """Unlock abilities for a learned concept"""
        unlocked = []
        for ability_id, ability in self.all_abilities.items():
            if ability.concept_id == concept_id and ability_id not in self.unlocked_abilities:
                self.unlocked_abilities.append(ability_id)
                unlocked.append(ability.name)
        return unlocked
    
    def equip_ability(self, ability_id: str) -> bool:
        """Equip an ability for use in combat"""
        if (ability_id in self.unlocked_abilities and 
            ability_id not in self.equipped_abilities and 
            len(self.equipped_abilities) < self.max_equipped):
            self.equipped_abilities.append(ability_id)
            return True
        return False
    
    def unequip_ability(self, ability_id: str) -> bool:
        """Unequip an ability"""
        if ability_id in self.equipped_abilities:
            self.equipped_abilities.remove(ability_id)
            return True
        return False
    
    def get_equipped_abilities(self) -> List[CloudAbilityAdvanced]:
        """Get list of equipped abilities"""
        return [self.all_abilities[ability_id] for ability_id in self.equipped_abilities 
                if ability_id in self.all_abilities]
    
    def get_unlocked_abilities(self) -> List[CloudAbilityAdvanced]:
        """Get list of all unlocked abilities"""
        return [self.all_abilities[ability_id] for ability_id in self.unlocked_abilities 
                if ability_id in self.all_abilities]
    
    def update_cooldowns(self):
        """Update all ability cooldowns"""
        for ability in self.all_abilities.values():
            ability.update_cooldown()
    
    def get_ability_stats(self) -> Dict[str, Dict]:
        """Get usage statistics for all abilities"""
        stats = {}
        for ability_id, ability in self.all_abilities.items():
            if ability_id in self.unlocked_abilities:
                stats[ability_id] = {
                    'name': ability.name,
                    'times_used': ability.times_used,
                    'total_damage': ability.total_damage_dealt,
                    'total_healing': ability.total_healing_done
                }
        return stats