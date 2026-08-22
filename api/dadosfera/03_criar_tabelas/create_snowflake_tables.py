"""
03_criar_tabelas/create_snowflake_tables.py - FASE 3: Criacao de Tabelas no Snowflake
======================================================================================
Define o schema das 7 entidades e cria as tabelas correspondentes no Snowflake
via POST /storage-explorer/tables.

FASE:   3 de 5
INPUT:  accessToken (de .state/auth_tokens.json)
OUTPUT: .state/created_tables.json com table_id de cada tabela criada
"""

import sys
import json
import time
from pathlib import Path

import requests

# ─── Import config
import importlib.util
_cfg_path = Path(__file__).resolve().parents[1] / "00_config.py"
_spec = importlib.util.spec_from_file_location("cfg", _cfg_path)
_cfg  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cfg)

_auth_path = Path(__file__).resolve().parents[1] / "01_auth" / "authenticate.py"
_aspec = importlib.util.spec_from_file_location("auth", _auth_path)
_auth  = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(_auth)

ENTITIES               = _cfg.ENTITIES
ENDPOINT_STORAGE_TABLES= _cfg.ENDPOINT_STORAGE_TABLES
SNOWFLAKE_SCHEMA_NAME  = _cfg.SNOWFLAKE_SCHEMA_NAME
STATE_TABLES_FILE      = _cfg.STATE_TABLES_FILE
ensure_state_dir       = _cfg.ensure_state_dir
get_logger             = _cfg.get_logger
refresh_token_if_needed = _auth.refresh_token_if_needed

log = get_logger("fase3.tabelas")


