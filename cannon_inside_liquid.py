import pygame, math

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Cannon inside Liquid")

raio = 10

# Classe Bola
class Bola:
    def __init__(self, x, y, raio, cor, numero, velocidade, angulo_degrees):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.numero = numero
        self.velocidade = velocidade / 50
        self.velocidade_x =  self.velocidade * math.sin(angulo_degrees * math.pi / 180)
        self.velocidade_y = self.velocidade * math.cos(angulo_degrees * math.pi / 180)
        self.gravity = 0.003

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        self.velocidade_y += - self.gravity

        # Colisão com as bordas
        if self.x - self.raio <= 0 or self.x + self.raio >= largura:
            self.velocidade_x *= -1

        if self.y - self.raio <= altura / 2:
            self.gravity = - 0.002

        if self.y - self.raio >= altura / 2:
            self.gravity = 0.003

# Loop principal
rodando = True
cannon_ball = Bola(largura / 2, altura / 2, raio, (255, 0, 0), 1, 75, 45)
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    cannon_ball.mover()

    # Desenhar a tela
    tela.fill((50, 100, 255), rect=(0, 0, largura, altura / 2))
    tela.fill((0, 0, 100), rect=(0, altura / 2, largura, altura))

    cannon_ball.desenhar(tela)

    pygame.display.flip()

pygame.quit()