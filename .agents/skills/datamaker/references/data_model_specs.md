# Data Model Specifications & Business Context

> Este arquivo é o repositório central para documentar o modelo de dados do projeto, regras de negócio específicas, restrições e informações extras para consulta da skill `datamaker`.

---

## 1. Visão Geral do Domínio (Business Overview)

- **Nome do Projeto / Módulo**: Case de Recuperação de Carrinho Abandonado — Marketplace
- **Descrição do Negócio**: Modelagem do ciclo de vida completo do carrinho de compras em um marketplace, desde a criação até o abandono, campanhas de resgate e conversão em pedido. Taxa de abandono estimada: ~70%. Valor perdido por carrinho: R$ 50–300.
- **Objetivo dos Dados**: Alimentar análises descritivas, prescritivas e o case principal de recuperação de carrinho para pitch de venda. Demonstrar valor com intervenções personalizadas (email, SMS, push, WhatsApp).

---

## 2. Entidades Principais & Requisitos

### `clientes`
- **Descrição**: Compradores do marketplace com segmentação RFM e preferências de comunicação
- **Campos Principais**:
  - `cliente_id`: INT, PK, SERIAL
  - `primeiro_nome`: VARCHAR(100), NOT NULL — personalização de campanhas
  - `ultimo_nome`: VARCHAR(100), nullable
  - `email`: VARCHAR(255), UNIQUE NOT NULL — chave natural
  - `telefone`: VARCHAR(20), nullable
  - `segmento_rfm`: VARCHAR(20) — `'premium'`, `'regular'`, `'dormant'`, `'novo'`
  - `data_primeira_compra`, `data_ultima_compra`: DATE
  - `total_compras`: INT, default 0
  - `lifetime_value`: DECIMAL(12,2), default 0.00
  - `permite_email`: BOOLEAN, default TRUE
  - `permite_sms`: BOOLEAN, default FALSE
  - `permite_push`: BOOLEAN, default FALSE
  - `status_ativo`: BOOLEAN, default TRUE
  - `data_criacao`: TIMESTAMPTZ, default NOW()

### `produtos`
- **Descrição**: Catálogo de produtos do marketplace
- **Campos Principais**:
  - `produto_id`: INT, PK, SERIAL
  - `nome`: VARCHAR(255), NOT NULL
  - `categoria`: VARCHAR(100), NOT NULL — ex: Eletrônicos, Moda, Casa
  - `subcategoria`: VARCHAR(100), nullable
  - `marca`: VARCHAR(100), nullable
  - `preco_atual`: DECIMAL(10,2), NOT NULL
  - `preco_original`: DECIMAL(10,2), nullable — preço antes de promoção
  - `em_estoque`: BOOLEAN, default TRUE
  - `avaliacao_media`: DECIMAL(2,1), nullable — 1.0 a 5.0
  - `total_avaliacoes`: INT, default 0
  - `url_imagem`: VARCHAR(500), nullable
  - `data_cadastro`: TIMESTAMPTZ, default NOW()
  - `ativo`: BOOLEAN, default TRUE

### `carrinhos`
- **Descrição**: Tabela central do domínio — lifecycle do carrinho de compras
- **Campos Principais**:
  - `carrinho_id`: INT, PK, SERIAL
  - `cliente_id`: INT, FK → clientes, NOT NULL
  - `data_criacao`: TIMESTAMPTZ, NOT NULL
  - `data_ultima_atividade`: TIMESTAMPTZ, nullable
  - `data_abandono`: TIMESTAMPTZ, nullable
  - `status`: VARCHAR(20), NOT NULL — `'ativo'`, `'abandonado'`, `'recuperado'`, `'comprado'`, `'expirado'`
  - `motivo_abandono`: VARCHAR(100), nullable — `'preco'`, `'frete'`, `'pagamento'`, `'indecisao'`, `'estoque'`, `'nao_informado'`
  - `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total`: DECIMAL(10,2)
  - `duracao_sessao_minutos`: INT
  - `dispositivo`: VARCHAR(50) — `'mobile'`, `'desktop'`, `'tablet'`
  - `browser`: VARCHAR(50)
  - `canal_origem`: VARCHAR(100) — `'google'`, `'facebook'`, `'direct'`, `'email'`, `'instagram'`
  - `cliente_novo`, `tem_conta_criada`: BOOLEAN
  - `created_at`, `updated_at`: TIMESTAMPTZ (audit)

