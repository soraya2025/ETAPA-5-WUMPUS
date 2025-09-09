
import random
import sys
from mundo import Mundo
from agente import AgenteGenetico, Agente

# Parâmetros do AG para testes rápidos
TAMANHO_POPULACAO = 100 # Aumentado para 100
NUM_GERACOES = 50 # Aumentado para 50
TAXA_CRUZAMENTO = 0.9 # Aumentado para maior convergência
TAXA_MUTACAO = 0.1 # Ligeiramente diminuído para estabilizar as melhores soluções
TAMANHO_CROMOSSOMO = 10 # Mantido em 10

def inicializar_populacao(tamanho_mundo):
    populacao = []
    acoes_possiveis = ["mover_aleatorio", "atirar", "pegar", "voltar_para_casa", "sair"]
    for _ in range(TAMANHO_POPULACAO):
        cromossomo = [random.choice(acoes_possiveis) for _ in range(TAMANHO_CROMOSSOMO)]
        populacao.append(AgenteGenetico(tamanho_mundo, cromossomo))
    return populacao

def calcular_fitness(agente, mundo):
    agente.reset()
    pontuacao = 0
    passos_max = 200 # Mantido em 200
    
    for _ in range(passos_max): # Limita o número de passos para evitar loops infinitos
        if not agente.vivo: # Verifica se o agente ainda está vivo
            break

        percepcoes = obter_percepcoes(mundo.matriz, agente.pos, agente)
        acao = agente.decidir_acao(percepcoes)
        
        # Penalidade por atirar sem flechas
        if acao == "atirar" and agente.flechas <= 0:
            agente.vivo = False
            pontuacao -= 500
            break

        # Executa a ação e verifica se terminou
        terminou = agente.executar_acao(acao, mundo.matriz)
        
        x, y = agente.pos
        
        # Penalidade por cada passo
        pontuacao -= 1

        # Penalidades por cair em poço ou encontrar Wumpus
        if mundo.matriz[x][y] == "P":
            pontuacao -= 5000 # Penalidade mais severa
            agente.vivo = False
        elif mundo.matriz[x][y] == "W":
            pontuacao -= 5000 # Penalidade mais severa
            agente.vivo = False
        
        # Recompensa por pegar o ouro
        if agente.ouro:
            pontuacao += 1000
        
        # Recompensa por se mover em direção ao ouro (se ainda não o pegou)
        if not agente.ouro:
            # Calcula a distância Manhattan até o ouro
            ouro_pos = None
            for r in range(len(mundo.matriz)):
                for c in range(len(mundo.matriz[r])):
                    if mundo.matriz[r][c] == "O":
                        ouro_pos = (r, c)
                        break
                if ouro_pos: break
            
            if ouro_pos:
                dist_atual = abs(x - ouro_pos[0]) + abs(y - ouro_pos[1])
                # Recompensa por diminuir a distância ao ouro
                if dist_atual < agente.dist_anterior_ouro:
                    pontuacao += 5
                # Penalidade por aumentar a distância ao ouro
                elif dist_atual > agente.dist_anterior_ouro:
                    pontuacao -= 2
                agente.dist_anterior_ouro = dist_atual

        # Recompensa por sobreviver a cada passo (incentiva a exploração segura)
        if agente.vivo:
            pontuacao += 1 # Pequena recompensa por sobrevivência

        if terminou:
            break
            
    # Recompensa final por pegar o ouro e voltar para casa
    if agente.ouro and agente.pos == [0,0]:
        pontuacao += 5000
    
    # Penalidade se o agente não pegou o ouro e não voltou para casa
    if not agente.ouro or agente.pos != [0,0]:
        pontuacao -= 100 # Penalidade por não completar o objetivo principal

    return pontuacao

def selecao(populacao, scores):
    # Implementando seleção por torneio para maior pressão seletiva
    tamanho_torneio = 5 # Número de indivíduos no torneio
    selecionados = []
    for _ in range(len(populacao)):
        competidores = random.sample(populacao, min(tamanho_torneio, len(populacao)))
        vencedor = max(competidores, key=lambda ag: ag.pontuacao)
        selecionados.append(vencedor)
    return selecionados

