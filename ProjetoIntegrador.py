"""
Projeto Integrador: Painel de Indicadores de Pesquisadores em Ciência Aberta
"""

import csv
import json
import time

arquivo_csv = "GSProfiles2.csv"

# 1. CARREGAMENTO E MANIPULAÇÃO DE DADOS

def carregar_pesquisadores(caminho_csv):
    registros = []
    try:
        with open(caminho_csv, mode="r", encoding="utf-8") as arq:
            leitor = csv.DictReader(arq)
            for i, linha in enumerate(leitor):
                registros.append({
                    "codigo": int(linha.get("codigo", i)),
                    "perfilID": linha.get("perfilID", linha.get("ProfileID")),
                    "nome": linha.get("pesquisador", linha.get("ProfileName", "")),
                    "afiliacao": linha.get("afiliacao", linha.get("Affiliation", "N/A")),
                    "area": linha.get("area_conhecimento", linha.get("Labels", "Open Science")),
                    "citacoes": int(linha.get("citacoes", linha.get("Citations", 0))),
                    "url": linha.get("url", linha.get("ProfileURL", ""))
                })
    except FileNotFoundError:
        print(f"Erro: O arquivo '{caminho_csv}' não foi encontrado na pasta atual.")
    return registros


# 2. ALGORITMOS DE BUSCA E ORDENAÇÃO MANUAL

def pesquisa_sequencial(registros, codigo):
    iteracoes = 0
    for i in range(len(registros)):
        iteracoes += 1
        if registros[i]["codigo"] == codigo:
            return i, iteracoes
    return -1, iteracoes

def pesquisa_binaria_iterativa(registros, codigo):
    inicio = 0
    fim = len(registros) - 1
    iteracoes = 0
    
    while inicio <= fim:
        meio = (inicio + fim) // 2
        iteracoes += 1
        if registros[meio]["codigo"] == codigo:
            return meio, iteracoes
        elif registros[meio]["codigo"] < codigo:
            inicio = meio + 1
        else:
            fim = meio - 1
    return -1, iteracoes

def pesquisa_binaria_recursiva(registros, codigo, inicio, fim, iteracoes=0):
    if inicio > fim:
        return -1, iteracoes
        
    meio = (inicio + fim) // 2
    iteracoes += 1
    
    if registros[meio]["codigo"] == codigo:
        return meio, iteracoes
    elif registros[meio]["codigo"] < codigo:
        return pesquisa_binaria_recursiva(registros, codigo, meio + 1, fim, iteracoes)
    else:
        return pesquisa_binaria_recursiva(registros, codigo, inicio, meio - 1, iteracoes)


def ordenacao_insercao(registros, chave="codigo", decrescente=False):
    lista = registros[:]
    for i in range(1, len(lista)):
        atual = lista[i]
        j = i - 1
        if decrescente:
            while j >= 0 and lista[j][chave] < atual[chave]:
                lista[j + 1] = lista[j]
                j -= 1
        else:
            while j >= 0 and lista[j][chave] > atual[chave]:
                lista[j + 1] = lista[j]
                j -= 1
        lista[j + 1] = atual
    return lista


# 3. ESTRUTURAS AVANÇADAS (MATRIZES, FILAS E AGREGADOS)

def gerar_matriz_afiliacao_citacoes(registros, top_n=10):
    ranking_completo = ordenacao_insercao(registros, chave="citacoes", decrescente=True)
    top_pesquisadores = ranking_completo[:top_n]
    matriz = [[0 for _ in range(3)] for _ in range(top_n)]
    
    for i in range(top_n):
        p = top_pesquisadores[i]
        matriz[i][0] = p["codigo"]
        matriz[i][1] = p["citacoes"]
        matriz[i][2] = p["afiliacao"]
    return matriz, [p["nome"] for p in top_pesquisadores]


class FilaConsultas:
    def __init__(self, capacidade=5):
        self.fila = []
        self.capacidade = capacidade
        
    def inserir_busca(self, codigo_buscado, encontrado=True):
        if len(self.fila) >= self.capacidade:
            self.fila.pop(0)
        status = "Encontrado" if encontrado else "Não Encontrado"
        self.fila.append(f"ID: {codigo_buscado} ({status}) às {time.strftime('%H:%M:%S')}")
        
    def exibir_historico(self):
        if not self.fila:
            print("\nNenhuma busca realizada nesta sessão.")
            return
        print("\nHistórico recente de consultas:")
        for idx, item in enumerate(self.fila, start=1):
            print(f"{idx}. {item}")