# ─── SCHEMAS DAS 7 ENTIDADES ─────────────────────────────────────────────────
# Cada schema define: nome da tabela, descricao e colunas tipadas
TABLE_SCHEMAS = {
    "clientes": {
        "name":        "clientes",
        "description": "Dados cadastrais dos clientes do marketplace",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "cliente_id",          "type": "VARCHAR",   "description": "Identificador unico do cliente"},
            {"name": "nome",                "type": "VARCHAR",   "description": "Nome completo"},
            {"name": "email",               "type": "VARCHAR",   "description": "Email de contato"},
            {"name": "telefone",            "type": "VARCHAR",   "description": "Telefone de contato"},
            {"name": "cidade",              "type": "VARCHAR",   "description": "Cidade de residencia"},
            {"name": "estado",              "type": "VARCHAR",   "description": "Estado (UF)"},
            {"name": "data_cadastro",       "type": "TIMESTAMP", "description": "Data de cadastro na plataforma"},
            {"name": "segmento",            "type": "VARCHAR",   "description": "Segmento comportamental do cliente"},
            {"name": "canal_aquisicao",     "type": "VARCHAR",   "description": "Canal de aquisicao do cliente"},
            {"name": "ltv_estimado",        "type": "FLOAT",     "description": "Lifetime Value estimado em R$"},
            {"name": "total_pedidos",       "type": "INTEGER",   "description": "Total de pedidos realizados"},
            {"name": "ticket_medio",        "type": "FLOAT",     "description": "Ticket medio por pedido"},
        ],
    },
    "produtos": {
        "name":        "produtos",
        "description": "Catalogo de produtos disponiveis no marketplace",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "produto_id",          "type": "VARCHAR",   "description": "Identificador unico do produto"},
            {"name": "nome",                "type": "VARCHAR",   "description": "Nome do produto"},
            {"name": "categoria",           "type": "VARCHAR",   "description": "Categoria do produto"},
            {"name": "subcategoria",        "type": "VARCHAR",   "description": "Subcategoria"},
            {"name": "preco",               "type": "FLOAT",     "description": "Preco atual em R$"},
            {"name": "estoque",             "type": "INTEGER",   "description": "Quantidade em estoque"},
            {"name": "marca",               "type": "VARCHAR",   "description": "Marca do produto"},
            {"name": "avaliacao_media",     "type": "FLOAT",     "description": "Nota media de avaliacoes (0-5)"},
            {"name": "num_avaliacoes",      "type": "INTEGER",   "description": "Numero total de avaliacoes"},
            {"name": "ativo",               "type": "BOOLEAN",   "description": "Se o produto esta ativo"},
        ],
    },
    "carrinhos": {
        "name":        "carrinhos",
        "description": "Carrinhos de compra criados pelos clientes",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "carrinho_id",         "type": "VARCHAR",   "description": "Identificador unico do carrinho"},
            {"name": "cliente_id",          "type": "VARCHAR",   "description": "FK: cliente proprietario"},
            {"name": "criado_em",           "type": "TIMESTAMP", "description": "Data/hora de criacao"},
            {"name": "atualizado_em",       "type": "TIMESTAMP", "description": "Data/hora da ultima atualizacao"},
            {"name": "status",              "type": "VARCHAR",   "description": "Status: aberto, abandonado, convertido"},
            {"name": "valor_total",         "type": "FLOAT",     "description": "Valor total dos itens em R$"},
            {"name": "num_itens",           "type": "INTEGER",   "description": "Numero de itens no carrinho"},
            {"name": "canal",               "type": "VARCHAR",   "description": "Canal: web, mobile, app"},
            {"name": "abandono_em",         "type": "TIMESTAMP", "description": "Data/hora do abandono (se aplicavel)"},
            {"name": "tempo_ate_abandono_min", "type": "FLOAT",  "description": "Minutos entre criacao e abandono"},
        ],
    },
    "itens_carrinho": {
        "name":        "itens_carrinho",
        "description": "Itens adicionados a cada carrinho",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "item_id",             "type": "VARCHAR",   "description": "Identificador unico do item"},
            {"name": "carrinho_id",         "type": "VARCHAR",   "description": "FK: carrinho pai"},
            {"name": "produto_id",          "type": "VARCHAR",   "description": "FK: produto"},
            {"name": "quantidade",          "type": "INTEGER",   "description": "Quantidade adicionada"},
            {"name": "preco_unitario",      "type": "FLOAT",     "description": "Preco unitario no momento da adicao"},
            {"name": "subtotal",            "type": "FLOAT",     "description": "quantidade x preco_unitario"},
            {"name": "adicionado_em",       "type": "TIMESTAMP", "description": "Data/hora de adicao ao carrinho"},
            {"name": "desconto_aplicado",   "type": "FLOAT",     "description": "Desconto aplicado ao item (R$)"},
        ],
    },
    "eventos_carrinho": {
        "name":        "eventos_carrinho",
        "description": "Log de eventos de interacao com carrinhos (maior tabela - 72k+ linhas)",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "evento_id",           "type": "VARCHAR",   "description": "Identificador unico do evento"},
            {"name": "carrinho_id",         "type": "VARCHAR",   "description": "FK: carrinho relacionado"},
            {"name": "cliente_id",          "type": "VARCHAR",   "description": "FK: cliente"},
            {"name": "tipo_evento",         "type": "VARCHAR",   "description": "Tipo: visualizacao, adicao, remocao, abandono"},
            {"name": "ocorrido_em",         "type": "TIMESTAMP", "description": "Data/hora do evento"},
            {"name": "canal",               "type": "VARCHAR",   "description": "Canal de origem"},
            {"name": "dispositivo",         "type": "VARCHAR",   "description": "Dispositivo: desktop, mobile, tablet"},
            {"name": "sessao_id",           "type": "VARCHAR",   "description": "Identificador da sessao"},
            {"name": "produto_id",          "type": "VARCHAR",   "description": "FK: produto envolvido (se aplicavel)"},
            {"name": "metadata",            "type": "VARIANT",   "description": "Dados adicionais do evento em JSON"},
        ],
    },
    "eventos_resgate": {
        "name":        "eventos_resgate",
        "description": "Tentativas de recuperacao de carrinhos abandonados",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "resgate_id",          "type": "VARCHAR",   "description": "Identificador unico do evento de resgate"},
            {"name": "carrinho_id",         "type": "VARCHAR",   "description": "FK: carrinho alvo"},
            {"name": "cliente_id",          "type": "VARCHAR",   "description": "FK: cliente alvo"},
            {"name": "canal_resgate",       "type": "VARCHAR",   "description": "Canal: email, sms, push, whatsapp"},
            {"name": "enviado_em",          "type": "TIMESTAMP", "description": "Data/hora do envio"},
            {"name": "aberto_em",           "type": "TIMESTAMP", "description": "Data/hora de abertura (se ocorreu)"},
            {"name": "clicado_em",          "type": "TIMESTAMP", "description": "Data/hora do clique (se ocorreu)"},
            {"name": "convertido",          "type": "BOOLEAN",   "description": "Se resultou em conversao"},
            {"name": "convertido_em",       "type": "TIMESTAMP", "description": "Data/hora da conversao"},
            {"name": "valor_recuperado",    "type": "FLOAT",     "description": "Valor recuperado em R$ (se convertido)"},
            {"name": "tipo_oferta",         "type": "VARCHAR",   "description": "Tipo de oferta: desconto, frete_gratis, lembrete"},
            {"name": "desconto_oferecido",  "type": "FLOAT",     "description": "Percentual de desconto oferecido"},
        ],
    },
    "pedidos": {
        "name":        "pedidos",
        "description": "Pedidos efetivados (conversoes de carrinhos)",
        "schema":      SNOWFLAKE_SCHEMA_NAME,
        "columns": [
            {"name": "pedido_id",           "type": "VARCHAR",   "description": "Identificador unico do pedido"},
            {"name": "carrinho_id",         "type": "VARCHAR",   "description": "FK: carrinho que originou o pedido"},
            {"name": "cliente_id",          "type": "VARCHAR",   "description": "FK: cliente"},
            {"name": "criado_em",           "type": "TIMESTAMP", "description": "Data/hora de criacao do pedido"},
            {"name": "valor_total",         "type": "FLOAT",     "description": "Valor total do pedido em R$"},
            {"name": "desconto_total",      "type": "FLOAT",     "description": "Total de descontos aplicados"},
            {"name": "valor_frete",         "type": "FLOAT",     "description": "Custo do frete em R$"},
            {"name": "status",              "type": "VARCHAR",   "description": "Status: aprovado, enviado, entregue, cancelado"},
            {"name": "metodo_pagamento",    "type": "VARCHAR",   "description": "Metodo: cartao, boleto, pix"},
            {"name": "num_parcelas",        "type": "INTEGER",   "description": "Numero de parcelas (se cartao)"},
            {"name": "origem_resgate",      "type": "BOOLEAN",   "description": "Se o pedido veio de um resgate de carrinho"},
            {"name": "resgate_id",          "type": "VARCHAR",   "description": "FK: resgate que gerou o pedido (se aplicavel)"},
        ],
    },
}


