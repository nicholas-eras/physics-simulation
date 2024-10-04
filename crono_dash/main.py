import pygame
import sys
from enum import Enum
import random

# Inicialização do Pygame
pygame.init()

# Configurações da tela
LARGURA = 1024
ALTURA = 768
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Chrono Dash")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
VERMELHO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
CINZA = (128, 128, 128)

# Estados do tempo
class EstadoTempo(Enum):
    NORMAL = 1.0
    LENTO = 0.3
    RAPIDO = 2.0
    PARADO = 0.0

# Classe de partículas para efeitos visuais
class Particula:
    def __init__(self, pos, cor, velocidade, tempo_vida, afetada_tempo=True):
        self.pos = pygame.Vector2(pos)
        self.cor = cor
        self.velocidade = pygame.Vector2(velocidade)
        self.tempo_vida = tempo_vida
        self.tempo_inicial = tempo_vida
        self.afetada_tempo = afetada_tempo

    def atualizar(self, dt, estado_tempo):
        # Partículas do jogador não são afetadas pelo tempo
        multiplicador = estado_tempo.value if self.afetada_tempo else 1.0
        self.pos += self.velocidade * dt * multiplicador
        self.tempo_vida -= dt * multiplicador
        return self.tempo_vida > 0

    def desenhar(self, superficie):
        alpha = int((self.tempo_vida / self.tempo_inicial) * 255)
        cor = (*self.cor[:3], alpha)
        pygame.draw.circle(superficie, cor, self.pos, 3)

# Classe base para entidades do jogo
class Entidade:
    def __init__(self, pos, tamanho):
        self.pos = pygame.Vector2(pos)
        self.vel = pygame.Vector2(0, 0)
        self.tamanho = tamanho
        self.rect = pygame.Rect(pos[0], pos[1], tamanho[0], tamanho[1])
        
    def atualizar_rect(self):
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
    def colide_com(self, outra_entidade):
        return self.rect.colliderect(outra_entidade.rect)

