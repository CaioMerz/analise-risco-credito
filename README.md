# AnÃ¡lise de Risco de CrÃ©dito com Score ExplicÃ¡vel
(Python, SQL e SQLite)

No Brasil, mais de 80 milhÃµes de pessoas estÃ£o inadimplentes. Decidir quem
recebe crÃ©dito â€” e em que condiÃ§Ãµes â€” Ã© um dos problemas mais concretos do
mercado financeiro. Este projeto aborda exatamente isso.

## 1. VisÃ£o geral e objetivo
Projeto desenvolvido para portfÃ³lio com foco em vagas no mercado financeiro,
fintechs e Ã¡reas de risco de crÃ©dito. O problema Ã© direto: identificar clientes
com maior probabilidade de nÃ£o pagar. A abordagem tambÃ©m â€” um score simples,
baseado em regras claras, fÃ¡cil de explicar e de aplicar na prÃ¡tica.

## 2. Tecnologias utilizadas
- Python 3
- pandas
- matplotlib
- numpy
- SQL
- SQLite (`sqlite3`)
- pathlib

## 3. Estrutura do projeto
```text
analise-risco-credito/
|-- dados/
|   |-- brutos/
|   |   `-- cs-training.csv
|   |-- tratados/
|   |   `-- risco_credito.db
|   `-- dicionario/
|       `-- descricao_variaveis.md
|-- graficos/
|   |-- inadimplencia_por_atrasos_90dias.png
|   |-- inadimplencia_por_idade.png
|   |-- inadimplencia_por_renda.png
|   |-- inadimplencia_por_utilizacao_credito.png
|   `-- taxa_inadimplencia_por_classificacao_score.png
|-- sql/
|   `-- 01_criar_tabela_raw.sql
|-- src/
|   |-- importar_csv_sqlite.py
|   |-- explorar_base.py
|   |-- analise_idade_risco.py
|   |-- analise_atrasos_risco.py
|   |-- analise_utilizacao_credito_risco.py
|   |-- analise_renda_risco.py
|   |-- construir_score_risco.py
|   |-- resumo_score_risco.py
|   `-- executar_pipeline.py
|-- requirements.txt
`-- README.md
```

## 4. Base de dados
- Fonte: dataset pÃºblico do Kaggle (arquivo `cs-training.csv`)
- Caminho no projeto: `dados/brutos/cs-training.csv`
- Tabela principal no banco: `credito_raw`
- VariÃ¡vel-alvo de inadimplÃªncia: `SeriousDlqin2yrs`

## 5. Etapas do projeto
1. ImportaÃ§Ã£o do CSV para SQLite.
2. ExploraÃ§Ã£o inicial da base para validar estrutura, tipos de dados e
   valores faltantes.
3. AnÃ¡lises de inadimplÃªncia por idade, atrasos graves, utilizaÃ§Ã£o de
   crÃ©dito e renda.
4. ConstruÃ§Ã£o do score de risco com regras de negÃ³cio.
5. ClassificaÃ§Ã£o final em baixo, mÃ©dio e alto risco.
6. GeraÃ§Ã£o de resumo tabular e visual da classificaÃ§Ã£o final.

## 6. Principais anÃ¡lises realizadas
- Taxa geral de inadimplÃªncia da base (mÃ©dia de `SeriousDlqin2yrs`).
- AnÃ¡lise por idade (`age` x taxa de inadimplÃªncia).
- AnÃ¡lise por atrasos graves (`NumberOfTimes90DaysLate` x taxa de inadimplÃªncia).
- AnÃ¡lise por utilizaÃ§Ã£o de crÃ©dito (`RevolvingUtilizationOfUnsecuredLines`
  em faixas).
- AnÃ¡lise por renda (`MonthlyIncome` em faixas, incluindo casos sem renda
  informada).

## 7. Lógica do score de risco
O score final é uma regra simples e interpretável de segmentação de risco: a pontuação total é a soma dos pontos de cada critério abaixo.

1. **Histórico de atrasos graves** (NumberOfTimes90DaysLate)
   - == 0 → 0 pontos  
   - == 1 → 2 pontos  
   - >= 2 → 3 pontos  

2. **Utilização de crédito** (RevolvingUtilizationOfUnsecuredLines)
   - <= 0.50 → 0 pontos  
   - > 0.50 e <= 1.00 → 1 ponto  
   - > 1.00 → 2 pontos  

