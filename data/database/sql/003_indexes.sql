-- ============================================================================
-- 003_indexes.sql
-- Índices de performance para consultas frequentes
-- SGBD: PostgreSQL
-- Projeto: Case Marketplace - Recuperação de Carrinho
-- ============================================================================

-- ──────────────────────────────────────────────
-- CLIENTES
-- ──────────────────────────────────────────────

-- Busca por email (já tem UNIQUE, mas explícito para clareza)
CREATE INDEX idx_clientes_email ON clientes(email);

-- Filtro por segmento RFM (segmentação de campanhas)
CREATE INDEX idx_clientes_rfm ON clientes(segmento_rfm);

-- Filtro de clientes ativos
CREATE INDEX idx_clientes_ativo ON clientes(status_ativo) WHERE status_ativo = TRUE;


-- ──────────────────────────────────────────────
-- PRODUTOS
-- ──────────────────────────────────────────────

-- Filtro por categoria (análises segmentadas)
CREATE INDEX idx_produtos_categoria ON produtos(categoria);

-- Filtro por marca
CREATE INDEX idx_produtos_marca ON produtos(marca);

-- Produtos em promoção (preco_original preenchido)
CREATE INDEX idx_produtos_promocao ON produtos(preco_atual, preco_original)
    WHERE preco_original IS NOT NULL;


-- ──────────────────────────────────────────────
-- CARRINHOS
-- ──────────────────────────────────────────────

-- Filtro por status (query mais frequente: buscar abandonados)
CREATE INDEX idx_carrinhos_status ON carrinhos(status);

-- Busca por data de abandono (campanhas de resgate por timing)
CREATE INDEX idx_carrinhos_abandono ON carrinhos(data_abandono)
    WHERE data_abandono IS NOT NULL;

-- FK lookup: carrinhos por cliente
CREATE INDEX idx_carrinhos_cliente ON carrinhos(cliente_id);

-- Combinado: carrinhos abandonados por data (dashboard de métricas)
CREATE INDEX idx_carrinhos_status_data ON carrinhos(status, data_criacao);

-- Filtro por dispositivo (análise de abandono por device)
CREATE INDEX idx_carrinhos_dispositivo ON carrinhos(dispositivo);


-- ──────────────────────────────────────────────
-- ITENS_CARRINHO
-- ──────────────────────────────────────────────

-- FK lookup: itens por carrinho
CREATE INDEX idx_itens_carrinho ON itens_carrinho(carrinho_id);

-- FK lookup: itens por produto (análise de produtos mais abandonados)
CREATE INDEX idx_itens_produto ON itens_carrinho(produto_id);


-- ──────────────────────────────────────────────
-- EVENTOS_CARRINHO
-- ──────────────────────────────────────────────

-- Time series: busca por timestamp
CREATE INDEX idx_eventos_timestamp ON eventos_carrinho(timestamp_evento);

-- Filtro por tipo de evento (análise de funil)
CREATE INDEX idx_eventos_tipo ON eventos_carrinho(tipo_evento);

-- FK lookup: eventos por carrinho
CREATE INDEX idx_eventos_carrinho ON eventos_carrinho(carrinho_id);

-- Agrupamento por sessão
CREATE INDEX idx_eventos_sessao ON eventos_carrinho(sessao_id)
    WHERE sessao_id IS NOT NULL;


-- ──────────────────────────────────────────────
-- EVENTOS_RESGATE
-- ──────────────────────────────────────────────

-- Filtro por sucesso (dashboard de conversão)
CREATE INDEX idx_resgate_sucesso ON eventos_resgate(sucesso);

-- Filtro por canal (análise de performance por canal)
CREATE INDEX idx_resgate_canal ON eventos_resgate(canal);

-- FK lookup: resgates por carrinho
CREATE INDEX idx_resgate_carrinho ON eventos_resgate(carrinho_id);

-- Busca por data de envio (relatórios temporais)
CREATE INDEX idx_resgate_envio ON eventos_resgate(data_envio)
    WHERE data_envio IS NOT NULL;

-- Combinado: sucesso por canal (ROI por canal)
CREATE INDEX idx_resgate_canal_sucesso ON eventos_resgate(canal, sucesso);


-- ──────────────────────────────────────────────
-- PEDIDOS
-- ──────────────────────────────────────────────

-- FK lookup: pedidos por cliente
CREATE INDEX idx_pedidos_cliente ON pedidos(cliente_id);

-- Filtro: pedidos originados de recuperação
CREATE INDEX idx_pedidos_recuperacao ON pedidos(origem_recuperacao)
    WHERE origem_recuperacao = TRUE;

-- Busca por data do pedido (relatórios)
CREATE INDEX idx_pedidos_data ON pedidos(data_pedido);

-- Status do pedido
CREATE INDEX idx_pedidos_status ON pedidos(status_pedido);
