import pygame 

def olivia_tela(screen):
    DONE = -1
    PLAYING = 1
    BACK_TO_MENU = 0
    state = PLAYING
    
    # ----- Carrega imagem de fundo
    background = pygame.image.load('assests/imagens/tela oliviarodrigo.png').convert()
    background = pygame.transform.scale(background, (1280, 720))

    # ===== Loop principal =====
    while state != DONE:

        # ----- Trata eventos
        for event in pygame.event.get():
            # ----- Verifica consequências
            if event.type == pygame.QUIT:
                state = DONE
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    state = BACK_TO_MENU
        
        # ----- Gera saídas
        screen.blit(background, (0, 0))  # Desenha o fundo na tela
        
        # ----- Atualiza estado do jogo
        pygame.display.update()

    
    return state 