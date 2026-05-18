import pygame
import random

SCREEN_OLIVIA = 1
SCREEN_TAYLOR = 2
SCREEN_OVER = 5

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
forca_pulo = -25
chao = 535
y = chao
moeda_img = None
moedas = None
pontos = 0
fonte = None

clock = pygame.time.Clock()

TILE_SIZE = 100
EMPTY = 0
BLOCK = 1
SECAO_LARGURA = 1280
MAPA_LINHAS = 10
MAPA_COLUNAS = SECAO_LARGURA // TILE_SIZE  # 12

blocks = None
bloco_img = None
secoes_criadas = None

# inimigos
allenemy = None
enemies_criados = None
newenemy = False
start_ticks = pygame.time.get_ticks()

musica_tocando = False

GROUND_ROW = MAPA_LINHAS - 6


def reset_olivia():
    """Reseta todas as variáveis globais da fase Olivia para reiniciar"""
    global sprite, frame, tempo, x, scroll_x, vel_y, y
    global moeda_img, moedas, pontos, fonte
    global blocks, bloco_img, secoes_criadas
    global allenemy, enemies_criados, newenemy, start_ticks
    global musica_tocando
    
    sprite = None
    frame = 0
    tempo = 0
    x = 550
    scroll_x = 0
    vel_y = 0
    y = 535  # chao
    moeda_img = None
    moedas = None
    pontos = 0
    fonte = None
    blocks = None
    bloco_img = None
    secoes_criadas = None
    allenemy = None
    enemies_criados = None
    newenemy = False
    start_ticks = pygame.time.get_ticks()
    musica_tocando = False


def gerar_secao(secao):
    random.seed(secao)

    mapa = [[EMPTY for _ in range(MAPA_COLUNAS)] for _ in range(MAPA_LINHAS)]

    # chão contínuo
    for col in range(MAPA_COLUNAS):
        mapa[GROUND_ROW][col] = BLOCK

    # pequenos buracos no chão
    for _ in range(2):
        gap_start = random.randint(2, MAPA_COLUNAS - 4)
        gap_len = random.randint(2, 3)
        for col in range(gap_start, min(gap_start + gap_len, MAPA_COLUNAS)):
            mapa[GROUND_ROW][col] = EMPTY

    # plataformas mais organizadas
    for _ in range(3):
        row = GROUND_ROW - random.randint(2, 3)
        start = random.randint(0, MAPA_COLUNAS - 5)
        length = random.randint(3, 6)
        for col in range(start, min(start + length, MAPA_COLUNAS)):
            mapa[row][col] = BLOCK

    return mapa


def achar_y_em_cima_do_bloco(x_pos, largura_inimigo=70, altura_inimigo=70):
    """
    Encontra um bloco embaixo do inimigo e devolve o y para ele ficar em cima.
    Se não achar nenhum bloco, usa o chão.
    """
    global blocks

    if blocks is None:
        return chao - altura_inimigo

    centro_x = x_pos + largura_inimigo // 2
    candidatos = []

    for bloco in blocks:
        if bloco.rect.left <= centro_x <= bloco.rect.right:
            candidatos.append(bloco)

    if candidatos:
        bloco_mais_alto = min(candidatos, key=lambda b: b.rect.top)
        return bloco_mais_alto.rect.top - altura_inimigo

    return chao - altura_inimigo


class Moeda(pygame.sprite.Sprite):
    def __init__(self, img, x, y):
        super().__init__()
        self.image = pygame.transform.scale(img, (40, 64))
        self.rect = self.image.get_rect(topleft=(x, y))


class Tile(pygame.sprite.Sprite):
    def __init__(self, tile_img, row, column, offset_x=0):
        super().__init__()
        self.image = pygame.transform.scale(tile_img, (TILE_SIZE, TILE_SIZE))
        self.rect = self.image.get_rect()
        self.rect.x = offset_x + column * TILE_SIZE
        self.rect.y = row * TILE_SIZE


class JogadorTemp(pygame.sprite.Sprite):
    def __init__(self, image, rect):
        super().__init__()
        self.image = image
        self.rect = rect
        self.mask = pygame.mask.from_surface(self.image)


class StillEnemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assests/imagens/paparazzi.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load('assests/imagens/paparazzi.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (70, 70))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

        self.velocidade = 3
        self.limite_esquerda = x - 80
        self.limite_direita = x + 80

    def update(self):
        self.rect.x += self.velocidade

        if self.rect.x <= self.limite_esquerda:
            self.velocidade = abs(self.velocidade)
        elif self.rect.x >= self.limite_direita:
            self.velocidade = -abs(self.velocidade)


def olivia_tela(window):
    global sprite, frame, tempo, scroll_x, vel_y, y
    global blocks, bloco_img, secoes_criadas
    global musica_tocando, moeda_img, moedas, pontos
    global allenemy, enemies_criados, newenemy, start_ticks
    global fonte

    if fonte is None:
        fonte = pygame.font.SysFont('arial', 30)

    if moeda_img is None:
        moeda_img = pygame.image.load('assests/imagens/moeda.png').convert_alpha()

    if moedas is None:
        moedas = pygame.sprite.Group()

    if allenemy is None:
        allenemy = pygame.sprite.Group()

    if enemies_criados is None:
        enemies_criados = set()

    # toca a música só quando entrar nessa tela
    if not musica_tocando:
        pygame.mixer.music.stop()
        pygame.mixer.music.load('assests/sons/brutal.ogg')
        pygame.mixer.music.play(-1)
        musica_tocando = True

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

            for row in range(len(mapa_secao)):
                for col in range(len(mapa_secao[row])):
                    if mapa_secao[row][col] == BLOCK:
                        if random.random() < 0.2:
                            # Verifica se há espaço vazio acima (pelo menos 2 fileiras)
                            tem_espaco_acima = True
                            if row < 2:  # Precisa ter pelo menos 2 fileiras acima
                                tem_espaco_acima = False
                            elif row >= 1:
                                # Verifica se os blocos acima estão vazios
                                if mapa_secao[row - 1][col] == BLOCK or mapa_secao[row - 2][col] == BLOCK:
                                    tem_espaco_acima = False
                            
                            if tem_espaco_acima:
                                moeda_x = secao * SECAO_LARGURA + col * TILE_SIZE + TILE_SIZE // 2 - 20
                                moeda_y = row * TILE_SIZE - 110
                                moedas.add(Moeda(moeda_img, moeda_x, moeda_y))

            # inimigos fixos nessa seção
            coordenadas_still = [
                [780, 100], [1140, 400], [1540, 100], [2000, 100], [2300, 100],
                [2610, 100], [2950, 100], [3230, 100], [3500, 100], [4000, 100]
            ]

            for coord in coordenadas_still:
                ex = coord[0]
                if secao * SECAO_LARGURA <= ex < (secao + 1) * SECAO_LARGURA:
                    if (ex, coord[1]) not in enemies_criados:
                        ey = achar_y_em_cima_do_bloco(ex)
                        still = StillEnemy(ex, ey)
                        allenemy.add(still)
                        enemies_criados.add((ex, coord[1]))

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
        (int(frame_w * 0.50), int(frame_h * 0.50))
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

    # atualiza retângulo do player
    player_rect = sprite_menor.get_rect(topleft=(x + scroll_x, y))

    # coleta moedas
    for moeda in moedas.copy():
        if player_rect.colliderect(moeda.rect):
            moedas.remove(moeda)
            pontos += 1

    # colisão vertical com os blocos
    for bloco in blocks:
        if player_rect.colliderect(bloco.rect):
            if vel_y > 0:
                y = bloco.rect.top - player_rect.height
                vel_y = 0
                player_rect.y = y
            elif vel_y < 0:
                y = bloco.rect.bottom
                vel_y = 0
                player_rect.y = y

    # chão antigo continua funcionando também
    if y > chao:
        y = chao
        vel_y = 0

    # inimigo novo a cada 5s, a partir de 10s
    time_in_seconds = int((pygame.time.get_ticks() - start_ticks) / 1000)

    if time_in_seconds >= 10 and time_in_seconds % 5 == 0 and newenemy is False:
        enemy_x = x + scroll_x + 600
        enemy_y = achar_y_em_cima_do_bloco(enemy_x)
        enemy = Enemy(enemy_x, enemy_y)
        allenemy.add(enemy)
        newenemy = True

    if time_in_seconds % 5 != 0:
        newenemy = False

    # colisão com inimigos
    jogador_temp = JogadorTemp(sprite_menor, player_rect)
    colisoes = pygame.sprite.spritecollide(
        jogador_temp, allenemy, False, pygame.sprite.collide_mask
    )

    if len(colisoes) > 0:
        return SCREEN_OVER

    # animação
    if andando:
        tempo += dt
        if tempo >= velocidade_anim:
            frame = (frame + 1) % total_frames
            tempo = 0
    else:
        frame = 1

    # desenha fundo repetido
    scroll = scroll_x % bg_w
    window.blit(background, (-scroll, 0))
    window.blit(background, (-scroll + bg_w, 0))
    window.blit(background, (-scroll - bg_w, 0))

    # desenha os blocos
    for tile in blocks:
        window.blit(tile.image, (tile.rect.x - scroll_x, tile.rect.y))

    # desenha as moedas
    for moeda in moedas:
        window.blit(moeda.image, (moeda.rect.x - scroll_x, moeda.rect.y))

    # atualiza e desenha inimigos
    for enemy in allenemy:
        if hasattr(enemy, "update"):
            enemy.update()
        window.blit(enemy.image, (enemy.rect.x - scroll_x, enemy.rect.y))

    # desenha personagem
    window.blit(sprite_menor, (x, y))
    texto = fonte.render(f'Moedas: {pontos}', True, (255, 255, 0))
    window.blit(texto, (20, 20))

    # CRITÉRIO DE VITÓRIA: Se pegar 10 moedas, passa para a Taylor Swift!
    if pontos >= 10:
        return SCREEN_TAYLOR

    return SCREEN_OLIVIA