import pygame
import math
import random

pygame.init()

largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Gravitação")

verde = (0, 0, 0)
raio = 25
escala = 0.5  # Fator de escala para o zoom out

class Bola:
    def __init__(self, x, y, raio, cor, numero):
        self.x = x
        self.y = y
        self.raio = raio
        self.cor = cor
        self.numero = numero
        self.velocidade_x = 0
        self.velocidade_y = 0
        self.aceleracao_x = 0
        self.aceleracao_y = 0

    def desenhar(self, tela):
        # Aplica a escala ao desenhar
        raio_ajustado = int(self.raio * escala)
        pos_x_ajustada = int(self.x * escala)
        pos_y_ajustada = int(self.y * escala)
        pygame.draw.circle(tela, self.cor, (pos_x_ajustada, pos_y_ajustada), raio_ajustado)
        font = pygame.font.Font(None, 36)
        texto = font.render(str(self.numero), True, (0, 0, 0))
        tela.blit(texto, (pos_x_ajustada - raio_ajustado // 2, pos_y_ajustada - raio_ajustado // 2))

    def verificar_atracao(self, outras_bolas):
        for outra_bola in outras_bolas:
            if outra_bola is not self:
                distancia = math.sqrt((self.x - outra_bola.x)**2 + (self.y - outra_bola.y)**2)

                if distancia == 0:
                    continue
                
                aceleracao_relativa = 10 / distancia ** 2

                angulo_rad, _ = self.calcular_angulo(self, outra_bola)
                self.aceleracao_x += aceleracao_relativa * math.cos(angulo_rad)
                self.aceleracao_y += - aceleracao_relativa * math.sin(angulo_rad)
    
    def mover(self):
        self.velocidade_x += self.aceleracao_x
        self.x += self.velocidade_x

        self.velocidade_y += self.aceleracao_y
        self.y += self.velocidade_y

    def calcular_angulo(self, bola_a, bola_b):
        delta_x = bola_b.x - bola_a.x
        delta_y = bola_a.y - bola_b.y

        angulo_rad = math.atan2(delta_y, delta_x)
        angulo_graus = math.degrees(angulo_rad)

        return angulo_rad, angulo_graus

centro_geometrico_x, centro_geometrico_y = largura / 2 - raio / 2, altura / 2 - raio / 2
bolas = [
    Bola(centro_geometrico_x, centro_geometrico_y, raio * random.uniform(0.7, 1.3), (200, 55, 155), 1),
    Bola(centro_geometrico_x - largura / 4, centro_geometrico_y , raio * random.uniform(0.7, 1.3), (200, 55, 155), 2),
    Bola(centro_geometrico_x, centro_geometrico_y - altura / 4, raio * random.uniform(0.7, 1.3), (55, 155, 200), 3)
]

velocidade_base = 1
for i, bola in enumerate(bolas):
    if i == 0:
        continue
    angulo_radian = random.randint(0, 360) * math.pi / 180
    bola.velocidade_x = velocidade_base * math.cos(angulo_radian)
    bola.velocidade_y = velocidade_base * math.sin(angulo_radian)

clock = pygame.time.Clock()
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    for i, bola in enumerate(bolas):
        if i == 0:
            continue
        bola.verificar_atracao(bolas)
        bola.mover()

    tela.fill(verde)
    for bola in bolas:
        bola.desenhar(tela)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
