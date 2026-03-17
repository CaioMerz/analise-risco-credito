"""Importa o dataset bruto para uma tabela SQLite."""

from pathlib import Path
import sqlite3

import pandas as pd


def main() -> None:
    """Executa o fluxo completo de importacao do CSV para o SQLite."""
    # Define caminhos relativos ao diretorio raiz do projeto.
    raiz_projeto = Path(__file__).resolve().parent.parent
    caminho_csv = raiz_projeto / "dados" / "brutos" / "cs-training.csv"
    caminho_banco = raiz_projeto / "dados" / "tratados" / "risco_credito.db"

    # Le o arquivo CSV com pandas.
    df = pd.read_csv(caminho_csv)

    # Remove coluna de indice antigo, quando existir.
    if "Unnamed: 0" in df.columns:
        df = df.drop(columns=["Unnamed: 0"])

    # Garante que a pasta do banco exista antes de conectar.
    caminho_banco.parent.mkdir(parents=True, exist_ok=True)

    # Salva os dados na tabela 'credito_raw', substituindo se ja existir.
    with sqlite3.connect(caminho_banco) as conexao:
        df.to_sql("credito_raw", conexao, if_exists="replace", index=False)

    print("Importacao concluida com sucesso.")
    print("Tabela criada: credito_raw")
    print(f"Numero de linhas: {df.shape[0]}")
    print(f"Numero de colunas: {df.shape[1]}")


if __name__ == "__main__":
    main()