### `itens_carrinho`
- **Descrição**: Itens de cada carrinho com snapshot de preço no momento da adição
- **Campos Principais**:
  - `item_id`: INT, PK, SERIAL
  - `carrinho_id`: INT, FK → carrinhos, NOT NULL
  - `produto_id`: INT, FK → produtos, NOT NULL
  - `quantidade`: INT, NOT NULL, default 1
  - `preco_unitario`: DECIMAL(10,2), NOT NULL — snapshot
  - `preco_total`: DECIMAL(10,2), NOT NULL — quantidade × preço_unitario
  - `data_adicao`: TIMESTAMPTZ, NOT NULL
  - `data_remocao`: TIMESTAMPTZ, nullable
- **Observações**: Campos de engagement (foi_visualizado_email, etc.) removidos — pertencem a `eventos_resgate`

### `eventos_carrinho`
- **Descrição**: Time series comportamental — ações do cliente na sessão de compra
- **Campos Principais**:
  - `evento_id`: BIGINT, PK, BIGSERIAL
  - `carrinho_id`: INT, FK → carrinhos, NOT NULL
  - `cliente_id`: INT, FK → clientes, NOT NULL (desnormalização intencional)
  - `sessao_id`: VARCHAR(50), nullable — agrupa eventos por visita
  - `timestamp_evento`: TIMESTAMPTZ, NOT NULL
  - `tipo_evento`: VARCHAR(50), NOT NULL — `'view_produto'`, `'add_carrinho'`, `'remove_carrinho'`, `'update_quantidade'`, `'view_checkout'`, `'inicio_pagamento'`, `'erro_pagamento'`, `'abandono'`, `'retorno'`
  - `duracao_evento_segundos`: INT, nullable
  - `dados_evento`: JSONB, nullable — dados contextuais por tipo

### `eventos_resgate`
- **Descrição**: Campanhas de recuperação: envio, engajamento e resultado por canal
- **Campos Principais**:
  - `resgate_id`: BIGINT, PK, BIGSERIAL
  - `carrinho_id`: INT, FK → carrinhos, NOT NULL
  - `cliente_id`: INT, FK → clientes, NOT NULL
  - `canal`: VARCHAR(50), NOT NULL — `'email'`, `'sms'`, `'push_app'`, `'whatsapp'`
  - `tipo_comunicacao`: VARCHAR(50), NOT NULL — `'lembrete_1h'`, `'lembrete_24h'`, `'desconto_48h'`, `'urgencia_72h'`
  - `data_schedule`, `data_envio`: TIMESTAMPTZ
  - `assunto`: VARCHAR(255)
  - `desconto_oferecido`: DECIMAL(10,2), default 0.00
  - `frete_gratis_oferecido`: BOOLEAN, default FALSE
  - `custo_envio`: DECIMAL(10,2), NOT NULL — varia por canal
  - `data_abertura`, `data_primeiro_clique`: TIMESTAMPTZ
  - `link_clicado`: VARCHAR(500)
  - `data_conversao`: TIMESTAMPTZ
  - `sucesso`: BOOLEAN, default FALSE
  - `valor_pedido_final`: DECIMAL(10,2), nullable

### `pedidos`
- **Descrição**: Pedidos finalizados — fecha o ciclo carrinho → conversão
- **Campos Principais**:
  - `pedido_id`: INT, PK, SERIAL
  - `carrinho_id`: INT, FK → carrinhos, NOT NULL, UNIQUE (1 carrinho → max 1 pedido)
  - `cliente_id`: INT, FK → clientes, NOT NULL
  - `data_pedido`: TIMESTAMPTZ, NOT NULL
  - `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total`: DECIMAL(10,2)
  - `metodo_pagamento`: VARCHAR(50) — `'cartao_credito'`, `'cartao_debito'`, `'boleto'`, `'pix'`
  - `status_pedido`: VARCHAR(20) — `'confirmado'`, `'enviado'`, `'entregue'`, `'cancelado'`
  - `origem_recuperacao`: BOOLEAN, default FALSE
  - `resgate_id`: BIGINT, FK → eventos_resgate, nullable

---

## 3. Relacionamentos & Cardinalidades

- **clientes (1) → (N) carrinhos**: Um cliente pode criar múltiplos carrinhos. CASCADE: RESTRICT.
- **clientes (1) → (N) eventos_resgate**: Um cliente recebe múltiplas comunicações. CASCADE: RESTRICT.
- **clientes (1) → (N) eventos_carrinho**: Desnormalização intencional. CASCADE: RESTRICT.
- **carrinhos (1) → (N) itens_carrinho**: Um carrinho contém múltiplos itens. CASCADE: CASCADE.
- **carrinhos (1) → (N) eventos_carrinho**: Time series por carrinho. CASCADE: CASCADE.
- **carrinhos (1) → (N) eventos_resgate**: Múltiplas tentativas de resgate. CASCADE: CASCADE.
- **carrinhos (1) → (0,1) pedidos**: Um carrinho gera no máximo um pedido. CASCADE: RESTRICT.
- **produtos (1) → (N) itens_carrinho**: Produto em múltiplos carrinhos. CASCADE: RESTRICT.
- **eventos_resgate (1) → (0,1) pedidos**: Campanha pode gerar um pedido. CASCADE: SET NULL.