def create_table(token: str, entity: str, schema_def: dict) -> dict:
    """
    Cria uma tabela no Snowflake via POST /storage-explorer/tables.
    Retorna dict com table_id e resultado.
    """
    headers = {
        "Authorization": token,
        "Content-Type":  "application/json",
    }

    payload = {
        "name":        schema_def["name"],
        "description": schema_def["description"],
        "schema":      schema_def["schema"],
        "columns":     schema_def["columns"],
    }

    log.info(f"  POST /storage-explorer/tables → {entity}")
    resp = requests.post(ENDPOINT_STORAGE_TABLES, headers=headers, json=payload, timeout=60)

    if resp.status_code not in (200, 201):
        log.error(f"  Erro ao criar tabela {entity}: {resp.status_code} - {resp.text[:500]}")
        return {
            "entity": entity,
            "status": "error",
            "code":   resp.status_code,
            "detail": resp.text[:500],
        }

    data = resp.json()
    table_id = (
        data.get("tableId")
        or data.get("table_id")
        or data.get("id")
    )

    log.info(f"  [OK] {entity} -> table_id={table_id}")
    return {
        "entity":   entity,
        "table_id": table_id,
        "name":     schema_def["name"],
        "schema":   schema_def["schema"],
        "status":   "success",
        "raw":      data,
    }


def create_all_tables() -> list[dict]:
    """
    Cria as 7 tabelas no Snowflake e persiste os table_ids.
    Retorna lista de resultados.
    """
    log.info("=== FASE 3: Criacao de Tabelas no Snowflake ===")
    log.info(f"Schema Snowflake: {SNOWFLAKE_SCHEMA_NAME}")
    log.info(f"Total de tabelas: {len(ENTITIES)}")

    token = refresh_token_if_needed()
    results = []

    for i, entity in enumerate(ENTITIES, 1):
        schema_def = TABLE_SCHEMAS[entity]
        log.info(f"\n[{i}/{len(ENTITIES)}] {entity} ({len(schema_def['columns'])} colunas)")
        result = create_table(token, entity, schema_def)
        results.append(result)

        if i < len(ENTITIES):
            time.sleep(0.5)

    # Persiste estado
    ensure_state_dir()
    STATE_TABLES_FILE.write_text(json.dumps(results, indent=2, ensure_ascii=False))

    # Sumario
    success = [r for r in results if r.get("status") == "success"]
    errors  = [r for r in results if r.get("status") != "success"]
    log.info(f"\n=== RESUMO FASE 3 ===")
    log.info(f"  [OK] Tabelas criadas: {len(success)}/{len(ENTITIES)}")
    if errors:
        log.warning(f"  [ERRO] Falhas: {len(errors)}")
        for e in errors:
            log.warning(f"    - {e['entity']}: {e.get('detail', e.get('status'))}")
    log.info(f"  Estado salvo em: {STATE_TABLES_FILE}")

    return results


if __name__ == "__main__":
    results = create_all_tables()
    print(f"\n[OK] Fase 3 concluida: {sum(1 for r in results if r.get('status') == 'success')}/{len(ENTITIES)} tabelas criadas")
