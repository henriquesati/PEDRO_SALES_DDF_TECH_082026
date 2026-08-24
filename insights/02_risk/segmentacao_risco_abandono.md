# Segmentação de Risco de Abandono (Score de Risco & Arquitetura de 3 Dashboards)

> **Referência Canônica de Negócio**: [`presentation/pitch/pitch_spec.md`](../../presentation/pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)

---

## ❓ Pergunta de Negócio

Podemos identificar carrinhos com alta probabilidade de abandono antes mesmo do encerramento da sessão? Qual é o perfil, os gatilhos causais e a viabilidade econômica de cada intervenção, separando claramente o que é **regra heurística (hipótese operacional)** do que é **evidência histórica validada empiricamente nos dados**?

---

## 📊 Métrica & Definição Estruturada do Score

### [1] Distinção Metodológica: Score Heurístico vs. Validação Empírica

> [!IMPORTANT]
> **SEPARAÇÃO CRÍTICA: HIPÓTESE OPERACIONAL vs. EVIDÊNCIA HISTÓRICA**
> - **Score Heurístico (Hipótese Operacional)**: É uma regra de negócio preliminar parametrizada para triagem em tempo real durante a navegação. Serve como *proxy* de risco para priorizar atenção operacional.
> - **Validação Empírica (Evidência Histórica)**: Nenhuma premissa (ex.: "mobile aumenta abandono em X%" ou "cliente novo tem Y% mais risco") é tratada como verdade dogmática a priori. O pipeline Dadosfera cruza continuamente o score calculado com o desfecho real observado (`status = 'abandonado'` vs `status = 'comprado'`), calibrando os pesos com base em regressão e telemetria observada.

### [2] KPIs Principais
- **KPI Primário**: Índice de Distribuição de Risco de Abandono (`% de carrinhos por faixa de risco`).
- **KPIs Secundários**:
  - Volume de Carrinhos em Risco Crítico / Alto (`unidades`).
  - Volume Financeiro sob Risco Crítico (`R$ Represado`).
  - Taxa de Abandono Observada por Nível de Risco (`%`).
  - Expected ROI Multiplicador de Resgate (`Receita Líquida Esperada / Custo de Intervenção`).

### [3] Fórmula e Componentes do Score de Risco (`RISK_SCORE`)

A pontuação de risco da sessão é calculada somando os fatores de risco observados no carrinho e nos eventos de checkout:

$$\text{RISK\_SCORE} = \text{Fator\_Valor} + \text{Fator\_Dispositivo} + \text{Fator\_Relacionamento} + \text{Fator\_Inatividade\_Checkout} + \text{Fator\_Atrito}$$

1. **Valor do Carrinho (`Fator_Valor`)**:
   - Se `valor_total > R$ 500,00`: **+2 pontos** (maior fricção de decisão / indecisão).
   - Senão: **+1 ponto**.
2. **Dispositivo (`Fator_Dispositivo`)**:
   - Se `dispositivo = 'mobile'`: **+2 pontos** (maior propensão a distrações e atrito no formulário).
   - Senão (`desktop` ou `tablet`): **+1 ponto**.
3. **Relacionamento (`Fator_Relacionamento`)**:
   - Se `cliente_novo = TRUE` (sem compras prévias): **+2 pontos** (ausência de histórico de confiança).
   - Senão: **+1 ponto**.
4. **Inatividade Específica no Checkout (`Fator_Inatividade_Checkout`)**:
   - *Nota de Consistência*: Diferencia-se rigorosamente a **duração total da sessão** (`duracao_sessao_minutos`) do **tempo parado na etapa de checkout** (`tempo_desde_ultima_interacao_checkout`).
   - Se `tempo_desde_ultima_interacao_checkout >= 3 minutos` (ou sem interação pós `CHECKOUT_STARTED`): **+2 pontos**.
   - Senão: **+1 ponto**.
5. **Sinal de Fricção / Erro Técnico (`Fator_Atrito`)**:
   - Se detectado evento `PAYMENT_ERROR`, erro de cartão, ou `valor_frete > 15% do subtotal`: **+3 pontos**.
   - Senão: **0 pontos**.

### [4] Classificação do Nível de Risco (`RISK_LEVEL`)
- **`CRÍTICO`**: $\text{RISK\_SCORE} \ge 8$ (Múltiplos fatores combinados: ex. Cliente Novo + Mobile + Frete Alto + Inatividade no Checkout).
- **`ALTO`**: $6 \le \text{RISK\_SCORE} < 8$.
- **`MÉDIO`**: $4 \le \text{RISK\_SCORE} < 6$.
- **`BAIXO`**: $\text{RISK\_SCORE} < 4$.

