# Relatório de Catalogação — Dadosfera API

> **Data/Hora de Geração:** 2026-08-22 20:47 UTC
> **Tenant:** Dadosfera Treinamentos
> **Pipeline:** `api/dadosfera/05_catalogar/catalog_assets.py` (Item 3 - Bônus API Catalogação)

---

## 1. Resumo Executivo

| Indicador | Quantidade |
|-----------|------------|
| Entidades do Case | 7 |
| Ativos Registrados nesta Execução | 0/7 |
| Total de Ativos Ativos no Catálogo Dadosfera | 10 |

---

## 2. Inventário de Ativos Catalogados (Case Recuperação de Carrinho)

| Entidade | ID no Catálogo Dadosfera | Tipo | Status | Tags |
|----------|--------------------------|------|--------|------|
| **clientes** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `clientes`, `marketplace`, `qualify`, `dimensao`, `pii_sensivel` |
| **produtos** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `produtos`, `catalogo`, `qualify`, `dimensao` |
| **carrinhos** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `carrinhos`, `transacional`, `qualify`, `fato_central` |
| **itens_carrinho** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `itens_carrinho`, `itens`, `qualify`, `fato_detalhe` |
| **eventos_carrinho** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `eventos_carrinho`, `telemetria`, `qualify`, `timeseries` |
| **eventos_resgate** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `eventos_resgate`, `recuperacao`, `qualify`, `crm_marketing` |
| **pedidos** | `—` | `dataset` | ⚠️ Pendente | `carrinho_abandonado`, `pedidos`, `conversoes`, `qualify`, `faturamento` |

---

## 3. Detalhamento dos Ativos e Metadados

### `clientes`
- **Nome de Exibição:** clientes
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Clientes (Dimensão Cadastral & RFM)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.CLIENTES | **Volumetria:** 2.000 registros

**Visão de Negócio:** Consolida o perfil demográfico, canal de aquisição e segmentação RFM (Recency, Frequency, Monetary) dos clientes para campanhas personalizadas de resgate.

**Dicionário de Colunas:**
- `cliente_id` (VARCHAR, PK): Identificador UUID exclusivo do cliente.
- `nome` (VARCHAR, PII): Nome completo do cliente (Dado Sensível LGPD).
- `email` (VARCHAR, PII): Endereço de email primário para envio de lembretes e descontos.
- `telefone` (VARCHAR, PII): Telefone para contato via WhatsApp/SMS.
- `cidade` / `estado` (VARCHAR): Localização geográfica para análise de frete regional.
- `data_cadastro` (TIMESTAMP): Data e hora de registro no e-commerce.
- `segmento` (VARCHAR): Segmento comportamental ('premium', 'regular', 'dormant', 'novo').
- `canal_aquisicao` (VARCHAR): Canal de origem ('organico', 'pago', 'rede_social', 'indicacao').
- `ltv_estimado` (FLOAT): Lifetime Value estimado em R$.
- `total_pedidos` (INTEGER): Total de compras finalizadas.
- `ticket_medio` (FLOAT): Gasto médio por pedido.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/clientes.csv` -> Snowflake `CART_RECOVERY.CLIENTES`
- **Tags:** carrinho_abandonado, clientes, marketplace, qualify, dimensao, pii_sensivel

### `produtos`
- **Nome de Exibição:** produtos
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Produtos (Catálogo & Estoque)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.PRODUTOS | **Volumetria:** 500 registros

**Visão de Negócio:** Catálogo central de itens comercializados no marketplace com controle de estoque, faixas de preço e avaliações dos consumidores.

**Dicionário de Colunas:**
- `produto_id` (VARCHAR, PK): Identificador UUID exclusivo do produto.
- `nome` (VARCHAR): Título descritivo do produto visível no e-commerce.
- `categoria` (VARCHAR): Categoria macro (ex: Eletrônicos, Moda, Casa).
- `subcategoria` (VARCHAR): Tipo detalhado do produto.
- `preco` (FLOAT): Preço atual de venda em R$.
- `estoque` (INTEGER): Quantidade física disponível no centro de distribuição.
- `marca` (VARCHAR): Fabricante ou marca comercial.
- `avaliacao_media` (FLOAT): Nota média de satisfação (0 a 5 estrelas).
- `num_avaliacoes` (INTEGER): Volume total de reviews recebidos.
- `ativo` (BOOLEAN): Flag indicadora de disponibilidade para venda.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/produtos.csv` -> Snowflake `CART_RECOVERY.PRODUTOS`
- **Tags:** carrinho_abandonado, produtos, catalogo, qualify, dimensao

