"""Faz uma exploracao inicial da tabela credito_raw no SQLite."""

from pathlib import Path
import sqlite3

import pandas as pd


def main() -> None:
    # Define o caminho do banco de dados a partir da raiz do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"

    # Conecta no SQLite e le a tabela credito_raw em um DataFrame.
    with sqlite3.connect(caminho_banco) as conexao:
        df = pd.read_sql_query("SELECT * FROM credito_raw", conexao)

    # Informacoes gerais da base.
    print("Inspecao inicial da tabela credito_raw")
    print(f"Numero total de linhas: {df.shape[0]}")
    print(f"Numero total de colunas: {df.shape[1]}")
    print(f"Nomes das colunas: {list(df.columns)}")

    # Exibe tipos de dados e quantidade de valores nao nulos.
    print("\n=== df.info() ===")
    df.info()

    # Exibe estatisticas descritivas das variaveis numericas.
    print("\n=== df.describe() ===")
    print(df.describe())

    # Calcula o percentual de inadimplencia (SeriousDlqin2yrs == 1).
    taxa_inadimplencia = (df["SeriousDlqin2yrs"] == 1).mean() * 100
    print("\n=== Taxa de inadimplencia ===")
    print(f"Percentual de inadimplencia: {taxa_inadimplencia:.2f}%")


if __name__ == "__main__":
    main()
