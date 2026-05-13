import pygame
import random

SCREEN_OLIVIA = 1

# carrega 1 vez só
sprite = None

# estado da personagem
frame = 0
tempo = 0
x = 550
velocidade = 10
velocidade_anim = 50
total_frames = 6
scroll_x = 0
vel_y = 0
gravidade = 0.8
forca_pulo = -15
chao = 515
y = chao

clock = pygame.time.Clock()

TILE_SIZE = 64
EMPTY = 0
BLOCK = 1
SECAO_LARGURA = 1280
MAPA_LINHAS = 10
MAPA_COLUNAS = SECAO_LARGURA // TILE_SIZE  # 20

blocks = None
bloco_img = None
secoes_criadas = None


def gerar_secao(secao):
    random.seed(secao)

    mapa = []
    for row in range(MAPA_LINHAS):
        linha = []
        for col in range(MAPA_COLUNAS):
            if row >= MAPA_LINHAS - 2 and random.random() < 0.18:
                linha.append(BLOCK)  # blocos mais perto do chão
            elif row >= MAPA_LINHAS - 5 and random.random() < 0.08:
                linha.append(BLOCK)  # alguns blocos mais altos
            else:
                linha.append(EMPTY)
        mapa.append(linha)

    return mapa


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_img, row, column, offset_x=0):
        super().__init__()
        self.image = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = offset_x + column * TILE_SIZE
        self.rect.y = row * TILE_SIZE


def olivia_tela(window):
    global sprite, frame, tempo, scroll_x, vel_y, y, blocks, bloco_img, secoes_criadas

    # carrega a imagem só na primeira vez
    if sprite is None:
        sprite = pygame.image.load('assests/sprites/olivia_sprite.png').convert_alpha()

    if bloco_img is None:
        bloco_img = pygame.image.load('assests/imagens/bloco.png').convert_alpha()

    if blocks is None:
        blocks = pygame.sprite.Group()

    if secoes_criadas is None:
        secoes_criadas = set()

    dt = clock.tick(60)

    # desenha fundo
    background = pygame.image.load('assests/imagens/tela oliviarodrigo.png').convert()
    background = pygame.transform.scale(background, (1280, 720))
    bg_w = background.get_width()

    # cria blocos das seções vizinhas ao scroll atual
    secao_atual = scroll_x // SECAO_LARGURA

    for secao in range(secao_atual - 1, secao_atual + 2):
        if secao not in secoes_criadas:
            mapa_secao = gerar_secao(secao)
            for row in range(len(mapa_secao)):
                for col in range(len(mapa_secao[row])):
                    if mapa_secao[row][col] == BLOCK:
                        blocks.add(Tile(bloco_img, row, col, secao * SECAO_LARGURA))
            secoes_criadas.add(secao)

    keys = pygame.key.get_pressed()
    andando = False

    if keys[pygame.K_RIGHT]:
        scroll_x += velocidade
        andando = True

    if keys[pygame.K_LEFT]:
        scroll_x -= velocidade
        andando = True

    # corta o frame certo
    frame_w = sprite.get_width() // total_frames
    frame_h = sprite.get_height()
    rect = pygame.Rect(frame * frame_w, 0, frame_w, frame_h)

    sprite_recortado = sprite.subsurface(rect)
    sprite_menor = pygame.transform.scale(
        sprite_recortado,
        (int(frame_w * 0.65), int(frame_h * 0.65))
    )

    # checa se pode pular
    player_rect = sprite_menor.get_rect(topleft=(x + scroll_x, y))
    pode_pular = False

    if y >= chao:
        pode_pular = True
    else:
        teste = player_rect.move(0, 1)
        for bloco in blocks:
            if teste.colliderect(bloco.rect):
                pode_pular = True
                break

    if keys[pygame.K_SPACE] and pode_pular:
        vel_y = forca_pulo

    # gravidade
    vel_y += gravidade
    y += vel_y

    # colisão vertical com os blocos
    player_rect = sprite_menor.get_rect(topleft=(x + scroll_x, y))
    for bloco in blocks:
        if player_rect.colliderect(bloco.rect):
            if vel_y > 0:  # caindo
                y = bloco.rect.top - player_rect.height
                vel_y = 0
                player_rect.y = y
            elif vel_y < 0:  # subindo
                y = bloco.rect.bottom
                vel_y = 0
                player_rect.y = y

    # chão antigo continua funcionando também
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

    # desenha fundo repetido
    scroll = scroll_x % bg_w
    window.blit(background, (-scroll, 0))
    window.blit(background, (-scroll + bg_w, 0))
    window.blit(background, (-scroll - bg_w, 0))

    # desenha os blocos
    for tile in blocks:
        window.blit(tile.image, (tile.rect.x - scroll_x, tile.rect.y))

    # desenha personagem
    window.blit(sprite_menor, (x, y))

    return SCREEN_OLIVIA