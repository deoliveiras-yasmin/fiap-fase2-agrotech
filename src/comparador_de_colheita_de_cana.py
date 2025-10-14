# Projeto Agrotech - Comparador de Colheita de Cana (manual x mecanica)

import json
import os
from pathlib import Path

# ==============================
# Constantes
# ==============================

# Metodos disponiveis
METODOS = ("manual", "mecanica")

# Perdas "base" (sem considerar atraso)
PERDA_BASE = {
    "manual": 0.05,
    "mecanica": 0.15
}

# Capacidade de colheita (hectares por dia)
CAPACIDADE_HA_DIA = {
    "manual": 3.0,
    "mecanica": 20.0
}

# Custo por dia (R$)
CUSTO_DIA = {
    "manual": 800.0,
    "mecanica": 3500.0
}

# Parametros de tempo/qualidade
# - janela_ideal_dias: se a colheita superar os dias, aplica-se perda adicional
# perda_diaria_extra: perda adicional por dia acima da janela ideal (ex.: 0.5% ao dia)
JANELA_IDEAL_PADRAO = 7
PERDA_DIARIA_EXTRA = 0.005

# Caminho de arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok = True)

ARQUIVO_JSON = OUTPUTS_DIR / "simulacoes_cana.json"
ARQUIVO_TXT = OUTPUTS_DIR / "relatorio_simples.txt"

# ==============================
# Utilitarios / Validacao
# ==============================

def ler_float (mensagem, minimo = None):
    """Funcao/Subalgoritmo para ler um float do usuario com validacao opcional de minimo."""
    while True:
        try:
            valor = float(input(mensagem).strip())
            if minimo is not None and valor < minimo:
                print(f"Valor deve ser >= {minimo}. Por favor, tente novamente.")
                continue
            return valor
        except ValueError:
            print("Entrada invalida. Digite um numero, por favor.")

def confirmar (msg = "Confirmar? (s/n): "):
    """Procedimento simples para confirmacao."""
    return input(msg).strip().lower().startswith("s")

# ==============================
# Calculo principal
# ==============================

def calcular_resultados (area_ha, prod_ton_ha, preco_ton, metodo,
                         janela_ideal_dias= JANELA_IDEAL_PADRAO,
                         perda_base = PERDA_BASE,
                         capacidade = CAPACIDADE_HA_DIA,
                         custo_dia = CUSTO_DIA,
                         perda_diaria_extra = PERDA_DIARIA_EXTRA):
    """
    Calcula producao, perdas (base + por atraso), custos e lucros para um metodo.
    Retorna um dicionario com todos os cammpos calculados. (Dicionario usado aqui)
    """

    producao_total_ton = area_ha * prod_ton_ha
    duracao_dias = area_ha / capacidade[metodo]

    # Calculo da penalidade por atraso (Inovacao do projeto)
    atraso = max(0.0, duracao_dias - janela_ideal_dias)
    perda_extra = atraso * perda_diaria_extra
    perda_percent_total = perda_base[metodo] + perda_extra
    # Limitar perda para evitar lucros irreais
    perda_percent_total = min(perda_percent_total, 0.99)

    perda_ton = producao_total_ton * perda_percent_total
    producao_liquida_ton = producao_total_ton - perda_ton

    receita_bruta = producao_liquida_ton * preco_ton
    custo_total = duracao_dias * custo_dia[metodo]
    lucro = receita_bruta - custo_total

    return {
        "metodo": metodo,
        "area_ha": round(area_ha, 2),
        "prod_ton_ha": round(prod_ton_ha, 2),
        "preco_ton": round(preco_ton, 2),
        "duracao_dias": round(duracao_dias, 2),
        "perda_percent_total": round(perda_percent_total * 100, 2),
        "perda_ton": round(perda_ton, 2),
        "producao_total_ton": round(producao_total_ton, 2),
        "producao_liquida_ton": round(producao_liquida_ton, 2),
        "receita_bruta": round(receita_bruta, 2),
        "custo_total": round(custo_total, 2),
        "lucro": round(lucro, 2),
        "atraso_dias": round(atraso, 2)
    }