# Classe do jogador
class Jogador(Entidade):
    def __init__(self):
        super().__init__((100, ALTURA - 100), (30, 50))
        self.vel = pygame.Vector2(0, 0)
        self.no_chao = False
        self.estado_tempo = EstadoTempo.NORMAL
        self.cor = AZUL
        self.energia_tempo = 100
        self.max_energia = 100
        self.recuperacao_energia = 20
        self.dash_disponivel = True
        self.invulneravel = False
        self.tempo_invulnerabilidade = 0
        self.particulas = []
        self.saude = 100
        
    def aplicar_gravidade(self, dt):
        if not self.no_chao:
            self.vel.y += 981 * dt  # Removido multiplicador de tempo
        
    def mover(self, dt, plataformas):
        # Atualiza posição sem multiplicador de tempo
        movimento = self.vel * dt
        
        # Movimento horizontal
        self.pos.x += movimento.x
        self.atualizar_rect()
        for plataforma in plataformas:
            if self.colide_com(plataforma):
                if movimento.x > 0:
                    self.pos.x = plataforma.rect.left - self.tamanho[0]
                elif movimento.x < 0:
                    self.pos.x = plataforma.rect.right
                self.vel.x = 0
                
        # Movimento vertical
        self.pos.y += movimento.y
        self.atualizar_rect()
        self.no_chao = False
        for plataforma in plataformas:
            if self.colide_com(plataforma):
                if movimento.y > 0:
                    self.pos.y = plataforma.rect.top - self.tamanho[1]
                    self.no_chao = True
                elif movimento.y < 0:
                    self.pos.y = plataforma.rect.bottom
                self.vel.y = 0
                
        # Limites da tela
        if self.pos.x < 0:
            self.pos.x = 0
        elif self.pos.x > LARGURA - self.tamanho[0]:
            self.pos.x = LARGURA - self.tamanho[0]
            
        self.atualizar_rect()
        
        # Atualiza invulnerabilidade (não afetada pelo tempo)
        if self.invulneravel:
            self.tempo_invulnerabilidade -= dt
            if self.tempo_invulnerabilidade <= 0:
                self.invulneravel = False
                
        # Atualiza partículas
        self.particulas = [p for p in self.particulas if p.atualizar(dt, EstadoTempo.NORMAL)]
        
        # Recupera energia
        if self.estado_tempo == EstadoTempo.NORMAL:
            self.energia_tempo = min(self.max_energia, 
                                   self.energia_tempo + self.recuperacao_energia * dt)
    
    def pular(self):
        # if self.no_chao:
            self.vel.y = -500  # Velocidade constante independente do tempo
            self.criar_particulas_pulo()
            
    def dash(self, direcao):
        if self.dash_disponivel and self.energia_tempo >= 30:
            self.vel.x = direcao * 800  # Velocidade constante
            self.vel.y = -200
            self.dash_disponivel = False
            self.energia_tempo -= 30
            self.invulneravel = True
            self.tempo_invulnerabilidade = 0.3
            self.criar_particulas_dash(direcao)
            
    def controlar_tempo(self, novo_estado):
        custo_energia = {
            EstadoTempo.LENTO: 30,
            EstadoTempo.RAPIDO: 40,
            EstadoTempo.PARADO: 50,
            EstadoTempo.NORMAL: 0
        }
        
        if novo_estado != EstadoTempo.NORMAL and self.energia_tempo < custo_energia[novo_estado]:
            return
            
        self.estado_tempo = novo_estado
        if novo_estado != EstadoTempo.NORMAL:
            self.energia_tempo -= custo_energia[novo_estado] * 0.5
            
        cores_estado = {
            EstadoTempo.NORMAL: AZUL,
            EstadoTempo.LENTO: VERMELHO,
            EstadoTempo.RAPIDO: VERDE,
            EstadoTempo.PARADO: AMARELO
        }
        self.cor = cores_estado[novo_estado]
        
    def receber_dano(self, dano):
        if not self.invulneravel:
            self.saude -= dano
            self.invulneravel = True
            self.tempo_invulnerabilidade = 1.0
            return True
        return False
        
    def criar_particulas_pulo(self):
        for _ in range(10):
            vel = (random.uniform(-50, 50), random.uniform(-20, 0))
            pos = (self.pos.x + self.tamanho[0]/2, self.pos.y + self.tamanho[1])
            # Partículas do jogador não são afetadas pelo tempo
            self.particulas.append(Particula(pos, BRANCO, vel, 0.5, afetada_tempo=False))
            
    def criar_particulas_dash(self, direcao):
        for _ in range(20):
            vel = (random.uniform(-100, 100) - direcao * 200, random.uniform(-100, 100))
            pos = (self.pos.x + self.tamanho[0]/2, self.pos.y + self.tamanho[1]/2)
            # Partículas do jogador não são afetadas pelo tempo
            self.particulas.append(Particula(pos, self.cor, vel, 0.3, afetada_tempo=False))
            
    def desenhar(self, superficie):
        # Desenha partículas
        for particula in self.particulas:
            particula.desenhar(superficie)
            
        # Desenha o jogador
        if not self.invulneravel or pygame.time.get_ticks() % 200 < 100:
            pygame.draw.rect(superficie, self.cor, self.rect)
            
        # Desenha barras de status
        energia_rect = pygame.Rect(10, 10, self.energia_tempo * 2, 20)
        pygame.draw.rect(superficie, AMARELO, energia_rect)
        
        saude_rect = pygame.Rect(10, 40, self.saude * 2, 20)
        pygame.draw.rect(superficie, VERMELHO, saude_rect)

# Classe para plataformas
class Plataforma(Entidade):
    def __init__(self, pos, tamanho):
        super().__init__(pos, tamanho)
        self.cor = CINZA
        
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)

# Classe base para inimigos
class Inimigo(Entidade):
    def __init__(self, pos, tamanho, velocidade, dano):
        super().__init__(pos, tamanho)
        self.velocidade = velocidade
        self.direcao = 1
        self.dano = dano
        self.afetado_tempo = True
        self.cor = ROXO
        
    def atualizar(self, dt, estado_tempo, jogador):
        if not self.afetado_tempo or estado_tempo != EstadoTempo.PARADO:
            multiplicador = estado_tempo.value if self.afetado_tempo else 1.0
            self.pos.x += self.velocidade * self.direcao * dt * multiplicador
            
            # Muda direção ao atingir limites
            if self.pos.x <= 0 or self.pos.x >= LARGURA - self.tamanho[0]:
                self.direcao *= -1
                
            self.atualizar_rect()
            
            # Verifica colisão com o jogador
            if self.colide_com(jogador):
                jogador.receber_dano(self.dano)
                
    def desenhar(self, superficie):
        pygame.draw.rect(superficie, self.cor, self.rect)

