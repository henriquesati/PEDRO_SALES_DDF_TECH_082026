"""
Script Utilitário para Geração de Metadados e Catálogo em Formato JSON Puro
Converte e unifica os metadados do Data Lakehouse e da Dadosfera em JSON estruturado
"""

import json
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = Path(__file__).resolve().parent.parent.parent.parent
DATALAKES_DIR = BASE_DIR / "pipelines" / "datalakes"
OUTPUTS_DIR = BASE_DIR / "pipelines" / "case-item-08" / "outputs"

CATALOG_METADATA = {
    "tenant": "treinamentos",
    "project_name": "recuperacao_carrinho_abandonado",
    "author": "Pedro Henrique Sales",
    "case_id": "PEDRO_SALES_DDF_TECH_082026",
    "framework": "Medallion Data Lakehouse Architecture (Bronze Raw -> Silver Qualify / Anomaly -> Gold Curated)",
    "layers": {
        "raw": {
            "display_name": "Zona Bronze (Raw Ingest)",
            "format": "parquet",
            "storage_prefix": "data/mock/output/parquet/",
            "entities": {
                "carrinhos_raw": {
                    "doc_id": "meta_raw_carrinhos_001",
                    "entity_name": "carrinhos_raw",
                    "dadosfera_asset_id": "e2d3b1bb-bf22-456e-bc66-4ac843deec82",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/e2d3b1bb-bf22-456e-bc66-4ac843deec82",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/carrinhos.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados & Webstore",
                    "upstream": {"source": "Webstore / E-commerce Session Collector", "protocol": "Batch S3 Landing"},
                    "downstream": [
                        {"layer": "qualify", "target": "qualify.carrinhos"},
                        {"layer": "anomaly", "target": "anomaly.carrinhos_anomalies"}
                    ],
                    "records_count": 7500,
                    "tags": ["carrinho_abandonado", "carrinhos", "transacional", "raw"]
                },
                "clientes_raw": {
                    "doc_id": "meta_raw_clientes_001",
                    "entity_name": "clientes_raw",
                    "dadosfera_asset_id": "0327fecc-f826-48fb-bb0a-1493fe18a32c",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/0327fecc-f826-48fb-bb0a-1493fe18a32c",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/clientes.parquet",
                    "classification": "Confidencial (PII)",
                    "owner": "Engenharia de Dados & CRM",
                    "upstream": {"source": "CRM / Cadastro de Usuários", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.clientes"}],
                    "records_count": 1500,
                    "tags": ["carrinho_abandonado", "clientes", "marketplace", "raw", "pii_sensivel"]
                },
                "produtos_raw": {
                    "doc_id": "meta_raw_produtos_001",
                    "entity_name": "produtos_raw",
                    "dadosfera_asset_id": "65fcfa25-a6f3-4cb8-a444-7fd23df3fa84",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/65fcfa25-a6f3-4cb8-a444-7fd23df3fa84",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/produtos.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados & Catálogo",
                    "upstream": {"source": "Catálogo de Produtos", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.produtos"}],
                    "records_count": 300,
                    "tags": ["carrinho_abandonado", "produtos", "catalogo", "raw"]
                },
                "itens_carrinho_raw": {
                    "doc_id": "meta_raw_itens_carrinho_001",
                    "entity_name": "itens_carrinho_raw",
                    "dadosfera_asset_id": "7649755a-c6e8-4b56-a092-be9eefde1dab",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/7649755a-c6e8-4b56-a092-be9eefde1dab",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/itens_carrinho.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados & Checkout",
                    "upstream": {"source": "Sessões de Carrinho", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.itens_carrinho"}],
                    "records_count": 18888,
                    "tags": ["carrinho_abandonado", "itens_carrinho", "raw"]
                },
                "eventos_carrinho_raw": {
                    "doc_id": "meta_raw_eventos_carrinho_001",
                    "entity_name": "eventos_carrinho_raw",
                    "dadosfera_asset_id": "397c3ebc-15cb-42d2-a717-a3b5d150c3ea",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/397c3ebc-15cb-42d2-a717-a3b5d150c3ea",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/eventos_carrinho.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados & Telemetria",
                    "upstream": {"source": "Clickstream Analytics", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.eventos_carrinho"}],
                    "records_count": 78931,
                    "tags": ["carrinho_abandonado", "eventos_carrinho", "telemetria", "raw"]
                },
                "eventos_resgate_raw": {
                    "doc_id": "meta_raw_eventos_resgate_001",
                    "entity_name": "eventos_resgate_raw",
                    "dadosfera_asset_id": "04739f6d-e8c3-4d6f-80b7-0f98c12a5798",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/04739f6d-e8c3-4d6f-80b7-0f98c12a5798",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/eventos_resgate.parquet",
                    "classification": "Interno",
                    "owner": "Marketing & CRM Operations",
                    "upstream": {"source": "CRM Dispatcher (Email, SMS, WhatsApp)", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.eventos_resgate"}],
                    "records_count": 6427,
                    "tags": ["carrinho_abandonado", "eventos_resgate", "recuperacao", "raw"]
                },
                "pedidos_raw": {
                    "doc_id": "meta_raw_pedidos_001",
                    "entity_name": "pedidos_raw",
                    "dadosfera_asset_id": "7f82a988-8e68-416a-b6fa-5007c4789d1a",
                    "direct_url": "https://app.dadosfera.ai/pt-BR/catalog/data-assets/7f82a988-8e68-416a-b6fa-5007c4789d1a",
                    "format": "parquet",
                    "storage_path": "data/mock/output/parquet/pedidos.parquet",
                    "classification": "Interno",
                    "owner": "Financeiro & Faturamento",
                    "upstream": {"source": "Gateway de Pagamentos / ERP", "protocol": "Batch S3 Landing"},
                    "downstream": [{"layer": "qualify", "target": "qualify.pedidos"}],
                    "records_count": 2229,
                    "tags": ["carrinho_abandonado", "pedidos", "conversoes", "raw"]
                }
            }
        },
        "qualify": {
            "display_name": "Zona Silver (Qualify Conforme)",
            "format": "Snowflake Table / Parquet",
            "schema": "CART_RECOVERY",
            "storage_prefix": "pipelines/case-item-08/outputs/qualify/",
            "entities": {
                "carrinhos_qualify": {
                    "doc_id": "meta_qualify_carrinhos_001",
                    "entity_name": "carrinhos_qualify",
                    "snowflake_table": "CART_RECOVERY.CARRINHOS",
                    "dadosfera_asset_id": "e2d3b1bb-bf22-456e-bc66-4ac843deec82",
                    "storage_path": "pipelines/case-item-08/outputs/qualify/carrinhos.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados",
                    "upstream": {"source": "raw.carrinhos_raw", "process": "Step 2 Validação & Qualify"},
                    "downstream": [{"layer": "curated", "target": "curated.fato_abandono"}],
                    "records_count": 7443,
                    "tags": ["qualify", "carrinhos", "conforme"]
                },
                "clientes_qualify": {
                    "doc_id": "meta_qualify_clientes_001",
                    "entity_name": "clientes_qualify",
                    "snowflake_table": "CART_RECOVERY.CLIENTES",
                    "dadosfera_asset_id": "0327fecc-f826-48fb-bb0a-1493fe18a32c",
                    "storage_path": "pipelines/case-item-08/outputs/qualify/clientes.parquet",
                    "classification": "Confidencial (PII)",
                    "owner": "Engenharia de Dados & CRM",
                    "upstream": {"source": "raw.clientes_raw", "process": "Step 2 Validação & Qualify"},
                    "downstream": [{"layer": "curated", "target": "curated.dim_clientes"}],
                    "records_count": 1500,
                    "tags": ["qualify", "clientes", "pii_sensivel"]
                },
                "eventos_resgate_qualify": {
                    "doc_id": "meta_qualify_resgate_001",
                    "entity_name": "eventos_resgate_qualify",
                    "snowflake_table": "CART_RECOVERY.EVENTOS_RESGATE",
                    "dadosfera_asset_id": "04739f6d-e8c3-4d6f-80b7-0f98c12a5798",
                    "storage_path": "pipelines/case-item-08/outputs/qualify/eventos_resgate.parquet",
                    "classification": "Interno",
                    "owner": "Engenharia de Dados & CRM",
                    "upstream": {"source": "raw.eventos_resgate_raw", "process": "Step 2 Validação & Qualify"},
                    "downstream": [{"layer": "curated", "target": "curated.fato_resgate"}],
                    "records_count": 6427,
                    "tags": ["qualify", "resgates", "marketing"]
                }
            }
        },
        "curated": {
            "display_name": "Zona Gold (Curated Kimball Star Schema)",
            "format": "Snowflake Table / View / Parquet",
            "schema": "GOLD_KIMBALL",
            "storage_prefix": "pipelines/case-item-08/outputs/curated/",
            "entities": {
                "dim_clientes": {
                    "doc_id": "meta_gold_dim_clientes_001",
                    "entity_name": "dim_clientes",
                    "snowflake_table": "GOLD_KIMBALL.DIM_CLIENTES",
                    "storage_path": "pipelines/case-item-08/outputs/curated/dim_clientes.parquet",
                    "classification": "Interno",
                    "upstream": {"source": "qualify.clientes", "process": "Step 4 Modelagem Dimensional"},
                    "downstream": [
                        {"consumer": "Metabase Dashboards", "purpose": "Segmentação RFM"},
                        {"consumer": "ML Training Pipeline", "purpose": "Propensity Features"}
                    ],
                    "records_count": 1500,
                    "tags": ["gold", "dimensao", "kimball", "clientes"]
                },
                "dim_tempo": {
                    "doc_id": "meta_gold_dim_tempo_001",
                    "entity_name": "dim_tempo",
                    "snowflake_table": "GOLD_KIMBALL.DIM_TEMPO",
                    "storage_path": "pipelines/case-item-08/outputs/curated/dim_tempo.parquet",
                    "classification": "Público",
                    "records_count": 731,
                    "tags": ["gold", "dimensao", "calendario"]
                },
                "dim_dispositivo": {
                    "doc_id": "meta_gold_dim_dispositivo_001",
                    "entity_name": "dim_dispositivo",
                    "snowflake_table": "GOLD_KIMBALL.DIM_DISPOSITIVO",
                    "storage_path": "pipelines/case-item-08/outputs/curated/dim_dispositivo.parquet",
                    "classification": "Interno",
                    "records_count": 3,
                    "tags": ["gold", "dimensao", "dispositivo"]
                },
                "dim_canal_resgate": {
                    "doc_id": "meta_gold_dim_canal_resgate_001",
                    "entity_name": "dim_canal_resgate",
                    "snowflake_table": "GOLD_KIMBALL.DIM_CANAL_RESGATE",
                    "storage_path": "pipelines/case-item-08/outputs/curated/dim_canal_resgate.parquet",
                    "classification": "Interno",
                    "records_count": 4,
                    "tags": ["gold", "dimensao", "canais_crm"]
                },
                "fato_abandono": {
                    "doc_id": "meta_gold_fato_abandono_001",
                    "entity_name": "fato_abandono",
                    "snowflake_table": "GOLD_KIMBALL.FATO_ABANDONO",
                    "storage_path": "pipelines/case-item-08/outputs/curated/fato_abandono.parquet",
                    "classification": "Interno",
                    "upstream": {"source": "qualify.carrinhos", "process": "Step 4 Modelagem Dimensional"},
                    "downstream": [{"consumer": "v_abandonment_summary", "purpose": "BI"}],
                    "records_count": 5183,
                    "tags": ["gold", "fato", "abandono", "gmv_em_risco"]
                },
                "fato_resgate": {
                    "doc_id": "meta_gold_fato_resgate_001",
                    "entity_name": "fato_resgate",
                    "snowflake_table": "GOLD_KIMBALL.FATO_RESGATE",
                    "storage_path": "pipelines/case-item-08/outputs/curated/fato_resgate.parquet",
                    "classification": "Interno",
                    "upstream": {"source": "qualify.eventos_resgate", "process": "Step 4 Modelagem Dimensional"},
                    "downstream": [
                        {"consumer": "v_recovery_roi_by_channel", "purpose": "ROI BI"},
                        {"consumer": "Step 5 ML Model", "purpose": "Supervised Training"}
                    ],
                    "records_count": 6427,
                    "tags": ["gold", "fato", "resgate", "roi_liquido"]
                },
                "v_abandonment_summary": {
                    "doc_id": "meta_gold_view_abandonment_001",
                    "entity_name": "v_abandonment_summary",
                    "snowflake_table": "GOLD_KIMBALL.V_ABANDONMENT_SUMMARY",
                    "storage_path": "pipelines/case-item-08/outputs/curated/v_abandonment_summary.parquet",
                    "classification": "Interno",
                    "records_count": 5183,
                    "tags": ["gold", "view", "metabase"]
                },
                "v_recovery_roi_by_channel": {
                    "doc_id": "meta_gold_view_roi_001",
                    "entity_name": "v_recovery_roi_by_channel",
                    "snowflake_table": "GOLD_KIMBALL.V_RECOVERY_ROI_BY_CHANNEL",
                    "storage_path": "pipelines/case-item-08/outputs/curated/v_recovery_roi_by_channel.parquet",
                    "classification": "Interno",
                    "records_count": 4,
                    "tags": ["gold", "view", "roi", "metabase"]
                }
            }
        }
    }
}


def main():
    OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)
    
    # 1. Salva o catálogo consolidado em JSON
    catalog_path = OUTPUTS_DIR / "catalog_assets.json"
    with open(catalog_path, "w", encoding="utf-8") as f:
        json.dump(CATALOG_METADATA, f, indent=2, ensure_ascii=False)
    print(f"✅ Catálogo consolidado gerado em JSON: {catalog_path}")

    # 2. Salva metadata.json individual em cada pasta de camada do Lakehouse
    for layer, ldata in CATALOG_METADATA["layers"].items():
        for entity_key, meta in ldata["entities"].items():
            target_dir = DATALAKES_DIR / layer / entity_key
            target_dir.mkdir(parents=True, exist_ok=True)
            json_file = target_dir / "metadata.json"
            with open(json_file, "w", encoding="utf-8") as f:
                json.dump(meta, f, indent=2, ensure_ascii=False)
            print(f"   -> Metadados JSON criados: {json_file.relative_to(BASE_DIR)}")

    print("\n🎉 Todos os metadados do Catálogo foram sincronizados e gerados em JSON puro com sucesso!")


if __name__ == "__main__":
    main()
