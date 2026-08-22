# Output Mappers — Dadosfera API & Data Assets

Este diretório contém os mapeadores de saída e registros de identificadores (`Data Asset IDs`) gerados na plataforma Dadosfera para as 7 entidades do case.

## Arquivos Disponíveis

1. **[`assets_registry.md`](assets_registry.md)**:
   - Tabela legível com links diretos, IDs oficiais, contagem de linhas e detalhamento de cada entidade para documentação humana e relatórios de entrega.
2. **[`assets_registry.json`](assets_registry.json)**:
   - Estrutura JSON programática contendo o mapa chave-valor (`entity` -> `data_asset_id`, `direct_url`, `snowflake_table`, `record_count`, etc.) para consumo por scripts de Data Quality, pipelines e notebooks de IA.
