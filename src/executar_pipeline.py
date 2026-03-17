"""Executa todos os scripts do pipeline na ordem correta."""

from analise_atrasos_risco import main as analise_atrasos_risco_main
from analise_idade_risco import main as analise_idade_risco_main
from analise_renda_risco import main as analise_renda_risco_main
from analise_utilizacao_credito_risco import main as analise_utilizacao_credito_main
from construir_score_risco import main as construir_score_risco_main
from explorar_base import main as explorar_base_main
from importar_csv_sqlite import main as importar_csv_sqlite_main
from resumo_score_risco import main as resumo_score_risco_main


def executar_pipeline() -> None:
    """Roda as etapas do pipeline em sequencia, interrompendo em caso de erro."""
    etapas = [
        ("importar_csv_sqlite", importar_csv_sqlite_main),
        ("explorar_base", explorar_base_main),
        ("analise_idade_risco", analise_idade_risco_main),
        ("analise_atrasos_risco", analise_atrasos_risco_main),
        ("analise_utilizacao_credito_risco", analise_utilizacao_credito_main),
        ("analise_renda_risco", analise_renda_risco_main),
        ("construir_score_risco", construir_score_risco_main),
        ("resumo_score_risco", resumo_score_risco_main),
    ]

    for nome, funcao in etapas:
        print(f"\nExecutando: {nome}")
        funcao()

    print("\nPipeline executado com sucesso.")


if __name__ == "__main__":
    executar_pipeline()
