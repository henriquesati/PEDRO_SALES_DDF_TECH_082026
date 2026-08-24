-- ============================================================================
-- 004_views.sql
-- Views de métricas e análises derivadas
-- Substitui a tabela física metricas_resgate por views sob demanda
-- SGBD: PostgreSQL
-- Projeto: Case Marketplace - Recuperação de Carrinho
-- ============================================================================

-- ──────────────────────────────────────────────
-- VIEW 1: Métricas diárias de resgate
-- Substitui a tabela metricas_resgate do modelo original
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_metricas_resgate_diarias AS
SELECT
    DATE(c.data_abandono) AS data,

    -- Volume
    COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN c.carrinho_id END)
        AS total_carrinhos_abandonados,
    COUNT(DISTINCT CASE WHEN c.status IN ('recuperado', 'comprado') AND p.origem_recuperacao = TRUE THEN c.carrinho_id END)
        AS total_carrinhos_resgatados,

    -- Taxas
    ROUND(
        COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN c.carrinho_id END)::DECIMAL /
        NULLIF(COUNT(DISTINCT c.carrinho_id), 0) * 100, 2
    ) AS taxa_abandono_pct,

    -- Valor
    COALESCE(SUM(CASE WHEN c.status = 'abandonado' THEN c.valor_total END), 0)
        AS valor_total_abandonado,
    COALESCE(SUM(CASE WHEN p.origem_recuperacao = TRUE THEN p.valor_total END), 0)
        AS valor_total_recuperado,
    ROUND(AVG(CASE WHEN c.status = 'abandonado' THEN c.valor_total END), 2)
        AS valor_medio_carrinho_abandonado

FROM carrinhos c
LEFT JOIN pedidos p ON p.carrinho_id = c.carrinho_id
WHERE c.data_abandono IS NOT NULL
GROUP BY DATE(c.data_abandono)
ORDER BY data;


-- ──────────────────────────────────────────────
-- VIEW 2: Performance de canais de resgate
-- ROI, taxa de abertura, clique e conversão por canal
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_performance_canais AS
SELECT
    er.canal,

    -- Volume
    COUNT(*) AS total_envios,
    COUNT(er.data_abertura) AS total_aberturas,
    COUNT(er.data_primeiro_clique) AS total_cliques,
    COUNT(CASE WHEN er.sucesso THEN 1 END) AS total_conversoes,

    -- Taxas
    ROUND(COUNT(er.data_abertura)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 2)
        AS taxa_abertura_pct,
    ROUND(COUNT(er.data_primeiro_clique)::DECIMAL / NULLIF(COUNT(er.data_abertura), 0) * 100, 2)
        AS taxa_clique_pct,
    ROUND(COUNT(CASE WHEN er.sucesso THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 2)
        AS taxa_conversao_pct,

    -- Financeiro
    COALESCE(SUM(er.custo_envio), 0) AS custo_total,
    COALESCE(SUM(CASE WHEN er.sucesso THEN er.valor_pedido_final END), 0) AS receita_total,
    COALESCE(SUM(CASE WHEN er.sucesso THEN er.desconto_oferecido END), 0) AS desconto_total,

    -- ROI
    ROUND(
        (COALESCE(SUM(CASE WHEN er.sucesso THEN er.valor_pedido_final - er.desconto_oferecido END), 0)
         - SUM(er.custo_envio))
        / NULLIF(SUM(er.custo_envio), 0), 2
    ) AS roi

FROM eventos_resgate er
GROUP BY er.canal
ORDER BY roi DESC;


-- ──────────────────────────────────────────────
-- VIEW 3: Performance por tipo de comunicação
-- Qual template/timing funciona melhor?
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_performance_comunicacao AS
SELECT
    er.tipo_comunicacao,
    er.canal,

    COUNT(*) AS total_envios,
    COUNT(CASE WHEN er.sucesso THEN 1 END) AS total_conversoes,
    ROUND(COUNT(CASE WHEN er.sucesso THEN 1 END)::DECIMAL / NULLIF(COUNT(*), 0) * 100, 2)
        AS taxa_conversao_pct,
    ROUND(AVG(CASE WHEN er.sucesso THEN er.valor_pedido_final END), 2)
        AS ticket_medio_convertido,
    ROUND(AVG(er.desconto_oferecido), 2) AS desconto_medio_oferecido

FROM eventos_resgate er
GROUP BY er.tipo_comunicacao, er.canal
ORDER BY taxa_conversao_pct DESC;


-- ──────────────────────────────────────────────
-- VIEW 4: Análise de abandono por motivo e dispositivo
-- Insights para o pitch: onde e por que abandonam?
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_abandono_analise AS
SELECT
    c.motivo_abandono,
    c.dispositivo,
    c.canal_origem,

    COUNT(*) AS total_abandonos,
    ROUND(AVG(c.valor_total), 2) AS valor_medio_carrinho,
    ROUND(AVG(c.duracao_sessao_minutos), 1) AS duracao_media_sessao_min,
    ROUND(AVG(c.valor_frete), 2) AS frete_medio,

    -- Taxa de recuperação por segmento
    ROUND(
        COUNT(CASE WHEN c.status IN ('recuperado', 'comprado')
              AND EXISTS (SELECT 1 FROM pedidos p WHERE p.carrinho_id = c.carrinho_id AND p.origem_recuperacao = TRUE)
              THEN 1 END)::DECIMAL
        / NULLIF(COUNT(*), 0) * 100, 2
    ) AS taxa_recuperacao_pct

FROM carrinhos c
WHERE c.status IN ('abandonado', 'recuperado', 'comprado', 'expirado')
  AND c.data_abandono IS NOT NULL
GROUP BY c.motivo_abandono, c.dispositivo, c.canal_origem
ORDER BY total_abandonos DESC;


-- ──────────────────────────────────────────────
-- VIEW 5: Produtos mais abandonados
-- Quais produtos ficam no carrinho e são abandonados?
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_produtos_abandonados AS
SELECT
    p.produto_id,
    p.nome,
    p.categoria,
    p.marca,
    p.preco_atual,

    COUNT(DISTINCT ic.carrinho_id) AS total_carrinhos,
    COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN ic.carrinho_id END) AS carrinhos_abandonados,
    COUNT(DISTINCT CASE WHEN c.status = 'comprado' THEN ic.carrinho_id END) AS carrinhos_convertidos,

    ROUND(
        COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN ic.carrinho_id END)::DECIMAL /
        NULLIF(COUNT(DISTINCT ic.carrinho_id), 0) * 100, 2
    ) AS taxa_abandono_pct