### `carrinhos`
- **Nome de Exibição:** carrinhos
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Carrinhos (Sessões & Lifecycle de Compra)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.CARRINHOS | **Volumetria:** 15.000 registros

**Visão de Negócio:** Tabela central do case de marketing. Registra sessões de carrinho, status de conversão/abandono e timing de inatividade para disparo de resgate.

**Dicionário de Colunas:**
- `carrinho_id` (VARCHAR, PK): Identificador UUID exclusivo da sessão de carrinho.
- `cliente_id` (VARCHAR, FK): Referência ao cliente proprietário da sessão.
- `criado_em` (TIMESTAMP): Data/hora de inicialização do carrinho.
- `atualizado_em` (TIMESTAMP): Data/hora da última alteração de itens.
- `status` (VARCHAR): Situação atual ('ativo', 'abandonado', 'recuperado', 'comprado', 'expirado').
- `valor_total` (FLOAT): Valor monetário total dos itens em R$.
- `num_itens` (INTEGER): Quantidade de itens físicos no carrinho.
- `canal` (VARCHAR): Plataforma de origem ('web', 'mobile', 'app').
- `abandono_em` (TIMESTAMP): Momento de marcação de abandono (30min inativo).
- `tempo_ate_abandono_min` (FLOAT): Minutos decorridos até a desistência.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/carrinhos.csv` -> Snowflake `CART_RECOVERY.CARRINHOS`
- **Tags:** carrinho_abandonado, carrinhos, transacional, qualify, fato_central

### `itens_carrinho`
- **Nome de Exibição:** itens_carrinho
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Itens do Carrinho (Composição do Carrinho)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.ITENS_CARRINHO | **Volumetria:** 22.500 registros

**Visão de Negócio:** Detalha a composição de produtos adicionados em cada carrinho, snapshots de preço e descontos aplicados por item.

**Dicionário de Colunas:**
- `item_id` (VARCHAR, PK): Identificador UUID exclusivo da linha de item.
- `carrinho_id` (VARCHAR, FK): Referência ao carrinho pai.
- `produto_id` (VARCHAR, FK): Referência ao produto adicionado.
- `quantidade` (INTEGER): Quantidade de unidades adicionadas.
- `preco_unitario` (FLOAT): Preço unitário no momento da adição.
- `subtotal` (FLOAT): Valor bruto (quantidade * preco_unitario).
- `adicionado_em` (TIMESTAMP): Instante exato de adição ao carrinho.
- `desconto_aplicado` (FLOAT): Valor monetário de desconto deduzido.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/itens_carrinho.csv` -> Snowflake `CART_RECOVERY.ITENS_CARRINHO`
- **Tags:** carrinho_abandonado, itens_carrinho, itens, qualify, fato_detalhe

### `eventos_carrinho`
- **Nome de Exibição:** eventos_carrinho
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Eventos de Carrinho (Telemetria & Funil de Conversão)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.EVENTOS_CARRINHO | **Volumetria:** 72.026 registros

**Visão de Negócio:** Log de cliques, navegação e erros técnicos (gateway de pagamento) que antecedem o abandono ou conversão da compra.

