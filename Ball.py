import pygame

class Bola:
    def __init__(self, x, y, raio, cor, numero):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.numero = numero
        self.velocidade_x = 0
        self.velocidade_y = 0

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        font = pygame.font.Font(None, 36)
        texto = font.render(str(self.numero), True, (0, 0, 0))
        tela.blit(texto, (int(self.x - self.raio/2), int(self.y - self.raio/2)))