---

## 💡 Hipóteses Operacionais vs. Evidências Empíricas

### [1] O "Ponto de Não Retorno" no Checkout (Hipótese a Investigar)
- **Hipótese de Trabalho**: Usuários navegando via mobile com carrinhos de valor elevado que permanecem mais de 3 minutos sem interação após o evento `CHECKOUT_STARTED` têm probabilidade de abandono estimada em $> 80\%$.
- **Evidência Histórica Necessária no Dataset**:
  - O pipeline mede a curva empírica de decaimento por minuto de inatividade no checkout a partir dos eventos `CHECKOUT_STARTED`, `CHECKOUT_INTERACTION`, `PAYMENT_STARTED` e `PAYMENT_ERROR`.
  - Essa métrica é tratada como **hipótese contínua de calibração**, e não como certeza a priori.

### [2] Distribuição de Volume e Concentração Financeira (Assimetria de Pareto)
Com base na **Entidade Exemplo de Baseline do Pitch** (7.500 carrinhos semestrais, Ticket Médio Global R$ 375,00):
- **Baixo Risco (~52% dos carrinhos / ~3.900 un)**: Majoritariamente clientes *Premium* e *Regular* navegando em Desktop; conversão orgânica alta (> 40%).
- **Médio Risco (~30% dos carrinhos / ~2.250 un)**: Clientes regulares navegando em mobile/desktop com tickets intermediários; sensíveis a frete.
- **Alto Risco (~12% dos carrinhos / ~900 un)**: Clientes novos ou recorrentes em mobile com atrito de frete/preço.
- **Crítico Risco (~6% dos carrinhos / ~450 un)**: Clientes novos em mobile com carrinhos > R$ 500 ou erro no checkout.
- **Assimetria de Pareto**: **~18% dos carrinhos (Alto + Crítico) concentram mais de 40% a 42% de todo o valor financeiro em risco**, permitindo intervenções cirúrgicas de altíssimo retorno sobre investimento.

---

## 🖥️ Arquitetura de 3 Dashboards Especializados

Para fornecer clareza executiva e acionabilidade sem poluição visual, o monitoramento de risco é dividido em **3 dashboards modulares e complementares**:

```text
┌─────────────────────────────────────────────────────────────────────────┐
│                    ARQUITETURA DE 3 DASHBOARDS DE RISCO                 │
├─────────────────────────┬───────────────────────┬───────────────────────┤
│ 1. RISK OVERVIEW        │ 2. RISK DRIVERS       │ 3. INTERVENTION/REC.  │
│ (Visão Executiva)       │ (Diagnóstico Causal)  │ (Operacional & ROI)   │
├─────────────────────────┼───────────────────────┼───────────────────────┤
│ • KPI Cards Executivos  │ • Heatmap Multidimens.│ • Fila de Acionamento │
│ • Barras de Distribuição│ • Abandono p/ Device  │ • Matriz Estratégica  │
│ • Pareto de Valor R$    │ • Abandono p/ Causa   │   Risk × Expected ROI │
└─────────────────────────┴───────────────────────┴───────────────────────┘
```

---

### Dashboard 1 — Risk Overview (Visão Executiva)

**Público**: Diretores de E-commerce, CMO, Head de Dados.  
**Pergunta Central**: *Qual é a nossa exposição atual ao risco de abandono e quanto valor financeiro está em jogo?*

#### 1. KPI Cards Superiores
- **Carrinhos em Risco (Alto + Crítico)**: `1.284 un` (~17,1% a 18% da base semestral).
- **Valor Financeiro em Risco**: `R$ 840k` (montante total represado nas faixas de maior atenção).
- **Concentração de Risco (Alto + Crítico)**: `18% da base` $\rightarrow$ `42% do valor`.
- **Taxa Global de Recuperação (Recovery Rate)**: `7,4% a 10,1%`.

#### 2. Gráfico 1 — Distribuição Proporcional de Risco (Barras Horizontais)
- `BAIXO`: `52%` (3.900 un)
- `MÉDIO`: `30%` (2.250 un)
- `ALTO`: `12%` (900 un)
- `CRÍTICO`: `6%` (450 un)
*(Visualização em barras horizontais para facilitar comparação visual e leitura executiva).*

