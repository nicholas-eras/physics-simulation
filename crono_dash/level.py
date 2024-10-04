# level.py (atualizado)

from enemy import Enemy
import pygame

from settings import BLACK

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(BLACK)  # Cor da plataforma (pode mudar para outra cor se quiser)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

class Level:
    def __init__(self, player, game_time):
        self.platforms = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()  # Grupo para inimigos
        self.player = player
        self.game_time = game_time
        self.create_level()

    def create_level(self):
        # Plataformas (x, y, largura, altura)
        platform_data = [
            (100, 500, 200, 20),
            (400, 400, 150, 20),
            (600, 300, 100, 20),
            (300, 200, 200, 20)
        ]
        
        for platform in platform_data:
            plat = Platform(*platform)
            self.platforms.add(plat)

        # Inimigos (x, y, largura, altura, velocidade)
        enemy_data = [
            (150, 480, 40, 40, 2),
            (450, 380, 40, 40, 3)
        ]

        for enemy in enemy_data:
            en = Enemy(*enemy)
            self.enemies.add(en)

    def update(self):
        # Atualizar o movimento e colisão do jogador
        self.player.rect.y += 1  # Testa a gravidade
        hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
        if hits:
            self.player.rect.y = hits[0].rect.top - self.player.rect.height

        # Atualizar inimigos
        self.enemies.update(self.game_time)

    def draw(self, screen):
        self.platforms.draw(screen)
        self.enemies.draw(screen)
