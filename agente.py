import random

class Agente:
    def __init__(self, tamanho_mundo):
        self.tamanho_mundo = tamanho_mundo
        self.pos = [0, 0]  # Posição inicial do agente
        self.ouro = False
        self.flechas = 1  # Agente começa com uma flecha
        self.vivo = True
        self.pontuacao = 0
        self.passos = 0
        self.historico_posicoes = []
        self.dist_anterior_ouro = float("inf") # Para o cálculo de fitness do AG

    def reset(self):
        self.pos = [0, 0]
        self.ouro = False
        self.flechas = 1
        self.vivo = True
        self.pontuacao = 0
        self.passos = 0
        self.historico_posicoes = []
        self.dist_anterior_ouro = float("inf")

    def decidir_acao(self, percepcoes):
        # Lógica padrão para o Agente V2 (com memória)
        # Esta é uma versão simplificada para permitir a execução dos testes
        # Em um cenário real, o Agente V2 teria uma lógica mais complexa baseada em memória
        self.passos += 1
        if "brilho" in percepcoes:
            return "pegar"
        if "fedor" in percepcoes and self.flechas > 0:
            return "atirar"
        
        # Movimento aleatório como fallback
        acoes_movimento = ["mover_cima", "mover_baixo", "mover_esquerda", "mover_direita"]
        return random.choice(acoes_movimento)

    def executar_acao(self, acao, matriz_mundo):
        x, y = self.pos
        terminou = False

        if acao == "mover_cima":
            if x > 0: self.pos[0] -= 1
        elif acao == "mover_baixo":
            if x < self.tamanho_mundo - 1: self.pos[0] += 1
        elif acao == "mover_esquerda":
            if y > 0: self.pos[1] -= 1
        elif acao == "mover_direita":
            if y < self.tamanho_mundo - 1: self.pos[1] += 1
        elif acao == "pegar":
            if matriz_mundo[x][y] == "O":
                self.ouro = True
                matriz_mundo[x][y] = "_" # Remove o ouro do mundo
                terminou = True
        elif acao == "atirar":
            if self.flechas > 0:
                self.flechas -= 1
                # Lógica simplificada para atirar: assume que acerta o Wumpus se estiver adjacente
                # Em um cenário real, precisaria de uma direção e verificação mais complexa
                # Para o propósito dos testes, apenas reduz a flecha
        elif acao == "voltar_para_casa":
            if self.pos == [0,0] and self.ouro:
                terminou = True
        elif acao == "sair":
            if self.pos == [0,0]:
                terminou = True

        # Verifica se caiu em poço ou encontrou Wumpus
        if matriz_mundo[self.pos[0]][self.pos[1]] == "P" or matriz_mundo[self.pos[0]][self.pos[1]] == "W":
            self.vivo = False
            
        return terminou

class AgenteGenetico(Agente):
    def __init__(self, tamanho_mundo, cromossomo):
        super().__init__(tamanho_mundo)
        self.cromossomo = cromossomo
        self.cromossomo_idx = 0

    def decidir_acao(self, percepcoes):
        self.passos += 1
        if self.cromossomo_idx >= len(self.cromossomo):
            self.cromossomo_idx = 0 # Reinicia o cromossomo se chegar ao fim
        
        acao = self.cromossomo[self.cromossomo_idx]
        self.cromossomo_idx += 1
        return acao


