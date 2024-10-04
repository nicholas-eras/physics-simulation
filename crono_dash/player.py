# player.py

import pygame
from settings import BLACK

class Player:
    def __init__(self, x, y):
        self.image = pygame.Surface((50, 50))
        self.image.fill(BLACK)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = 5

    def update(self, game_time):
        keys = pygame.key.get_pressed()
        
        # Manipulação do tempo influencia a velocidade do jogador
        movement_speed = self.speed * game_time.time_factor
        
        if keys[pygame.K_LEFT]:
            self.rect.x -= movement_speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += movement_speed
        if keys[pygame.K_UP]:
            self.rect.y -= movement_speed
        if keys[pygame.K_DOWN]:
            self.rect.y += movement_speed

    def draw(self, screen):
        screen.blit(self.image, self.rect)
