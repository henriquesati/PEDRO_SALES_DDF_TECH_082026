# Especificação: Análise de Dados, Visualizações de BI (Metabase) & Camada Semântica — Recuperação de Carrinho

**Doc ID**: `spec_bi_visualizations_001`  
**Versão**: 1.0  
**Módulo:** `pipelines/case-item-07/`  
**Case Oficial Dadosfera:** Item 7 — Sobre Análise de Dados (Analisar)  
**Papel Arquitetural:** **Hub Central de BI, Serving Analítico, Dashboards e Governança Semântica**  
**Framework Normativo:** Visualizações Canônicas + Padrão charts-maker (Fundo Branco `#FFFFFF`, 300 DPI) + DEC-001 (Métricas em %) + DEC-008 (Kimball DW)  
**Status**: Active / Production Ready  
**Escopo**: Case Técnico de Estágio em Solutions Engineering / Dados (Dadosfera)  

---

## 📋 1. EXECUTIVE SUMMARY & ARQUITETURA HUB

### 🎯 1.1 Objetivo Estratégico do Item 7
Consolidar e disponibilizar a camada analítica de consumo visual (**BI / Metabase / Dashboards**) a partir dos dados limpos e modelados no Data Lakehouse (camadas Silver Qualify e Gold Kimball), entregando visualizações executivas e operacionais de alto impacto para responder às principais perguntas de negócio do case de **Recuperação de Carrinho Abandonado**:

1. **Série Temporal (Evolução & Sazonalidade)**: Como se comportam o volume de abandono, a taxa de recuperação e o faturamento ao longo do tempo?
2. **Performance de Catálogo por Categoria**: Quais categorias de produtos apresentam maior atrito no checkout e maior potencial financeiro de resgate?
3. **Eficiência de Canais & ROI (CAC de Resgate)**: Qual o retorno multiplicador (ROI) de cada canal de mensageria (E-mail, WhatsApp, SMS, Push) sobre o custo de disparo?
4. **Matriz de Atrito e Segmentação RFM**: Quais as causas-raiz de abandono para cada perfil de cliente (*Novos* vs *Dormant* vs *Premium*)?
5. **Matriz Prescritiva de Viabilidade (Decisão de Acionamento)**: Quais carrinhos abandonados devem ser priorizados pelas equipes de CRM e atendimento para maximizar o GMV líquido recuperado?
6. **Confiabilidade e Qualidade dos Dados**: Qual o nível de conformidade dos dados de suporte às decisões analíticas?

---

### 🌐 1.2 Mapa do Hub Central & Referências Cruzadas
O módulo `pipelines/case-item-07/` atua como o **Hub Central de Conexão Analítica** do projeto. Ele consolida os requisitos do Item 7 sem duplicar definições, conectando-se diretamente aos módulos especializados:

```text
                                  ┌────────────────────────────────────────────────────────┐
                                  │      PIPELINES / CASE-ITEM-07 (HUB CENTRAL DE BI)      │
                                  │   • specs.md (Esta especificação)                      │
                                  │   • notebooks/07_bi_dashboards_visualizations.ipynb    │
                                  │   • scripts/run_bi_analysis.py                         │
                                  │   • outputs/bi_analysis_report.md & outputs/assets/    │
                                  └───────────────────────────┬────────────────────────────┘
                                                              │
                 ┌─────────────────────────┬──────────────────┴───────────────┬─────────────────────────┐
                 ▼                         ▼                                  ▼                         ▼
  ┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐ ┌─────────────────────────────┐
  │  DASHBOARDS METABASE (ITEM 7)│ │ CAMADA SEMÂNTICA DE MÉTRICAS│ │ MODELAGEM KIMBALL DW (IT. 6)│ │  GALERIA DE INSIGHTS & BI   │
  │ • dashboards/               │ │ • metrics/                  │ │ • pipelines/case-item-06/   │ │ • presentation/insights/    │
  │   dashboard_recuperacao_    │ │   catalogo_kpis.md          │ │   v_abandonment_summary     │ │   01_descriptive/           │
  │   carrinho.md               │ │   matriz_metricas_dimensoes │ │   v_recovery_roi_by_segment │ │   02_risk/                  │
  │ • Queries SQL para Metabase │ │   arvore_metricas_driver_tree││ • Star Schema Snowflake     │ │   03_prescriptive/          │
  └─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘ └─────────────────────────────┘
```

