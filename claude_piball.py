import pygame
import sys
import math
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
WIDTH = 800
HEIGHT = 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pinball Espacial")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)

# Configurações da física
FPS = 60
GRAVITY = 0.5
BALL_SPEED_LOSS = 0.8
FLIPPER_STRENGTH = 15

class Ball:
    def __init__(self):
        self.radius = 10
        self.reset_position()
        
    def reset_position(self):
        self.x = WIDTH - 50
        self.y = HEIGHT - 200
        self.dx = 0
        self.dy = -20
        
    def update(self):
        # Aplicar gravidade
        self.dy += GRAVITY
        
        # Atualizar posição
        self.x += self.dx
        self.y += self.dy
        
        # Colisão com as paredes
        if self.x - self.radius < 0:
            self.x = self.radius
            self.dx *= -BALL_SPEED_LOSS
        elif self.x + self.radius > WIDTH:
            self.x = WIDTH - self.radius
            self.dx *= -BALL_SPEED_LOSS
            
        if self.y - self.radius < 0:
            self.y = self.radius
            self.dy *= -BALL_SPEED_LOSS
        
        # Verificar se a bola caiu
        if self.y > HEIGHT:
            self.reset_position()
            
    def draw(self):
        pygame.draw.circle(screen, WHITE, (int(self.x), int(self.y)), self.radius)

class Flipper:
    def __init__(self, x, y, length, is_left=True):
        self.x = x
        self.y = y
        self.length = length
        self.angle = 0 if is_left else 180
        self.target_angle = self.angle
        self.is_left = is_left
        self.rotation_speed = 10
        
    def update(self, is_active):
        if is_active:
            self.target_angle = 45 if self.is_left else 135
        else:
            self.target_angle = 0 if self.is_left else 180
            
        # Suavizar a rotação
        angle_diff = self.target_angle - self.angle
        if abs(angle_diff) > self.rotation_speed:
            self.angle += self.rotation_speed * (1 if angle_diff > 0 else -1)
        else:
            self.angle = self.target_angle
            
    def draw(self):
        angle_rad = math.radians(self.angle)
        end_x = self.x + math.cos(angle_rad) * self.length
        end_y = self.y - math.sin(angle_rad) * self.length
        pygame.draw.line(screen, BLUE, (self.x, self.y), (end_x, end_y), 8)

