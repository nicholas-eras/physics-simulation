# game_time.py

import pygame

class GameTime:
    def __init__(self):
        self.time_factor = 1  # Fator de tempo padrão (1 = tempo normal)
        self.cooldown = 5000  # Cooldown de 5 segundos para mudar o tempo
        self.last_time_change = pygame.time.get_ticks()

    def update(self):
        current_time = pygame.time.get_ticks()

        # Verificar se o cooldown passou
        if current_time - self.last_time_change > self.cooldown:
            keys = pygame.key.get_pressed()
            
            if keys[pygame.K_a]:  # Pressiona 'A' para desacelerar o tempo
                self.time_factor = 0.5
                self.last_time_change = current_time
            elif keys[pygame.K_d]:  # Pressiona 'D' para acelerar o tempo
                self.time_factor = 2
                self.last_time_change = current_time
            else:
                self.time_factor = 1  # Tempo normal