| Módulo Referenciado | Caminho no Repositório | Conteúdo e Papel no Hub |
|---|---|---|
| **Especificação de Dashboards** | [`dashboards/dashboard_recuperacao_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/dashboard_recuperacao_carrinho.md) | Especificação das 6 visualizações no Metabase da Dadosfera, filtros globais e layout executivo |
| **Catálogo de KPIs Master** | [`metrics/catalogo_kpis.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/catalogo_kpis.md) | Fórmulas em $\LaTeX$, grão, interpretação e benchmarks de mercado dos 13 KPIs de negócio |
| **Matriz Semântica Dimensional** | [`metrics/matriz_metricas_dimensoes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/matriz_metricas_dimensoes.md) | Fatiamento dimensional cruzando os KPIs analíticos contra as 6 Dimensões Conformadas Kimball |
| **Driver Tree da North Star** | [`metrics/arvore_metricas_driver_tree.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/arvore_metricas_driver_tree.md) | Decomposição causal da North Star Metric (Taxa Líquida de Recuperação e ROI de ~45x) |
| **Métricas de DQ & SLO** | [`metrics/metricas_data_quality_slo.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/metrics/metricas_data_quality_slo.md) | Telemetria de volumetria auditada, taxa de conformidade (98.76%) e quarentena Silver Anomalies |
| **Modelagem Dimensional Gold** | [`pipelines/case-item-06/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/specs.md) | Schemas dimensionais Kimball, tabelas de fatos (`fato_abandono`, `fato_resgate`) e visões analíticas |
| **Regras Canônicas de Negócio** | [`data/data-models/logical/business-rules.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/data-models/logical/business-rules.md) | SSOT de invariantes contábeis, temporalidade de abandono (15 min) e lógicas de BI |
| **Galeria de Gráficos Analíticos** | [`presentation/insights/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/) | Scripts e specs de visualizações analíticas em alta resolução (300 DPI) |

---

## 📈 2. CATÁLOGO DAS 6 VISUALIZAÇÕES DE BI & GROUND TRUTH

Todas as visualizações são renderizadas no padrão canônico [`charts-maker`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/.agents/skills/charts-maker/SKILL.md) (**fundo branco puro `#FFFFFF`**, resolução **300 DPI**, paleta executiva semântica e dados 100% calculados a partir dos Parquets do Lakehouse):

---

### 📊 2.1 Visualização 1: Série Temporal — Evolução Semanal de Abandono vs Recuperação
- **Tipo de Gráfico**: Gráfico de Linha Duplo Eixo (Time Series Combo Chart com marcadores e `fill_between` suave).
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_01_serie_temporal_abandono_resgate.png)
- **Requisito Atendido**: Requisito explícito de **Análise de Série Temporal** do Item 7.
- **Grão e Eixos**:
  - *Eixo X*: Semana do Ano (Jan–Jun 2026).
  - *Eixo Y (Esquerda)*: Taxa de Abandono (~70.9%) vs Taxa de Recuperação (~10.1%).
  - *Eixo Y (Direita)*: GMV Total Abandonado (R$) vs GMV Recuperado (R$).
- **Insight de Negócio**: Evidencia a consistência temporal das taxas de abandono com picos sazonais de conversão após a ativação das réguas de resgate da Dadosfera.

```sql
-- Query Canônica Snowflake / Metabase
SELECT
    DATE_TRUNC('week', c.data_criacao) AS semana,
    COUNT(c.carrinho_id) AS total_carrinhos,
    COUNT(CASE WHEN c.status = 'abandonado' THEN 1 END) AS carrinhos_abandonados,
    COUNT(CASE WHEN c.status = 'recuperado' THEN 1 END) AS carrinhos_recuperados,
    ROUND(COUNT(CASE WHEN c.status = 'abandonado' THEN 1 END) * 100.0 / NULLIF(COUNT(c.carrinho_id), 0), 2) AS taxa_abandono_pct,
    ROUND(COUNT(CASE WHEN c.status = 'recuperado' THEN 1 END) * 100.0 / NULLIF(COUNT(CASE WHEN c.status = 'abandonado' THEN 1 END), 0), 2) AS taxa_recuperacao_pct,
    SUM(c.valor_total) AS gmv_total,
    SUM(CASE WHEN c.status = 'recuperado' THEN c.valor_total ELSE 0 END) AS gmv_recuperado
FROM carrinhos_qualify c
GROUP BY 1
ORDER BY 1 ASC;
```

