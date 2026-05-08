
import pygame

pygame.init()

# ----- Gera tela principal
window = pygame.display.set_mode((1280, 720)) #No final mudar essa parte para tela cheia 
pygame.display.set_caption('Jogo das Divas Pop')

# ----- Carrega imagem de fundo
background = pygame.image.load('assests/Background inicial.png').convert()
background = pygame.transform.scale(background, (1280, 720))

# ----- Inicia estruturas de dados
game = True

# ===== Loop principal =====
while game:
    # ----- Trata eventos
    for event in pygame.event.get():
        # ----- Verifica consequências
        if event.type == pygame.QUIT:
            game = False

    # ----- Gera saídas
    window.blit(background, (0, 0))  # Desenha o fundo na tela

    # ----- Atualiza estado do jogo
    pygame.display.update()  # Mostra o novo frame para o jogador

# ===== Finalização =====
pygame.quit()  # Função do PyGame que finaliza os recursos utilizados
