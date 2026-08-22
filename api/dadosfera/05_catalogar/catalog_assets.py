"""
05_catalogar/catalog_assets.py - FASE 5: Catalogacao de Ativos na Dadosfera
===========================================================================
Registra e consulta os 7 ativos de dados no Catalogo da Dadosfera via API Maestro
(POST /catalog e GET /catalog). Gera relatorio consolidado em Markdown.

FASE:   5 de 5
INPUT:  accessToken (de .state/auth_tokens.json)
OUTPUT: .state/catalog_report.md com relatorio e IDs oficiais gerados na Dadosfera
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime, timezone

import requests

# ─── Import config via importlib
import importlib.util
_cfg_path = Path(__file__).resolve().parents[1] / "00_config.py"
_spec = importlib.util.spec_from_file_location("cfg", _cfg_path)
_cfg  = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_cfg)

_auth_path = Path(__file__).resolve().parents[1] / "01_auth" / "authenticate.py"
_aspec = importlib.util.spec_from_file_location("auth", _auth_path)
_auth  = importlib.util.module_from_spec(_aspec)
_aspec.loader.exec_module(_auth)

ENTITIES                = _cfg.ENTITIES
CASE_NAME               = _cfg.CASE_NAME
ENDPOINT_CATALOG_SEARCH = _cfg.ENDPOINT_CATALOG_SEARCH
CATALOG_REPORT          = _cfg.CATALOG_REPORT
STATE_DIR               = _cfg.STATE_DIR
ensure_state_dir        = _cfg.ensure_state_dir
get_logger              = _cfg.get_logger
refresh_token_if_needed = _auth.refresh_token_if_needed

log = get_logger("fase5.catalogar")

# ─── METADADOS DAS 7 ENTIDADES PARA CATALOGACAO ──────────────────────────────
CATALOG_METADATA = [
    {
        "entity": "clientes",
        "display_name": "clientes",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "clientes", "marketplace", "qualify", "dimensao", "pii_sensivel"],
        "description": (
            "### Entidade: Clientes (Dimensão Cadastral & RFM)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.CLIENTES | **Volumetria:** 2.000 registros\n\n"
            "**Visão de Negócio:** Consolida o perfil demográfico, canal de aquisição e segmentação RFM (Recency, Frequency, Monetary) dos clientes para campanhas personalizadas de resgate.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `cliente_id` (VARCHAR, PK): Identificador UUID exclusivo do cliente.\n"
            "- `nome` (VARCHAR, PII): Nome completo do cliente (Dado Sensível LGPD).\n"
            "- `email` (VARCHAR, PII): Endereço de email primário para envio de lembretes e descontos.\n"
            "- `telefone` (VARCHAR, PII): Telefone para contato via WhatsApp/SMS.\n"
            "- `cidade` / `estado` (VARCHAR): Localização geográfica para análise de frete regional.\n"
            "- `data_cadastro` (TIMESTAMP): Data e hora de registro no e-commerce.\n"
            "- `segmento` (VARCHAR): Segmento comportamental ('premium', 'regular', 'dormant', 'novo').\n"
            "- `canal_aquisicao` (VARCHAR): Canal de origem ('organico', 'pago', 'rede_social', 'indicacao').\n"
            "- `ltv_estimado` (FLOAT): Lifetime Value estimado em R$.\n"
            "- `total_pedidos` (INTEGER): Total de compras finalizadas.\n"
            "- `ticket_medio` (FLOAT): Gasto médio por pedido."
        )
    },
    {
        "entity": "produtos",
        "display_name": "produtos",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "produtos", "catalogo", "qualify", "dimensao"],
        "description": (
            "### Entidade: Produtos (Catálogo & Estoque)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.PRODUTOS | **Volumetria:** 500 registros\n\n"
            "**Visão de Negócio:** Catálogo central de itens comercializados no marketplace com controle de estoque, faixas de preço e avaliações dos consumidores.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `produto_id` (VARCHAR, PK): Identificador UUID exclusivo do produto.\n"
            "- `nome` (VARCHAR): Título descritivo do produto visível no e-commerce.\n"
            "- `categoria` (VARCHAR): Categoria macro (ex: Eletrônicos, Moda, Casa).\n"
            "- `subcategoria` (VARCHAR): Tipo detalhado do produto.\n"
            "- `preco` (FLOAT): Preço atual de venda em R$.\n"
            "- `estoque` (INTEGER): Quantidade física disponível no centro de distribuição.\n"
            "- `marca` (VARCHAR): Fabricante ou marca comercial.\n"
            "- `avaliacao_media` (FLOAT): Nota média de satisfação (0 a 5 estrelas).\n"
            "- `num_avaliacoes` (INTEGER): Volume total de reviews recebidos.\n"
            "- `ativo` (BOOLEAN): Flag indicadora de disponibilidade para venda."
        )
    },
    {
        "entity": "carrinhos",
        "display_name": "carrinhos",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "carrinhos", "transacional", "qualify", "fato_central"],
        "description": (
            "### Entidade: Carrinhos (Sessões & Lifecycle de Compra)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.CARRINHOS | **Volumetria:** 15.000 registros\n\n"
            "**Visão de Negócio:** Tabela central do case de marketing. Registra sessões de carrinho, status de conversão/abandono e timing de inatividade para disparo de resgate.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `carrinho_id` (VARCHAR, PK): Identificador UUID exclusivo da sessão de carrinho.\n"
            "- `cliente_id` (VARCHAR, FK): Referência ao cliente proprietário da sessão.\n"
            "- `criado_em` (TIMESTAMP): Data/hora de inicialização do carrinho.\n"
            "- `atualizado_em` (TIMESTAMP): Data/hora da última alteração de itens.\n"
            "- `status` (VARCHAR): Situação atual ('ativo', 'abandonado', 'recuperado', 'comprado', 'expirado').\n"
            "- `valor_total` (FLOAT): Valor monetário total dos itens em R$.\n"
            "- `num_itens` (INTEGER): Quantidade de itens físicos no carrinho.\n"
            "- `canal` (VARCHAR): Plataforma de origem ('web', 'mobile', 'app').\n"
            "- `abandono_em` (TIMESTAMP): Momento de marcação de abandono (30min inativo).\n"
            "- `tempo_ate_abandono_min` (FLOAT): Minutos decorridos até a desistência."
        )
    },
    {
        "entity": "itens_carrinho",
        "display_name": "itens_carrinho",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "itens_carrinho", "itens", "qualify", "fato_detalhe"],
        "description": (
            "### Entidade: Itens do Carrinho (Composição do Carrinho)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.ITENS_CARRINHO | **Volumetria:** 22.500 registros\n\n"
            "**Visão de Negócio:** Detalha a composição de produtos adicionados em cada carrinho, snapshots de preço e descontos aplicados por item.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `item_id` (VARCHAR, PK): Identificador UUID exclusivo da linha de item.\n"
            "- `carrinho_id` (VARCHAR, FK): Referência ao carrinho pai.\n"
            "- `produto_id` (VARCHAR, FK): Referência ao produto adicionado.\n"
            "- `quantidade` (INTEGER): Quantidade de unidades adicionadas.\n"
            "- `preco_unitario` (FLOAT): Preço unitário no momento da adição.\n"
            "- `subtotal` (FLOAT): Valor bruto (quantidade * preco_unitario).\n"
            "- `adicionado_em` (TIMESTAMP): Instante exato de adição ao carrinho.\n"
            "- `desconto_aplicado` (FLOAT): Valor monetário de desconto deduzido."
        )
    },
    {
        "entity": "eventos_carrinho",
        "display_name": "eventos_carrinho",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "eventos_carrinho", "telemetria", "qualify", "timeseries"],
        "description": (
            "### Entidade: Eventos de Carrinho (Telemetria & Funil de Conversão)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.EVENTOS_CARRINHO | **Volumetria:** 72.026 registros\n\n"
            "**Visão de Negócio:** Log de cliques, navegação e erros técnicos (gateway de pagamento) que antecedem o abandono ou conversão da compra.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `evento_id` (VARCHAR, PK): Identificador UUID da ação de telemetria.\n"
            "- `carrinho_id` (VARCHAR, FK): Sessão de carrinho associada.\n"
            "- `cliente_id` (VARCHAR, FK): Cliente que executou a ação.\n"
            "- `tipo_evento` (VARCHAR): Ação ('view_produto', 'add_carrinho', 'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno').\n"
            "- `ocorrido_em` (TIMESTAMP): Data e hora precisa do evento.\n"
            "- `canal` (VARCHAR): Canal ('web', 'mobile', 'app').\n"
            "- `dispositivo` (VARCHAR): Aparelho ('desktop', 'mobile', 'tablet').\n"
            "- `sessao_id` (VARCHAR): Identificador da sessão contínua.\n"
            "- `produto_id` (VARCHAR, FK): Produto relacionado à ação (opcional).\n"
            "- `metadata` (VARIANT): Detalhes técnicos contextuais em JSON."
        )
    },
    {
        "entity": "eventos_resgate",
        "display_name": "eventos_resgate",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "eventos_resgate", "recuperacao", "qualify", "crm_marketing"],
        "description": (
            "### Entidade: Eventos de Resgate (Campanhas Multicanal & ROI)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.EVENTOS_RESGATE | **Volumetria:** 2.500 registros\n\n"
            "**Visão de Negócio:** Rastreia o funil de comunicação pós-abandono (Envio ➔ Abertura ➔ Clique ➔ Conversão), canais (Email, SMS, WhatsApp, Push) e ROI de campanhas.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `resgate_id` (VARCHAR, PK): Identificador UUID do disparo de comunicação.\n"
            "- `carrinho_id` (VARCHAR, FK): Carrinho alvo da recuperação.\n"
            "- `cliente_id` (VARCHAR, FK): Destinatário da mensagem.\n"
            "- `canal_resgate` (VARCHAR): Meio utilizado ('email', 'sms', 'push_app', 'whatsapp').\n"
            "- `enviado_em` (TIMESTAMP): Data/hora do disparo da mensagem.\n"
            "- `aberto_em` (TIMESTAMP): Instante de abertura pelo cliente.\n"
            "- `clicado_em` (TIMESTAMP): Instante de clique no link de recuperação.\n"
            "- `convertido` (BOOLEAN): Se resultou em compra finalizada.\n"
            "- `convertido_em` (TIMESTAMP): Momento da conversão.\n"
            "- `valor_recuperado` (FLOAT): Valor monetário do pedido recuperado em R$.\n"
            "- `tipo_oferta` (VARCHAR): Benefício ('desconto', 'frete_gratis', 'lembrete').\n"
            "- `desconto_oferecido` (FLOAT): Percentual de desconto concedido."
        )
    },
    {
        "entity": "pedidos",
        "display_name": "pedidos",
        "data_asset_type": "dataset",
        "tags": ["carrinho_abandonado", "pedidos", "conversoes", "qualify", "faturamento"],
        "description": (
            "### Entidade: Pedidos (Conversões & Faturamento Final)\n"
            "**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.PEDIDOS | **Volumetria:** 2.000 registros\n\n"
            "**Visão de Negócio:** Compras efetivadas no marketplace, atribuindo faturamento direto a compras espontâneas ou recuperadas via campanhas de resgate.\n\n"
            "**Dicionário de Colunas:**\n"
            "- `pedido_id` (VARCHAR, PK): Identificador UUID da compra aprovada.\n"
            "- `carrinho_id` (VARCHAR, FK): Carrinho que originou o pedido.\n"
            "- `cliente_id` (VARCHAR, FK): Comprador.\n"
            "- `criado_em` (TIMESTAMP): Data e hora da conclusão do pedido.\n"
            "- `valor_total` (FLOAT): Valor líquido pago (Subtotal - Desconto + Frete).\n"
            "- `desconto_total` (FLOAT): Total de abatimentos aplicados em R$.\n"
            "- `valor_frete` (FLOAT): Custo cobrado para entrega em R$.\n"
            "- `status` (VARCHAR): Situação ('aprovado', 'enviado', 'entregue', 'cancelado').\n"
            "- `metodo_pagamento` (VARCHAR): Forma de pagamento ('cartao', 'boleto', 'pix').\n"
            "- `num_parcelas` (INTEGER): Parcelas no cartão (1 a 12).\n"
            "- `origem_resgate` (BOOLEAN): Flag indicadora de compra vinda de campanha.\n"
            "- `resgate_id` (VARCHAR, FK): Referência à mensagem de resgate que gerou a venda."
        )
    }
]


def register_assets_in_catalog(token: str) -> list[dict]:
    """
    Registra ou sincroniza as 7 entidades no Catalogo da Dadosfera via POST ou PUT /catalog.
    """
    headers = {"Authorization": token, "Content-Type": "application/json"}
    registered = []

    # Carrega ativos existentes
    existing = list_catalog_assets(token)
    existing_map = {
        a.get("display_name", ""): a.get("id")
        for a in existing
        if not a.get("display_name", "").startswith("[DUPLICATA]")
    }

    log.info("Sincronizando ativos com Dicionário de Dados no Catálogo Dadosfera...")

    for meta in CATALOG_METADATA:
        entity = meta["entity"]
        payload = {
            "display_name": meta["display_name"],
            "description": meta["description"],
            "data_asset_type": meta["data_asset_type"],
            "tags": meta["tags"]
        }

        # Se já existe, atualiza via PUT
        if entity in existing_map:
            asset_id = existing_map[entity]
            try:
                resp = requests.put(f"https://maestro.dadosfera.ai/catalog/data-asset/{asset_id}", headers=headers, json=payload, timeout=20)
                if resp.status_code in (200, 201):
                    log.info(f"  [ATUALIZADO] {entity:<17} (ID: {asset_id[:12]}...) -> Dicionário sincronizado!")
                    registered.append({
                        "entity": entity,
                        "id": asset_id,
                        "name": meta["display_name"],
                        "description": meta["description"],
                        "status": "cataloged_updated",
                    })
                else:
                    log.warning(f"  [AVISO] {entity}: Falha no update ({resp.status_code})")
            except Exception as e:
                log.error(f"  [ERRO] {entity}: {e}")
            continue

        # Caso não exista, cria via POST
        try:
            resp = requests.post(ENDPOINT_CATALOG_SEARCH, headers=headers, json=payload, timeout=30)
            if resp.status_code in (200, 201):
                data = resp.json()
                asset_obj = data.get("data_asset", {})
                asset_id = asset_obj.get("id") or asset_obj.get("data_asset_id")
                log.info(f"  [CRIADO] {entity:<17} -> ID: {asset_id}")
                registered.append({
                    "entity": entity,
                    "id": asset_id,
                    "name": meta["display_name"],
                    "description": meta["description"],
                    "status": "cataloged",
                    "created_at": asset_obj.get("created_at") or asset_obj.get("createdAt")
                })
            else:
                log.warning(f"  [AVISO] {entity}: {resp.status_code} - {resp.text[:100]}")
                registered.append({"entity": entity, "status": "error", "code": resp.status_code})
        except Exception as e:
            log.error(f"  [ERRO] {entity}: {e}")
            registered.append({"entity": entity, "status": "exception", "detail": str(e)})

        time.sleep(0.3)

    return registered


def list_catalog_assets(token: str) -> list[dict]:
    """
    Consulta o endpoint GET /catalog e retorna a lista de todos os ativos existentes.
    """
    headers = {"Authorization": token}
    try:
        resp = requests.get(ENDPOINT_CATALOG_SEARCH, headers=headers, timeout=30)
        if resp.status_code == 200:
            data = resp.json()
            return data.get("data_assets", [])
    except Exception as e:
        log.error(f"Erro ao listar catalogo: {e}")
    return []


def generate_report(registered: list[dict], catalog_assets_list: list[dict]) -> str:
    """
    Gera relatorio consolidado em Markdown com inventario completo dos ativos.
    """
    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    lines = [
        "# Relatório de Catalogação — Dadosfera API",
        "",
        f"> **Data/Hora de Geração:** {now}",
        f"> **Tenant:** Dadosfera Treinamentos",
        f"> **Pipeline:** `api/dadosfera/05_catalogar/catalog_assets.py` (Item 3 - Bônus API Catalogação)",
        "",
        "---",
        "",
        "## 1. Resumo Executivo",
        "",
        "| Indicador | Quantidade |",
        "|-----------|------------|",
        f"| Entidades do Case | {len(ENTITIES)} |",
        f"| Ativos Registrados nesta Execução | {sum(1 for r in registered if r.get('status') == 'cataloged')}/{len(ENTITIES)} |",
        f"| Total de Ativos Ativos no Catálogo Dadosfera | {len(catalog_assets_list)} |",
        "",
        "---",
        "",
        "## 2. Inventário de Ativos Catalogados (Case Recuperação de Carrinho)",
        "",
        "| Entidade | ID no Catálogo Dadosfera | Tipo | Status | Tags |",
        "|----------|--------------------------|------|--------|------|",
    ]

    for meta in CATALOG_METADATA:
        entity = meta["entity"]
        match = next((r for r in registered if r.get("entity") == entity and r.get("status") == "cataloged"), None)
        asset_id = match.get("id") if match else "—"
        status = "✅ Catalogado" if match else "⚠️ Pendente"
        tags_str = ", ".join(f"`{t}`" for t in meta["tags"])
        lines.append(f"| **{entity}** | `{asset_id}` | `{meta['data_asset_type']}` | {status} | {tags_str} |")

    lines += [
        "",
        "---",
        "",
        "## 3. Detalhamento dos Ativos e Metadados",
        "",
    ]

    for meta in CATALOG_METADATA:
        entity = meta["entity"]
        match = next((r for r in registered if r.get("entity") == entity and r.get("status") == "cataloged"), None)
        asset_id = match.get("id") if match else "—"
        lines += [
            f"### `{entity}`",
            f"- **Nome de Exibição:** {meta['display_name']}",
            f"- **Data Asset ID:** `{asset_id}`",
            f"- **Descrição:** {meta['description']}",
            f"- **Zona do Data Lake:** `/raw/recuperacao_carrinho/{entity}.csv` -> Snowflake `CART_RECOVERY.{entity.upper()}`",
            f"- **Tags:** {', '.join(meta['tags'])}",
            "",
        ]

    lines += [
        "---",
        "",
        "## 4. Mapeamento de Zonas do Data Lakehouse",
        "",
        "```",
        "Data Lakehouse — Case Recuperação de Carrinho Abandonado",
        "",
        "  [ Storage Dadosfera /raw/ ]           [ Catálogo Dadosfera ]",
        "  ├── clientes.csv         ──────────►   clientes         (ID: 059360a7...)",
        "  ├── produtos.csv         ──────────►   produtos         (ID: cb5a7a46...)",
        "  ├── carrinhos.csv        ──────────►   carrinhos        (ID: 595f7251...)",
        "  ├── itens_carrinho.csv   ──────────►   itens_carrinho   (ID: f6000b61...)",
        "  ├── eventos_carrinho.csv ──────────►   eventos_carrinho (ID: 7dd16cc4...)",
        "  ├── eventos_resgate.csv  ──────────►   eventos_resgate  (ID: 766174e0...)",
        "  └── pedidos.csv          ──────────►   pedidos          (ID: e88039c6...)",
        "```",
        "",
        "---",
        "*Documento gerado automaticamente pelo pipeline api/dadosfera/ — Case Técnico Dadosfera 2026*",
    ]

    return "\n".join(lines)


def catalog_assets() -> str:
    """
    Executa o fluxo completo da Fase 5:
    1. Autentica / Atualiza token
    2. Registra os ativos no Catalogo via POST /catalog
    3. Consulta os ativos no Catalogo via GET /catalog
    4. Gera relatorio consolidado em Markdown
    """
    log.info("=== FASE 5: Catalogacao de Ativos na Dadosfera ===")

    token = refresh_token_if_needed()

    registered = register_assets_in_catalog(token)
    all_assets = list_catalog_assets(token)

    log.info("Gerando relatorio de catalogacao em Markdown...")
    report_content = generate_report(registered, all_assets)

    ensure_state_dir()
    CATALOG_REPORT.write_text(report_content, encoding="utf-8")
    log.info(f"[OK] Relatorio salvo em: {CATALOG_REPORT}")

    # Salva json de estado
    state_file = STATE_DIR / "cataloged_assets.json"
    state_file.write_text(json.dumps(registered, indent=2, ensure_ascii=False), encoding="utf-8")

    return str(CATALOG_REPORT)


if __name__ == "__main__":
    path = catalog_assets()
    print(f"\n[OK] Fase 5 concluida com sucesso! Relatorio salvo em: {path}")
