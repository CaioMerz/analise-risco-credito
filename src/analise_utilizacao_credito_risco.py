"""Analisa a relacao entre utilização de credito e inadimplência."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def main() -> None:
    # Define caminhos principais do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"
    caminho_grafico = (
        raiz_projeto / "graficos" / "inadimplencia_por_utilizacao_credito.png"
    )

    # Agrupa a utilização de credito em faixas e calcula metricas por faixa.
    query = """
    SELECT
        faixa_utilizacao,
        AVG(SeriousDlqin2yrs) AS taxa_inadimplencia,
        COUNT(*) AS total_clientes
    FROM (
        SELECT
            CASE
                WHEN RevolvingUtilizationOfUnsecuredLines <= 0.25 THEN 'ate 0.25'
                WHEN RevolvingUtilizationOfUnsecuredLines <= 0.50 THEN '0.25 a 0.50'
                WHEN RevolvingUtilizationOfUnsecuredLines <= 0.75 THEN '0.50 a 0.75'
                WHEN RevolvingUtilizationOfUnsecuredLines <= 1.00 THEN '0.75 a 1.00'
                ELSE 'acima de 1.00'
            END AS faixa_utilizacao,
            SeriousDlqin2yrs
        FROM credito_raw
    )
    GROUP BY faixa_utilizacao
    ORDER BY
        CASE faixa_utilizacao
            WHEN 'ate 0.25' THEN 1
            WHEN '0.25 a 0.50' THEN 2
            WHEN '0.50 a 0.75' THEN 3
            WHEN '0.75 a 1.00' THEN 4
            WHEN 'acima de 1.00' THEN 5
        END
    """

    with sqlite3.connect(caminho_banco) as conexao:
        df_utilizacao = pd.read_sql_query(query, conexao)

    # Mostra a tabela no terminal.
    print("Tabela por faixa de utilização de credito:")
    print(df_utilizacao)
    taxa = df_utilizacao.set_index("faixa_utilizacao")["taxa_inadimplencia"]
    volume = df_utilizacao.set_index("faixa_utilizacao")["total_clientes"]

    caminho_grafico.parent.mkdir(parents=True, exist_ok=True)

    # Cria grafico de barras da taxa de inadimplência por faixa.
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
    ax1.set_xlabel("Faixa de utilização de credito", fontsize=11)
    ax1.set_ylabel("Taxa de inadimplência", fontsize=11)
    ax1.set_title("Taxa de inadimplência por faixa de utilização de credito", fontsize=13)
    plt.xticks(rotation=20)
    ax1.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()

    print(f"\nGrafico salvo em: {caminho_grafico}")


if __name__ == "__main__":
    main()
