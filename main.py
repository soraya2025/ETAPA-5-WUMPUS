import sys
import os
from mundo import Mundo
from agente import Agente
from main_ag import main_ag as iniciar_agente_genetico # Importa a função do AG

def obter_percepcoes(mundo, pos, agente):
    x, y = pos
    percepcoes = set()
    vizinhos = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
    
    for i, j in vizinhos:
        if 0 <= i < len(mundo) and 0 <= j < len(mundo):
            if mundo[i][j] == "P":
                percepcoes.add("brisa")
            elif mundo[i][j] == "W":
                percepcoes.add("fedor")
    
    if mundo[x][y] == "O" and not agente.ouro:
        percepcoes.add("brilho")
    
    return percepcoes

def modo_automatizado_console():
    while True:
        try:
            n = int(input("Digite o tamanho da matriz (n >= 3): "))
            while n < 3:
                n = int(input("Valor inválido. Digite um número >= 3: "))
        except ValueError:
            print("Entrada inválida. Usando o tamanho padrão n=4.")
            n = 4

        ambiente = Mundo(n)
        jogador = Agente(n)

        print("Bem-vindo ao Mundo de Wumpus (Modo Automático - Console)!")

        while True:
            print(f"\n--- Rodada {jogador.passos} ---")
            print(f"Posição: [Linha {jogador.pos[0]}, Coluna {jogador.pos[1]}]")
            
            percepcoes = obter_percepcoes(ambiente.matriz, jogador.pos, jogador)
            
            if not percepcoes:
                print("Percepções: O agente não percebe nada de diferente.")
            else:
                print(f"Percepções: {percepcoes}")

            print("\nMemória do Agente:")
            for linha in jogador.memoria:
                print(" ".join(linha))
            
            acao = jogador.decidir_acao(percepcoes)
            
            if acao.startswith("mover_") and ',' in acao:
                coords = acao.split('_')[1].split(',')
                print(f"Agente escolheu: mover para Linha {coords[0]}, Coluna {coords[1]}")
            else:
                print(f"Agente escolheu: {acao}")
            
            if acao == "pegar":
                print("Ouro encontrado! A missão agora é retornar para a saída [Linha 0, Coluna 0].")
                
            terminou = jogador.executar_acao(acao, ambiente.matriz)
            
            x, y = jogador.pos
            if ambiente.matriz[x][y] == "P":
                print("\nGame Over! O agente caiu em um poço.")
                jogador.vivo = False
                break
            elif ambiente.matriz[x][y] == "W":
                print("\nGame Over! O agente encontrou o Wumpus.")
                jogador.vivo = False
                break
            
            if terminou:
                print("\nGame Over! O agente venceu.")
                break
            
            input("Pressione Enter para a próxima rodada...")
        
        jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
        if jogar_novamente != "s":
            break

def modo_interativo():
    while True:
        print("Bem-vindo ao Mundo de Wumpus (Modo Interativo)!")
        try:
            n = int(input("Digite o tamanho da matriz (n >= 3): "))
            while n < 3:
                n = int(input("Valor inválido. Digite um número >= 3: "))
        except ValueError:
            print("Entrada inválida. Usando o tamanho padrão n=4.")
            n = 4
            
        ambiente = Mundo(n)
        jogador = Agente(n)

        print("Controles: mover, pegar, atirar, sair")

        while True:
            print("\nVisão do Agente:")
            for i in range(len(ambiente.matriz)):
                linha = []
                for j in range(len(ambiente.matriz[i])):
                    if [i, j] == jogador.pos:
                        linha.append(" 🥷🏻 ")
                    else:
                        linha.append(" ❓ ")
                print(" ".join(linha))
            
            percepcoes = obter_percepcoes(ambiente.matriz, jogador.pos, jogador)
            
            if not percepcoes:
                print("Percepções: O agente não percebe nada de diferente.")
            else:
                print(f"Percepções: {percepcoes}")

            acao = input("Escolha uma ação: ").lower()
            
            if acao == "sair":
                break
            
            if acao == "auto":
                acao = jogador.decidir_acao(percepcoes)
                print(f"Agente escolheu: {acao}")
                terminou = jogador.executar_acao(acao, ambiente.matriz)
                
            elif acao == "mover":
                direcao = input("Direção (cima, baixo, esquerda, direita): ").lower()
                jogador.mover(direcao, len(ambiente.matriz))
                terminou = False
            elif acao == "pegar":
                jogador.pegar_ouro(ambiente.matriz)
                terminou = False
            elif acao == "atirar":
                direcao = input("Direção (cima, baixo, esquerda, direita): ").lower()
                jogador.atirar(ambiente.matriz, direcao)
                terminou = False
            
            else:
                print("Ação inválida.")
                terminou = False

            x, y = jogador.pos
            if ambiente.matriz[x][y] == "W":
                print("Você encontrou o Wumpus! Game Over!")
                break
            if ambiente.matriz[x][y] == "P":
                print("Você caiu em um poço! Game Over!")
                break
            if terminou:
                if jogador.ouro and jogador.pos == [0, 0]:
                    print("Parabéns! Você venceu com o ouro!")
                break
        
        jogar_novamente = input("Deseja jogar novamente? (s/n): ").lower()
        if jogar_novamente != "s":
            break

if __name__ == "__main__":
    while True:
        print("--- Menu Principal do Mundo de Wumpus ---")
        print("1. Algoritmo Genético")
        print("2. Modo Automático (Console)")
        print("3. Modo Interativo (Console)")
        print("4. Sair")
        
        escolha = input("Digite sua escolha: ")
        
        if escolha == "1":
            iniciar_agente_genetico()
            break
        elif escolha == "2":
            modo_automatizado_console()
            break
        elif escolha == "3":
            modo_interativo()
            break
        elif escolha == "4":
            sys.exit()
        else:
            print("Escolha inválida. Tente novamente.")