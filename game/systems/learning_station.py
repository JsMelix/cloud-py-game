"""Learning Station System"""

class LearningStation:
    def __init__(self, x, y, concept_id, education_system):
        self.x = x
        self.y = y
        self.concept_id = concept_id
        self.education_system = education_system
        self.player_nearby = False
    
    def update(self, player_x, player_y, dt):
        distance = ((player_x - self.x) ** 2 + (player_y - self.y) ** 2) ** 0.5
        self.player_nearby = distance <= 48
    
    def interact(self, player):
        if self.player_nearby:
            concept = self.education_system.get_concept(self.concept_id)
            if concept:
                player.learn_concept(self.concept_id)
                player.gain_experience(100)
                return True
        return False
    
    def get_interaction_prompt(self):
        if self.player_nearby:
            concept = self.education_system.get_concept(self.concept_id)
            if concept:
                return f"Press E to learn: {concept.name}"
        return None

class LearningStationManager:
    def __init__(self, education_system):
        self.education_system = education_system
        self.stations = []
    
    def add_station(self, x, y, concept_id):
        station = LearningStation(x, y, concept_id, self.education_system)
        self.stations.append(station)
    
    def update(self, player_x, player_y, dt):
        for station in self.stations:
            station.update(player_x, player_y, dt)
    
    def handle_event(self, event, player):
        import pygame
        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:
            for station in self.stations:
                if station.interact(player):
                    return True
        return False
    
    def render(self, screen):
        pass