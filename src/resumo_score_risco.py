"""Gera resumo tabular e visual da classificação do score de risco."""

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
        raiz_projeto
        / "graficos"
        / "taxa_inadimplencia_por_classificacao_score.png"
    )

    # Conecta no banco e le a tabela com score final.
    with sqlite3.connect(caminho_banco) as conexao:
        df = pd.read_sql_query("SELECT * FROM credito_score", conexao)

    # Cria a tabela-resumo por classificação de risco.
    resumo = (
        df.groupby("classificacao_risco", as_index=False)
        .agg(
            total_clientes=("classificacao_risco", "count"),
            taxa_inadimplencia_media=("SeriousDlqin2yrs", "mean"),
        )
    )

    # Define a ordem desejada para a classificação.
    ordem_classificacao = ["baixo risco", "medio risco", "alto risco"]
    resumo["classificacao_risco"] = pd.Categorical(
        resumo["classificacao_risco"],
        categories=ordem_classificacao,
        ordered=True,
    )
    resumo = resumo.sort_values("classificacao_risco")

    # Mostra tabela-resumo no terminal.
    print("Resumo por classificação de risco:")
    print(resumo)

    caminho_grafico.parent.mkdir(parents=True, exist_ok=True)

    # Cria grafico de barras com taxa media de inadimplência.
    fig, ax1 = plt.subplots(figsize=(8, 5))
    ax1.bar(
        resumo["classificacao_risco"],
        resumo["taxa_inadimplencia_media"],
        color="#1a6b8a",
        edgecolor="#0f3f52",
        linewidth=0.5,
    )
    ax1.yaxis.set_major_formatter(mtick.PercentFormatter(xmax=1, decimals=1))
    for i, (taxa_val, vol) in enumerate(
        zip(resumo["taxa_inadimplencia_media"], resumo["total_clientes"])
    ):
        ax1.text(
            i,
            taxa_val + 0.005,
            f"n={vol:,}".replace(",", "."),
            ha="center",
            va="bottom",
            fontsize=8,
            color="#777777",
        )
    ax1.set_xlabel("Classificação de risco", fontsize=11)
    ax1.set_ylabel("Taxa media de inadimplência", fontsize=11)
    ax1.set_title("Taxa de inadimplência por classificação do score", fontsize=13)
    ax1.grid(axis="y", alpha=0.2)
    plt.tight_layout()
    plt.savefig(caminho_grafico, dpi=150)
    plt.close()

    print(f"Grafico salvo em: {caminho_grafico}")


if __name__ == "__main__":
    main()