**Dicionário de Colunas:**
- `evento_id` (VARCHAR, PK): Identificador UUID da ação de telemetria.
- `carrinho_id` (VARCHAR, FK): Sessão de carrinho associada.
- `cliente_id` (VARCHAR, FK): Cliente que executou a ação.
- `tipo_evento` (VARCHAR): Ação ('view_produto', 'add_carrinho', 'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno').
- `ocorrido_em` (TIMESTAMP): Data e hora precisa do evento.
- `canal` (VARCHAR): Canal ('web', 'mobile', 'app').
- `dispositivo` (VARCHAR): Aparelho ('desktop', 'mobile', 'tablet').
- `sessao_id` (VARCHAR): Identificador da sessão contínua.
- `produto_id` (VARCHAR, FK): Produto relacionado à ação (opcional).
- `metadata` (VARIANT): Detalhes técnicos contextuais em JSON.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/eventos_carrinho.csv` -> Snowflake `CART_RECOVERY.EVENTOS_CARRINHO`
- **Tags:** carrinho_abandonado, eventos_carrinho, telemetria, qualify, timeseries

### `eventos_resgate`
- **Nome de Exibição:** eventos_resgate
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Eventos de Resgate (Campanhas Multicanal & ROI)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.EVENTOS_RESGATE | **Volumetria:** 2.500 registros

**Visão de Negócio:** Rastreia o funil de comunicação pós-abandono (Envio ➔ Abertura ➔ Clique ➔ Conversão), canais (Email, SMS, WhatsApp, Push) e ROI de campanhas.

**Dicionário de Colunas:**
- `resgate_id` (VARCHAR, PK): Identificador UUID do disparo de comunicação.
- `carrinho_id` (VARCHAR, FK): Carrinho alvo da recuperação.
- `cliente_id` (VARCHAR, FK): Destinatário da mensagem.
- `canal_resgate` (VARCHAR): Meio utilizado ('email', 'sms', 'push_app', 'whatsapp').
- `enviado_em` (TIMESTAMP): Data/hora do disparo da mensagem.
- `aberto_em` (TIMESTAMP): Instante de abertura pelo cliente.
- `clicado_em` (TIMESTAMP): Instante de clique no link de recuperação.
- `convertido` (BOOLEAN): Se resultou em compra finalizada.
- `convertido_em` (TIMESTAMP): Momento da conversão.
- `valor_recuperado` (FLOAT): Valor monetário do pedido recuperado em R$.
- `tipo_oferta` (VARCHAR): Benefício ('desconto', 'frete_gratis', 'lembrete').
- `desconto_oferecido` (FLOAT): Percentual de desconto concedido.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/eventos_resgate.csv` -> Snowflake `CART_RECOVERY.EVENTOS_RESGATE`
- **Tags:** carrinho_abandonado, eventos_resgate, recuperacao, qualify, crm_marketing

### `pedidos`
- **Nome de Exibição:** pedidos
- **Data Asset ID:** `—`
- **Descrição:** ### Entidade: Pedidos (Conversões & Faturamento Final)
**Zona Lakehouse:** Qualify (Silver) | **Localização:** CART_RECOVERY.PEDIDOS | **Volumetria:** 2.000 registros

**Visão de Negócio:** Compras efetivadas no marketplace, atribuindo faturamento direto a compras espontâneas ou recuperadas via campanhas de resgate.

**Dicionário de Colunas:**
- `pedido_id` (VARCHAR, PK): Identificador UUID da compra aprovada.
- `carrinho_id` (VARCHAR, FK): Carrinho que originou o pedido.
- `cliente_id` (VARCHAR, FK): Comprador.
- `criado_em` (TIMESTAMP): Data e hora da conclusão do pedido.
- `valor_total` (FLOAT): Valor líquido pago (Subtotal - Desconto + Frete).
- `desconto_total` (FLOAT): Total de abatimentos aplicados em R$.
- `valor_frete` (FLOAT): Custo cobrado para entrega em R$.
- `status` (VARCHAR): Situação ('aprovado', 'enviado', 'entregue', 'cancelado').
- `metodo_pagamento` (VARCHAR): Forma de pagamento ('cartao', 'boleto', 'pix').
- `num_parcelas` (INTEGER): Parcelas no cartão (1 a 12).
- `origem_resgate` (BOOLEAN): Flag indicadora de compra vinda de campanha.
- `resgate_id` (VARCHAR, FK): Referência à mensagem de resgate que gerou a venda.
- **Zona do Data Lake:** `/raw/recuperacao_carrinho/pedidos.csv` -> Snowflake `CART_RECOVERY.PEDIDOS`
- **Tags:** carrinho_abandonado, pedidos, conversoes, qualify, faturamento

---

## 4. Mapeamento de Zonas do Data Lakehouse

```
Data Lakehouse — Case Recuperação de Carrinho Abandonado

  [ Storage Dadosfera /raw/ ]           [ Catálogo Dadosfera ]
  ├── clientes.csv         ──────────►   clientes         (ID: 059360a7...)
  ├── produtos.csv         ──────────►   produtos         (ID: cb5a7a46...)
  ├── carrinhos.csv        ──────────►   carrinhos        (ID: 595f7251...)
  ├── itens_carrinho.csv   ──────────►   itens_carrinho   (ID: f6000b61...)
  ├── eventos_carrinho.csv ──────────►   eventos_carrinho (ID: 7dd16cc4...)
  ├── eventos_resgate.csv  ──────────►   eventos_resgate  (ID: 766174e0...)
  └── pedidos.csv          ──────────►   pedidos          (ID: e88039c6...)
```

---
*Documento gerado automaticamente pelo pipeline api/dadosfera/ — Case Técnico Dadosfera 2026*