---

### 📊 2.2 Visualização 2: Performance de Catálogo por Categoria
- **Tipo de Gráfico**: Gráfico de Barras Horizontais Empilhadas/Agrupadas com anotações de taxa e ticket médio.
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_02_performance_categorias.png)
- **Requisito Atendido**: Requisito explícito de **Análise por Categorias de Produto** do Item 7.
- **Dimensões**: Categorias (*Eletrônicos, Casa & Decoração, Moda, Esportes, Beleza, Livros, Brinquedos*).
- **Métricas**: Volume Abandonado, Volume Convertido, Taxa de Abandono (%) e Ticket Médio (R$).
- **Insight de Negócio**: *Eletrônicos* possui o maior ticket médio (R$ 850+) e maior taxa de atrito por sensibilidade a frete e preço; *Moda* e *Beleza* possuem alta rotatividade com maior taxa de resposta a cupons.

```sql
-- Query Canônica Snowflake / Metabase
SELECT
    p.categoria,
    COUNT(DISTINCT ic.carrinho_id) AS volume_carrinhos,
    COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN ic.carrinho_id END) AS volume_abandonado,
    COUNT(DISTINCT CASE WHEN c.status = 'recuperado' THEN ic.carrinho_id END) AS volume_recuperado,
    ROUND(AVG(p.preco), 2) AS preco_medio,
    ROUND(COUNT(DISTINCT CASE WHEN c.status = 'abandonado' THEN ic.carrinho_id END) * 100.0 / NULLIF(COUNT(DISTINCT ic.carrinho_id), 0), 2) AS taxa_abandono_pct
FROM itens_carrinho_qualify ic
JOIN produtos_qualify p ON ic.produto_id = p.produto_id
JOIN carrinhos_qualify c ON ic.carrinho_id = c.carrinho_id
GROUP BY 1
ORDER BY volume_abandonado DESC;
```

---

### 📊 2.3 Visualização 3: Rentabilidade & ROI por Canal de Mensageria
- **Tipo de Gráfico**: Combo Chart (Barras de Custo vs Receita Gerada e Linha de Multiplicador de ROI Líquido).
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_03_roi_eficiencia_canais.png)
- **Dimensões**: Canais de Resgate (`email`, `push_app`, `sms`, `whatsapp`).
- **Métricas**: Custo Total de Mensageria (R$), Receita Recuperada (R$) e ROI Multiplicador ($ROI = \frac{\text{Receita Recuperada}}{\text{Custo Total}}$).
- **Insight de Negócio**: O canal *Email* lidera em eficiência de ROI unitário (~113x) devido ao custo marginal irrisório (R$ 0,02/envio), enquanto o *WhatsApp* entrega o maior volume financeiro recuperado em valor absoluto com ticket médio elevado.

```sql
-- Query Canônica Snowflake / Metabase
SELECT
    er.canal,
    COUNT(er.evento_resgate_id) AS disparos_totais,
    COUNT(CASE WHEN er.status_entrega = 'convertido' THEN 1 END) AS resgates_sucesso,
    SUM(er.custo_disparo) AS custo_total_disparos,
    SUM(CASE WHEN er.status_entrega = 'convertido' THEN c.valor_total ELSE 0 END) AS receita_recuperada,
    ROUND(
        SUM(CASE WHEN er.status_entrega = 'convertido' THEN c.valor_total ELSE 0 END) / 
        NULLIF(SUM(er.custo_disparo), 0), 
        1
    ) AS multiplicador_roi
FROM eventos_resgate_qualify er
JOIN carrinhos_qualify c ON er.carrinho_id = c.carrinho_id
GROUP BY 1
ORDER BY multiplicador_roi DESC;
```

