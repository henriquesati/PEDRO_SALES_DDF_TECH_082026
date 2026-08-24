"""
Configuração Imutável e Centralizada de Pipelines (Item 8 - Dadosfera)
Segue os padrões canônicos da skill declarative-functional-coding.
"""

from pathlib import Path
from types import MappingProxyType
from typing import Final, Literal, Mapping, TypeAlias, TypedDict

# =============================================================================
# 📁 Diretórios e Caminhos Base
# =============================================================================

BASE_DIR: Final[Path] = Path(__file__).resolve().parent.parent.parent.parent
ITEM_DIR: Final[Path] = BASE_DIR / "pipelines" / "case-item-08"
RAW_DATA_DIR: Final[Path] = BASE_DIR / "data" / "mock" / "output" / "parquet"
OUTPUTS_DIR: Final[Path] = ITEM_DIR / "outputs"
ASSETS_DIR: Final[Path] = OUTPUTS_DIR / "assets"
QUALIFY_DIR: Final[Path] = OUTPUTS_DIR / "qualify"
ANOMALIES_DIR: Final[Path] = OUTPUTS_DIR / "anomalies"
CURATED_DIR: Final[Path] = OUTPUTS_DIR / "curated"

# =============================================================================
# ⚙️ Perfis de Execução Imutáveis (Profile Pattern)
# =============================================================================

ProfileName: TypeAlias = Literal["dev", "standard", "rich"]


class ExecutionProfile(TypedDict):
    profile_name: ProfileName
    sample_limit: int | None
    enable_ml_training: bool
    ml_test_size: float
    random_state: int
    generate_charts: bool
    chart_dpi: int


PROFILES: Final[Mapping[ProfileName, ExecutionProfile]] = MappingProxyType(
    {
        "dev": {
            "profile_name": "dev",
            "sample_limit": 5_000,
            "enable_ml_training": True,
            "ml_test_size": 0.20,
            "random_state": 42,
            "generate_charts": True,
            "chart_dpi": 150,
        },
        "standard": {
            "profile_name": "standard",
            "sample_limit": None,  # Processa 100% da base (115.777+ registros)
            "enable_ml_training": True,
            "ml_test_size": 0.20,
            "random_state": 42,
            "generate_charts": True,
            "chart_dpi": 300,
        },
        "rich": {
            "profile_name": "rich",
            "sample_limit": None,
            "enable_ml_training": True,
            "ml_test_size": 0.25,
            "random_state": 42,
            "generate_charts": True,
            "chart_dpi": 300,
        },
    }
)

ACTIVE_PROFILE_NAME: Final[ProfileName] = "standard"
ACTIVE_CONFIG: Final[ExecutionProfile] = PROFILES[ACTIVE_PROFILE_NAME]

# =============================================================================
# 🏛️ Catálogo de Entidades e Mapeamento de Arquivos
# =============================================================================

ENTITY_FILES: Final[Mapping[str, str]] = MappingProxyType(
    {
        "clientes": "clientes.parquet",
        "produtos": "produtos.parquet",
        "carrinhos": "carrinhos.parquet",
        "itens_carrinho": "itens_carrinho.parquet",
        "eventos_carrinho": "eventos_carrinho.parquet",
        "eventos_resgate": "eventos_resgate.parquet",
        "pedidos": "pedidos.parquet",
    }
)

# Metadados e IDs Dadosfera
DADOSFERA_METADATA: Final[Mapping[str, str]] = MappingProxyType(
    {
        "workspace_id": "pedro-sales-ddf-tech-082026",
        "pipeline_id": "pipe_cart_recovery_medallion_001",
        "snowpark_session_app": "Dadosfera_Snowpark_CartRecovery",
        "snowflake_database": "CART_RECOVERY_DW",
        "snowflake_schema_bronze": "BRONZE_RAW",
        "snowflake_schema_silver": "SILVER_QUALIFY",
        "snowflake_schema_gold": "GOLD_KIMBALL",
    }
)
