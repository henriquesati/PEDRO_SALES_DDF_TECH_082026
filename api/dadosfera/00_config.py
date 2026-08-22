"""
00_config.py - Configuracao Central do Pipeline de API Dadosfera
================================================================
Fonte unica de verdade para credenciais, URLs, constantes de nomes
e caminhos de arquivo usados em todas as fases do pipeline.

INPUT:  nenhum (configuracao estatica)
OUTPUT: modulo importavel com constantes e helpers
"""

from pathlib import Path
import logging

# ─── CREDENCIAIS ──────────────────────────────────────────────────────────────
DADOSFERA_USERNAME      = "pedrohenriquebtcc@gmail.com"
DADOSFERA_PASSWORD      = "Is@que2000"
DADOSFERA_CUSTOMER_NAME = "pedro-sales"

# ─── URLS BASE DA API ─────────────────────────────────────────────────────────
API_BASE_URL            = "https://maestro.dadosfera.ai"
ENDPOINT_AUTH_SIGNIN    = f"{API_BASE_URL}/auth/sign-in"
ENDPOINT_AUTH_REFRESH   = f"{API_BASE_URL}/auth/refresh-access-token"
ENDPOINT_STORAGE_UPLOAD = f"{API_BASE_URL}/storage-explorer/storage/upload/batch"
ENDPOINT_STORAGE_TABLES = f"{API_BASE_URL}/storage-explorer/tables"
ENDPOINT_CATALOG_SEARCH = f"{API_BASE_URL}/catalog"


def endpoint_link_dataset(table_id: str) -> str:
    """Retorna o endpoint para vincular um dataset a uma tabela."""
    return f"{API_BASE_URL}/storage-explorer/tables/{table_id}/datasets"


# ─── NOMES DO CASE ────────────────────────────────────────────────────────────
CASE_NAME               = "recuperacao_carrinho"
DATALAKE_ZONE_RAW       = "raw"
DATALAKE_ZONE_QUALIFY   = "qualify"
STORAGE_FOLDER_RAW      = f"/{DATALAKE_ZONE_RAW}/{CASE_NAME}"
SNOWFLAKE_SCHEMA_NAME   = "CART_RECOVERY"

# ─── ENTIDADES (ordem = dependencia referencial) ──────────────────────────────
ENTITIES = [
    "clientes",
    "produtos",
    "carrinhos",
    "itens_carrinho",
    "eventos_carrinho",
    "eventos_resgate",
    "pedidos",
]

# ─── CAMINHOS DE ARQUIVO ──────────────────────────────────────────────────────
REPO_ROOT         = Path(__file__).resolve().parents[2]
CSV_DIR           = REPO_ROOT / "data" / "mock" / "output" / "csv"
PARQUET_DIR       = REPO_ROOT / "data" / "mock" / "output" / "parquet"
STATE_DIR         = Path(__file__).resolve().parent / ".state"
STATE_TOKEN_FILE  = STATE_DIR / "auth_tokens.json"
STATE_UPLOADS_FILE= STATE_DIR / "uploaded_datasets.json"
STATE_TABLES_FILE = STATE_DIR / "created_tables.json"
STATE_LINKS_FILE  = STATE_DIR / "linked_datasets.json"
CATALOG_REPORT    = STATE_DIR / "catalog_report.md"

# ─── LOGGING ─────────────────────────────────────────────────────────────────
LOG_FORMAT = "%(asctime)s [%(levelname)s] %(name)s - %(message)s"

def get_logger(name: str) -> logging.Logger:
    """Configura e retorna um logger padrao para o pipeline."""
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    return logging.getLogger(name)

# ─── HELPERS ─────────────────────────────────────────────────────────────────
def ensure_state_dir() -> None:
    """Garante que o diretorio de estado existe."""
    STATE_DIR.mkdir(parents=True, exist_ok=True)
