import pygame
import random
import math
from pygame import mixer

# Inicialização do Pygame
pygame.init()

# Configuração da tela
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Space Invaders")

# Carregando imagens (usando retângulos coloridos como placeholder)
class Sprites:
    def __init__(self):
        self.jogador = pygame.Surface((50, 50))
        self.jogador.fill((0, 255, 0))
        self.inimigo = pygame.Surface((40, 40))
        self.inimigo.fill((255, 0, 0))
        self.tiro = pygame.Surface((5, 15))
        self.tiro.fill((255, 255, 255))
        self.powerup = pygame.Surface((20, 20))
        self.powerup.fill((255, 255, 0))

sprites = Sprites()

# Classes
class Jogador:
    def __init__(self):
        self.x = LARGURA // 2
        self.y = ALTURA - 70
        self.velocidade = 5
        self.vida = 100
        self.pontos = 0
        self.tiros_especiais = 0
        self.superficie = sprites.jogador
        self.rect = self.superficie.get_rect(center=(self.x, self.y))
    
    def mover(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.x > 0:
            self.x -= self.velocidade
        if teclas[pygame.K_RIGHT] and self.x < LARGURA - 50:
            self.x += self.velocidade
        self.rect.centerx = self.x

    def desenhar(self):
        tela.blit(self.superficie, self.rect)

class Inimigo:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidade_x = 2
        self.velocidade_y = 30
        self.superficie = sprites.inimigo
        self.rect = self.superficie.get_rect(center=(self.x, self.y))
        
        if tipo == "elite":
            self.vida = 3
            self.superficie.fill((150, 0, 150))
        else:
            self.vida = 1
            self.superficie.fill((0, 0, 150))

    
    def mover(self):
        self.x += self.velocidade_x
        self.rect.centerx = self.x
        
        # Mudança de direção ao atingir as bordas
        if self.rect.right >= LARGURA or self.rect.left <= 0:
            self.velocidade_x *= -1
            self.y += self.velocidade_y
            self.rect.centery = self.y
    
    def atirar(self):
        if random.random() < 0.01:  # 1% de chance de atirar a cada frame
            return Tiro(self.x, self.y + 20, -1, "inimigo")
        return None

    def desenhar(self):
        tela.blit(self.superficie, self.rect)

class Tiro:
    def __init__(self, x, y, direcao, tipo="normal"):
        self.x = x
        self.y = y
        self.tipo = tipo
        self.velocidade = 7 * direcao
        self.superficie = sprites.tiro
        
        if tipo == "especial":
            self.superficie = pygame.Surface((10, 20))
            self.superficie.fill((0, 255, 255))
        
        self.rect = self.superficie.get_rect(center=(self.x, self.y))
    
    def mover(self):
        self.y += self.velocidade
        self.rect.centery = self.y
    
    def desenhar(self):
        tela.blit(self.superficie, self.rect)

class PowerUp:
    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo  # "vida", "tiro_especial", "velocidade"
        self.velocidade = 2
        self.superficie = sprites.powerup
        self.rect = self.superficie.get_rect(center=(self.x, self.y))
    
    def mover(self):
        self.y += self.velocidade
        self.rect.centery = self.y
    
    def desenhar(self):
        tela.blit(self.superficie, self.rect)

class Explosao:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.tamanho = 20
        self.tempo_vida = 10
    
    def atualizar(self):
        self.tempo_vida -= 1
        self.tamanho += 2
    
    def desenhar(self):
        pygame.draw.circle(tela, (255, 165, 0), (self.x, self.y), self.tamanho)

class Jogo:
    def __init__(self):
        self.jogador = Jogador()
        self.inimigos = []
        self.tiros = []
        self.powerups = []
        self.explosoes = []
        self.nivel = 1
        self.game_over = False
        self.criar_inimigos()
    
    def criar_inimigos(self):
        for i in range(5):  # linhas
            for j in range(8):  # colunas
                tipo = "normal"
                if random.random() < 0.2:  # 20% de chance de ser elite
                    tipo = "elite"
                self.inimigos.append(Inimigo(100 + j * 80, 50 + i * 60, tipo))
    
    def criar_powerup(self, x, y):
        if random.random() < 0.1:  # 10% de chance de criar power-up
            tipo = random.choice(["vida", "tiro_especial", "velocidade"])
            self.powerups.append(PowerUp(x, y, tipo))
    
    def colisao(self, rect1, rect2):
        return rect1.colliderect(rect2)
    
    def atualizar(self):
        if self.game_over:
            return
        
        # Atualizar jogador
        self.jogador.mover()
        
        # Atualizar inimigos
        for inimigo in self.inimigos[:]:
            inimigo.mover()
            tiro_inimigo = inimigo.atirar()
            if tiro_inimigo:
                self.tiros.append(tiro_inimigo)
            
            # Verificar se inimigo chegou muito perto do jogador
            if inimigo.y > ALTURA - 100:
                self.game_over = True
        
        # Atualizar tiros
        for tiro in self.tiros[:]:
            tiro.mover()
            
            # Remover tiros fora da tela
            if tiro.y < 0 or tiro.y > ALTURA:
                self.tiros.remove(tiro)
                continue
            
            # Colisão tiro jogador com inimigos
            if tiro.velocidade < 0:  # Tiro do jogador
                for inimigo in self.inimigos[:]:
                    if self.colisao(tiro.rect, inimigo.rect):
                        inimigo.vida -= 2 if tiro.tipo == "especial" else 1
                        self.explosoes.append(Explosao(inimigo.x, inimigo.y))
                        if inimigo.vida <= 0:
                            self.jogador.pontos += 20 if inimigo.tipo == "elite" else 10
                            self.criar_powerup(inimigo.x, inimigo.y)
                            self.inimigos.remove(inimigo)
                        if tiro in self.tiros:
                            self.tiros.remove(tiro)
            
            # Colisão tiro inimigo com jogador
            elif self.colisao(tiro.rect, self.jogador.rect):
                self.jogador.vida -= 10
                self.explosoes.append(Explosao(self.jogador.x, self.jogador.y))
                self.tiros.remove(tiro)
                if self.jogador.vida <= 0:
                    self.game_over = True
        
        # Atualizar power-ups
        for powerup in self.powerups[:]:
            powerup.mover()
            
            if powerup.y > ALTURA:
                self.powerups.remove(powerup)
            elif self.colisao(powerup.rect, self.jogador.rect):
                if powerup.tipo == "vida":
                    self.jogador.vida = min(100, self.jogador.vida + 20)
                elif powerup.tipo == "tiro_especial":
                    self.jogador.tiros_especiais += 3
                elif powerup.tipo == "velocidade":
                    self.jogador.velocidade = min(10, self.jogador.velocidade + 1)
                self.powerups.remove(powerup)
        
        # Atualizar explosões
        for explosao in self.explosoes[:]:
            explosao.atualizar()
            if explosao.tempo_vida <= 0:
                self.explosoes.remove(explosao)
        
        # Verificar vitória do nível
        if not self.inimigos:
            self.nivel += 1
            self.criar_inimigos()
    
    def desenhar(self):
        # Fundo
        tela.fill((0, 0, 20))
        
        # Desenhar elementos
        self.jogador.desenhar()
        for inimigo in self.inimigos:
            inimigo.desenhar()
        for tiro in self.tiros:
            tiro.desenhar()
        for powerup in self.powerups:
            powerup.desenhar()
        for explosao in self.explosoes:
            explosao.desenhar()
        
        # Interface
        fonte = pygame.font.Font(None, 36)
        
        texto_vida = fonte.render(f'Vida: {self.jogador.vida}', True, (255, 255, 255))
        texto_pontos = fonte.render(f'Pontos: {self.jogador.pontos}', True, (255, 255, 255))
        texto_nivel = fonte.render(f'Nível: {self.nivel}', True, (255, 255, 255))
        texto_especiais = fonte.render(f'Tiros Especiais: {self.jogador.tiros_especiais}', True, (255, 255, 255))
        
        tela.blit(texto_vida, (10, 10))
        tela.blit(texto_pontos, (10, 50))
        tela.blit(texto_nivel, (LARGURA - 100, 10))
        tela.blit(texto_especiais, (LARGURA - 250, 50))
        
        if self.game_over:
            texto_game_over = fonte.render('GAME OVER! Pressione R para reiniciar', True, (255, 0, 0))
            tela.blit(texto_game_over, (LARGURA//2 - 200, ALTURA//2))
        
        pygame.display.update()

def main():
    clock = pygame.time.Clock()
    jogo = Jogo()
    rodando = True
    
    while rodando:
        clock.tick(60)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    if not jogo.game_over:
                        # Tiro normal
                        jogo.tiros.append(Tiro(jogo.jogador.x, jogo.jogador.y - 20, -1))
                elif evento.key == pygame.K_z and jogo.jogador.tiros_especiais > 0:
                    # Tiro especial
                    jogo.tiros.append(Tiro(jogo.jogador.x, jogo.jogador.y - 20, -1, "especial"))
                    jogo.jogador.tiros_especiais -= 1
                elif evento.key == pygame.K_r and jogo.game_over:
                    # Reiniciar jogo
                    jogo = Jogo()
        
        jogo.atualizar()
        jogo.desenhar()
    
    pygame.quit()

if __name__ == "__main__":
    main()