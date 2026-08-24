-- ============================================================================
-- 001_create_tables.sql
-- Criação das tabelas do modelo de Recuperação de Carrinho Abandonado
-- SGBD: PostgreSQL
-- Projeto: Case Marketplace - Pitch de Recuperação de Carrinho
-- ============================================================================

-- 1. CLIENTES
-- Compradores do marketplace com segmentação RFM e preferências de contato
CREATE TABLE clientes (
    cliente_id    SERIAL PRIMARY KEY,
    primeiro_nome VARCHAR(100) NOT NULL,
    ultimo_nome   VARCHAR(100),
    email         VARCHAR(255) NOT NULL,
    telefone      VARCHAR(20),

    -- Segmentação RFM
    segmento_rfm       VARCHAR(20),
    data_primeira_compra DATE,
    data_ultima_compra   DATE,
    total_compras        INT DEFAULT 0,
    lifetime_value       DECIMAL(12,2) DEFAULT 0.00,

    -- Preferências de contato
    permite_email BOOLEAN NOT NULL DEFAULT TRUE,
    permite_sms   BOOLEAN NOT NULL DEFAULT FALSE,
    permite_push  BOOLEAN NOT NULL DEFAULT FALSE,

    -- Status
    status_ativo  BOOLEAN NOT NULL DEFAULT TRUE,
    data_criacao  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 2. PRODUTOS
-- Catálogo de produtos do marketplace
CREATE TABLE produtos (
    produto_id      SERIAL PRIMARY KEY,
    nome            VARCHAR(255) NOT NULL,
    categoria       VARCHAR(100) NOT NULL,
    subcategoria    VARCHAR(100),
    marca           VARCHAR(100),
    preco_atual     DECIMAL(10,2) NOT NULL,
    preco_original  DECIMAL(10,2),
    em_estoque      BOOLEAN NOT NULL DEFAULT TRUE,
    avaliacao_media DECIMAL(2,1),
    total_avaliacoes INT NOT NULL DEFAULT 0,
    url_imagem      VARCHAR(500),
    data_cadastro   TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    ativo           BOOLEAN NOT NULL DEFAULT TRUE
);


-- 3. CARRINHOS
-- Tabela central do domínio: lifecycle do carrinho de compras
CREATE TABLE carrinhos (
    carrinho_id          SERIAL PRIMARY KEY,
    cliente_id           INT NOT NULL,
    data_criacao         TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_ultima_atividade TIMESTAMPTZ,
    data_abandono        TIMESTAMPTZ,

    -- Status do lifecycle
    status           VARCHAR(20) NOT NULL DEFAULT 'ativo',
    motivo_abandono  VARCHAR(100),

    -- Valores monetários
    valor_subtotal   DECIMAL(10,2),
    valor_frete      DECIMAL(10,2),
    valor_desconto   DECIMAL(10,2) DEFAULT 0.00,
    valor_total      DECIMAL(10,2),

    -- Contexto de sessão
    duracao_sessao_minutos INT,
    dispositivo            VARCHAR(50),
    browser                VARCHAR(50),
    canal_origem           VARCHAR(100),

    -- Flags
    cliente_novo      BOOLEAN NOT NULL DEFAULT FALSE,
    tem_conta_criada  BOOLEAN NOT NULL DEFAULT FALSE,

    -- Audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 4. ITENS_CARRINHO
-- Itens de cada carrinho com snapshot de preço
CREATE TABLE itens_carrinho (
    item_id        SERIAL PRIMARY KEY,
    carrinho_id    INT NOT NULL,
    produto_id     INT NOT NULL,
    quantidade     INT NOT NULL DEFAULT 1,
    preco_unitario DECIMAL(10,2) NOT NULL,
    preco_total    DECIMAL(10,2) NOT NULL,
    data_adicao    TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    data_remocao   TIMESTAMPTZ
);


-- 5. EVENTOS_CARRINHO
-- Time series comportamental: ações do cliente na sessão de compra
CREATE TABLE eventos_carrinho (
    evento_id              BIGSERIAL PRIMARY KEY,
    carrinho_id            INT NOT NULL,
    cliente_id             INT NOT NULL,
    sessao_id              VARCHAR(50),
    timestamp_evento       TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    tipo_evento            VARCHAR(50) NOT NULL,
    duracao_evento_segundos INT,
    dados_evento           JSONB
);


-- 6. EVENTOS_RESGATE
-- Campanhas de recuperação: envio, engajamento e resultado
CREATE TABLE eventos_resgate (
    resgate_id            BIGSERIAL PRIMARY KEY,
    carrinho_id           INT NOT NULL,
    cliente_id            INT NOT NULL,

    -- Comunicação
    canal                 VARCHAR(50) NOT NULL,
    tipo_comunicacao      VARCHAR(50) NOT NULL,
    data_schedule         TIMESTAMPTZ NOT NULL,
    data_envio            TIMESTAMPTZ,
    assunto               VARCHAR(255),

    -- Oferta
    desconto_oferecido    DECIMAL(10,2) DEFAULT 0.00,
    frete_gratis_oferecido BOOLEAN NOT NULL DEFAULT FALSE,
    custo_envio           DECIMAL(10,2) NOT NULL,

    -- Engajamento
    data_abertura         TIMESTAMPTZ,
    data_primeiro_clique  TIMESTAMPTZ,
    link_clicado          VARCHAR(500),

    -- Resultado
    data_conversao        TIMESTAMPTZ,
    sucesso               BOOLEAN NOT NULL DEFAULT FALSE,
    valor_pedido_final    DECIMAL(10,2),

    -- Audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);


-- 7. PEDIDOS
-- Pedidos finalizados: fecha o ciclo carrinho → conversão
CREATE TABLE pedidos (
    pedido_id          SERIAL PRIMARY KEY,
    carrinho_id        INT NOT NULL,
    cliente_id         INT NOT NULL,
    data_pedido        TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    valor_subtotal     DECIMAL(10,2) NOT NULL,
    valor_frete        DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    valor_desconto     DECIMAL(10,2) NOT NULL DEFAULT 0.00,
    valor_total        DECIMAL(10,2) NOT NULL,
    metodo_pagamento   VARCHAR(50),
    status_pedido      VARCHAR(20) NOT NULL DEFAULT 'confirmado',
    origem_recuperacao BOOLEAN NOT NULL DEFAULT FALSE,
    resgate_id         BIGINT,

    -- Audit
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);
