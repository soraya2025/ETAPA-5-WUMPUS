import pygame
import sys
import time
import os
from mundo import Mundo
from agente import Agente

def obter_percepcoes(mundo, pos):
    x, y = pos
    percepcoes = set()
    vizinhos = [(x-1,y), (x+1,y), (x,y-1), (x,y+1)]
    
    for i, j in vizinhos:
        if 0 <= i < len(mundo) and 0 <= j < len(mundo):
            if mundo[i][j] == "P":
                percepcoes.add("brisa")
            elif mundo[i][j] == "W":
                percepcoes.add("fedor")
            elif mundo[i][j] == "O":
                percepcoes.add("brilho")
    
    return percepcoes


pygame.init()
pygame.font.init()

TAMANHO_CELULA = 80
MARGIN = 10

BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
CINZA = (200, 200, 200)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
AMARELO = (255, 255, 0)
ROXO = (128, 0, 128)
LARANJA = (255, 165, 0)

base_dir = os.path.dirname(os.path.abspath(__file__))
IMAGENS_DIR = os.path.join(base_dir, "imagens")

try:
    img_agente = pygame.image.load(os.path.join(IMAGENS_DIR, "agente.png"))
    img_ouro = pygame.image.load(os.path.join(IMAGENS_DIR, "ouro.png"))
    img_poco = pygame.image.load(os.path.join(IMAGENS_DIR, "poco.png"))
    img_wumpus = pygame.image.load(os.path.join(IMAGENS_DIR, "wumpus.png"))
    img_brisa = pygame.image.load(os.path.join(IMAGENS_DIR, "brisa.png"))
    img_fedor = pygame.image.load(os.path.join(IMAGENS_DIR, "fedor.png"))
    img_brilho = pygame.image.load(os.path.join(IMAGENS_DIR, "brilho.png"))
except pygame.error as e:
    print(f"Erro ao carregar imagem: {e}. Verifique se o caminho '{IMAGENS_DIR}' existe e contém os arquivos.")
    img_agente = pygame.Surface((TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)); img_agente.fill(AZUL)
    img_ouro = pygame.Surface((TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)); img_ouro.fill(AMARELO)
    img_poco = pygame.Surface((TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)); img_poco.fill(PRETO)
    img_wumpus = pygame.Surface((TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)); img_wumpus.fill(VERMELHO)
    img_brisa = pygame.Surface((20, 20)); img_brisa.fill(AZUL)
    img_fedor = pygame.Surface((20, 20)); img_fedor.fill(ROXO)
    img_brilho = pygame.Surface((20, 20)); img_brilho.fill(AMARELO)


fonte_pequena = pygame.font.SysFont("arial", 16)
fonte_media = pygame.font.SysFont("arial", 20)
fonte_grande = pygame.font.SysFont("arial", 28)