def comparar_metodos (area_ha, prod_ton_ha, preco_ton, janela_ideal_dias = JANELA_IDEAL_PADRAO):
    """Calcula resultados para manual e mecanica retornando ambos + diferencas."""
    res_manual = calcular_resultados(area_ha, prod_ton_ha, preco_ton, "manual", janela_ideal_dias)
    res_mecanica = calcular_resultados(area_ha, prod_ton_ha, preco_ton, "mecanica", janela_ideal_dias)

    diferencas = {
        "lucro_diff": round(res_mecanica["lucro"] - res_manual["lucro"], 2),
        "tempo_diff_dias": round(res_mecanica["duracao_dias"] - res_manual["duracao_dias"], 2),
        "perda_diff_ton": round(res_mecanica["perda_ton"] - res_manual["perda_ton"], 2)
    }
    return res_manual, res_mecanica, diferencas

# ==============================
# Percistencia
# ==============================

def verificar_diretorio (caminho):
    """Procedimento para garantir que o diretorio 'outputs' exista."""
    p = Path(caminho)
    p.parent.mkdir(parents = True, exist_ok = True)

def carregar_json ():
    """Carregar o historico de simulacoes do arquivo JSON."""
    verificar_diretorio(ARQUIVO_JSON)
    try:
        p = Path(ARQUIVO_JSON)
        if not p.exists():
            return []
        with open(ARQUIVO_JSON, "r", encoding = "utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("\n[AVISO] JSON existente estava vazio/corrompido. Reiniciando lista de simulacoes.")
        return []
    
def salvar_json (lista):
    """Salvar o historico de simulacoes no archivo JSON."""
    verificar_diretorio(ARQUIVO_JSON)
    p = Path(ARQUIVO_JSON)
    with p.open("w", encoding = "utf-8") as f:
        # Lista usada aqui para salvar registros
        json.dump(lista, f, ensure_ascii = False, indent = 2)
        print(f"[INFO] Simulacao salva com sucesso em {p}")

def salvar_relatorio_txt(res_manual, res_mecanica, diffs):
    """Salvar um relatorio detalhado em arquivo de texto."""
    verificar_diretorio(ARQUIVO_TXT)
    p = Path(ARQUIVO_TXT)
    with p.open("w", encoding = "utf-8") as f:
        f.write("=== Relatorio Comparativo de Colheita (Cana) ===\n\n")
        f.write("Parametros de entrada:\n")
        f.write(f" Area (ha): {res_manual['area_ha']}\n")
        f.write(f" Produtividade (ton/ha): {res_manual['prod_ton_ha']}\n")
        f.write(f" Preco (R$/ton): {res_manual['preco_ton']}\n")
        f.write(f" Janela ideal (dias): {JANELA_IDEAL_PADRAO}\n\n")

        # Estrutura de loop/dicionario para escrever os resultados
        for res in (res_manual, res_mecanica):
            f.write(f"--- Metodo: {res['metodo'].upper()} ---\n")
            f.write(f" Duracao (dias): {res['duracao_dias']}\n")
            f.write(f" Perda total (%): {res['perda_percent_total']}%\n")
            f.write(f" Perda (ton): {res['perda_ton']}\n")
            f.write(f" Producao liquida (ton): {res['producao_liquida_ton']}\n")
            f.write(f" Custo total (R$): {res['custo_total']}\n")
            f.write(f" Lucro (R$): {res['lucro']}\n\n")

        f.write("--- Diferencas (mecanica - manual) ---\n")
        f.write(f" Diferenca de Lucro: R$ {diffs['lucro_diff']}\n")
        f.write(f" Diferenca de Tempo (dias): {diffs['tempo_diff_dias']}\n")
        f.write(f" Diferenca de Perda (ton): {diffs['perda_diff_ton']}\n")
    print(f"[INFO] Relatorio gerado com sucesso em {p}")

# ==============================
# Conexao Oracle (placeholder)
# ==============================

def testar_conexao_oracle ():
    """
    Placeholder para o requisito de Conexao com DB Oracle.
    Usa try/except para demonstrar a estrutura, mesmo sem o modulo instalado.
    """
    try:
        # import cx_Oracle
        # Se estivesse conectando de verdade:
        # conn = cx_Oracle.connect("usuario", "senha", "host: porta/servico")
        print("\n[OK] Biblioteca 'cx_Oracle' encontrada. Estrutura de conexao OK (placeholder).")
    except ImportError:
        print("\n[AVISO] Biblioteca 'cx_Oracle' nao instalado.")
    except Exception as e:
        print(f"\n[ERRO] Ocorreu um erro na simulacao de conexao: {e}")

# ==============================
# UI CLI
# ==============================

def imprimir_tabela_simples (simulacoes):
    """Procedimento para mostrar uma 'tabela' em memoria com campos principais."""
    if not simulacoes:
        print("Sem simulacoes salvas.")
        return
    
    print("\n--- Historico de Simulacoes Salvas (Metodo Mecanica) ---")
    print("#  area  prod  dura(d)  perda%  lucro(R$)")
    print("-- ----- ----- ------- -------- ----------")

    for i, reg in enumerate(simulacoes, start = 1):
        if "comparacao" in reg and "mecanica" in reg["comparacao"]:
            r = reg["comparacao"]["mecanica"]
            print(f"{i: > 2} {r['area_ha']: > 5.1f} {r['prod_ton_ha']: > 5.1f} "
                  f"{r['duracao_dias']: > 7.1f} {r['perda_percent_total']: > 5.1f}% {r['lucro']: > 11.2f}")
            
def exibir_resultados (res_manual, res_mecanica, diffs):
    """Procedimento para exibir os resultados da comparacao no console."""
    print("\n--- Resultado: MANUAL ---")
    print(f" Duracao (dias): {res_manual['duracao_dias']}")
    print(f" Perda Total (%): {res_manual['perda_percent_total']}%")
    print(f" Producao Liquida (ton): {res_manual['producao_liquida_ton']}")
    print(f" Custo Total (R$): {res_manual['custo_total']: .2f}")
    print(f" LUCRO FINAL (R$): {res_manual['lucro']: .2f}")

    print("\n--- Resultado: MECANICA ---")
    print(f" Duracao (dias): {res_mecanica['duracao_dias']}")
    print(f" Perda Total (%): {res_mecanica['perda_percent_total']}%")
    print(f" Producao Liquida (ton): {res_mecanica['producao_liquida_ton']}")
    print(f" Custo Total (R$): {res_mecanica['custo_total']: .2f}")
    print(f" LUCRO FINAL (R$): {res_mecanica['lucro']: .2f}")

    print("\n--- Diferencas (Mecanica - Manual) ---")
    if diffs['lucro_diff'] > 0:
        print(f"[SUCESSO] Mecanica e {abs(diffs['lucro_diff']): .2f} R$ MAIS LUCRATIVA")
    else:
        print(f"[AVISO] Manual e {abs(diffs['lucro_diff']): .2f} R$ MAIS LUCRATIVA")
    print(f" Diferenca de Tempo (dias): {diffs['tempo_diff_dias']}")
    print(f" Diferenca de Perda (ton): {diffs['perda_diff_ton']}")

def menu ():
    """Procedimento principal que executa a CLI"""
    simulacoes = carregar_json()

    while True:
        print("\n\n=== Menu Comparador (Agrotech) ===")
        print("1) Simular e comparar (manual x mecanica)")
        print("2) Listar simulacoes salvas")
        print("3) Testar conexao Oracle (placeholder)")
        print("4) Sair")
        operacao = input("Escolha: ").strip()

        if operacao == "1":
            print("\n[ENTRADA DE DADOS]")
            area = ler_float(" Area do Cultivo (ha): ", minimo = 0.1)
            prod = ler_float(" Produtividade esperada (ton/ha): ", minimo = 0.1)
            preco = ler_float(" Preco da cana (R$/ton): ", minimo = 0.0)
            janela = ler_float(f" Janela ideal de colheita (dias) [padrao {JANELA_IDEAL_PADRAO}]: ", minimo = 1.0)
            if not janela: janela = JANELA_IDEAL_PADRAO

            res_manual, res_mecanica, diffs = comparar_metodos(area, prod, preco, janela)

            exibir_resultados(res_manual, res_mecanica, diffs)

            if confirmar("\nSalvar esta simulacao no JSON de historico? (s/n): "):
                registro = {
                    "comparacao": {
                        "manual": res_manual,
                        "mecanica": res_mecanica,
                        "diferencas": diffs
                    }
                }
                simulacoes.append(registro)
                salvar_json(simulacoes)

            if confirmar("Gerar relatorio TXT desta comparacao? (s/n): "):
                salvar_relatorio_txt(res_manual, res_mecanica, diffs)

        elif operacao == "2":
            imprimir_tabela_simples(simulacoes)
        elif operacao == "3":
            testar_conexao_oracle()
        elif operacao =="4":
            print("Saindo. Ate logo!")
            break
        else:
            print("Operacao invalida.")
    
if __name__ == "__main__":
    menu()