#### 3. Gráfico 2 — Concentração de Valor em Risco por Nível (Assimetria Financeira)
- `CRÍTICO`: `R$ 360k` (Ticket médio mais elevado)
- `ALTO`: `R$ 290k`
- `MÉDIO`: `R$ 150k`
- `BAIXO`: `R$ 40k`
- **Narrativa Executiva**: 18% dos carrinhos concentram 42% da receita em risco, justificando alocação direcionada de canais nobres.

---

### Dashboard 2 — Risk Drivers (Diagnóstico Causal)

**Público**: Gerentes de Produto (PM), Engenheiros de Conversão (CRO), Time de UX/UI.  
**Pergunta Central**: *Por que esses carrinhos estão entrando em risco e onde estão os maiores atritos?*

#### 1. Heatmap Multidimensional: Motivo de Atrito vs. Dispositivo de Navegação
| Causa-Raiz / Motivo | Mobile | Desktop | Tablet | Diagnóstico & Ação Prioritária |
|---|:---:|:---:|:---:|---|
| **Frete Caro (> 15%)** | 🔴 *Crítico (34%)* | 🟡 *Médio (21%)* | 🟢 *Baixo (15%)* | Mobile sofre maior sensibilidade ao frete no checkout |
| **Preço Alto / Comparação** | 🔴 *Crítico (28%)* | 🟡 *Médio (24%)* | 🟢 *Baixo (18%)* | Comportamento de busca de cupons em abas concorrentes |
| **Erro no Pagamento / PIX** | 🔴 *Crítico (22%)* | 🟡 *Médio (14%)* | 🟡 *Médio (16%)* | Falha de carregamento de chave PIX / cartão em telas touch |
| **Indecisão / Dúvida Técnica**| 🟡 *Médio (16%)* | 🟢 *Baixo (11%)* | 🟢 *Baixo (12%)* | Falta de avaliações visíveis ou especificações claras |

#### 2. Gráfico de Barras: Volume de Abandono por Dispositivo
- `Mobile`: **61%** do volume total de abandono.
- `Desktop`: **31%** do volume total.
- `Tablet`: **8%** do volume total.

#### 3. Gráfico de Barras: Volume de Abandono por Causa-Raiz
- `Frete Caro`: **1.207 un** (23,1%)
- `Preço Alto`: **1.307 un** (25,0%)
- `Erro no Pagamento`: **961 un** (18,4%)
- `Indecisão / Dúvida`: **1.045 un** (20,0%)
- `Não Informado / Estoque`: **711 un** (13,5%)

---

### Dashboard 3 — Intervention & Recovery (Prescrição Operacional & ROI)

**Público**: Analistas de CRM, Automação de Marketing, Especialistas de Atendimento VIP.  
**Pergunta Central**: *Quem devemos abordar, por qual canal e quando economicamente vale a pena agir?*

#### 1. Fila de Acionamento Operacional (Tabela com Decisão Econômica)
O dashboard não diz apenas que um carrinho está em risco; ele determina se **economicamente vale a pena intervir**:

| Carrinho ID | Nível de Risco | Valor da Cesta | Prob. Resgate | Custo Canal | Expected ROI | Ação Prescrita |
|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `#1042` | **CRÍTICO** | R$ 520,00 | 78% | R$ 0,30 (WhatsApp) | **3,1x** | 🟢 WhatsApp / Suporte VIP Instantâneo |
| `#9381` | **CRÍTICO** | R$ 680,00 | 81% | R$ 0,30 (WhatsApp) | **2,8x** | 🟢 WhatsApp / Reserva de Estoque Sem Desconto |
| `#1291` | **ALTO** | R$ 340,00 | 64% | R$ 0,05 (Email) | **2,2x** | 🟡 Email + Push / Cupom 5% Condicionado |
| `#7732` | **BAIXO** | R$ 210,00 | 31% | R$ 0,02 (Push) | **0,4x** | ⚪ Push Transacional / Não Incentivar Desconto |
| `#5519` | **CRÍTICO** | R$ 25,00 | 90% | R$ 0,30 (WhatsApp) | **< 0,1x** | 🔴 Automação Zero Cost (Email) / Sem Disparo Manual |

---

## 🎯 Matriz Estratégica: Risk $\times$ Expected ROI