class Obstacle:
    def __init__(self, x, y, width, height, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        
    def draw(self):
        pygame.draw.rect(screen, self.color, self.rect)

class Bumper:
    def __init__(self, x, y, radius):
        self.x = x
        self.y = y
        self.radius = radius
        self.active = False
        self.active_timer = 0
        
    def update(self):
        if self.active:
            self.active_timer -= 1
            if self.active_timer <= 0:
                self.active = False
                
    def activate(self):
        self.active = True
        self.active_timer = 5
        
    def draw(self):
        color = YELLOW if self.active else RED
        pygame.draw.circle(screen, color, (self.x, self.y), self.radius)

class Game:
    def __init__(self):
        self.ball = Ball()
        self.score = 0
        self.lives = 3
        
        # Criar flippers
        self.left_flipper = Flipper(WIDTH//2 - 100, HEIGHT - 100, 80, True)
        self.right_flipper = Flipper(WIDTH//2 + 100, HEIGHT - 100, 80, False)
        
        # Criar obstáculos
        self.obstacles = [
            Obstacle(0, 0, 20, HEIGHT, BLUE),  # Parede esquerda
            Obstacle(WIDTH-20, 0, 20, HEIGHT, BLUE),  # Parede direita
            Obstacle(0, 0, WIDTH, 20, BLUE),  # Teto
        ]
        
        # Criar bumpers
        self.bumpers = [
            Bumper(WIDTH//2, HEIGHT//3, 30),
            Bumper(WIDTH//3, HEIGHT//2, 25),
            Bumper(2*WIDTH//3, HEIGHT//2, 25),
        ]
        
        self.font = pygame.font.Font(None, 36)
        
    def check_collision_with_flipper(self, flipper):
        angle_rad = math.radians(flipper.angle)
        end_x = flipper.x + math.cos(angle_rad) * flipper.length
        end_y = flipper.y - math.sin(angle_rad) * flipper.length
        
        # Verificar distância da bola até a linha do flipper
        line_vec = pygame.math.Vector2(end_x - flipper.x, end_y - flipper.y)
        ball_vec = pygame.math.Vector2(self.ball.x - flipper.x, self.ball.y - flipper.y)
        
        if line_vec.length() > 0:
            projection = ball_vec.dot(line_vec) / line_vec.length()
            if 0 <= projection <= line_vec.length():
                normal = pygame.math.Vector2(-line_vec.y, line_vec.x).normalize()
                distance = abs(ball_vec.dot(normal))
                
                if distance < self.ball.radius + 4:
                    # Aplicar impulso baseado no movimento do flipper
                    impulse = FLIPPER_STRENGTH if flipper.target_angle != flipper.angle else 5
                    self.ball.dx += normal.x * impulse
                    self.ball.dy += normal.y * impulse
                    return True
        return False
    
    def check_collision_with_bumper(self, bumper):
        dx = self.ball.x - bumper.x
        dy = self.ball.y - bumper.y
        distance = math.sqrt(dx*dx + dy*dy)
        
        if distance < self.ball.radius + bumper.radius:
            # Normalizar o vetor de direção
            if distance > 0:
                nx = dx / distance
                ny = dy / distance
            else:
                nx, ny = 1, 0
                
            # Aplicar impulso
            impulse = 15
            self.ball.dx = nx * impulse
            self.ball.dy = ny * impulse
            
            # Ativar o bumper e aumentar a pontuação
            bumper.activate()
            self.score += 100
            return True
        return False
    
    def update(self):
        keys = pygame.key.get_pressed()
        self.left_flipper.update(keys[pygame.K_LEFT])
        self.right_flipper.update(keys[pygame.K_RIGHT])
        
        # Atualizar a bola e verificar colisões
        self.ball.update()
        
        # Verificar colisão com flippers
        self.check_collision_with_flipper(self.left_flipper)
        self.check_collision_with_flipper(self.right_flipper)
        
        # Verificar colisão com bumpers
        for bumper in self.bumpers:
            bumper.update()
            self.check_collision_with_bumper(bumper)
        
        # Verificar colisão com obstáculos
        for obstacle in self.obstacles:
            if obstacle.rect.colliderect(pygame.Rect(
                self.ball.x - self.ball.radius,
                self.ball.y - self.ball.radius,
                self.ball.radius * 2,
                self.ball.radius * 2
            )):
                # Determinar direção da colisão e reverter velocidade
                if abs(self.ball.x - obstacle.rect.centerx) > abs(self.ball.y - obstacle.rect.centery):
                    self.ball.dx *= -BALL_SPEED_LOSS
                else:
                    self.ball.dy *= -BALL_SPEED_LOSS
                    
        # Verificar se a bola caiu
        if self.ball.y > HEIGHT:
            self.lives -= 1
            if self.lives <= 0:
                self.reset_game()
            else:
                self.ball.reset_position()
                
    def reset_game(self):
        self.score = 0
        self.lives = 3
        self.ball.reset_position()
        
    def draw(self):
        screen.fill(BLACK)
        
        # Desenhar elementos do jogo
        self.ball.draw()
        self.left_flipper.draw()
        self.right_flipper.draw()
        
        for obstacle in self.obstacles:
            obstacle.draw()
            
        for bumper in self.bumpers:
            bumper.draw()
            
        # Desenhar pontuação e vidas
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 120, 10))
        
        pygame.display.flip()

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
        game.update()
        game.draw()
        clock.tick(FPS)
        
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()