FROM itens_carrinho ic
JOIN produtos p ON p.produto_id = ic.produto_id
JOIN carrinhos c ON c.carrinho_id = ic.carrinho_id
WHERE ic.data_remocao IS NULL  -- Apenas itens que permaneceram no carrinho
GROUP BY p.produto_id, p.nome, p.categoria, p.marca, p.preco_atual
ORDER BY carrinhos_abandonados DESC;


-- ──────────────────────────────────────────────
-- VIEW 6: LTV vs Abandono de Carrinho
-- Análise de valor em risco e ROI por segmento de cliente
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_ltv_abandono AS
SELECT
    COALESCE(cl.segmento_rfm, 'novo') AS segmento_rfm,
    
    -- Volume de carrinhos
    COUNT(c.carrinho_id) AS total_carrinhos,
    COUNT(CASE WHEN c.status = 'abandonado' THEN c.carrinho_id END) AS carrinhos_abandonados,
    COUNT(CASE WHEN c.status IN ('recuperado', 'comprado') AND p.origem_recuperacao = TRUE THEN c.carrinho_id END) AS carrinhos_recuperados,
    
    -- Taxa de abandono por segmento
    ROUND(
        COUNT(CASE WHEN c.status = 'abandonado' THEN c.carrinho_id END)::DECIMAL /
        NULLIF(COUNT(c.carrinho_id), 0) * 100, 2
    ) AS taxa_abandono_pct,
    
    -- Taxa de recuperação por segmento
    ROUND(
        COUNT(CASE WHEN c.status IN ('recuperado', 'comprado') AND p.origem_recuperacao = TRUE THEN c.carrinho_id END)::DECIMAL /
        NULLIF(COUNT(CASE WHEN c.status = 'abandonado' THEN c.carrinho_id END), 0) * 100, 2
    ) AS taxa_recuperacao_pct,
    
    -- Valores financeiros
    COALESCE(SUM(CASE WHEN c.status = 'abandonado' THEN c.valor_total END), 0) AS valor_total_em_risco,
    ROUND(AVG(CASE WHEN c.status = 'abandonado' THEN c.valor_total END), 2) AS ticket_medio_abandonado,
    COALESCE(SUM(CASE WHEN p.origem_recuperacao = TRUE THEN p.valor_total END), 0) AS receita_recuperada,
    
    -- LTV Médio do Segmento
    ROUND(AVG(cl.lifetime_value), 2) AS ltv_medio_cliente

FROM clientes cl
JOIN carrinhos c ON c.cliente_id = cl.cliente_id
LEFT JOIN pedidos p ON p.carrinho_id = c.carrinho_id
GROUP BY COALESCE(cl.segmento_rfm, 'novo')
ORDER BY valor_total_em_risco DESC;


