import pygame

SCREEN_KATY = 1

sprite = None
background = None

frame = 0
tempo = 0
x = 550
velocidade = 10
velocidade_anim = 50
total_frames = 7
scroll_x = 0
vel_y = 0
gravidade = 0.8
forca_pulo = -15
chao = 550
y = chao

clock = pygame.time.Clock()


def katy_tela(window):
    global sprite, background, frame, tempo, scroll_x, vel_y, y

    if sprite is None:
        sprite = pygame.image.load('assets/sprites/katy_sprite.png').convert_alpha()

    if background is None:
        background = pygame.image.load(
            'assets/sprites/tela_katy_seamless.png'
        ).convert()
        background = pygame.transform.scale(background, (1280, 720))

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

    if andando:
        tempo += dt
        if tempo >= velocidade_anim:
            frame = (frame + 1) % total_frames
            tempo = 0
    else:
        frame = 0

    frame_w = sprite.get_width() // total_frames
    frame_h = sprite.get_height()
    rect = pygame.Rect(frame * frame_w, 0, frame_w, frame_h)

    sprite_recortado = sprite.subsurface(rect)
    sprite_menor = pygame.transform.scale(
        sprite_recortado,
        (int(frame_w * 0.75), int(frame_h * 0.75))
    )

    bg_w = background.get_width()
    scroll_x = scroll_x % bg_w

    window.blit(background, (-scroll_x, 0))
    window.blit(background, (-scroll_x + bg_w, 0))
    window.blit(background, (-scroll_x - bg_w, 0))

    window.blit(sprite_menor, (x, y))

    return SCREEN_KATY