# Instanciação global da Fila
historico_fila = FilaConsultas()


# 4. VALIDAÇÕES E EXPORTAÇÕES (SISTEMA DE ARQUIVOS)

def validar_entrada_codigo():
    while True:
        entrada = input("Digite o Código ID do pesquisador: ").strip()
        if not entrada:
            print("Erro: A entrada não pode estar vazia.")
            continue
        if not entrada.isdigit():
            print("Erro: Digite apenas números inteiros positivos.")
            continue
        return int(entrada)


def salvar_ranking_json(registros, caminho_json="ranking_open_science.json"):
    ranking_atual = ordenacao_insercao(registros, chave="citacoes", decrescente=True)
    top_20 = ranking_atual[:20]
    try:
        with open(caminho_json, mode="w", encoding="utf-8") as arq_json:
            json.dump(top_20, arq_json, indent=2, ensure_ascii=False)
        print(f"Arquivo exportado e salvo em '{caminho_json}'.")
    except Exception as e:
        print(f"Erro ao salvar arquivo: {e}")

# 5. ESTATÍSTICAS E ANÁLISES

def comp_pesquisa(pesquisadores):    
    base_ordenada_codigo = ordenacao_insercao(pesquisadores, chave="codigo", decrescente=False)
    # Teste com um código localizado no final da lista (pior caso para busca sequencial)
    codigo_teste = base_ordenada_codigo[-5]["codigo"]

    # 1. Execução pesquisa sequencial
    t0 = time.perf_counter()
    pos_seq, comp_seq = pesquisa_sequencial(pesquisadores, codigo_teste)
    t1 = time.perf_counter()
    tempo_seq_ms = (t1 - t0) * 1000

    # 2. Execução pesquisa binária iterativa
    t0 = time.perf_counter()
    pos_ite, comp_ite = pesquisa_binaria_iterativa(base_ordenada_codigo, codigo_teste)
    t1 = time.perf_counter()
    tempo_ite_ms = (t1 - t0) * 1000

    # 2. Execução pesquisa binária recursiva
    t0 = time.perf_counter()
    pos_rec, comp_rec = pesquisa_binaria_recursiva(base_ordenada_codigo, codigo_teste, 0, len(base_ordenada_codigo) - 1)
    t1 = time.perf_counter()
    tempo_rec_ms = (t1 - t0) * 1000

    print("\n" + "-" * 65)
    print(f"Análise de desempenho (Código buscado: {codigo_teste})")
    print("-" * 65)
    print(f"Pesquisa sequencial           : {comp_seq:<4} comparações | Tempo: {tempo_seq_ms:.4f} ms")
    print(f"Pesquisa binária iterativa    : {comp_ite:<4} comparações | Tempo: {tempo_ite_ms:.4f} ms")
    print(f"Pesquisa binária recursiva    : {comp_rec:<4} comparações | Tempo: {tempo_rec_ms:.4f} ms")
    print("-" * 65)

def relatorio_estatisticas(pesquisadores):
    ranking = ordenacao_insercao(pesquisadores, chave="citacoes", decrescente=True)
    total = len(pesquisadores)
    total_citacoes = sum(p["citacoes"] for p in pesquisadores)
    media_citacoes = total_citacoes / total if total > 0 else 0
    mais_citado = ranking[0]
    
    print("\n" + "-" * 65)
    print("         Relatório estatístico de pesquisadores em Open Science")
    print("-" * 65)
    print(f" Total de perfis analisados (Google Scholar): {total}")
    print(f" Total acumulado de citações                : {total_citacoes:,}")
    print(f" Média de citações por pesquisador          : {media_citacoes:.2f}")
    print(f" Pesquisador com mais citações              : {mais_citado['nome']} ({mais_citado['citacoes']:,} citações)")
    print(f" Afiliação com mais citações                : {mais_citado['afiliacao']}")
    print("-" * 65)


