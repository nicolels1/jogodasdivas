import pygame

SCREEN_OLIVIA = 1

# carrega 1 vez só
sprite = None

# estado da personagem
frame = 0
tempo = 0
x = 550
velocidade = 10
velocidade_anim = 50
total_frames = 6   # troque para 6 se sua sprite tiver 6 mesmo
scroll_x = 0
vel_y = 0
gravidade = 0.8
forca_pulo = -15
chao = 500
y = chao

clock = pygame.time.Clock()


def olivia_tela(window):
    global sprite, frame, tempo, scroll_x, vel_y, y

    # carrega a imagem só na primeira vez
    if sprite is None:
        sprite = pygame.image.load('assests/sprites/olivia_sprite.png').convert_alpha()

    dt = clock.tick(60)

    keys = pygame.key.get_pressed()
    andando = False

    if keys[pygame.K_RIGHT]:
        scroll_x += velocidade
        andando = True

    if keys[pygame.K_LEFT]:
        scroll_x -= velocidade
        andando = True

    if keys[pygame.K_SPACE] and y >= chao:
        vel_y = forca_pulo

    vel_y += gravidade
    y += vel_y

    if y > chao:
        y = chao
        vel_y = 0

    # animação
    if andando:
        tempo += dt
        if tempo >= velocidade_anim:
            frame = (frame + 1) % total_frames
            tempo = 0
    else:
        frame = 0

    # desenha fundo
    background = pygame.image.load('assests/imagens/tela oliviarodrigo.png').convert()
    background = pygame.transform.scale(background, (1280, 720))

    # corta o frame certo
    frame_w = sprite.get_width() // total_frames
    frame_h = sprite.get_height()
    rect = pygame.Rect(frame * frame_w, 0, frame_w, frame_h)

    #diminui o tamanho do sprite
    sprite_recortado = sprite.subsurface(rect)
    sprite_menor = pygame.transform.scale(
        sprite_recortado,
        (int(frame_w * 0.75), int(frame_h * 0.75))
    )

    #desenha fundo
    bg_w = background.get_width()
    scroll_x = scroll_x % bg_w
    window.blit(background, (-scroll_x, 0))
    window.blit(background, (-scroll_x + bg_w, 0))
    window.blit(background, (-scroll_x - bg_w, 0))

    #desenha personagem
    window.blit(sprite_menor, (x, y))


    return SCREEN_OLIVIA