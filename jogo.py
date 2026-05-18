from olivia import olivia_tela
from taylor import taylor_tela
from ladygaga import ladygaga_tela
from katy import katy_tela
import pygame

# estados
DONE = -1
MENU = 0
SCREEN_OLIVIA = 1
SCREEN_TAYLOR = 2
SCREEN_KATY = 3
SCREEN_LADYGAGA = 4
SCREEN_OVER = 5
SCREEN_WIN = 6

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((1280, 720)) 
pygame.display.set_caption('Jogo das Divas Pop')

# ----- Carrega imagem de fundo
background = pygame.image.load('assests/imagens/tela inicio.png').convert()
background = pygame.transform.scale(background, (1280, 720))

# carrega imagem de game over
gameover_bg = pygame.image.load('assests/imagens/tela gameover.png').convert()
gameover_bg = pygame.transform.scale(gameover_bg, (1280, 720))

# cria botão
botao_img = pygame.image.load('assests/imagens/botao_jogar.png').convert_alpha()
botao_rect = botao_img.get_rect()
botao_rect.midbottom = (1280 // 2, 700)

# gera imagem/musica inicial
pygame.mixer.music.load('assests/sons/ophelia.ogg') 
pygame.mixer.music.play(-1)  

# ----- Inicia estruturas de dados
game = True
screen_state = MENU
fase_atual = SCREEN_OLIVIA  # Guarda a última fase para saber onde reviver

clock = pygame.time.Clock()

# ===== Loop principal =====
while game:
    # ----- 1. TRATA EVENTOS (Cliques e Teclado) -----
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False

        # Eventos no MENU
        if screen_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if botao_rect.collidepoint(event.pos):
                    screen_state = SCREEN_OLIVIA

        # Eventos no GAME OVER (Reiniciar na fase certa)
        elif screen_state == SCREEN_OVER:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                if fase_atual == SCREEN_OLIVIA:
                    from olivia import reset_olivia
                    reset_olivia()
                    screen_state = SCREEN_OLIVIA
                elif fase_atual == SCREEN_TAYLOR:
                    from taylor import reset_taylor
                    reset_taylor()
                    screen_state = SCREEN_TAYLOR
                elif fase_atual == SCREEN_KATY:
                    from katy import reset_katy
                    reset_katy()
                    screen_state = SCREEN_KATY
                elif fase_atual == SCREEN_LADYGAGA:
                    from ladygaga import reset_ladygaga
                    reset_ladygaga()
                    screen_state = SCREEN_LADYGAGA

    # ----- 2. ATUALIZA E DESENHA AS TELAS (Fora do loop de eventos) -----
    if screen_state == MENU:
        window.blit(background, (0, 0))
        window.blit(botao_img, botao_rect)

    elif screen_state == SCREEN_OLIVIA:
        fase_atual = SCREEN_OLIVIA  # Salva que estamos na Olivia
        screen_state = olivia_tela(window)
        
    elif screen_state == SCREEN_TAYLOR:
        fase_atual = SCREEN_TAYLOR  # Salva que estamos na Taylor
        screen_state = taylor_tela(window)
        
    elif screen_state == SCREEN_LADYGAGA:
        fase_atual = SCREEN_LADYGAGA  # Salva que estamos na Gaga
        screen_state = ladygaga_tela(window)
        
    elif screen_state == SCREEN_KATY:
        fase_atual = SCREEN_KATY  # Salva que estamos na Katy
        screen_state = katy_tela(window)
        
    elif screen_state == SCREEN_OVER:
        window.blit(gameover_bg, (0, 0))
        
    elif screen_state == DONE:
        game = False

    pygame.display.flip()
    clock.tick(60)

# ===== Finalização =====
pygame.quit()