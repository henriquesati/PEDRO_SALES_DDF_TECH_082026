-- ============================================================================
-- 002_constraints.sql
-- Foreign keys, unique constraints e check constraints
-- SGBD: PostgreSQL
-- Projeto: Case Marketplace - Recuperação de Carrinho
-- ============================================================================

-- ──────────────────────────────────────────────
-- UNIQUE CONSTRAINTS
-- ──────────────────────────────────────────────

ALTER TABLE clientes
    ADD CONSTRAINT uq_clientes_email UNIQUE (email);

-- Um carrinho gera no máximo um pedido (relação 1:0,1)
ALTER TABLE pedidos
    ADD CONSTRAINT uq_pedidos_carrinho UNIQUE (carrinho_id);


-- ──────────────────────────────────────────────
-- FOREIGN KEYS
-- ──────────────────────────────────────────────

-- carrinhos → clientes
ALTER TABLE carrinhos
    ADD CONSTRAINT fk_carrinhos_cliente
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- itens_carrinho → carrinhos
ALTER TABLE itens_carrinho
    ADD CONSTRAINT fk_itens_carrinho
    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(carrinho_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- itens_carrinho → produtos (CASCADE: produto pode ser excluído; carrinho remove o item)
ALTER TABLE itens_carrinho
    ADD CONSTRAINT fk_itens_produto
    FOREIGN KEY (produto_id) REFERENCES produtos(produto_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- eventos_carrinho → carrinhos
ALTER TABLE eventos_carrinho
    ADD CONSTRAINT fk_eventos_carrinho
    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(carrinho_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- eventos_carrinho → clientes (desnormalização intencional)
ALTER TABLE eventos_carrinho
    ADD CONSTRAINT fk_eventos_carrinho_cliente
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- eventos_resgate → carrinhos
ALTER TABLE eventos_resgate
    ADD CONSTRAINT fk_resgate_carrinho
    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(carrinho_id)
    ON DELETE CASCADE ON UPDATE CASCADE;

-- eventos_resgate → clientes
ALTER TABLE eventos_resgate
    ADD CONSTRAINT fk_resgate_cliente
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- pedidos → carrinhos
ALTER TABLE pedidos
    ADD CONSTRAINT fk_pedidos_carrinho
    FOREIGN KEY (carrinho_id) REFERENCES carrinhos(carrinho_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- pedidos → clientes
ALTER TABLE pedidos
    ADD CONSTRAINT fk_pedidos_cliente
    FOREIGN KEY (cliente_id) REFERENCES clientes(cliente_id)
    ON DELETE RESTRICT ON UPDATE CASCADE;

-- pedidos → eventos_resgate (nullable - só para pedidos de recuperação)
ALTER TABLE pedidos
    ADD CONSTRAINT fk_pedidos_resgate
    FOREIGN KEY (resgate_id) REFERENCES eventos_resgate(resgate_id)
    ON DELETE SET NULL ON UPDATE CASCADE;


-- ──────────────────────────────────────────────
-- CHECK CONSTRAINTS
-- ──────────────────────────────────────────────

-- Status válidos do carrinho
ALTER TABLE carrinhos
    ADD CONSTRAINT chk_carrinhos_status
    CHECK (status IN ('ativo', 'abandonado', 'recuperado', 'comprado', 'expirado'));

-- Dispositivos válidos
ALTER TABLE carrinhos
    ADD CONSTRAINT chk_carrinhos_dispositivo
    CHECK (dispositivo IN ('mobile', 'desktop', 'tablet'));

-- Valores não-negativos em carrinhos
ALTER TABLE carrinhos
    ADD CONSTRAINT chk_carrinhos_valor_frete CHECK (valor_frete >= 0),
    ADD CONSTRAINT chk_carrinhos_valor_desconto CHECK (valor_desconto >= 0),
    ADD CONSTRAINT chk_carrinhos_valor_total CHECK (valor_total >= 0);

-- Quantidade positiva em itens
ALTER TABLE itens_carrinho
    ADD CONSTRAINT chk_itens_quantidade CHECK (quantidade > 0),
    ADD CONSTRAINT chk_itens_preco CHECK (preco_unitario > 0),
    ADD CONSTRAINT chk_itens_preco_total CHECK (preco_total > 0);

-- Tipos de evento válidos
ALTER TABLE eventos_carrinho
    ADD CONSTRAINT chk_eventos_tipo
    CHECK (tipo_evento IN (
        'view_produto', 'add_carrinho', 'remove_carrinho', 'update_quantidade',
        'view_checkout', 'inicio_pagamento', 'erro_pagamento', 'abandono', 'retorno'
    ));

-- Canais válidos de resgate
ALTER TABLE eventos_resgate
    ADD CONSTRAINT chk_resgate_canal
    CHECK (canal IN ('email', 'sms', 'push_app', 'whatsapp'));

-- Tipos de comunicação válidos
ALTER TABLE eventos_resgate
    ADD CONSTRAINT chk_resgate_tipo_comunicacao
    CHECK (tipo_comunicacao IN ('lembrete_1h', 'lembrete_24h', 'desconto_48h', 'urgencia_72h'));

-- Custo de envio positivo
ALTER TABLE eventos_resgate
    ADD CONSTRAINT chk_resgate_custo CHECK (custo_envio >= 0);

-- Preço do produto positivo
ALTER TABLE produtos
    ADD CONSTRAINT chk_produtos_preco CHECK (preco_atual > 0);

-- Avaliação entre 1.0 e 5.0
ALTER TABLE produtos
    ADD CONSTRAINT chk_produtos_avaliacao
    CHECK (avaliacao_media IS NULL OR (avaliacao_media >= 1.0 AND avaliacao_media <= 5.0));

-- Status do pedido
ALTER TABLE pedidos
    ADD CONSTRAINT chk_pedidos_status
    CHECK (status_pedido IN ('confirmado', 'enviado', 'entregue', 'cancelado'));

-- Método de pagamento
ALTER TABLE pedidos
    ADD CONSTRAINT chk_pedidos_pagamento
    CHECK (metodo_pagamento IN ('cartao_credito', 'cartao_debito', 'boleto', 'pix'));

-- Valor do pedido positivo
ALTER TABLE pedidos
    ADD CONSTRAINT chk_pedidos_valor CHECK (valor_total > 0);

-- Segmento RFM válido
ALTER TABLE clientes
    ADD CONSTRAINT chk_clientes_rfm
    CHECK (segmento_rfm IS NULL OR segmento_rfm IN ('premium', 'regular', 'dormant', 'novo'));
