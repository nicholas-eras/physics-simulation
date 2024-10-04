import pygame, math, time

pygame.init()

# Dimensões da janela
largura, altura = 1000, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pendulum")

class Bola:
    def __init__(self, x, y, altura_do_fio, angulo_inicial, ponto_suporte):
        self.x = x
        self.initial_y = y    
        self.y = self.initial_y    
        self.raio = 15
        self.amplitude = math.radians(angulo_inicial)  # Amplitude em radianos
        self.angulo = self.amplitude  # Ângulo inicial
        self.length = altura_do_fio  # Comprimento do fio (altura)
        self.gravity = 1  # Gravidade
        self.velocidade_angular = 0  # Velocidade angular inicial
        self.ponto_suporte = ponto_suporte

    def desenhar(self, tela):
        # Desenha a linha (fio)
        ponto_fixo = (largura // 2, self.ponto_suporte)  # Ponto de fixação no topo da tela
        bola_pos = (int(self.x), int(self.y))
        pygame.draw.line(tela, (255, 255, 255), ponto_fixo, bola_pos, 2)
        # Desenha a bola (pêndulo)
        pygame.draw.circle(tela, (255, 255, 255), bola_pos, self.raio)

    def mover(self):
        # Cálculo da aceleração angular (usando a equação do pêndulo simples)
        aceleracao_angular = (-self.gravity / self.length) * math.sin(self.angulo)
        # Atualiza a velocidade angular e ângulo
        self.velocidade_angular += aceleracao_angular
        self.angulo += self.velocidade_angular

        # Atualiza a posição X e Y com base no ângulo atual
        self.x = largura // 2 + self.length * math.sin(self.angulo)
        self.y = self.length * math.cos(self.angulo)

class Bola:
    def __init__(self, x, y, altura_do_fio, angulo_inicial, ponto_suporte):
        self.x = x
        self.initial_y = y    
        self.y = self.initial_y    
        self.raio = 15
        self.amplitude = math.radians(angulo_inicial)  # Amplitude em radianos
        self.angulo = self.amplitude  # Ângulo inicial
        self.length = altura_do_fio  # Comprimento do fio (altura)
        self.gravity = 1  # Gravidade
        self.velocidade_angular = 0  # Velocidade angular inicial
        self.ponto_suporte = ponto_suporte

    def desenhar(self, tela):
        # Desenha a linha (fio)
        ponto_fixo = (largura // 2, self.ponto_suporte)  # Ponto de fixação no topo da tela
        bola_pos = (int(self.x), int(self.y))
        pygame.draw.line(tela, (255, 255, 255), ponto_fixo, bola_pos, 2)
        # Desenha a bola (pêndulo)
        pygame.draw.circle(tela, (255, 255, 255), bola_pos, self.raio)

    def mover(self):
        # Cálculo da aceleração angular (usando a equação do pêndulo simples)
        aceleracao_angular = (-self.gravity / self.length) * math.sin(self.angulo)
        # Atualiza a velocidade angular e ângulo
        self.velocidade_angular += aceleracao_angular
        self.angulo += self.velocidade_angular

        # Atualiza a posição X e Y com base no ângulo atual
        self.x = largura // 2 + self.length * math.sin(self.angulo)
        self.y = self.length * math.cos(self.angulo)

class Bola2:
    def __init__(self, x, y, altura_do_fio, angulo_inicial, ponto_suporte, bola):
        self.x = x
        self.initial_y = y    
        self.y = self.initial_y    
        self.raio = 15
        self.amplitude = math.radians(angulo_inicial)  # Amplitude em radianos
        self.angulo = self.amplitude  # Ângulo inicial
        self.length = altura_do_fio / 2  # Comprimento do fio (altura)
        self.gravity = 1  # Gravidade
        self.velocidade_angular = 0  # Velocidade angular inicial
        self.ponto_suporte = ponto_suporte
        self.bola = bola

    def desenhar(self, tela):
        # Desenha a linha (fio)
        ponto_fixo = (self.bola.x, self.bola.y)  # Ponto de fixação no topo da tela
        bola_pos = (int(self.x), int(self.y))
        pygame.draw.line(tela, (255, 255, 255), ponto_fixo, bola_pos, 2)
        # Desenha a bola (pêndulo)
        pygame.draw.circle(tela, (255, 255, 255), bola_pos, self.raio)

    def mover(self):
        # Cálculo da aceleração angular (usando a equação do pêndulo simples)
        aceleracao_angular = (-self.gravity / self.length) * math.sin(self.angulo)
        # Atualiza a velocidade angular e ângulo
        self.velocidade_angular += aceleracao_angular
        self.angulo += self.velocidade_angular

        # Atualiza a posição X e Y com base no ângulo atual
        self.x = self.bola.x + self.length * math.sin(self.angulo)
        self.y = self.bola.y + self.length * math.cos(self.angulo)

# Inicializa a bola (pêndulo) com ponto inicial no meio da tela e fio de comprimento 300
pendulo_1 = Bola(largura // 2, altura // 4, 300, 45, 0)  # Ângulo inicial de 45 graus
pendulo_2 = Bola2(pendulo_1.x, pendulo_1.y + pendulo_1.length, 300, 45, pendulo_1.y, pendulo_1)  # Ângulo inicial de 45 graus

rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Movimenta o pêndulo
    pendulo_1.mover()
    pendulo_2.mover()

    # Desenha a cena
    tela.fill((0, 0, 0))
    pendulo_1.desenhar(tela)
    pendulo_2.desenhar(tela)

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
