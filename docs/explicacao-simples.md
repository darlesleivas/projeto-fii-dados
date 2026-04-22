# Explicacao simples do projeto

## Em uma frase

Peguei 4 tabelas de um dataset de FIIs, limpei o basico, juntei os dados e gerei CSVs finais.

## O que cada arquivo principal faz

- `src/build_portfolio.py`: roda o projeto inteiro
- `data/gold/base_final_fiis.csv`: base consolidada final
- `data/gold/ranking_fiis.csv`: ranking dos fundos com mais cotistas
- `data/gold/resumo_tickers.csv`: resumo dos tickers com maior volume

## Como explicar em entrevista

Voce pode dizer algo assim:

"Eu peguei um dataset publico de FIIs e fiz um recorte de 4 tabelas para praticar leitura, limpeza, padronizacao e join de dados. Depois gerei uma base final e dois CSVs de apoio para analise."

## Passo a passo do script

1. Ler os arquivos parquet
2. Renomear colunas para ficar mais facil de entender
3. Remover linhas nulas ou invalidas
4. Pegar o registro mais recente dos informes
5. Pegar a cotacao mais recente de cada ticker
6. Juntar tudo em uma base unica
7. Salvar os resultados em CSV