def desenhar_celula(screen, x, y, conteudo, agente_pos=None):
    rect = pygame.Rect(y * TAMANHO_CELULA, x * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
    
    cor_fundo = BRANCO
    if conteudo == "V":
        cor_fundo = (220, 255, 220)
    elif conteudo == "B":
        cor_fundo = (220, 220, 255)
    elif conteudo == "F":
        cor_fundo = (255, 220, 220)
    
    pygame.draw.rect(screen, cor_fundo, rect)
    pygame.draw.rect(screen, PRETO, rect, 1)

    if conteudo == "B":
        screen.blit(pygame.transform.scale(img_brisa, (20, 20)), (y * TAMANHO_CELULA + 5, x * TAMANHO_CELULA + 5))
    elif conteudo == "F":
        screen.blit(pygame.transform.scale(img_fedor, (20, 20)), (y * TAMANHO_CELULA + 5, x * TAMANHO_CELULA + 5))

    if agente_pos and agente_pos[0] == x and agente_pos[1] == y:
        screen.blit(pygame.transform.scale(img_agente, (TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)), 
                    (y * TAMANHO_CELULA + 5, x * TAMANHO_CELULA + 5))


def desenhar_ambiente_real(screen, mundo_matriz, offset_x, offset_y):
    n = len(mundo_matriz)
    for i in range(n):
        for j in range(n):
            rect = pygame.Rect(offset_x + j * TAMANHO_CELULA, offset_y + i * TAMANHO_CELULA, TAMANHO_CELULA, TAMANHO_CELULA)
            pygame.draw.rect(screen, BRANCO, rect)
            pygame.draw.rect(screen, CINZA, rect, 1)
            
            if mundo_matriz[i][j] == "W":
                screen.blit(pygame.transform.scale(img_wumpus, (TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)), 
                            (offset_x + j * TAMANHO_CELULA + 5, offset_y + i * TAMANHO_CELULA + 5))
            elif mundo_matriz[i][j] == "P":
                screen.blit(pygame.transform.scale(img_poco, (TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)), 
                            (offset_x + j * TAMANHO_CELULA + 5, offset_y + i * TAMANHO_CELULA + 5))
            elif mundo_matriz[i][j] == "O":
                screen.blit(pygame.transform.scale(img_ouro, (TAMANHO_CELULA - 10, TAMANHO_CELULA - 10)), 
                            (offset_x + j * TAMANHO_CELULA + 5, offset_y + i * TAMANHO_CELULA + 5))


def desenhar_info_agente(screen, agente, percepcoes, n_grid, info_width):
    start_y = n_grid * TAMANHO_CELULA + MARGIN
    
    texto_pos = fonte_media.render(f"Posição: {agente.pos}", True, PRETO)
    screen.blit(texto_pos, (MARGIN, start_y))
    
    texto_passos = fonte_media.render(f"Passos: {agente.passos}", True, PRETO)
    screen.blit(texto_passos, (MARGIN, start_y + 30))

    texto_percepcoes_label = fonte_media.render("Percepções:", True, PRETO)
    screen.blit(texto_percepcoes_label, (MARGIN, start_y + 60))
    offset_x_percepcoes = MARGIN + texto_percepcoes_label.get_width() + 5
    
    if "brisa" in percepcoes:
        screen.blit(pygame.transform.scale(img_brisa, (20, 20)), (offset_x_percepcoes, start_y + 60))
        offset_x_percepcoes += 25
    if "fedor" in percepcoes:
        screen.blit(pygame.transform.scale(img_fedor, (20, 20)), (offset_x_percepcoes, start_y + 60))
        offset_x_percepcoes += 25
    if "brilho" in percepcoes:
        screen.blit(pygame.transform.scale(img_brilho, (20, 20)), (offset_x_percepcoes, start_y + 60))
        offset_x_percepcoes += 25

    texto_ouro = fonte_media.render(f"Ouro: {'Sim' if agente.ouro else 'Não'}", True, PRETO)
    screen.blit(texto_ouro, (MARGIN, start_y + 90))

    texto_flechas = fonte_media.render(f"Flechas: {agente.flechas}", True, PRETO)
    screen.blit(texto_flechas, (MARGIN, start_y + 120))


def iniciar_jogo_grafico_automatizado():
    try:
        n = int(input("Digite o tamanho da matriz (n >= 3): "))
        while n < 3:
            n = int(input("Valor inválido. Digite um número >= 3: "))
    except ValueError:
        print("Entrada inválida. Usando o tamanho padrão n=4.")
        n = 4

    INFO_HEIGHT = 200 
    WIDTH = n * TAMANHO_CELULA * 2 + MARGIN * 3
    HEIGHT = n * TAMANHO_CELULA + INFO_HEIGHT + MARGIN * 2

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Mundo de Wumpus - Agente Inteligente (Etapa 3)")

    ambiente = Mundo(n)
    agente = Agente(n)
    matriz_mundo = ambiente.matriz

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    pass

        percepcoes_atuais = obter_percepcoes(matriz_mundo, agente.pos)
        acao = agente.decidir_acao(percepcoes_atuais)
        terminou = agente.executar_acao(acao, matriz_mundo)

        screen.fill(BRANCO)

        offset_x_real = n * TAMANHO_CELULA + MARGIN * 2
        pygame.draw.rect(screen, LARANJA, (offset_x_real - 5, MARGIN - 5, n * TAMANHO_CELULA + 10, n * TAMANHO_CELULA + 10), 2)
        texto_real = fonte_grande.render("Mundo Real", True, PRETO)
        screen.blit(texto_real, (offset_x_real + n * TAMANHO_CELULA / 2 - texto_real.get_width() / 2, MARGIN - 30))
        desenhar_ambiente_real(screen, matriz_mundo, offset_x_real, MARGIN)

        pygame.draw.rect(screen, AZUL, (MARGIN - 5, MARGIN - 5, n * TAMANHO_CELULA + 10, n * TAMANHO_CELULA + 10), 2)
        texto_memoria = fonte_grande.render("Memória do Agente", True, PRETO)
        screen.blit(texto_memoria, (MARGIN + n * TAMANHO_CELULA / 2 - texto_memoria.get_width() / 2, MARGIN - 30))
        for i in range(n):
            for j in range(n):
                desenhar_celula(screen, i, j, agente.memoria[i][j], agente.pos)

        desenhar_info_agente(screen, agente, percepcoes_atuais, n, INFO_HEIGHT)
        
        pygame.display.flip()

        print(f"Agente em {agente.pos}, Percepções: {percepcoes_atuais}, Ação: {acao}")

        x, y = agente.pos
        if matriz_mundo[x][y] == "P":
            print("\nGame Over! O agente caiu em um poço.")
            agente.vivo = False
        elif matriz_mundo[x][y] == "W":
            print("\nGame Over! O agente encontrou o Wumpus.")
            agente.vivo = False
        
        if not agente.vivo or terminou:
            running = False
            
        time.sleep(0.5)

    screen.fill(BRANCO)
    if agente.ouro and agente.pos == [0,0]:
        mensagem = fonte_grande.render("VITÓRIA! O agente escapou com o ouro!", True, VERDE)
    elif not agente.vivo:
        if matriz_mundo[agente.pos[0]][agente.pos[1]] == "P":
             mensagem = fonte_grande.render("DERROTA! O agente caiu no poço!", True, VERMELHO)
        else:
             mensagem = fonte_grande.render("DERROTA! O agente encontrou o Wumpus!", True, VERMELHO)
    else:
        mensagem = fonte_grande.render("Fim do Jogo. Nenhuma vitória ou derrota clara.", True, PRETO)

    rect_mensagem = mensagem.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(mensagem, rect_mensagem)
    pygame.display.flip()

    time.sleep(3)
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    pass