# 6. EXECUÇÃO DO FLUXO PRINCIPAL (INTERFACE DO TERMINAL)

def executar_painel(pesquisadores):
    if not pesquisadores:
        print("A base de dados está vazia ou não pôde ser carregada.")
        return
        
    base_ordenada_codigo = ordenacao_insercao(pesquisadores, chave="codigo", decrescente=False)
    
    while True:
        print("\n" + "="*65)
        print("     PAINEL DE INDICADORES EM OPEN SCIENCE - PROJETO INTEGRADOR")
        print("="*65)
        print("1. Listar os primeiros registros (top 5)")
        print(f"2. Buscar pesquisador por código ID (de 0 a {len(pesquisadores) - 1})")
        print("3. Visualizar matriz de produtividade (top 10 pesquisadores por citações)")
        print("4. Exibir histórico de consultas de pesquisadores por código ID")
        print("5. Comparação de algoritmos de pesquisa")
        print("6. Estatísticas gerais da base de pesquisadores em Open Science")
        print("7. Exportar ranking atualizado para JSON (top 20)")
        print("0. Sair do programa")
        print("="*65)
        
        opcao = input("Escolha uma opção: ").strip()
        
        if opcao == "1":
            print(f"\nExibindo os 5 primeiros de {len(pesquisadores)} registros:")
            for p in pesquisadores[:5]:
                nome_formatado = p["nome"].upper()
                area_formatada = p["area"].replace(",", " |")
                print(f"[{p['codigo']}] {nome_formatado} \n\t Áreas: {area_formatada}\n\t Afiliação: {p['afiliacao']} \n\t Citações: {p['citacoes']:,} \n\t URL: {p['url']}")
                
        elif opcao == "2":
            codigo_busca = validar_entrada_codigo()
            pos_seq, comp_seq = pesquisa_sequencial(pesquisadores, codigo_busca)
            pos_ite, comp_ite = pesquisa_binaria_iterativa(pesquisadores, codigo_busca)
            pos_rec, comp_rec = pesquisa_binaria_recursiva(base_ordenada_codigo, codigo_busca, 0, len(base_ordenada_codigo)-1)
            
            if pos_rec != -1:
                p = base_ordenada_codigo[pos_rec]                
                print(f"\n[{p['codigo']}] {p['nome']} \n\t Áreas: {p['area']}\n\t Afiliação: {p['afiliacao']} \n\t Citações: {p['citacoes']:,} \n\t URL: {p['url']}")
                print(f"\n- Pesquisa sequencial: {comp_seq} iterações \n- Pesquisa binária iterativa: {comp_ite} iterações \n- Pesquisa binária recursiva: {comp_rec} iterações")
                historico_fila.inserir_busca(codigo_busca, encontrado=True)
            else:
                print(f"\nCódigo {codigo_busca} não localizado na base.")
                historico_fila.inserir_busca(codigo_busca, encontrado=False)
                
        elif opcao == "3":
            matriz, nomes = gerar_matriz_afiliacao_citacoes(pesquisadores)
            print("\n" + "-" * 85)
            print("Matriz de produtividade (top 10 pesquisadores por citações)")
            print("-" * 85)
            print(f"{' ID':<6} | {'Pesquisador':<20} | {' Afiliação':<40} | {' Citações':<10}")
            print("-" * 85)
            for i in range(len(matriz)):
                print(f"{matriz[i][0]:<6} | {nomes[i][:19]:<20} | {matriz[i][2][:39]:<40} | {matriz[i][1]:<10,}")
                
        elif opcao == "4":
            historico_fila.exibir_historico()

        elif opcao == "5":
            comp_pesquisa(pesquisadores)

        elif opcao == "6":
            relatorio_estatisticas(pesquisadores)
            
        elif opcao == "7":
            salvar_ranking_json(pesquisadores)
            
        elif opcao == "0":
            print("\nEncerrando o painel de indicadores.")
            break
        else:
            print("Opção inválida! Tente novamente.")


# Ponto de entrada padrão para scripts Python estruturados
if __name__ == "__main__":
    # Carrega os dados iniciais do CSV ao ligar o script
    dados_pesquisadores = carregar_pesquisadores(arquivo_csv)
    # Ativa o loop do painel interativo
    executar_painel(dados_pesquisadores)