def cruzamento(pai1_cromossomo, pai2_cromossomo):
    ponto = random.randint(1, TAMANHO_CROMOSSOMO - 1)
    cromossomo_filho = pai1_cromossomo[:ponto] + pai2_cromossomo[ponto:]
    return cromossomo_filho

def mutacao(cromossomo):
    for i in range(len(cromossomo)):
        if random.random() < TAXA_MUTACAO:
            acoes_possiveis = ["mover_aleatorio", "atirar", "pegar", "voltar_para_casa", "sair"]
            cromossomo[i] = random.choice(acoes_possiveis)
    return cromossomo

def main_ag():
    tamanho_mundo = 4
    melhor_agente_global = None
    melhor_fitness_global = float("-inf")
    
    for geracao in range(NUM_GERACOES):
        print(f"--- Geração {geracao} ---")
        # Cria um novo mundo para cada geração para avaliação consistente
        mundo_atual = Mundo(tamanho_mundo)
        populacao = inicializar_populacao(tamanho_mundo)
        
        populacao_ordenada = []
        for agente in populacao:
            agente.pontuacao = calcular_fitness(agente, mundo_atual)
            populacao_ordenada.append(agente)
        
        populacao_ordenada = sorted(populacao_ordenada, key=lambda ag: ag.pontuacao, reverse=True)
        melhor_agente_geracao = populacao_ordenada[0]
        
        # Atualiza o melhor agente global se o agente da geração atual for melhor
        if melhor_agente_geracao.pontuacao > melhor_fitness_global:
            melhor_fitness_global = melhor_agente_geracao.pontuacao
            # Cria uma nova instância do AgenteGenetico para o melhor agente global
            # para evitar que ele seja modificado por mutações ou cruzamentos subsequentes
            melhor_agente_global = AgenteGenetico(tamanho_mundo, list(melhor_agente_geracao.cromossomo))
            melhor_agente_global.pontuacao = melhor_fitness_global

        print(f"Melhor fitness da geração {geracao}: {melhor_agente_geracao.pontuacao}")
        print(f"Cromossomo do melhor agente: {melhor_agente_geracao.cromossomo}")
        
        nova_populacao = []
        # Elitismo: Mantém o melhor agente global na próxima população
        if melhor_agente_global:
            nova_populacao.append(AgenteGenetico(tamanho_mundo, list(melhor_agente_global.cromossomo)))

        # Seleção e cruzamento para preencher o restante da nova população
        # Aumentar a taxa de elitismo para 10% da população
        num_elite = int(TAMANHO_POPULACAO * 0.1)
        elite_da_geracao = populacao_ordenada[:num_elite]
        nova_populacao.extend([AgenteGenetico(tamanho_mundo, list(ag.cromossomo)) for ag in elite_da_geracao])

        # Garante que `selecionados` seja definido antes de ser usado
        selecionados = selecao(populacao_ordenada, [ag.pontuacao for ag in populacao_ordenada])

        while len(nova_populacao) < TAMANHO_POPULACAO:
            pai1 = random.choice(selecionados)
            pai2 = random.choice(selecionados)
            
            if random.random() < TAXA_CRUZAMENTO:
                filho_cromossomo = cruzamento(pai1.cromossomo, pai2.cromossomo)
            else:
                filho_cromossomo = random.choice([pai1.cromossomo, pai2.cromossomo])
            
            filho_cromossomo = mutacao(filho_cromossomo)
            nova_populacao.append(AgenteGenetico(tamanho_mundo, filho_cromossomo))
            
        populacao = nova_populacao

    print("\nTreinamento do Agente Genético finalizado.")
    print(f"Melhor estratégia encontrada (global): {melhor_agente_global.cromossomo}")
    print(f"Melhor fitness encontrado (global): {melhor_fitness_global}")
    
def obter_percepcoes(mundo_matriz, pos, agente):
    x, y = pos
    percepcoes = set()
    vizinhos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for i, j in vizinhos:
        if 0 <= i < len(mundo_matriz) and 0 <= j < len(mundo_matriz):
            if mundo_matriz[i][j] == "P":
                percepcoes.add("brisa")
            elif mundo_matriz[i][j] == "W":
                percepcoes.add("fedor")
    
    if mundo_matriz[x][y] == "O" and not agente.ouro:
        percepcoes.add("brilho")
    
    return percepcoes

if __name__ == "__main__":
    main_ag()