# Classe para projéteis
class Projetil(Entidade):
    def __init__(self, pos, velocidade, dano):
        super().__init__(pos, (10, 10))
        self.vel = pygame.Vector2(velocidade)
        self.dano = dano
        self.tempo_vida = 3.0
        self.cor = VERMELHO
        
    def atualizar(self, dt, estado_tempo):
        if estado_tempo != EstadoTempo.PARADO:
            self.pos += self.vel * dt * estado_tempo.value
            self.atualizar_rect()
            self.tempo_vida -= dt
            return self.tempo_vida > 0 and 0 <= self.pos.x <= LARGURA and 0 <= self.pos.y <= ALTURA
        return True
        
    def desenhar(self, superficie):
        pygame.draw.circle(superficie, self.cor, self.pos, 5)

# Classe do atirador
class InimigoAtirador(Inimigo):
    def __init__(self, pos):
        super().__init__(pos, (40, 40), 100, 10)
        self.tempo_recarga = 0
        self.intervalo_tiro = 2.0
        self.cor = VERMELHO
        self.projeteis = []
        
    def atualizar(self, dt, estado_tempo, jogador):
        super().atualizar(dt, estado_tempo, jogador)
        
        if estado_tempo != EstadoTempo.PARADO:
            # Atualiza tempo de recarga
            if self.tempo_recarga > 0:
                self.tempo_recarga -= dt * estado_tempo.value
                
            # Atira quando possível
            if self.tempo_recarga <= 0:
                direcao = pygame.Vector2(jogador.pos - self.pos).normalize()
                velocidade = direcao * 300
                self.projeteis.append(Projetil(self.pos.copy(), velocidade, 10))
                self.tempo_recarga = self.intervalo_tiro
                
            # Atualiza projéteis
            self.projeteis = [p for p in self.projeteis 
                            if p.atualizar(dt, estado_tempo)]
            
            # Verifica colisão dos projéteis com o jogador
            for projetil in self.projeteis:
                if projetil.colide_com(jogador):
                    if jogador.receber_dano(projetil.dano):
                        self.projeteis.remove(projetil)
                        
    def desenhar(self, superficie):
        super().desenhar(superficie)
        for projetil in self.projeteis:
            projetil.desenhar(superficie)

