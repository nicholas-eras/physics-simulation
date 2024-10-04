import pygame
import math
import numpy as np
from scipy.integrate import odeint

# Inicialização do Pygame
pygame.init()
width = 800
height = 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Pêndulo Duplo Caótico")

# Parâmetros físicos
g = 9.81 / 10  # aceleração da gravidade
L1 = 1.0  # comprimento da primeira haste
L2 = 1.0  # comprimento da segunda haste
m1 = 1.0  # massa do primeiro pêndulo
m2 = 1.0  # massa do segundo pêndulo

# Escala para visualização
scale = 150

# Ponto de origem (centro da tela)
origin = (width // 2, height // 3)

# Cores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

def derivatives(state, t, L1, L2, m1, m2, g):
    """Calcula as derivadas do sistema de equações diferenciais"""
    theta1, omega1, theta2, omega2 = state
    
    c = math.cos(theta1 - theta2)
    s = math.sin(theta1 - theta2)
    
    theta1_dot = omega1
    theta2_dot = omega2
    
    omega1_dot = (-g*(2*m1 + m2)*math.sin(theta1) - m2*g*math.sin(theta1 - 2*theta2)
                  - 2*s*m2*(omega2**2*L2 + omega1**2*L1*c)) / (L1*(2*m1 + m2 - m2*c**2))
    
    omega2_dot = (2*s*(omega1**2*L1*(m1 + m2) + g*(m1 + m2)*math.cos(theta1)
                  + omega2**2*L2*m2*c)) / (L2*(2*m1 + m2 - m2*c**2))
    
    return [theta1_dot, omega1_dot, theta2_dot, omega2_dot]

# Estado inicial [theta1, omega1, theta2, omega2]
state = [math.pi/2, 0, math.pi/2, 0]

# Configuração do tempo
t = np.linspace(0, 0.1, 2)
clock = pygame.time.Clock()

# Lista para armazenar a trajetória
trail = []
max_trail = 100

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Integração numérica
    state = odeint(derivatives, state, t, args=(L1, L2, m1, m2, g))[-1]
    
    # Cálculo das posições
    x1 = origin[0] + L1 * scale * math.sin(state[0])
    y1 = origin[1] + L1 * scale * math.cos(state[0])
    
    x2 = x1 + L2 * scale * math.sin(state[2])
    y2 = y1 + L2 * scale * math.cos(state[2])
    
    # Atualização da trajetória
    trail.append((int(x2), int(y2)))
    if len(trail) > max_trail:
        trail.pop(0)
    
    # Desenho
    screen.fill(BLACK)
    
    # Desenho da trajetória
    if len(trail) > 1:
        pygame.draw.lines(screen, (50, 50, 255), False, trail, 2)
    
    # Desenho das hastes
    pygame.draw.line(screen, WHITE, origin, (int(x1), int(y1)), 2)
    pygame.draw.line(screen, WHITE, (int(x1), int(y1)), (int(x2), int(y2)), 2)
    
    # Desenho das massas
    pygame.draw.circle(screen, RED, (int(x1), int(y1)), 10)
    pygame.draw.circle(screen, RED, (int(x2), int(y2)), 10)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()