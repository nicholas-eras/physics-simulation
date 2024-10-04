import pygame
import math
import random

# Inicialização do Pygame
pygame.init()

# Dimensões da tela
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Sinuca")

# Cor verde para a mesa
verde = (0, 0, 0)
raio = 25

# Classe Bola
class Bola:
    def __init__(self, x, y, raio, cor, numero):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.numero = numero
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.massa = raio

    def desenhar(self, tela):
        pygame.draw.circle(tela, self.cor, (int(self.x), int(self.y)), self.raio)
        font = pygame.font.Font(None, 36)
        texto = font.render(str(self.numero), True, (0, 0, 0))
        tela.blit(texto, (int(self.x - self.raio / 2), int(self.y - self.raio / 2)))

    def mover(self):
        self.x += self.velocidade_x
        self.y += self.velocidade_y

        # Colisão com as bordas
        if self.x - self.raio <= 0 or self.x + self.raio >= largura:
            self.velocidade_x *= -1
        if self.y - self.raio <= 0 or self.y + self.raio >= altura:
            self.velocidade_y *= -1

    def verificar_colisoes(self, outras_bolas):
        for outra_bola in outras_bolas:
            if outra_bola is not self:
                distancia = math.sqrt((self.x - outra_bola.x)**2 + (self.y - outra_bola.y)**2)

                if distancia < self.raio + outra_bola.raio:
                    # Calculo da direção do vetor de colisão
                    normal_x = outra_bola.x - self.x
                    normal_y = outra_bola.y - self.y
                    normal_length = math.sqrt(normal_x**2 + normal_y**2)

                    if normal_length > 0:  # Para evitar divisão por zero
                        normal_x /= normal_length
                        normal_y /= normal_length

                    # Projetar as velocidades nas normais
                    vel_rel_x = self.velocidade_x - outra_bola.velocidade_x
                    vel_rel_y = self.velocidade_y - outra_bola.velocidade_y

                    velocidade_relativa_normal = vel_rel_x * normal_x + vel_rel_y * normal_y

                    # Verificar se a colisão está acontecendo
                    if velocidade_relativa_normal < 0:
                        return  # Colisão não está ocorrendo

                    # Coeficiente de restituição (elasticidade)
                    e = 1  # Colisão perfeitamente elástica

                    # Cálculo das novas velocidades
                    self.velocidade_x -= (1 + e) * velocidade_relativa_normal * normal_x * outra_bola.massa / (self.massa + outra_bola.massa)
                    self.velocidade_y -= (1 + e) * velocidade_relativa_normal * normal_y * outra_bola.massa / (self.massa + outra_bola.massa)

                    outra_bola.velocidade_x += (1 + e) * velocidade_relativa_normal * normal_x * self.massa / (self.massa + outra_bola.massa)
                    outra_bola.velocidade_y += (1 + e) * velocidade_relativa_normal * normal_y * self.massa / (self.massa + outra_bola.massa)

import random

# Criando 10 bolas com maior variação no raio (70% a 130% do valor original)
bolas = [
    Bola(100, 100, raio * random.uniform(0.7, 1.3), (200, 55, 155), 1),
    Bola(200, 150, raio * random.uniform(0.7, 1.3), (170, 150, 190), 2),
    Bola(300, 200, raio * random.uniform(0.7, 1.3), (100, 255, 100), 3),
    Bola(400, 250, raio * random.uniform(0.7, 1.3), (255, 100, 100), 4),
    Bola(500, 300, raio * random.uniform(0.7, 1.3), (0, 0, 255), 5),
    Bola(600, 350, raio * random.uniform(0.7, 1.3), (255, 255, 0), 6),
    Bola(700, 400, raio * random.uniform(0.7, 1.3), (0, 255, 255), 7),
    Bola(300, 450, raio * random.uniform(0.7, 1.3), (255, 0, 255), 8),
    Bola(400, 100, raio * random.uniform(0.7, 1.3), (120, 255, 120), 9),
    Bola(500, 150, raio * random.uniform(0.7, 1.3), (255, 120, 120), 10)
]

velocidade_base = 1.5

# Definindo velocidades iniciais
for bola in bolas:
    angulo_radian = random.randint(0, 360) * math.pi / 180
    bola.velocidade_x = velocidade_base * math.cos(angulo_radian)
    bola.velocidade_y = velocidade_base * math.sin(angulo_radian)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Atualizar as posições das bolas
    for bola in bolas:
        bola.mover()
        bola.verificar_colisoes(bolas)

    # Desenhar a tela
    tela.fill(verde)
    for bola in bolas:
        bola.desenhar(tela)

    pygame.display.flip()

pygame.quit()
