"""
E-commerce Analytics com SQL
-----------------------------
Executa as consultas SQL da pasta 'queries/' contra o banco SQLite
e gera gráficos no estilo escuro do portfólio.

Autora: Mariana Moreira
"""

import os
import glob
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

DB = "data/ecommerce.db"
PASTA_QUERIES = "queries"
PASTA_OUTPUT = "outputs"
os.makedirs(PASTA_OUTPUT, exist_ok=True)

plt.style.use("dark_background")
CORES = {
    "roxo": "#a78bfa", "rosa": "#f472b6",
    "ciano": "#67e8f9", "texto": "#f5f3ff",
    "grid": "#292d42",
}


def executar_query(arquivo):
    with open(arquivo, "r", encoding="utf-8-sig") as f: 
        sql = f.read().strip()
    if not sql:
        raise ValueError(f"Arquivo vazio: {arquivo}")
    conn = sqlite3.connect(DB)
    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        print(f"Erro na consulta {arquivo}: {e}")
        conn.close()
        return pd.DataFrame() 
    conn.close()
    return df


def salvar_consultas_txt(resultados):
    caminho = f"{PASTA_OUTPUT}/resultado_consultas.txt"
    with open(caminho, "w", encoding="utf-8") as f:
        for nome, df in resultados.items():
            f.write(f"\n{'='*60}\n{nome}\n{'='*60}\n")
            f.write(df.to_string(index=False))
            f.write("\n")
    print(f"✔ Resultados salvos: {caminho}")


def grafico_categoria(df):
    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.barh(df["categoria"], df["faturamento"],
                   color=CORES["roxo"], alpha=0.85)
    for bar, val in zip(bars, df["faturamento"]):
        ax.text(bar.get_width() + max(df["faturamento"])*0.01,
                bar.get_y() + bar.get_height()/2,
                f"R$ {val:,.0f}", va="center",
                color=CORES["texto"], fontsize=10)
    ax.set_title("Faturamento por categoria", fontsize=14,
                 color=CORES["texto"], pad=15)
    ax.set_xlabel("Faturamento (R$)", color=CORES["texto"])
    ax.grid(axis="x", alpha=0.2, color=CORES["grid"])
    plt.tight_layout()
    plt.savefig(f"{PASTA_OUTPUT}/grafico_categoria.png", dpi=150, facecolor="#0f1117")
    plt.close()
    print("✔ grafico_categoria.png")


def grafico_top_clientes(df):
    df = df.sort_values("total_gasto")
    fig, ax = plt.subplots(figsize=(9, 6))
    bars = ax.barh(df["nome"], df["total_gasto"],
                   color=CORES["rosa"], alpha=0.85)
    for bar, val in zip(bars, df["total_gasto"]):
        ax.text(bar.get_width() + max(df["total_gasto"])*0.01,
                bar.get_y() + bar.get_height()/2,
                f"R$ {val:,.0f}", va="center",
                color=CORES["texto"], fontsize=9)
    ax.set_title("Top 10 clientes por valor gasto", fontsize=14,
                 color=CORES["texto"], pad=15)
    ax.set_xlabel("Total gasto (R$)", color=CORES["texto"])
    ax.grid(axis="x", alpha=0.2, color=CORES["grid"])
    plt.tight_layout()
    plt.savefig(f"{PASTA_OUTPUT}/grafico_top_clientes.png", dpi=150, facecolor="#0f1117")
    plt.close()
    print("✔ grafico_top_clientes.png")


def grafico_mensal(df):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(df["mes"], df["faturamento"],
            color=CORES["ciano"], linewidth=2.5, marker="o")
    ax.fill_between(range(len(df)), df["faturamento"],
                    color=CORES["ciano"], alpha=0.15)
    ax.set_title("Faturamento mensal (2024)", fontsize=14,
                 color=CORES["texto"], pad=15)
    ax.set_xlabel("Mês", color=CORES["texto"])
    ax.set_ylabel("Faturamento (R$)", color=CORES["texto"])
    ax.grid(alpha=0.2, color=CORES["grid"])
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(f"{PASTA_OUTPUT}/grafico_mensal.png", dpi=150, facecolor="#0f1117")
    plt.close()
    print("✔ grafico_mensal.png")


if __name__ == "__main__":
    if not os.path.exists(DB):
        raise FileNotFoundError(
            "Banco não encontrado. Rode primeiro: python criar_banco.py"
        )

    resultados = {}
    for arquivo in sorted(glob.glob(f"{PASTA_QUERIES}/*.sql")):
        nome = os.path.basename(arquivo).replace(".sql", "")
        print(f"⏳ Executando: {nome}")
        resultados[nome] = executar_query(arquivo)

    salvar_consultas_txt(resultados)


    if "01_faturamento_categoria" in resultados and not resultados["01_faturamento_categoria"].empty:
        grafico_categoria(resultados["01_faturamento_categoria"])

    if "02_top_clientes" in resultados and not resultados["02_top_clientes"].empty:
        grafico_top_clientes(resultados["02_top_clientes"])

    if "05_faturamento_mensal" in resultados and not resultados["05_faturamento_mensal"].empty:
        grafico_mensal(resultados["05_faturamento_mensal"])

    print("\nINSIGHTS RÁPIDOS")
    print("=" * 50)

    cat = resultados.get("01_faturamento_categoria")
    if cat is not None and not cat.empty:
        print(f"• Categoria líder: {cat.iloc[0]['categoria']} "
              f"(R$ {cat.iloc[0]['faturamento']:,.0f})")
        print(f"• Faturamento total: R$ {cat['faturamento'].sum():,.0f}")

    top = resultados.get("02_top_clientes")
    if top is not None and not top.empty:
        linha = top.iloc[0]
        print(f"• Cliente top: {linha['nome']} — R$ {linha['total_gasto']:,.0f}")

    print("=" * 50)
    print("\ Análise concluída! Veja a pasta 'outputs/'.")