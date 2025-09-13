"""
Audio and Visual Effects System
"""

import pygame
import random
import math
from typing import Dict, List, Optional, Tuple

class AudioManager:
    """Manages game audio and sound effects"""
    
    def __init__(self):
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_volume = 0.7
        self.sfx_volume = 0.8
        self.muted = False
        
        # Initialize mixer if not already done
        if not pygame.mixer.get_init():
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=512)
    
    def load_sound(self, name: str, filepath: str):
        """Load a sound effect"""
        try:
            sound = pygame.mixer.Sound(filepath)
            sound.set_volume(self.sfx_volume)
            self.sounds[name] = sound
        except pygame.error:
            # Create a simple beep sound if file doesn't exist
            self.sounds[name] = self._create_beep_sound()
    
    def _create_beep_sound(self, frequency: int = 440, duration: float = 0.1) -> pygame.mixer.Sound:
        """Create a simple beep sound programmatically"""
        try:
            import numpy as np
            sample_rate = 22050
            frames = int(duration * sample_rate)
            
            # Generate sine wave
            arr = np.sin(2 * np.pi * frequency * np.linspace(0, duration, frames))
            arr = (arr * 32767).astype(np.int16)
            arr = np.repeat(arr.reshape(frames, 1), 2, axis=1)
            
            sound = pygame.sndarray.make_sound(arr)
            sound.set_volume(self.sfx_volume)
            return sound
        except:
            # Fallback: create silent sound
            arr = [[0, 0] for _ in range(1000)]
            try:
                sound = pygame.sndarray.make_sound(arr)
                sound.set_volume(0)
                return sound
            except:
                # Ultimate fallback: return None
                return None
    
    def play_sound(self, name: str, volume: float = 1.0):
        """Play a sound effect"""
        if self.muted or name not in self.sounds or self.sounds[name] is None:
            return
        
        try:
            sound = self.sounds[name]
            sound.set_volume(self.sfx_volume * volume)
            sound.play()
        except:
            pass  # Ignore audio errors
    
    def set_sfx_volume(self, volume: float):
        """Set sound effects volume"""
        self.sfx_volume = max(0.0, min(1.0, volume))
        for sound in self.sounds.values():
            sound.set_volume(self.sfx_volume)
    
    def toggle_mute(self):
        """Toggle mute state"""
        self.muted = not self.muted