---

### 📊 2.4 Visualização 4: Matriz de Atrito RFM (Heatmap de Causas-Raiz)
- **Tipo de Gráfico**: Mapa de Calor (Heatmap com anotações de intensidade e percentuais).
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_04_matriz_motivos_rfm_heatmap.png)
- **Dimensões**: Motivos de Abandono (*Preço/Frete, Indecisão, Falha de Pagamento, Problemas no Checkout, Navegação*) × Segmentos RFM (*Novos, Regulares, Dormant, Premium*).
- **Métrica**: Frequência e Volume de GMV represado.
- **Insight de Negócio**: Clientes *Novos* abandonam predominantemente por atrito de frete/preço (alta sensibilidade); clientes *Premium* abandonam por indecisão ou experiência de navegação, demandando atendimento humanizado via WhatsApp em vez de descontos genéricos.

```sql
-- Query Canônica Snowflake / Metabase
SELECT
    cli.segmento_rfm,
    c.motivo_abandono,
    COUNT(c.carrinho_id) AS total_carrinhos,
    SUM(c.valor_total) AS gmv_represado
FROM carrinhos_qualify c
JOIN clientes_qualify cli ON c.cliente_id = cli.cliente_id
WHERE c.status = 'abandonado'
GROUP BY 1, 2
ORDER BY 1, total_carrinhos DESC;
```

---

### 📊 2.5 Visualização 5: Dispersão de Viabilidade & Priorização Prescritiva
- **Tipo de Gráfico**: Scatter Plot com Bolhas (Eixo X: Probabilidade de Conversão, Eixo Y: Valor do Carrinho, Cores por Nível de Viabilidade ALTA/MÉDIA/BAIXA, Tamanho por Retorno Esperado).
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_05_dispersao_viabilidade_recuperacao.png)
- **Insight de Negócio**: Fornece o quadrante de ouro de acionamento imediato (Alto Ticket + Alta Probabilidade de Conversão), permitindo às réguas automatizadas direcionar cupons de maior agressividade apenas para os casos de ROI garantido.

```sql
-- Query Canônica Snowflake / Metabase
SELECT
    c.carrinho_id,
    c.cliente_id,
    cli.segmento_rfm,
    c.valor_total,
    c.probabilidade_recuperacao_pct,
    ROUND(c.valor_total * (c.probabilidade_recuperacao_pct / 100.0), 2) AS retorno_esperado_bruto,
    CASE 
        WHEN c.probabilidade_recuperacao_pct >= 70 AND c.valor_total >= 300 THEN 'ALTA'
        WHEN c.probabilidade_recuperacao_pct >= 40 OR c.valor_total >= 200 THEN 'MEDIA'
        ELSE 'BAIXA'
    END AS nivel_viabilidade
FROM carrinhos_qualify c
JOIN clientes_qualify cli ON c.cliente_id = cli.cliente_id
WHERE c.status = 'abandonado';
```

---

### 📊 2.6 Visualização 6: Resumo de Data Quality & Quarentena de Dados
- **Tipo de Gráfico**: Donut Chart + Barra Horizontal de Severidade de Anomalias.
- **Artefato Gerado**: [`pipelines/case-item-07/outputs/assets/chart_06_data_quality_anomalies_summary.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-07/outputs/assets/chart_06_data_quality_anomalies_summary.png)
- **Insight de Negócio**: Garante transparência na governança de dados ao demonstrar que 94,2% dos registros de checkout estão qualificados na Silver Qualify, enquanto 5,8% de dados anômalos foram segregados na Quarentena sem contaminar os KPIs executivos.

---

## 🛠️ 3. COMANDOS DE EXECUÇÃO & TASK RUNNER (PYTHON PURO)

O Item 7 pode ser executado via CLI multiplataforma ou de forma granular:

```bash
# Executa a geração completa das 6 visualizações de BI e relatório de métricas:
python make.py notebook-gen

# Ou diretamente pelo script dedicado do Item 7:
python pipelines/case-item-07/scripts/run_bi_analysis.py
```