# Classe principal do jogo
class Jogo:
    def __init__(self):
        self.jogador = Jogador()
        self.clock = pygame.time.Clock()
        self.rodando = True
        self.fonte = pygame.font.SysFont(None, 36)
        
        # Criar layout do nível
        self.plataformas = [
            Plataforma((0, ALTURA - 40), (LARGURA, 40)),  # Chão
            Plataforma((300, ALTURA - 200), (200, 20)),
            Plataforma((100, ALTURA - 350), (200, 20)),
            Plataforma((500, ALTURA - 500), (200, 20)),
            Plataforma((700, ALTURA - 300), (200, 20)),
        ]
        
        # Criar inimigos
        self.inimigos = [
            Inimigo((400, ALTURA - 80), (30, 30), 150, 10),
            InimigoAtirador((700, ALTURA - 340)),
            Inimigo((200, ALTURA - 230), (30, 30), 100, 15),
            InimigoAtirador((300, ALTURA - 540))
        ]
        
    def processar_eventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    self.jogador.pular()
                elif evento.key == pygame.K_q:
                    self.jogador.controlar_tempo(EstadoTempo.LENTO)
                elif evento.key == pygame.K_e:
                    self.jogador.controlar_tempo(EstadoTempo.RAPIDO)
                elif evento.key == pygame.K_r:
                    self.jogador.controlar_tempo(EstadoTempo.PARADO)
                elif evento.key == pygame.K_LSHIFT:
                    teclas = pygame.key.get_pressed()
                    if teclas[pygame.K_LEFT]:
                        self.jogador.dash(-1)
                    elif teclas[pygame.K_RIGHT]:
                        self.jogador.dash(1)
                elif evento.key == pygame.K_ESCAPE:
                    self.pausar_jogo()
            elif evento.type == pygame.KEYUP:
                if evento.key in (pygame.K_q, pygame.K_e, pygame.K_r):
                    self.jogador.controlar_tempo(EstadoTempo.NORMAL)
                elif evento.key == pygame.K_LSHIFT:
                    self.jogador.dash_disponivel = True
                    
    def pausar_jogo(self):
        pausado = True
        while pausado:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False
                    pausado = False
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        pausado = False
                        
            # Desenha menu de pausa
            superficie_pausa = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
            superficie_pausa.fill((0, 0, 0, 128))
            tela.blit(superficie_pausa, (0, 0))
            
            texto_pausa = self.fonte.render("JOGO PAUSADO", True, BRANCO)
            texto_rect = texto_pausa.get_rect(center=(LARGURA/2, ALTURA/2))
            tela.blit(texto_pausa, texto_rect)
            
            texto_controles = self.fonte.render("ESC para continuar", True, BRANCO)
            texto_rect = texto_controles.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
            tela.blit(texto_controles, texto_rect)
            
            pygame.display.flip()
                    
    def atualizar(self, dt):
        if self.jogador.saude <= 0:
            self.reiniciar_jogo()
            return
            
        # Movimento horizontal
        teclas = pygame.key.get_pressed()
        self.jogador.vel.x = 0
        if teclas[pygame.K_LEFT]:
            self.jogador.vel.x = -300
        if teclas[pygame.K_RIGHT]:
            self.jogador.vel.x = 300
            
        # Atualiza jogador
        self.jogador.aplicar_gravidade(dt)
        self.jogador.mover(dt, self.plataformas)
        
        # Atualiza inimigos
        for inimigo in self.inimigos:
            inimigo.atualizar(dt, self.jogador.estado_tempo, self.jogador)
            
    def reiniciar_jogo(self):
        self.mostrar_game_over()
        self.jogador = Jogador()
        # Reinicia posição dos inimigos
        for inimigo in self.inimigos:
            inimigo.pos = inimigo.pos.copy()
            if isinstance(inimigo, InimigoAtirador):
                inimigo.projeteis.clear()
                
    def mostrar_game_over(self):
        superficie_game_over = pygame.Surface((LARGURA, ALTURA), pygame.SRCALPHA)
        superficie_game_over.fill((0, 0, 0, 200))
        tela.blit(superficie_game_over, (0, 0))
        
        texto_game_over = self.fonte.render("GAME OVER", True, VERMELHO)
        texto_rect = texto_game_over.get_rect(center=(LARGURA/2, ALTURA/2))
        tela.blit(texto_game_over, texto_rect)
        
        texto_reiniciar = self.fonte.render("Reiniciando...", True, BRANCO)
        texto_rect = texto_reiniciar.get_rect(center=(LARGURA/2, ALTURA/2 + 50))
        tela.blit(texto_reiniciar, texto_rect)
        
        pygame.display.flip()
        pygame.time.wait(2000)
        
    def desenhar_hud(self):
        # Instruções
        instrucoes = [
            "CONTROLES:",
            "Setas: Movimento",
            "ESPAÇO: Pular",
            "SHIFT + Direção: Dash",
            "Q: Tempo Lento",
            "E: Tempo Rápido",
            "R: Parar Tempo",
            "ESC: Pausar"
        ]
        
        y = 100
        for instrucao in instrucoes:
            texto = self.fonte.render(instrucao, True, BRANCO)
            tela.blit(texto, (LARGURA - 250, y))
            y += 30
            
    def desenhar(self):
        tela.fill(PRETO)
        
        # Desenha plataformas
        for plataforma in self.plataformas:
            plataforma.desenhar(tela)
            
        # Desenha inimigos
        for inimigo in self.inimigos:
            inimigo.desenhar(tela)
            
        # Desenha jogador
        self.jogador.desenhar(tela)
        
        # Desenha HUD
        self.desenhar_hud()
        
        pygame.display.flip()
        
    def executar(self):
        while self.rodando:
            dt = self.clock.tick(60) / 1000
            self.processar_eventos()
            self.atualizar(dt)
            self.desenhar()
            
        pygame.quit()
        sys.exit()

# Iniciar o jogo
if __name__ == "__main__":
    jogo = Jogo()
    jogo.executar()