3. **Renda mensal** (MonthlyIncome)
   - isna() (sem renda informada) → 1 ponto  
   - > 5000 → 0 pontos  
   - >= 2000 e <= 5000 → 1 ponto  
   - < 2000 → 2 pontos  
   > *Clientes sem renda informada recebem 1 ponto pela ausência da informação, não pelo comportamento. Na base, esse grupo teve inadimplência menor que as faixas de renda baixa, mas a falta de dado foi tratada de forma conservadora.*

4. **Idade** (`age`)
   - >= 18 e <= 29 → 1 ponto  
   - >= 30 → 0 pontos  

**Classificação final:**
- **baixo risco**: score total de **0 a 2**
- **médio risco**: score total de **3 a 5**
- **alto risco**: score total de **6 ou mais**

Resultado salvo em SQLite na tabela credito_score.

## 8. Principais resultados
- Taxa geral de inadimplÃªncia da base: **6,7%**.
- **Baixo risco**: inadimplÃªncia de **4,2%**.
- **MÃ©dio risco**: inadimplÃªncia de **26,8%**.
- **Alto risco**: inadimplÃªncia de **54,1%**.

O score separa bem os trÃªs grupos â€” e os padrÃµes por idade, atrasos,
utilizaÃ§Ã£o de crÃ©dito e renda sÃ£o consistentes com o que se espera
num problema real de crÃ©dito.

## Contexto brasileiro
O dataset Ã© americano por uma razÃ£o prÃ¡tica: no Brasil, dados individuais
de crÃ©dito nÃ£o sÃ£o disponibilizados publicamente por conta do sigilo
bancÃ¡rio e da LGPD. Mesmo assim, os padrÃµes que o projeto analisa fazem
total sentido no contexto nacional.

- Segundo a PEIC/CNC (fev/2025), **76,4%** das famÃ­lias estavam endividadas
  e **28,6%** tinham contas em atraso.
- O Mapa da InadimplÃªncia da Serasa (jan/2026) registrou **81,3 milhÃµes**
  de consumidores inadimplentes, com **R$ 524 bilhÃµes** em dÃ©bitos ativos.
- Os dÃ©bitos se concentram em bancos/cartÃµes (26,3%), contas bÃ¡sicas (22,0%)
  e financeiras (19,8%) â€” exatamente as frentes que as variÃ¡veis do score
  buscam capturar.

## VisualizaÃ§Ãµes principais
![InadimplÃªncia por idade](graficos/inadimplencia_por_idade.png)

![InadimplÃªncia por atrasos graves](graficos/inadimplencia_por_atrasos_90dias.png)

![InadimplÃªncia por utilizaÃ§Ã£o de crÃ©dito](graficos/inadimplencia_por_utilizacao_credito.png)

![InadimplÃªncia por renda](graficos/inadimplencia_por_renda.png)

![Taxa de inadimplÃªncia por classificaÃ§Ã£o do score](graficos/taxa_inadimplencia_por_classificacao_score.png)

## 9. Como executar o projeto
1. Instale as dependÃªncias:
```bash
pip install -r requirements.txt
```

2. Execute os scripts na ordem sugerida:
```bash
python src/importar_csv_sqlite.py
python src/explorar_base.py
python src/analise_idade_risco.py
python src/analise_atrasos_risco.py
python src/analise_utilizacao_credito_risco.py
python src/analise_renda_risco.py
python src/construir_score_risco.py
python src/resumo_score_risco.py
```

3. Ou execute todo o pipeline de uma vez:
```bash
python src/executar_pipeline.py
```

No Windows, vocÃª pode usar `py` no lugar de `python`.

## 10. PrÃ³ximos passos
1. Evoluir o dicionÃ¡rio de dados em `dados/dicionario/descricao_variaveis.md`.
2. Adicionar testes automatizados para validar as regras do score.
3. Testar regressÃ£o logÃ­stica como benchmark em relaÃ§Ã£o ao score por regras.
4. Avaliar a importÃ¢ncia das variÃ¡veis para a separaÃ§Ã£o de risco.
5. Testar novas segmentaÃ§Ãµes de variÃ¡veis e faixas de corte.
6. Criar um dashboard interativo para exploraÃ§Ã£o dos resultados.


