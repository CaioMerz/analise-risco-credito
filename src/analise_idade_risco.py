"""Analisa a relacao entre idade e taxa de inadimplência."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def main() -> None:
    # Define caminhos principais do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"
    caminho_grafico = raiz_projeto / "graficos" / "inadimplencia_por_idade.png"

    # Consulta SQL para calcular taxa de inadimplência e total de clientes por idade.
    query = """
    SELECT
        age,
        AVG(SeriousDlqin2yrs) AS taxa_inadimplencia,
        COUNT(*) AS total_clientes
    FROM credito_raw
    GROUP BY age
    ORDER BY age
    """

    # Conecta no banco e carrega o resultado em um DataFrame.
    with sqlite3.connect(caminho_banco) as conexao:
        df_idade = pd.read_sql_query(query, conexao)

    # Mostra as primeiras linhas para inspecao inicial.
    print("Primeiras linhas da analise por idade:")
    print(df_idade.head())

    # Remove idades muito altas para reduzir ruido por baixa amostra.
    df_idade = df_idade[df_idade["age"] <= 90]

    # Garante que a pasta de graficos exista antes de salvar.
    caminho_grafico.parent.mkdir(parents=True, exist_ok=True)

    # Cria grafico de duplo eixo: taxa de inadimplência e volume de clientes.
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax2 = ax1.twinx()
    ax2.bar(
        df_idade["age"],
        df_idade["total_clientes"],
        color="#b0c4d8",
        alpha=0.4,
        label="Nº de clientes",
    )
    ax1.plot(
        df_idade["age"],
        df_idade["taxa_inadimplencia"],
        color="#1a6b8a",
        linewidth=2,
        label="Taxa de inadimplência",
    )
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel("Idade", fontsize=11)
    ax1.set_ylabel("Taxa de inadimplência", fontsize=11)
    ax2.set_ylabel("Número de clientes", fontsize=11)
    ax1.set_title("Taxa de inadimplência por idade", fontsize=13)
    ax1.grid(True, alpha=0.2)
    ax1.annotate(
        "Idades acima de 90 omitidas por amostra insuficiente",
        xy=(0.99, 0.02),
        xycoords="axes fraction",
        ha="right",
        va="bottom",
        fontsize=9,
        alpha=0.8,
    )
    linhas1, labels1 = ax1.get_legend_handles_labels()
    linhas2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(linhas1 + linhas2, labels1 + labels2, loc="upper right")
    plt.tight_layout()
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()

    print(f"\nGrafico salvo em: {caminho_grafico}")


if __name__ == "__main__":
    main()
