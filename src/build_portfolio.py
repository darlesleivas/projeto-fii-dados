from pathlib import Path

import pandas as pd


base_dir = Path(__file__).resolve().parents[1]
raw_dir = base_dir / "data" / "dataset_zip"
gold_dir = base_dir / "data" / "gold"


gold_dir.mkdir(parents=True, exist_ok=True)

if not raw_dir.exists():
    raise FileNotFoundError(
        "A pasta data/dataset_zip nao foi encontrada. Extraia o dataset antes de rodar o script."
    )

# 1. Ler as 4 tabelas que vamos usar no projeto
fundos = pd.read_parquet(
    raw_dir / "FundosImobiliarios.parquet",
    columns=["id", "nome", "cnpj", "visivel"],
)

tickers = pd.read_parquet(
    raw_dir / "Tickers.parquet",
    columns=["idFundoImobiliario", "codNegociacaoCota", "visivel"],
)

informes = pd.read_parquet(
    raw_dir / "InformesMensais.parquet",
    columns=["idFundoImobiliario", "dataInformacao", "totalCotistas", "valorPatrimonioLiquido"],
)

cotacoes = pd.read_parquet(
    raw_dir / "ticker-cotacoes.parquet",
    columns=["codigo", "periodo", "fechamento", "volume"],
)

# 2. Padronizar nomes de colunas para facilitar os joins
fundos = fundos.rename(columns={"id": "id_fundo", "nome": "fundo"})
tickers = tickers.rename(
    columns={"idFundoImobiliario": "id_fundo", "codNegociacaoCota": "ticker"}
)
informes = informes.rename(
    columns={
        "idFundoImobiliario": "id_fundo",
        "dataInformacao": "data_informacao",
        "totalCotistas": "total_cotistas",
        "valorPatrimonioLiquido": "patrimonio_liquido",
    }
)
cotacoes = cotacoes.rename(
    columns={
        "codigo": "ticker",
        "periodo": "data_pregao",
        "fechamento": "preco_fechamento",
        "volume": "volume_negociado",
    }
)

# 3. Fazer uma limpeza simples
fundos = fundos[fundos["visivel"] == True][["id_fundo", "fundo", "cnpj"]]
tickers = tickers[tickers["visivel"] == True][["id_fundo", "ticker"]]
tickers = tickers.dropna().drop_duplicates(subset=["id_fundo"]).copy()

informes["data_informacao"] = pd.to_datetime(informes["data_informacao"], errors="coerce")
informes["total_cotistas"] = pd.to_numeric(informes["total_cotistas"], errors="coerce")
informes["patrimonio_liquido"] = pd.to_numeric(informes["patrimonio_liquido"], errors="coerce")
informes = informes.dropna(subset=["id_fundo", "data_informacao"]).copy()
informes = informes[informes["total_cotistas"] >= 0].copy()
informes = informes[informes["patrimonio_liquido"] > 0].copy()

cotacoes["data_pregao"] = pd.to_datetime(cotacoes["data_pregao"], errors="coerce")
cotacoes["preco_fechamento"] = pd.to_numeric(cotacoes["preco_fechamento"], errors="coerce")
cotacoes["volume_negociado"] = pd.to_numeric(cotacoes["volume_negociado"], errors="coerce")
cotacoes = cotacoes.dropna(subset=["ticker", "data_pregao"]).copy()
cotacoes = cotacoes[cotacoes["preco_fechamento"] > 0].copy()

# 4. Pegar o dado mais recente de informes por fundo
informes_mais_recentes = (
    informes.sort_values("data_informacao")
    .groupby("id_fundo", as_index=False)
    .tail(1)
)

# 5. Pegar a cotacao mais recente por ticker
cotacoes_mais_recentes = (
    cotacoes.sort_values("data_pregao")
    .groupby("ticker", as_index=False)
    .tail(1)
)

# 6. Juntar tudo em uma tabela final
base_final = fundos.merge(tickers, on="id_fundo", how="left")
base_final = base_final.merge(informes_mais_recentes, on="id_fundo", how="left")
base_final = base_final.merge(cotacoes_mais_recentes, on="ticker", how="left")

# 7. Criar ranking simples para portfolio
ranking_fiis = base_final[
    [
        "ticker",
        "fundo",
        "cnpj",
        "data_informacao",
        "total_cotistas",
        "patrimonio_liquido",
        "preco_fechamento",
        "volume_negociado",
    ]
].dropna(subset=["ticker", "total_cotistas"])

ranking_fiis = ranking_fiis.sort_values("total_cotistas", ascending=False).head(15)

# 8. Criar uma segunda tabela com volume total por ticker
resumo_tickers = (
    cotacoes.groupby("ticker", as_index=False)
    .agg(
        dias_negociados=("data_pregao", "count"),
        volume_total=("volume_negociado", "sum"),
        ultimo_preco=("preco_fechamento", "last"),
    )
    .sort_values("volume_total", ascending=False)
    .head(15)
)

# 9. Salvar os arquivos finais
base_final.to_csv(gold_dir / "base_final_fiis.csv", index=False)
ranking_fiis.to_csv(gold_dir / "ranking_fiis.csv", index=False)
resumo_tickers.to_csv(gold_dir / "resumo_tickers.csv", index=False)

print("Projeto gerado com sucesso.")
print("Arquivos criados na pasta data/gold:")
print("- base_final_fiis.csv")
print("- ranking_fiis.csv")
print("- resumo_tickers.csv")
