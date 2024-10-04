# enemy.py

import pygame
from settings import RED

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, speed):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.speed = speed
        self.direction = 1  # 1 para direita, -1 para esquerda

    def update(self, game_time):
        # Atualiza o movimento do inimigo com base no fator de tempo
        self.rect.x += self.speed * self.direction * game_time.time_factor

        # Inverte a direção quando atinge uma borda
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.direction *= -1