class ParticleEffect:
    """Individual particle for effects"""
    
    def __init__(self, x: float, y: float, vel_x: float, vel_y: float, 
                 color: Tuple[int, int, int], size: int, lifetime: float):
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.gravity = 50  # pixels per second squared
    
    def update(self, dt: float) -> bool:
        """Update particle, return False if expired"""
        self.x += self.vel_x * dt
        self.y += self.vel_y * dt
        self.vel_y += self.gravity * dt  # Apply gravity
        
        self.lifetime -= dt
        return self.lifetime > 0
    
    def render(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Render the particle"""
        screen_x = int(self.x - camera_x)
        screen_y = int(self.y - camera_y)
        
        # Fade out over time
        alpha = int(255 * (self.lifetime / self.max_lifetime))
        color = (*self.color, alpha)
        
        # Create surface with alpha
        particle_surface = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(particle_surface, color, (self.size, self.size), self.size)
        
        screen.blit(particle_surface, (screen_x - self.size, screen_y - self.size))

class VisualEffectsManager:
    """Manages visual effects and particles"""
    
    def __init__(self):
        self.particles: List[ParticleEffect] = []
        self.screen_shakes: List[Dict] = []
        self.flash_effects: List[Dict] = []
    
    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int] = (255, 100, 0), 
                        particle_count: int = 20):
        """Create explosion effect"""
        for _ in range(particle_count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(50, 150)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = ParticleEffect(
                x, y, vel_x, vel_y,
                color, random.randint(2, 5),
                random.uniform(0.5, 1.5)
            )
            self.particles.append(particle)
    
    def create_heal_effect(self, x: float, y: float):
        """Create healing effect"""
        for _ in range(15):
            vel_x = random.uniform(-30, 30)
            vel_y = random.uniform(-80, -40)  # Upward motion
            
            particle = ParticleEffect(
                x + random.uniform(-10, 10), y,
                vel_x, vel_y,
                (0, 255, 100), random.randint(3, 6),
                random.uniform(1.0, 2.0)
            )
            particle.gravity = -20  # Negative gravity for floating effect
            self.particles.append(particle)
    
    def create_damage_effect(self, x: float, y: float):
        """Create damage effect"""
        for _ in range(10):
            vel_x = random.uniform(-50, 50)
            vel_y = random.uniform(-60, -20)
            
            particle = ParticleEffect(
                x, y, vel_x, vel_y,
                (255, 50, 50), random.randint(2, 4),
                random.uniform(0.3, 0.8)
            )
            self.particles.append(particle)
    
    def create_learning_effect(self, x: float, y: float):
        """Create learning/knowledge effect"""
        for _ in range(12):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(20, 60)
            vel_x = math.cos(angle) * speed
            vel_y = math.sin(angle) * speed
            
            particle = ParticleEffect(
                x, y, vel_x, vel_y,
                (100, 150, 255), random.randint(3, 5),
                random.uniform(1.5, 2.5)
            )
            particle.gravity = -10  # Slight upward drift
            self.particles.append(particle)
    
    def add_screen_shake(self, intensity: float, duration: float):
        """Add screen shake effect"""
        self.screen_shakes.append({
            'intensity': intensity,
            'duration': duration,
            'max_duration': duration
        })
    
    def add_flash_effect(self, color: Tuple[int, int, int], duration: float, alpha: int = 100):
        """Add screen flash effect"""
        self.flash_effects.append({
            'color': color,
            'duration': duration,
            'max_duration': duration,
            'alpha': alpha
        })
    
    def update(self, dt: float):
        """Update all effects"""
        # Update particles
        self.particles = [p for p in self.particles if p.update(dt)]
        
        # Update screen shakes
        for shake in self.screen_shakes[:]:
            shake['duration'] -= dt
            if shake['duration'] <= 0:
                self.screen_shakes.remove(shake)
        
        # Update flash effects
        for flash in self.flash_effects[:]:
            flash['duration'] -= dt
            if flash['duration'] <= 0:
                self.flash_effects.remove(flash)
    
    def get_screen_shake_offset(self) -> Tuple[int, int]:
        """Get current screen shake offset"""
        if not self.screen_shakes:
            return (0, 0)
        
        total_x = 0
        total_y = 0
        
        for shake in self.screen_shakes:
            intensity = shake['intensity'] * (shake['duration'] / shake['max_duration'])
            total_x += random.uniform(-intensity, intensity)
            total_y += random.uniform(-intensity, intensity)
        
        return (int(total_x), int(total_y))
    
    def render_particles(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Render all particles"""
        for particle in self.particles:
            particle.render(screen, camera_x, camera_y)
    
    def render_flash_effects(self, screen: pygame.Surface):
        """Render screen flash effects"""
        for flash in self.flash_effects:
            alpha = int(flash['alpha'] * (flash['duration'] / flash['max_duration']))
            
            flash_surface = pygame.Surface(screen.get_size())
            flash_surface.set_alpha(alpha)
            flash_surface.fill(flash['color'])
            
            screen.blit(flash_surface, (0, 0))

class AudioVisualManager:
    """Combined audio and visual effects manager"""
    
    def __init__(self):
        self.audio = AudioManager()
        self.visual = VisualEffectsManager()
        
        # Initialize default sounds
        self._initialize_sounds()
    
    def _initialize_sounds(self):
        """Initialize default sound effects"""
        # Create programmatic sounds since we don't have audio files
        self.audio.sounds['hit'] = self.audio._create_beep_sound(200, 0.1)
        self.audio.sounds['heal'] = self.audio._create_beep_sound(600, 0.3)
        self.audio.sounds['learn'] = self.audio._create_beep_sound(800, 0.5)
        self.audio.sounds['level_up'] = self.audio._create_beep_sound(1000, 0.8)
        self.audio.sounds['enemy_hit'] = self.audio._create_beep_sound(150, 0.2)
        self.audio.sounds['ability_use'] = self.audio._create_beep_sound(500, 0.2)
    
    def play_hit_effect(self, x: float, y: float):
        """Play hit effect (audio + visual)"""
        self.audio.play_sound('hit')
        self.visual.create_damage_effect(x, y)
        self.visual.add_screen_shake(3, 0.2)
    
    def play_heal_effect(self, x: float, y: float):
        """Play heal effect (audio + visual)"""
        self.audio.play_sound('heal')
        self.visual.create_heal_effect(x, y)
    
    def play_learning_effect(self, x: float, y: float):
        """Play learning effect (audio + visual)"""
        self.audio.play_sound('learn')
        self.visual.create_learning_effect(x, y)
        self.visual.add_flash_effect((100, 150, 255), 0.5, 50)
    
    def play_level_up_effect(self, x: float, y: float):
        """Play level up effect (audio + visual)"""
        self.audio.play_sound('level_up')
        self.visual.create_explosion(x, y, (255, 215, 0), 30)
        self.visual.add_flash_effect((255, 255, 0), 1.0, 80)
        self.visual.add_screen_shake(5, 0.5)
    
    def play_enemy_defeat_effect(self, x: float, y: float):
        """Play enemy defeat effect (audio + visual)"""
        self.audio.play_sound('enemy_hit')
        self.visual.create_explosion(x, y, (255, 0, 0), 25)
        self.visual.add_screen_shake(4, 0.3)
    
    def play_ability_effect(self, x: float, y: float, ability_type: str):
        """Play ability use effect (audio + visual)"""
        self.audio.play_sound('ability_use')
        
        # Different effects based on ability type
        if 'heal' in ability_type.lower() or 'backup' in ability_type.lower():
            self.visual.create_heal_effect(x, y)
        elif 'attack' in ability_type.lower() or 'damage' in ability_type.lower():
            self.visual.create_explosion(x, y, (100, 150, 255), 15)
        else:
            self.visual.create_learning_effect(x, y)
    
    def update(self, dt: float):
        """Update all effects"""
        self.visual.update(dt)
    
    def render(self, screen: pygame.Surface, camera_x: int = 0, camera_y: int = 0):
        """Render all visual effects"""
        # Apply screen shake
        shake_x, shake_y = self.visual.get_screen_shake_offset()
        
        # Render particles
        self.visual.render_particles(screen, camera_x - shake_x, camera_y - shake_y)
        
        # Render flash effects
        self.visual.render_flash_effects(screen)
    
    def set_volume(self, volume: float):
        """Set audio volume"""
        self.audio.set_sfx_volume(volume)
    
    def toggle_mute(self):
        """Toggle audio mute"""
        self.audio.toggle_mute()