```text
Expected ROI
    ↑
    │
4.0x│                  🟢 QUADRANTE 1: PRIORIDADE MÁXIMA
    │                  (Alto Risco + Alto Expected ROI)
    │                  -> Ação: WhatsApp VIP / Suporte Humano
    │
2.0x│         🟡 QUADRANTE 2: AVALIAR / AUTOMAÇÃO
    │         (Risco Médio + Ticket Intermediário)
    │         -> Ação: Email Inbound + Push Notification
    │
1.0x├─────────────────────────────────────────────────────── (Linha de Breakeven)
    │
0.0x│ 🔴 QUADRANTE 3: NÃO INTERVIR COM INCENTIVO
    │ (Alto Risco + Baixo Ticket OU Baixo Risco Orgânico)
    │ -> Ação: Automação Leve / Preservar Margem
    └──────────────────────────────────────────────────────────→
     BAIXO           MÉDIO           ALTO           CRÍTICO    (Risco de Abandono)
```

### Por que Alto Risco $\neq$ Automaticamente Alta Prioridade?

1. **Cenário de Ineficiência / Prejuízo (Evitado pela Matriz)**:
   - Carrinho com `Risco = 90%`, `Valor = R$ 20,00`, `Custo de Intervenção + Desconto = R$ 6,00`.
   - Como a margem bruta de R$ 20 é ~R$ 7, gastar R$ 6 para tentar recuperar um carrinho de baixíssimo ticket gera margem líquida residual nula ou prejuízo operacional.
2. **Cenário de Alta Oportunidade**:
   - Carrinho com `Risco = 55%` (Médio/Alto), `Valor = R$ 2.000,00`, `Custo do Canal = R$ 0,30`.
   - O ganho esperado absoluto é gigantesco, tornando este carrinho a **prioridade absoluta de resgate**, mesmo não sendo o de maior score de risco.

---

## 📍 Mapeamento dos Dados na Dadosfera

- **Tipo**: Pipeline Analítico / View / Data App de Monitoramento em Tempo Real (Metabase & Streamlit).
- **Camada Lakehouse**: `Silver (Qualify)` $\rightarrow$ `Gold (Curated Kimball)`.
- **Tabelas e Visões Envolvidas**:
  - `carrinhos.parquet` (`carrinho_id`, `cliente_id`, `valor_total`, `valor_frete`, `dispositivo`, `cliente_novo`, `status`)
  - `clientes.parquet` (`cliente_id`, `segmento_rfm`, `lifetime_value`)
  - `eventos_carrinho.parquet` (`carrinho_id`, `tipo_evento`, `data_evento`)
  - `eventos_resgate.parquet` (`carrinho_id`, `canal`, `custo_envio`, `sucesso`, `valor_pedido_final`)
  - `pedidos.parquet` (`carrinho_id`, `origem_recuperacao`, `valor_total`)

---

## ✅ Como Validar (Definition of Done)

1. **Consistência do Score**: `RISK_SCORE` contido estritamente no intervalo [4, 11].
2. **Separação de Métricas**: Nenhuma hipótese de inatividade é apresentada como dado histórico sem validação temporal sobre `eventos_carrinho`.
3. **Reconciliação Financeira**: A soma de valor em risco por nível reconcilia com o valor total represado da Entidade Exemplo (~R$ 1.945k semestral).
4. **Viabilidade Econômica**: Nenhuma recomendação de disparo via canal pago (WhatsApp R$ 0,30) pode ter Expected ROI inferior a 1,0x.

---

## 💰 Análise de Risco de Prejuízo (O que precisaria acontecer para gerar prejuízo?)

Para que a operação de recuperação de carrinhos resulte em prejuízo financeiro para o e-commerce, uma das seguintes falhas operacionais teria que ocorrer:

1. **Canibalização de Margem em Clientes Orgânicos (Baixo Risco / Premium)**:
   - Oferecer cupons de desconto agressivos (ex: 10% a 15%) para clientes fiéis que retornariam e comprariam pelo preço cheio.
   - *Solução Dadosfera*: Regra de **Desconto Zero** para o segmento Premium (substituído por suporte técnico e reserva de estoque).
2. **Custo de Canal Superior à Margem do Pedido (Disparo Cego em Baixo Ticket)**:
   - Disparar WhatsApp (R$ 0,30) ou SMS (R$ 0,15) para milhares de carrinhos de R$ 15 a R$ 30 com cupons de frete grátis.
   - *Solução Dadosfera*: Triagem de Viabilidade Líquida no Dashboard 3 (carrinhos < R$ 100 recebem apenas Email ou Push de custo marginal zero).
3. **Fadiga de Canal e Descadastros (Spamming)**:
   - Disparar 4 a 5 mensagens em menos de 12 horas, gerando bloqueios de WhatsApp e perda do LTV do cliente.
   - *Solução Dadosfera*: Cadência com espaçamento ótimo (+1h, +24h, +48h) com limite máximo de 3 toques.