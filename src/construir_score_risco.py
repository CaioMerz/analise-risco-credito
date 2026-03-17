"""Constroi um score simples e explicavel de risco de credito."""

from pathlib import Path
import sqlite3

import numpy as np
import pandas as pd


def main() -> None:
    # Define o caminho do banco a partir da raiz do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"

    # Conecta no SQLite e le a tabela base para um DataFrame.
    with sqlite3.connect(caminho_banco) as conexao:
        df = pd.read_sql_query("SELECT * FROM credito_raw", conexao)

    # Regra 1: pontos por historico de atrasos graves.
    df["pontos_atrasos_90dias"] = np.select(
        [
            df["NumberOfTimes90DaysLate"] == 0,
            df["NumberOfTimes90DaysLate"] == 1,
            df["NumberOfTimes90DaysLate"] >= 2,
        ],
        [0, 2, 3],
        default=0,
    )

    # Regra 2: pontos por utilizacao de credito.
    df["pontos_utilizacao_credito"] = np.select(
        [
            df["RevolvingUtilizationOfUnsecuredLines"] <= 0.50,
            df["RevolvingUtilizationOfUnsecuredLines"] <= 1.00,
            df["RevolvingUtilizationOfUnsecuredLines"] > 1.00,
        ],
        [0, 1, 2],
        default=0,
    )

    # Regra 3: pontos por renda mensal (inclui caso sem renda informada).
    df["pontos_renda_mensal"] = np.select(
        [
            df["MonthlyIncome"].isna(),
            df["MonthlyIncome"] > 5000,
            (df["MonthlyIncome"] >= 2000) & (df["MonthlyIncome"] <= 5000),
            df["MonthlyIncome"] < 2000,
        ],
        [1, 0, 1, 2],
        default=1,
    )

    # Regra 4: pontos por idade.
    df["pontos_idade"] = np.select(
        [
            (df["age"] >= 18) & (df["age"] <= 29),
            df["age"] >= 30,
        ],
        [1, 0],
        default=0,
    )

    # Soma dos pontos para gerar o score final.
    df["score_risco"] = (
        df["pontos_atrasos_90dias"]
        + df["pontos_utilizacao_credito"]
        + df["pontos_renda_mensal"]
        + df["pontos_idade"]
    )

    # Classificacao final por faixa de score.
    df["classificacao_risco"] = np.select(
        [
            df["score_risco"] <= 2,
            (df["score_risco"] >= 3) & (df["score_risco"] <= 5),
            df["score_risco"] >= 6,
        ],
        ["baixo risco", "medio risco", "alto risco"],
        default="medio risco",
    )

    # Exibe amostra com score e classificacao.
    print("Primeiras linhas com score e classificacao:")
    print(df[["score_risco", "classificacao_risco"]].head())

    # Exibe distribuicao de clientes por classificacao.
    print("\nDistribuicao de clientes por classificacao:")
    print(df["classificacao_risco"].value_counts())

    # Exibe taxa media de inadimplencia por classificacao.
    print("\nTaxa media de inadimplencia por classificacao:")
    print(df.groupby("classificacao_risco")["SeriousDlqin2yrs"].mean())

    # Salva o resultado completo na tabela credito_score.
    with sqlite3.connect(caminho_banco) as conexao:
        df.to_sql("credito_score", conexao, if_exists="replace", index=False)

    print("\nTabela 'credito_score' salva com sucesso no SQLite.")


if __name__ == "__main__":
    main()
