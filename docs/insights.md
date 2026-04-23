# Insights do Projeto

Este documento resume o recorte analitico, os principais outputs gerados e as conclusoes observadas a partir do pipeline de dados de FIIs.

## Recorte escolhido

Em vez de usar todas as tabelas do dataset, o projeto prioriza 4 fontes com maior potencial analitico:

- cadastro dos fundos
- relacao fundo x ticker
- informes mensais
- cotacoes historicas

Esse recorte permite responder perguntas de negocio relevantes sem aumentar desnecessariamente a complexidade do pipeline.

## Outputs principais

- `fii_snapshot_latest.csv`: ultimo retrato disponivel de cada fundo
- `top_fundos_por_cotistas.csv`: ranking dos fundos com maior base de investidores
- `mercado_mensal.csv`: evolucao do volume negociado e da quantidade de tickers ativos por mes
- `historico_top5_tickers.csv`: serie mensal dos tickers mais liquidos

## Graficos gerados

![Top FIIs por cotistas](./charts/top_fundos_cotistas.png)

![Volume mensal do mercado](./charts/volume_mensal_mercado.png)

![Historico dos tickers mais liquidos](./charts/top5_fechamento_mensal.png)

## Principais conclusoes

1. O recorte adotado cobre cadastro, negociacao e historico de cotacoes, o que permite combinar visao cadastral com comportamento de mercado.
2. A padronizacao previa das tabelas reduz inconsistencias antes da consolidacao final e melhora a confiabilidade das metricas mensais.
3. A camada `gold` concentra saidas voltadas para consulta e comparacao, com arquivos especificos para snapshot, ranking e evolucao temporal.
4. A estrutura do projeto favorece reproducibilidade e extensao futura, mantendo separacao clara entre fonte, processamento e artefatos analiticos.
