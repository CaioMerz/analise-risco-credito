"""Analisa a relacao entre atrasos graves e taxa de inadimplência."""

from pathlib import Path
import sqlite3

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import pandas as pd


def main() -> None:
    # Define caminhos principais do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"
    caminho_grafico = raiz_projeto / "graficos" / "inadimplencia_por_atrasos_90dias.png"

    # Consulta SQL para taxa de inadimplência por faixas de atrasos graves.
    query = """
    SELECT
        faixa_atrasos,
        AVG(SeriousDlqin2yrs) AS taxa_inadimplencia,
        COUNT(*) AS total_clientes
    FROM (
        SELECT
            CASE
                WHEN NumberOfTimes90DaysLate = 0 THEN '0 atrasos'
                WHEN NumberOfTimes90DaysLate = 1 THEN '1 atraso'
                WHEN NumberOfTimes90DaysLate BETWEEN 2 AND 3 THEN '2 a 3 atrasos'
                WHEN NumberOfTimes90DaysLate BETWEEN 4 AND 5 THEN '4 a 5 atrasos'
                WHEN NumberOfTimes90DaysLate BETWEEN 6 AND 10 THEN '6 a 10 atrasos'
                ELSE 'acima de 10 atrasos'
            END AS faixa_atrasos,
            SeriousDlqin2yrs
        FROM credito_raw
    )
    GROUP BY faixa_atrasos
    ORDER BY
        CASE faixa_atrasos
            WHEN '0 atrasos' THEN 1
            WHEN '1 atraso' THEN 2
            WHEN '2 a 3 atrasos' THEN 3
            WHEN '4 a 5 atrasos' THEN 4
            WHEN '6 a 10 atrasos' THEN 5
            WHEN 'acima de 10 atrasos' THEN 6
        END
    """

    # Conecta no banco e carrega o resultado em um DataFrame.
    with sqlite3.connect(caminho_banco) as conexao:
        df_atrasos = pd.read_sql_query(query, conexao)

    # Mostra as primeiras linhas para inspecao inicial.
    print("Primeiras linhas da analise por faixa de atrasos:")
    print(df_atrasos.head())

    taxa = df_atrasos.set_index("faixa_atrasos")["taxa_inadimplencia"]
    volume = df_atrasos.set_index("faixa_atrasos")["total_clientes"]

    # Garante que a pasta de graficos exista antes de salvar.
    caminho_grafico.parent.mkdir(parents=True, exist_ok=True)

    # Cria grafico de barras da taxa de inadimplência por faixa de atrasos.
    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(
        taxa.index,
        taxa.values,
        color="#1a6b8a",
        edgecolor="#0f3f52",
        linewidth=0.5,
    )
    for i, (taxa_val, n) in enumerate(zip(taxa.values, volume.values)):
        ax1.text(
            i,
            taxa_val + 0.002,
            f"n={n:,}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#777777",
        )
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))
    ax1.set_xlabel("Faixa de atrasos (90 dias)", fontsize=11)
    ax1.set_ylabel("Taxa de inadimplência", fontsize=11)
    ax1.set_title("Taxa de inadimplência por faixa de atrasos", fontsize=13)
    ax1.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()

    print(f"\nGrafico salvo em: {caminho_grafico}")


if __name__ == "__main__":
    main()
