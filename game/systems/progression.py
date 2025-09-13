"""
Level Progression and Unlock System
"""

from typing import Dict, List, Optional, Set
from dataclasses import dataclass
from enum import Enum

class UnlockType(Enum):
    """Types of unlockable content"""
    LEVEL = "level"
    ABILITY = "ability"
    CONCEPT = "concept"
    ACHIEVEMENT = "achievement"
    FEATURE = "feature"

@dataclass
class UnlockRequirement:
    """Requirement for unlocking content"""
    requirement_type: str  # "level", "concept", "achievement", "enemy_defeats"
    value: str  # The specific requirement (level number, concept ID, etc.)
    count: int = 1  # For requirements that need multiple (e.g., defeat 5 enemies)

@dataclass
class UnlockableContent:
    """Content that can be unlocked"""
    id: str
    name: str
    unlock_type: UnlockType
    requirements: List[UnlockRequirement]
    description: str
    unlocked: bool = False

class LevelProgressionSystem:
    """Manages level progression and content unlocking"""
    
    def __init__(self):
        self.unlocked_levels: Set[str] = {"compute_valley"}  # Start with first level
        self.unlocked_concepts: Set[str] = set()
        self.unlocked_abilities: Set[str] = set()
        self.unlocked_features: Set[str] = set()
        
        # Player progress tracking
        self.player_level = 1
        self.concepts_learned: Set[str] = set()
        self.achievements_earned: Set[str] = set()
        self.enemies_defeated: Dict[str, int] = {}
        
        # Content definitions
        self.unlockable_content: Dict[str, UnlockableContent] = {}
        
        # Initialize unlock system
        self._initialize_unlock_content()
    
    def _initialize_unlock_content(self):
        """Initialize all unlockable content and requirements"""
        
        # Level unlocks
        self.unlockable_content["storage_caverns"] = UnlockableContent(
            id="storage_caverns",
            name="Storage Caverns",
            unlock_type=UnlockType.LEVEL,
            requirements=[
                UnlockRequirement("concept", "ec2_basics"),
                UnlockRequirement("level", "3")
            ],
            description="Explore the depths of cloud storage services"
        )
        
        self.unlockable_content["network_nexus"] = UnlockableContent(
            id="network_nexus",
            name="Network Nexus",
            unlock_type=UnlockType.LEVEL,
            requirements=[
                UnlockRequirement("concept", "s3_storage"),
                UnlockRequirement("concept", "ec2_basics"),
                UnlockRequirement("level", "5")
            ],
            description="Navigate the complex world of cloud networking"
        )
        
        self.unlockable_content["security_citadel"] = UnlockableContent(
            id="security_citadel",
            name="Security Citadel",
            unlock_type=UnlockType.LEVEL,
            requirements=[
                UnlockRequirement("concept", "vpc_networking"),
                UnlockRequirement("level", "7"),
                UnlockRequirement("enemy_defeats", "security_breach", 3)
            ],
            description="Master cloud security in this fortified realm"
        )
        
        self.unlockable_content["devops_domain"] = UnlockableContent(
            id="devops_domain",
            name="DevOps Domain",
            unlock_type=UnlockType.LEVEL,
            requirements=[
                UnlockRequirement("concept", "iam_security"),
                UnlockRequirement("level", "10"),
                UnlockRequirement("achievement", "cloud_expert")
            ],
            description="The ultimate challenge for cloud masters"
        )
        
        # Advanced concept unlocks
        self.unlockable_content["advanced_ec2"] = UnlockableContent(
            id="advanced_ec2",
            name="Advanced EC2 Concepts",
            unlock_type=UnlockType.CONCEPT,
            requirements=[
                UnlockRequirement("concept", "ec2_basics"),
                UnlockRequirement("level", "4"),
                UnlockRequirement("enemy_defeats", "latency_monster", 5)
            ],
            description="Deep dive into EC2 optimization and scaling"
        )
        
        self.unlockable_content["kubernetes_concepts"] = UnlockableContent(
            id="kubernetes_concepts",
            name="Kubernetes & Containers",
            unlock_type=UnlockType.CONCEPT,
            requirements=[
                UnlockRequirement("concept", "lambda_serverless"),
                UnlockRequirement("concept", "advanced_ec2"),
                UnlockRequirement("level", "6")
            ],
            description="Container orchestration in the cloud"
        )
        
        # Advanced ability unlocks
        self.unlockable_content["multi_az_deployment"] = UnlockableContent(
            id="multi_az_deployment",
            name="Multi-AZ Deployment",
            unlock_type=UnlockType.ABILITY,
            requirements=[
                UnlockRequirement("concept", "vpc_networking"),
                UnlockRequirement("concept", "advanced_ec2"),
                UnlockRequirement("level", "8")
            ],
            description="Deploy across multiple availability zones for ultimate resilience"
        )
        
        self.unlockable_content["disaster_recovery"] = UnlockableContent(
            id="disaster_recovery",
            name="Disaster Recovery Protocol",
            unlock_type=UnlockType.ABILITY,
            requirements=[
                UnlockRequirement("concept", "s3_storage"),
                UnlockRequirement("achievement", "flawless_victory"),
                UnlockRequirement("level", "9")
            ],
            description="Ultimate defensive ability that can revive from defeat"
        )
        
        # Feature unlocks
        self.unlockable_content["advanced_combat"] = UnlockableContent(
            id="advanced_combat",
            name="Advanced Combat System",
            unlock_type=UnlockType.FEATURE,
            requirements=[
                UnlockRequirement("level", "5"),
                UnlockRequirement("achievement", "ability_master")
            ],
            description="Unlocks combo attacks and advanced combat mechanics"
        )
        
        self.unlockable_content["cloud_architect_mode"] = UnlockableContent(
            id="cloud_architect_mode",
            name="Cloud Architect Mode",
            unlock_type=UnlockType.FEATURE,
            requirements=[
                UnlockRequirement("level", "15"),
                UnlockRequirement("achievement", "cloud_expert"),
                UnlockRequirement("achievement", "boss_slayer")
            ],
            description="Design and deploy your own cloud architectures"
        )
    
    def update_player_progress(self, level: int, concepts: Set[str], 
                             achievements: Set[str], enemy_defeats: Dict[str, int]):
        """Update player progress for unlock checking"""
        self.player_level = level
        self.concepts_learned = concepts.copy()
        self.achievements_earned = achievements.copy()
        self.enemies_defeated = enemy_defeats.copy()
        
        # Check for new unlocks
        self._check_all_unlocks()
    
    def _check_all_unlocks(self):
        """Check all content for potential unlocks"""
        newly_unlocked = []
        
        for content_id, content in self.unlockable_content.items():
            if not content.unlocked and self._check_requirements(content.requirements):
                content.unlocked = True
                newly_unlocked.append(content)
                
                # Add to appropriate unlock set
                if content.unlock_type == UnlockType.LEVEL:
                    self.unlocked_levels.add(content_id)
                elif content.unlock_type == UnlockType.CONCEPT:
                    self.unlocked_concepts.add(content_id)
                elif content.unlock_type == UnlockType.ABILITY:
                    self.unlocked_abilities.add(content_id)
                elif content.unlock_type == UnlockType.FEATURE:
                    self.unlocked_features.add(content_id)
        
        # Notify about new unlocks
        for content in newly_unlocked:
            print(f"🔓 Unlocked: {content.name}")
            print(f"   {content.description}")
    
    def _check_requirements(self, requirements: List[UnlockRequirement]) -> bool:
        """Check if all requirements are met"""
        for req in requirements:
            if not self._check_single_requirement(req):
                return False
        return True
    
    def _check_single_requirement(self, req: UnlockRequirement) -> bool:
        """Check a single requirement"""
        if req.requirement_type == "level":
            return self.player_level >= int(req.value)
        
        elif req.requirement_type == "concept":
            return req.value in self.concepts_learned
        
        elif req.requirement_type == "achievement":
            return req.value in self.achievements_earned
        
        elif req.requirement_type == "enemy_defeats":
            return self.enemies_defeated.get(req.value, 0) >= req.count
        
        return False
    
    def is_level_unlocked(self, level_id: str) -> bool:
        """Check if a level is unlocked"""
        return level_id in self.unlocked_levels
    
    def is_concept_unlocked(self, concept_id: str) -> bool:
        """Check if a concept is unlocked"""
        return concept_id in self.unlocked_concepts
    
    def is_ability_unlocked(self, ability_id: str) -> bool:
        """Check if an ability is unlocked"""
        return ability_id in self.unlocked_abilities
    
    def is_feature_unlocked(self, feature_id: str) -> bool:
        """Check if a feature is unlocked"""
        return feature_id in self.unlocked_features
    
    def get_available_levels(self) -> List[str]:
        """Get list of available levels"""
        return list(self.unlocked_levels)
    
    def get_next_unlocks(self) -> List[Dict]:
        """Get information about next possible unlocks"""
        next_unlocks = []
        
        for content in self.unlockable_content.values():
            if not content.unlocked:
                # Check how close we are to unlocking
                met_requirements = 0
                total_requirements = len(content.requirements)
                missing_requirements = []
                
                for req in content.requirements:
                    if self._check_single_requirement(req):
                        met_requirements += 1
                    else:
                        missing_requirements.append(self._format_requirement(req))
                
                next_unlocks.append({
                    'name': content.name,
                    'description': content.description,
                    'type': content.unlock_type.value,
                    'progress': f"{met_requirements}/{total_requirements}",
                    'missing': missing_requirements,
                    'close_to_unlock': met_requirements >= total_requirements - 1
                })
        
        # Sort by how close to unlocking
        next_unlocks.sort(key=lambda x: (not x['close_to_unlock'], x['progress']))
        return next_unlocks
    
    def _format_requirement(self, req: UnlockRequirement) -> str:
        """Format a requirement for display"""
        if req.requirement_type == "level":
            return f"Reach level {req.value}"
        elif req.requirement_type == "concept":
            return f"Learn {req.value}"
        elif req.requirement_type == "achievement":
            return f"Earn achievement: {req.value}"
        elif req.requirement_type == "enemy_defeats":
            current = self.enemies_defeated.get(req.value, 0)
            return f"Defeat {req.value} ({current}/{req.count})"
        return str(req.value)
    
    def get_unlock_progress_summary(self) -> Dict:
        """Get summary of unlock progress"""
        total_content = len(self.unlockable_content)
        unlocked_content = sum(1 for content in self.unlockable_content.values() if content.unlocked)
        
        return {
            'total_levels': len([c for c in self.unlockable_content.values() if c.unlock_type == UnlockType.LEVEL]),
            'unlocked_levels': len(self.unlocked_levels),
            'total_concepts': len([c for c in self.unlockable_content.values() if c.unlock_type == UnlockType.CONCEPT]),
            'unlocked_concepts': len(self.unlocked_concepts),
            'total_abilities': len([c for c in self.unlockable_content.values() if c.unlock_type == UnlockType.ABILITY]),
            'unlocked_abilities': len(self.unlocked_abilities),
            'total_features': len([c for c in self.unlockable_content.values() if c.unlock_type == UnlockType.FEATURE]),
            'unlocked_features': len(self.unlocked_features),
            'overall_progress': f"{unlocked_content}/{total_content}"
        }
    
    def force_unlock(self, content_id: str) -> bool:
        """Force unlock content (for testing/debugging)"""
        if content_id in self.unlockable_content:
            content = self.unlockable_content[content_id]
            content.unlocked = True
            
            if content.unlock_type == UnlockType.LEVEL:
                self.unlocked_levels.add(content_id)
            elif content.unlock_type == UnlockType.CONCEPT:
                self.unlocked_concepts.add(content_id)
            elif content.unlock_type == UnlockType.ABILITY:
                self.unlocked_abilities.add(content_id)
            elif content.unlock_type == UnlockType.FEATURE:
                self.unlocked_features.add(content_id)
            
            print(f"Force unlocked: {content.name}")
            return True
        return False