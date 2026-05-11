from olivia import olivia_tela
from taylor import taylor_tela
from ladygaga import ladygaga_tela
from katy import katy_tela
import pygame

#estados
DONE = -1
MENU = 0
SCREEN_OLIVIA = 1
SCREEN_TAYLOR = 2
SCREEN_LADY = 3
SCREEN_KATY = 4

pygame.init()
pygame.mixer.init()

# ----- Gera tela principal
window = pygame.display.set_mode((1280, 720)) #No final mudar essa parte para tela cheia 
pygame.display.set_caption('Jogo das Divas Pop')

# ----- Carrega imagem de fundo
background = pygame.image.load('assests/imagens/tela inicio.png').convert()
background = pygame.transform.scale(background, (1280, 720))

#cria botão
botao_img = pygame.image.load('assests/imagens/botao_jogar.png').convert_alpha()
botao_rect = botao_img.get_rect()
botao_rect.midbottom = (1280 // 2, 700)

#gera imagem
pygame.mixer.music.load('assests/sons/ophelia.ogg') # mudar para a musica de introdução
pygame.mixer.music.play(-1)  # toca em loop até fechar o jogo

# ----- Inicia estruturas de dados
game = True
screen_state = MENU

clock = pygame.time.Clock()


# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

            # clique no botão (só no menu)
        if screen_state == MENU:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if botao_rect.collidepoint(event.pos):
                        screen_state = SCREEN_OLIVIA

    if screen_state == MENU:
        window.blit(background, (0, 0))

        # desenha botão imagem
        window.blit(botao_img, botao_rect)

    if screen_state == SCREEN_OLIVIA:
        screen_state = olivia_tela(window)
    elif screen_state == SCREEN_TAYLOR:
        screen_state = taylor_tela(window)
    elif screen_state == SCREEN_LADY:
        screen_state = ladygaga_tela(window)
    elif screen_state == SCREEN_KATY:
        screen_state = katy_tela(window)
    elif screen_state == DONE:
        game = False

    pygame.display.flip()
    clock.tick(60)

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