---

## 4. Regras de Negócio & Validações

1. **Lifecycle do carrinho**: `ativo → abandonado → recuperado → comprado` ou `ativo → comprado` (direto). `abandonado → expirado` após 90 dias.
2. **Valores monetários**: Sempre `DECIMAL(10,2)`, nunca `FLOAT`. `valor_total ≥ 0`, `valor_desconto ≤ valor_subtotal`.
3. **Campanha de resgate**: Máximo 4 tentativas por carrinho. Respeitar opt-in do cliente. Intervalo mínimo de 4h entre envios.
4. **Sequência padrão de resgate**: lembrete_1h (email) → lembrete_24h (email+push) → desconto_48h (email+SMS, 5-10%) → urgencia_72h (email+WhatsApp, 10-15%+frete grátis).
5. **Segmentação RFM**: premium (LTV > R$2k, 5+ compras), regular (LTV R$500-2k, 2-4 compras), dormant (LTV < R$500, 1 compra), novo (0 compras).
6. **Consistência temporal**: `data_criacao ≤ data_ultima_atividade ≤ data_abandono`. `data_schedule ≤ data_envio ≤ data_abertura ≤ data_primeiro_clique ≤ data_conversao`.
7. **ROI calculado na análise** (não como coluna): `(valor_pedido_final - desconto_oferecido - custo_envio) / custo_envio`.
8. **Custo por canal**: email R$0.05, SMS R$0.15, push R$0.02, WhatsApp R$0.30.

---

## 5. Especificações do Banco de Dados Alvo

- **Tipo / SGBD**: PostgreSQL
- **Versão Alvo**: 15+
- **Convenções de Nomenclatura**: snake_case, tabelas no plural, campos descritivos em português
- **Tipos de Dados Especiais**: TIMESTAMPTZ (timestamps com timezone), JSONB (dados flexíveis em eventos), DECIMAL(10,2) para monetários, SERIAL/BIGSERIAL para PKs

---

## 6. Diretrizes para Geração de Dados Mock & Dirty Data

- **Volume de Dados Desejado**:
  - ~1.000 clientes
  - ~200 produtos
  - ~5.000 carrinhos (70% abandonados)
  - ~15.000 itens de carrinho
  - ~50.000 eventos de carrinho
  - ~3.500 eventos de resgate
  - ~1.500 pedidos
- **Período Temporal**: Janeiro 2026 – Junho 2026 (6 meses)
- **Proporção de Dirty Data**: 5% a 10% de anomalias/inconsistências
- **Cenários de Inconsistência Desejados**:
  - Anomalias de formato (datas em padrões diferentes, telefones sem máscara)
  - Valores nulos ou ausentes em campos opcionais
  - Emails duplicados com variações de casing
  - Valores de frete inconsistentes (negativos, muito altos)
  - data_remocao anterior a data_adicao (inversão temporal)
  - Carrinhos com valor_total inconsistente com soma dos itens
  - Eventos de resgate com data_abertura antes de data_envio
  - Produtos com preço_atual > preço_original (promoção invertida)

---

## 7. Informações e Anotações Extras

### Decisões de Design
- **`metricas_resgate` removida**: Substituída por views SQL (`004_views.sql`) que calculam métricas sob demanda — evita redundância e manutenção de ETL.
- **`produtos` adicionada**: Referenciada por FK em `itens_carrinho` mas ausente no modelo original.
- **`pedidos` adicionada**: Fecha o ciclo carrinho → conversão, mencionada no lifecycle original mas nunca definida.
- **Campos de engagement movidos**: `foi_visualizado_email`, `foi_clicado`, etc. movidos de `itens_carrinho` para `eventos_resgate`.
- **`source_origem` → `canal_origem`**: Renomeado para evitar redundância pt/en.
- **`tipo_email` → `tipo_comunicacao`**: Generalizado para suportar múltiplos canais.

### Limites de Escopo (não incluir)
- Tabela de sellers/lojistas (complexidade de marketplace)
- Tabela de cupons/promoções separada
- Sistema de A/B testing
- Tabela de sessões separada
- Histórico de preços de produtos

### Arquivos de Implementação
- **Modelagem Lógica**: `data/models/logical/`
- **DDL SQL**: `data/database/sql/001_create_tables.sql` → `004_views.sql`
- **Mock Generators**: `data/mock/generators/` (a criar)
- **Datasets**: `data/mock/output/` (a gerar)