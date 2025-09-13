"""
Progress Tracking and Experience System
"""

import json
import os
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class Achievement:
    """Represents a game achievement"""
    id: str
    name: str
    description: str
    icon: str
    unlocked: bool = False
    unlock_date: Optional[str] = None
    progress: int = 0
    max_progress: int = 1

@dataclass
class LearningStats:
    """Statistics for learning progress"""
    concepts_learned: int = 0
    total_study_time: float = 0.0
    quiz_attempts: int = 0
    quiz_successes: int = 0
    favorite_category: str = ""
    learning_streak: int = 0

@dataclass
class CombatStats:
    """Statistics for combat performance"""
    battles_won: int = 0
    battles_lost: int = 0
    total_damage_dealt: int = 0
    total_damage_taken: int = 0
    enemies_defeated: Dict[str, int] = None
    favorite_ability: str = ""
    
    def __post_init__(self):
        if self.enemies_defeated is None:
            self.enemies_defeated = {}

@dataclass
class ExplorationStats:
    """Statistics for exploration"""
    distance_traveled: float = 0.0
    areas_discovered: int = 0
    secrets_found: int = 0
    time_played: float = 0.0

class ProgressTracker:
    """Tracks player progress, achievements, and statistics"""
    
    def __init__(self, save_file: str = "progress.json"):
        self.save_file = save_file
        
        # Core progress
        self.player_level = 1
        self.total_experience = 0
        self.experience_to_next_level = 100
        
        # Statistics
        self.learning_stats = LearningStats()
        self.combat_stats = CombatStats()
        self.exploration_stats = ExplorationStats()
        
        # Achievements
        self.achievements: Dict[str, Achievement] = {}
        self.unlocked_achievements: List[str] = []
        
        # Session tracking
        self.session_start_time = datetime.now()
        self.session_experience = 0
        self.session_concepts_learned = 0
        
        # Initialize achievements
        self._initialize_achievements()
        
        # Load existing progress
        self.load_progress()
    
    def _initialize_achievements(self):
        """Initialize all available achievements"""
        achievements_data = [
            # Learning achievements
            ("first_concept", "First Steps", "Learn your first cloud concept", "🎓"),
            ("concept_master", "Concept Master", "Learn 5 cloud concepts", "📚", 5),
            ("cloud_expert", "Cloud Expert", "Learn all available concepts", "☁️", 10),
            ("quiz_ace", "Quiz Ace", "Answer 10 quiz questions correctly", "🎯", 10),
            ("perfect_score", "Perfect Score", "Get 100% on any quiz", "⭐"),
            
            # Combat achievements
            ("first_victory", "First Victory", "Win your first battle", "⚔️"),
            ("enemy_hunter", "Enemy Hunter", "Defeat 10 enemies", "🏹", 10),
            ("ability_master", "Ability Master", "Use 5 different abilities in combat", "🔮", 5),
            ("flawless_victory", "Flawless Victory", "Win a battle without taking damage", "🛡️"),
            ("boss_slayer", "Boss Slayer", "Defeat a boss enemy", "👑"),
            
            # Exploration achievements
            ("explorer", "Explorer", "Travel 1000 pixels", "🗺️", 1000),
            ("area_scout", "Area Scout", "Discover all areas in a level", "🔍"),
            ("speed_runner", "Speed Runner", "Complete a level in under 5 minutes", "⚡"),
            
            # Special achievements
            ("dedicated_learner", "Dedicated Learner", "Play for 30 minutes", "⏰", 1800),
            ("comeback_kid", "Comeback Kid", "Win a battle with less than 10% health", "💪"),
            ("efficiency_expert", "Efficiency Expert", "Use abilities with perfect timing", "⚙️"),
        ]
        
        for achievement_data in achievements_data:
            achievement_id = achievement_data[0]
            name = achievement_data[1]
            description = achievement_data[2]
            icon = achievement_data[3]
            max_progress = achievement_data[4] if len(achievement_data) > 4 else 1
            
            self.achievements[achievement_id] = Achievement(
                id=achievement_id,
                name=name,
                description=description,
                icon=icon,
                max_progress=max_progress
            )
    
    def gain_experience(self, amount: int, source: str = "unknown") -> bool:
        """Add experience and check for level up"""
        self.total_experience += amount
        self.session_experience += amount
        
        leveled_up = False
        while self.total_experience >= self.experience_to_next_level:
            self.total_experience -= self.experience_to_next_level
            self.player_level += 1
            self.experience_to_next_level = self._calculate_exp_for_level(self.player_level)
            leveled_up = True
            print(f"Level up! Now level {self.player_level}")
        
        # Check achievements
        self._check_experience_achievements()
        
        return leveled_up
    
    def _calculate_exp_for_level(self, level: int) -> int:
        """Calculate experience required for a given level"""
        return 100 + (level - 1) * 50  # Increasing requirement
    
    def learn_concept(self, concept_id: str):
        """Track learning a new concept"""
        self.learning_stats.concepts_learned += 1
        self.session_concepts_learned += 1
        
        # Update learning streak
        self.learning_stats.learning_streak += 1
        
        # Check achievements
        self._check_learning_achievements()
    
    def complete_quiz(self, concept_id: str, score: float, attempts: int):
        """Track quiz completion"""
        self.learning_stats.quiz_attempts += attempts
        if score >= 70:  # Passing grade
            self.learning_stats.quiz_successes += 1
        
        # Check achievements
        if score == 100:
            self.unlock_achievement("perfect_score")
        
        self._check_learning_achievements()
    
    def win_battle(self, enemy_type: str, damage_dealt: int, damage_taken: int, 
                   abilities_used: List[str]):
        """Track battle victory"""
        self.combat_stats.battles_won += 1
        self.combat_stats.total_damage_dealt += damage_dealt
        self.combat_stats.total_damage_taken += damage_taken
        
        # Track enemy defeats
        if enemy_type in self.combat_stats.enemies_defeated:
            self.combat_stats.enemies_defeated[enemy_type] += 1
        else:
            self.combat_stats.enemies_defeated[enemy_type] = 1
        
        # Track ability usage
        for ability in abilities_used:
            if not self.combat_stats.favorite_ability:
                self.combat_stats.favorite_ability = ability
        
        # Check achievements
        if self.combat_stats.battles_won == 1:
            self.unlock_achievement("first_victory")
        
        if damage_taken == 0:
            self.unlock_achievement("flawless_victory")
        
        total_enemies = sum(self.combat_stats.enemies_defeated.values())
        if total_enemies >= 10:
            self.unlock_achievement("enemy_hunter")
        
        self._check_combat_achievements()
    
    def lose_battle(self, damage_taken: int):
        """Track battle defeat"""
        self.combat_stats.battles_lost += 1
        self.combat_stats.total_damage_taken += damage_taken
    
    def track_movement(self, distance: float):
        """Track player movement for exploration stats"""
        self.exploration_stats.distance_traveled += distance
        
        # Check exploration achievements
        if self.exploration_stats.distance_traveled >= 1000:
            self.unlock_achievement("explorer")
    
    def discover_area(self, area_name: str):
        """Track area discovery"""
        self.exploration_stats.areas_discovered += 1
    
    def update_session_time(self, dt: float):
        """Update session play time"""
        self.exploration_stats.time_played += dt
        
        # Check time-based achievements
        if self.exploration_stats.time_played >= 1800:  # 30 minutes
            self.unlock_achievement("dedicated_learner")
    
    def unlock_achievement(self, achievement_id: str) -> bool:
        """Unlock an achievement"""
        if achievement_id in self.achievements and not self.achievements[achievement_id].unlocked:
            achievement = self.achievements[achievement_id]
            achievement.unlocked = True
            achievement.unlock_date = datetime.now().isoformat()
            self.unlocked_achievements.append(achievement_id)
            
            print(f"🏆 Achievement Unlocked: {achievement.name}")
            print(f"   {achievement.description}")
            
            return True
        return False
    
    def _check_learning_achievements(self):
        """Check for learning-related achievements"""
        if self.learning_stats.concepts_learned >= 1:
            self.unlock_achievement("first_concept")
        
        if self.learning_stats.concepts_learned >= 5:
            self.unlock_achievement("concept_master")
        
        if self.learning_stats.concepts_learned >= 10:
            self.unlock_achievement("cloud_expert")
        
        if self.learning_stats.quiz_successes >= 10:
            self.unlock_achievement("quiz_ace")
    
    def _check_combat_achievements(self):
        """Check for combat-related achievements"""
        # Already handled in win_battle method
        pass
    
    def _check_experience_achievements(self):
        """Check for experience-related achievements"""
        # Could add level-based achievements here
        pass
    
    def get_progress_summary(self) -> Dict:
        """Get a summary of all progress"""
        return {
            'level': self.player_level,
            'experience': self.total_experience,
            'exp_to_next': self.experience_to_next_level,
            'concepts_learned': self.learning_stats.concepts_learned,
            'battles_won': self.combat_stats.battles_won,
            'achievements_unlocked': len(self.unlocked_achievements),
            'total_achievements': len(self.achievements),
            'time_played': self.exploration_stats.time_played,
            'session_exp': self.session_experience,
            'session_concepts': self.session_concepts_learned
        }
    
    def get_achievement_progress(self) -> List[Dict]:
        """Get achievement progress for UI display"""
        achievement_list = []
        for achievement in self.achievements.values():
            achievement_list.append({
                'name': achievement.name,
                'description': achievement.description,
                'icon': achievement.icon,
                'unlocked': achievement.unlocked,
                'progress': achievement.progress,
                'max_progress': achievement.max_progress,
                'unlock_date': achievement.unlock_date
            })
        
        # Sort by unlocked status and name
        achievement_list.sort(key=lambda x: (not x['unlocked'], x['name']))
        return achievement_list
    
    def save_progress(self):
        """Save progress to file"""
        try:
            progress_data = {
                'player_level': self.player_level,
                'total_experience': self.total_experience,
                'learning_stats': asdict(self.learning_stats),
                'combat_stats': asdict(self.combat_stats),
                'exploration_stats': asdict(self.exploration_stats),
                'achievements': {aid: asdict(achievement) for aid, achievement in self.achievements.items()},
                'unlocked_achievements': self.unlocked_achievements,
                'save_date': datetime.now().isoformat()
            }
            
            with open(self.save_file, 'w') as f:
                json.dump(progress_data, f, indent=2)
            
        except Exception as e:
            print(f"Failed to save progress: {e}")
    
    def load_progress(self):
        """Load progress from file"""
        try:
            if os.path.exists(self.save_file):
                with open(self.save_file, 'r') as f:
                    data = json.load(f)
                
                self.player_level = data.get('player_level', 1)
                self.total_experience = data.get('total_experience', 0)
                
                # Load stats
                if 'learning_stats' in data:
                    self.learning_stats = LearningStats(**data['learning_stats'])
                if 'combat_stats' in data:
                    combat_data = data['combat_stats']
                    if 'enemies_defeated' not in combat_data:
                        combat_data['enemies_defeated'] = {}
                    self.combat_stats = CombatStats(**combat_data)
                if 'exploration_stats' in data:
                    self.exploration_stats = ExplorationStats(**data['exploration_stats'])
                
                # Load achievements
                if 'achievements' in data:
                    for aid, achievement_data in data['achievements'].items():
                        if aid in self.achievements:
                            self.achievements[aid] = Achievement(**achievement_data)
                
                self.unlocked_achievements = data.get('unlocked_achievements', [])
                
                print(f"Progress loaded: Level {self.player_level}, {len(self.unlocked_achievements)} achievements")
                
        except Exception as e:
            print(f"Failed to load progress: {e}")
    
    def reset_progress(self):
        """Reset all progress (for testing or new game)"""
        self.player_level = 1
        self.total_experience = 0
        self.experience_to_next_level = 100
        
        self.learning_stats = LearningStats()
        self.combat_stats = CombatStats()
        self.exploration_stats = ExplorationStats()
        
        # Reset achievements
        for achievement in self.achievements.values():
            achievement.unlocked = False
            achievement.unlock_date = None
            achievement.progress = 0
        
        self.unlocked_achievements.clear()
        
        # Delete save file
        if os.path.exists(self.save_file):
            os.remove(self.save_file)
        
        print("Progress reset!")