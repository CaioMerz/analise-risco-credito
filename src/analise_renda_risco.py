"""Analisa a relacao entre renda mensal e taxa de inadimplência."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def main() -> None:
    # Define caminhos principais do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"
    caminho_grafico = raiz_projeto / "graficos" / "inadimplencia_por_renda.png"

    # Agrupa a renda mensal em faixas e calcula metricas por faixa.
    query = """
    SELECT
        faixa_renda,
        AVG(SeriousDlqin2yrs) AS taxa_inadimplencia,
        COUNT(*) AS total_clientes
    FROM (
        SELECT
            CASE
                WHEN MonthlyIncome IS NULL THEN 'sem renda informada'
                WHEN MonthlyIncome <= 2000 THEN 'ate 2000'
                WHEN MonthlyIncome <= 5000 THEN '2000 a 5000'
                WHEN MonthlyIncome <= 10000 THEN '5000 a 10000'
                ELSE 'acima de 10000'
            END AS faixa_renda,
            SeriousDlqin2yrs
        FROM credito_raw
    )
    GROUP BY faixa_renda
    ORDER BY
        CASE faixa_renda
            WHEN 'sem renda informada' THEN 1
            WHEN 'ate 2000' THEN 2
            WHEN '2000 a 5000' THEN 3
            WHEN '5000 a 10000' THEN 4
            WHEN 'acima de 10000' THEN 5
        END
    """

    with sqlite3.connect(caminho_banco) as conexao:
        df_renda = pd.read_sql_query(query, conexao)

    # Mostra a tabela no terminal.
    print("Tabela por faixa de renda mensal:")
    print(df_renda)
    taxa = df_renda.set_index("faixa_renda")["taxa_inadimplencia"]
    volume = df_renda.set_index("faixa_renda")["total_clientes"]

    caminho_grafico.parent.mkdir(parents=True, exist_ok=True)

    # Cria grafico de barras da taxa de inadimplência por faixa de renda.
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(
        taxa.index,
        taxa.values,
        color="#1a6b8a",
        edgecolor="#0f3f52",
        linewidth=0.5,
    )
    for i, (taxa_val, vol) in enumerate(zip(taxa.values, volume.values)):
        ax1.text(
            i,
            taxa_val + 0.002,
            f"n={vol:,}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#777777",
        )
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel("Faixa de renda mensal", fontsize=11)
    ax1.set_ylabel("Taxa de inadimplência", fontsize=11)
    ax1.set_title("Taxa de inadimplência por faixa de renda", fontsize=13)
    plt.xticks(rotation=20)
    ax1.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()

    print(f"\nGrafico salvo em: {caminho_grafico}")


if __name__ == "__main__":
    main()
