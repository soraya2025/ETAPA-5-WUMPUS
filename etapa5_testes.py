import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import random
import math
import pandas as pd
import os
from mundo import Mundo
from agente import Agente
from agente import AgenteGenetico
from main_ag import obter_percepcoes # Remove a importação de OUTPUT_DIR

# Caminho de saída para os arquivos (ajuste para o seu ambiente Windows)
OUTPUT_DIR = r'C:\Soraya\Mestrado\Trabalho Mundo Wumps\Trabalho Mundo Wumps - Etapa 5'

# --- Definição do Agente V1 (Simples Reativo) ---
class AgenteV1(Agente):
    def __init__(self, tamanho_mundo):
        super().__init__(tamanho_mundo)
        self.cromossomo = ["mover_aleatorio", "mover_aleatorio", "atirar", "pegar", "mover_aleatorio"]

    def decidir_acao(self, percepcoes):
        self.passos += 1
        
        if "brilho" in percepcoes:
            return "pegar"
        if "fedor" in percepcoes and self.flechas > 0:
            return "atirar"
        
        return "mover_aleatorio"

# --- Estratégia do Agente V3 (copiada do log de execução do main_ag.py) ---
MELHOR_CROMOSSOMO = ["sair", "voltar_para_casa", "mover_aleatorio", "mover_aleatorio", "mover_aleatorio", "sair", "atirar", "pegar", "pegar", "pegar"]


# --- Função Principal de Teste ---
def executar_teste(agente, tamanho_mundo, agente_tipo):
    pontuacoes = []
    
    print(f"Iniciando testes para {agente_tipo} no ambiente {tamanho_mundo}x{tamanho_mundo}...")
    
    for i in range(20):
        try:
            mundo = Mundo(tamanho_mundo)
            agente.reset()
            
            while agente.vivo and agente.passos < 200:
                percepcoes = obter_percepcoes(mundo.matriz, agente.pos, agente)
                acao = agente.decidir_acao(percepcoes)
                terminou = agente.executar_acao(acao, mundo.matriz)
                
                x, y = agente.pos
                
                agente.pontuacao -= 1

                if mundo.matriz[x][y] == "P" or mundo.matriz[x][y] == "W":
                    agente.pontuacao -= 1000
                    agente.vivo = False
                    break
                
                if agente.ouro:
                    agente.pontuacao += 1000

                if terminou:
                    agente.pontuacao += 1000
                    break
            
            pontuacoes.append(agente.pontuacao)
        except Exception as e:
            print(f"Erro inesperado durante a execução do teste {i+1}: {e}")
            pontuacoes.append(float("-inf"))
            
    return pontuacoes

def main_etapa5():
    tamanhos_ambiente = [4, 5, 10, 15, 20]
    resultados_detalhados = []
    resultados_agregados = {}

    print("--- Iniciando testes da Etapa 5 ---")

    # Cria o diretório de saída se não existir
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    for versao in ["v1", "v2", "v3"]:
        resultados_agregados[versao] = {}
        for n in tamanhos_ambiente:
            if versao == "v1":
                agente = AgenteV1(n)
                agente_tipo = "Agente V1"
            elif versao == "v2":
                agente = Agente(n)
                agente_tipo = "Agente V2"
            else: # v3
                agente = AgenteGenetico(n, MELHOR_CROMOSSOMO)
                agente_tipo = "Agente V3"

            pontuacoes = executar_teste(agente, n, agente_tipo)
            resultados_agregados[versao][n] = pontuacoes

            for i, pontuacao in enumerate(pontuacoes):
                resultados_detalhados.append({
                    "Execução": i + 1,
                    "Ambiente": f"{n}x{n}",
                    "Agente": versao,
                    "Pontuação": pontuacao
                })

    # --- Geração da Tabela Detalhada ---
    df_detalhado = pd.DataFrame(resultados_detalhados)
    tabela_pivotada = df_detalhado.pivot_table(index="Execução", columns=["Ambiente", "Agente"], values="Pontuação")
    
    # Reordenar as colunas para o formato solicitado
    col_order = []
    for n in tamanhos_ambiente:
        for v in ["v1", "v2", "v3"]:
            col_order.append((f"{n}x{n}", v))
    tabela_pivotada = tabela_pivotada[col_order]

    print("\n--- Tabela Detalhada de Resultados ---")
    print(tabela_pivotada.to_string())
    
    # Salvar a tabela detalhada
    try:
        output_csv_path = os.path.join(OUTPUT_DIR, "tabela_detalhada_resultados.csv")
        tabela_pivotada.to_csv(output_csv_path)
        print(f"Tabela detalhada salva em: {output_csv_path}")
    except Exception as e:
        print(f"Erro ao salvar tabela detalhada: {e}")

    # --- Geração de Gráficos ---
    # Gráfico de Desempenho para Agentes V1 e V2
    fig, ax = plt.subplots(figsize=(10, 6))
    for versao in ["v1", "v2"]:
        medias = [sum(resultados_agregados[versao][n]) / len(resultados_agregados[versao][n]) for n in tamanhos_ambiente]
        ax.plot(tamanhos_ambiente, medias, marker="o", linestyle="-", label=f"Agente {versao}")

    ax.set_xlabel("Tamanho do Ambiente (n)")
    ax.set_ylabel("Pontuação Média")
    ax.set_title("Desempenho dos Agentes V1 e V2")
    ax.legend()
    ax.grid(True)
    
    # Salvar o gráfico V1 e V2
    try:
        output_v1v2_path = os.path.join(OUTPUT_DIR, "grafico_desempenho_v1_v2.png")
        plt.savefig(output_v1v2_path)
        print(f"Gráfico V1 e V2 salvo em: {output_v1v2_path}")
    except Exception as e:
        print(f"Erro ao salvar gráfico V1 e V2: {e}")
    plt.close()

    # Gráfico de Gerações x Fitness para Agente V3 (usando dados reais)
    print("\nGerando gráfico para Agente V3 (Gerações x Fitness) com dados reais...")
    try:
        fitness_csv_path = os.path.join(OUTPUT_DIR, "fitness_agente_v3.csv")
        df_fitness = pd.read_csv(fitness_csv_path)
        geracoes = df_fitness["Geracao"]
        melhor_fitness = df_fitness["Melhor_Fitness"]
        pior_fitness = df_fitness["Pior_Fitness"]
        media_fitness = df_fitness["Media_Fitness"]

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(geracoes, melhor_fitness, marker="o", linestyle="-", label="Melhor Fitness")
        ax.plot(geracoes, pior_fitness, marker="o", linestyle="-", label="Pior Fitness")
        ax.plot(geracoes, media_fitness, marker="o", linestyle="-", label="Média Fitness")
        ax.set_xlabel("Geração")
        ax.set_ylabel("Fitness")
        ax.set_title("Agente V3: Gerações x Fitness (Dados Reais)")
        ax.legend()
        ax.grid(True)
        
        # Salvar o gráfico V3
        output_v3_path = os.path.join(OUTPUT_DIR, "grafico_geracoes_fitness_v3.png")
        plt.savefig(output_v3_path)
        print(f"Gráfico V3 salvo em: {output_v3_path}")
    except FileNotFoundError:
        print("Erro: O arquivo fitness_agente_v3.csv não foi encontrado. Certifique-se de que main_ag.py foi executado e salvou o arquivo.")
    except Exception as e:
        print(f"Erro ao gerar gráfico V3 com dados reais: {e}")
    plt.close()

    print("\nGráficos e tabela detalhada foram gerados e salvos.")

if __name__ == "__main__":
    main_etapa5()