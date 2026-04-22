# Projeto Inicial de Engenharia de Dados com FIIs

Este e um projeto simples de portfolio para praticar conceitos iniciais de engenharia de dados com um dataset publico de FIIs.

## Objetivo

Separar 4 tabelas do dataset, fazer uma limpeza basica, juntar os dados e gerar arquivos finais em CSV.

## Tabelas usadas

- `FundosImobiliarios.parquet`
- `Tickers.parquet`
- `InformesMensais.parquet`
- `ticker-cotacoes.parquet`

## O que o script faz

1. Le os arquivos parquet
2. Renomeia algumas colunas
3. Remove registros invalidos mais obvios
4. Junta as tabelas
5. Gera 3 arquivos finais para analise

## Arquivos gerados

- `data/gold/base_final_fiis.csv`
- `data/gold/ranking_fiis.csv`
- `data/gold/resumo_tickers.csv`

## Como executar

```bash
python src/build_portfolio.py
```

## O que eu pratiquei neste projeto

- leitura de arquivos parquet
- limpeza basica de dados
- padronizacao de nomes de colunas
- join entre tabelas
- exportacao de CSV

## Observacao

Este projeto foi feito com foco em aprendizado. A ideia aqui nao e reproduzir um ambiente completo de empresa, mas mostrar entendimento dos passos iniciais mais comuns no tratamento e consolidacao de dados.
