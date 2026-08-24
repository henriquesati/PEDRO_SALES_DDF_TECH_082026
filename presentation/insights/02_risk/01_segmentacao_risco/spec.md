# Especificação Visual & BI: Segmentação de Risco de Abandono (Arquitetura de 3 Dashboards)

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)  
> **Documento de Regras de Negócio**: [`insights/02_risk/segmentacao_risco_abandono.md`](../../../../insights/02_risk/segmentacao_risco_abandono.md)

---

## 📌 Contexto & Pergunta de Negócio
- **Pergunta Central**: Como identificar carrinhos em risco crítico/alto durante a sessão ativa, quais fatores causais geram o atrito e qual a política ótima de acionamento que maximiza o Expected ROI sem gerar prejuízo financeiro?
- **Separação Metodológica (Hipótese vs Evidência)**: O score da sessão atua como regra heurística de triagem em tempo real, enquanto o pipeline de dados valida ex-post a correlação real entre tempo de inatividade no checkout (`CHECKOUT_STARTED`), dispositivo e novidade do cliente.

> [!NOTE]
> **Foco do Projeto em Proporções (%) & Referência Pitch Spec**: A matriz de calor e a triagem de risco fundamentam-se em proporções de tráfego e taxas relativas de propensão ao abandono (DEC-001). Os valores em R$ exemplificam a perda financeira usando a *Entidade Exemplo de Baseline* declarada em [`presentation/pitch/pitch_spec.md`](../../../pitch/pitch_spec.md#42-entidade-exemplo-de-negócio-baseline-mock-para-simulações-monetárias) (Premium R$ 800, Regular R$ 360, Novo R$ 250, Dormant R$ 200).

---

## 📊 Métricas & Fórmulas (Ground Truth)

- **Score de Risco da Sessão (`RISK_SCORE`)**:
  - `Valor do Carrinho > R$ 500`: +2 (senão +1)
  - `Dispositivo Mobile`: +2 (senão +1)
  - `Cliente Novo`: +2 (senão +1)
  - `Inatividade no Checkout >= 3 min`: +2 (senão +1)
  - `Fricção Técnica / Frete > 15%`: +3 (senão 0)
- **Faixas de Classificação**:
  - `CRÍTICO`: Score $\ge 8$
  - `ALTO`: Score $6 \le \text{Score} < 8$
  - `MÉDIO`: Score $4 \le \text{Score} < 6$
  - `BAIXO`: Score $< 4$
- **Expected ROI Multiplicador**: $\frac{\text{Probabilidade de Resgate} \times \text{Valor do Carrinho} - \text{Custo do Desconto} - \text{Custo do Canal}}{\text{Custo do Canal}}$.

---

## 🎨 Arquitetura de 3 Dashboards Especializados

### 1. Dashboard 1 — Risk Overview (Visão Executiva & Pareto)
- **Arquivo**: [`chart_03_dashboard_01_risk_overview.png`](chart_03_dashboard_01_risk_overview.png)
- **Componentes**:
  - Top KPI Cards: Carrinhos em Risco (1.284 un / 18%), Valor Represado sob Alto Risco (R$ 840k), Assimetria Pareto (18% da base $\rightarrow$ 42% do valor) e Recovery Rate (10.1%).
  - Painel Esquerdo: Distribuição Proporcional de Risco em Barras Horizontais (Baixo 52%, Médio 30%, Alto 12%, Crítico 6%).
  - Painel Direito: Concentração de Valor em Risco por Nível (Crítico R$ 360k, Alto R$ 290k, Médio R$ 150k, Baixo R$ 40k).

### 2. Dashboard 2 — Risk Drivers (Diagnóstico Causal & Atrito Técnico)
- **Arquivo**: [`chart_03_dashboard_02_risk_drivers.png`](chart_03_dashboard_02_risk_drivers.png)
- **Componentes**:
  - Painel Esquerdo: Heatmap 2D de Motivos de Abandono $\times$ Dispositivo (Mobile, Desktop, Tablet) com gradiente semântico de calor.
  - Painel Direito: Decomposição de Abandono por Plataforma (Mobile 61%, Desktop 31%, Tablet 8%) e ranking de Causas-Raiz (Preço 25%, Frete 23,1%, Indecisão 20%, Pagamento 18,4%).

### 3. Dashboard 3 — Intervention & Recovery (Prescrição Operacional & Matriz Risk $\times$ ROI)

Para garantir máxima legibilidade e evitar qualquer sobreposição visual de texto/tabela, o Dashboard 3 é disponibilizado em **duas visualizações autônomas dedicadas** além do painel combinado:

- **Dashboard 3A — Fila de Acionamento Prescritiva (Tabela Dedicada)**:
  - **Arquivo**: [`chart_03_dashboard_03a_fila_acionamento.png`](chart_03_dashboard_03a_fila_acionamento.png)
  - **Componentes**: Tabela operacional com largura expandida (Carrinho ID, Nível de Risco, Valor Cesta, Probabilidade de Resgate, Custo Canal, Expected ROI, Ação Prescrita/Canal e Política de Desconto) e card inferior de regras de governança para prevenção de prejuízo.
- **Dashboard 3B — Matriz Estratégica Risk $\times$ Expected ROI (Imagem Dedicada)**:
  - **Arquivo**: [`chart_03_dashboard_03b_matriz_risk_roi.png`](chart_03_dashboard_03b_matriz_risk_roi.png)
  - **Componentes**: Dispersão ampla com os 3 quadrantes estratégicos destacados e caixas de anotação com espaçamento generoso:
    - 🟢 **[QUADRANTE 1: PRIORIDADE MÁXIMA]**: Alto Risco + Alto Ticket (WhatsApp VIP / Suporte Humano / ROI 2.5x a 5.0x).
    - 🟡 **[QUADRANTE 2: AVALIAR / EMAIL]**: Risco Médio + Ticket Intermediário (Email Inbound + Push Notification / ROI 1.2x a 2.5x).
    - 🔴 **[QUADRANTE 3: NÃO INTERVIR COM CUSTO]**: Alto Risco de Baixo Ticket (Email Zero Cost / Sem WhatsApp, evitando margem negativa).
- **Dashboard 3 Combinado (Painel Duplo)**:
  - **Arquivo**: [`chart_03_dashboard_03_intervention_matrix.png`](chart_03_dashboard_03_intervention_matrix.png)

### 4. Painel Consolidado de Referência Rápida
- **Arquivo**: [`chart_03_segmentacao_risco.png`](chart_03_segmentacao_risco.png)
- **Componentes**: Matriz 2D de Risco RFM + Distribuição de Volume e Taxa Observada de Abandono.

---

## 📍 Mapeamento dos Dados Parquet
- **Entidades Utilizadas**:
  - `data/mock/output_cleaned/parquet/carrinhos.parquet`
  - `data/mock/output_cleaned/parquet/clientes.parquet`
  - `data/mock/output_cleaned/parquet/eventos_resgate.parquet`
  - `data/mock/output_cleaned/parquet/pedidos.parquet`

---

## 🖼️ Script Gerador
- **Script Oficial**: [`generate_chart.py`](generate_chart.py) (gera automaticamente todos os 6 artefatos em 300 DPI com fundo branco `#FFFFFF`).