-- ──────────────────────────────────────────────
-- VIEW 7: Viabilidade de Recuperação por Carrinho
-- Score de recuperabilidade, custo estimado e retorno esperado
-- ──────────────────────────────────────────────
CREATE OR REPLACE VIEW vw_viabilidade_recuperacao AS
WITH base_carrinhos AS (
    SELECT
        c.carrinho_id,
        c.cliente_id,
        cl.segmento_rfm,
        c.valor_total,
        c.valor_frete,
        c.motivo_abandono,
        c.status,
        c.data_abandono,
        c.dispositivo,
        
        -- Probabilidade Base por RFM
        CASE cl.segmento_rfm
            WHEN 'premium' THEN 0.18
            WHEN 'novo' THEN 0.12
            WHEN 'regular' THEN 0.10
            WHEN 'dormant' THEN 0.06
            ELSE 0.10
        END AS p_base,
        
        -- Fator Motivo
        CASE c.motivo_abandono
            WHEN 'indecisao' THEN 1.2
            WHEN 'frete' THEN 1.1
            WHEN 'preco' THEN 1.0
            WHEN 'pagamento' THEN 0.8
            WHEN 'estoque' THEN 0.3
            ELSE 0.9
        END AS fator_motivo,
        
        -- Fator Valor
        CASE
            WHEN c.valor_total > 500 THEN 1.1
            WHEN c.valor_total >= 100 THEN 1.0
            ELSE 0.9
        END AS fator_valor,
        
        -- Custo Estimado de Envio por Segmento
        CASE cl.segmento_rfm
            WHEN 'premium' THEN 0.40  -- WhatsApp + Email
            WHEN 'dormant' THEN 0.20  -- Email + SMS
            ELSE 0.07                -- Email + Push
        END AS custo_envio_est,
        
        -- Canal Recomendado
        CASE cl.segmento_rfm
            WHEN 'premium' THEN 'whatsapp'
            WHEN 'dormant' THEN 'sms'
            ELSE 'email'
        END AS canal_recomendado

    FROM carrinhos c
    JOIN clientes cl ON cl.cliente_id = c.cliente_id
    WHERE c.status = 'abandonado'
      AND c.data_abandono IS NOT NULL
),
score_calculado AS (
    SELECT
        bc.*,
        
        -- Probabilidade Final Capped [1%, 50%]
        ROUND(
            LEAST(GREATEST(bc.p_base * bc.fator_motivo * bc.fator_valor, 0.01), 0.50)::NUMERIC,
            4
        ) AS prob_recuperacao,
        
        -- Custo Total Estimado
        ROUND(bc.custo_envio_est::NUMERIC, 2) AS custo_estimado,
        
        -- Retorno Esperado = P_Recuperacao * Valor_Total
        ROUND(
            (LEAST(GREATEST(bc.p_base * bc.fator_motivo * bc.fator_valor, 0.01), 0.50) * bc.valor_total)::NUMERIC,
            2
        ) AS retorno_esperado
    FROM base_carrinhos bc
)
SELECT
    sc.carrinho_id,
    sc.cliente_id,
    sc.segmento_rfm,
    sc.motivo_abandono,
    sc.valor_total,
    sc.valor_frete,
    sc.dispositivo,
    sc.data_abandono,
    sc.canal_recomendado,
    
    ROUND((sc.prob_recuperacao * 100)::NUMERIC, 1) AS prob_recuperacao_pct,
    sc.custo_estimado,
    sc.retorno_esperado,
    
    -- ROI Esperado Unitário
    ROUND((sc.retorno_esperado / NULLIF(sc.custo_estimado, 0))::NUMERIC, 1) AS roi_esperado,
    
    -- Classificação de Viabilidade
    CASE
        WHEN (sc.retorno_esperado / NULLIF(sc.custo_estimado, 0)) >= 50 AND sc.retorno_esperado >= 10.0 THEN 'ALTA'
        WHEN (sc.retorno_esperado / NULLIF(sc.custo_estimado, 0)) >= 10 AND sc.retorno_esperado >= 2.0 THEN 'MEDIA'
        ELSE 'BAIXA'
    END AS viabilidade_recuperacao,
    
    -- Ação Prescrita
    CASE
        WHEN (sc.retorno_esperado / NULLIF(sc.custo_estimado, 0)) >= 50 AND sc.retorno_esperado >= 10.0
            THEN 'Resgate Imediato (+1h) via ' || UPPER(sc.canal_recomendado)
        WHEN (sc.retorno_esperado / NULLIF(sc.custo_estimado, 0)) >= 10 AND sc.retorno_esperado >= 2.0
            THEN 'Regua Padrao (+24h) via EMAIL/PUSH'
        ELSE 'Nao Disparar Outbound (Apenas Retargeting Passivo)'
    END AS acao_prescrita

FROM score_calculado sc
ORDER BY sc.retorno_esperado DESC;

