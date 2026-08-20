# Segmentação de Risco de Abandono (Score de Risco em Tempo de Sessão)

## ❓ Pergunta de Negócio
Podemos identificar carrinhos com alta probabilidade de abandono antes mesmo do encerramento da sessão? Qual é o perfil e o momento crítico ("ponto de não retorno") onde o risco atinge níveis críticos, exigindo intervenção proativa?

---

## 📊 Métrica

- **KPI Primário**: Índice de Distribuição de Risco de Abandono (`% de carrinhos por faixa de risco`)
- **KPIs Secundários**:
  - Volume de Carrinhos em Risco Crítico / Alto (`unidades`)
  - Volume Financeiro sob Risco Crítico (`R$ Represado`)
  - Taxa de Abandono Observada por Nível de Risco (`%`)

- **Fórmula**:
  - **Cálculo do Score de Risco (`RISK_SCORE`)**:
    - Pontuação ponderada somando os fatores de risco observados no carrinho e sessão:
      - `Valor do Carrinho`: Se `valor_total > R$ 500` soma **2**, senão soma **1**.
      - `Dispositivo`: Se `dispositivo = 'mobile'` soma **2**, senão soma **1**.
      - `Relacionamento`: Se `cliente_novo = TRUE` (ou sem histórico) soma **2**, senão soma **1**.
      - `Velocidade da Sessão`: Se `duracao_sessao_minutos < 5` soma **2**, senão soma **1**.
      - `Sinal de Fricção / Motivo Esperado`: Se detectado evento de erro de pagamento ou frete > 15% soma **3**, senão soma **0**.
  - **Classificação do Nível de Risco (`RISK_LEVEL`)**:
    - `CRÍTICO`: `RISK_SCORE >= 8`
    - `ALTO`: `RISK_SCORE >= 6` e `< 8`
    - `MÉDIO`: `RISK_SCORE >= 4` e `< 6`
    - `BAIXO`: `RISK_SCORE < 4`
- **Granularidade**: Nível de Carrinho (individual), com agregações Diária, Semanal e Mensal por Nível de Risco e Segmento RFM.
- **Dimensões**:
  - `Nível de Risco`: `RISK_LEVEL` (`CRÍTICO`, `ALTO`, `MÉDIO`, `BAIXO`).
  - `Segmento RFM`: `clientes.segmento_rfm` (`premium`, `regular`, `dormant`, `novo`).
  - `Dispositivo`: `carrinhos.dispositivo` (`mobile`, `desktop`, `tablet`).
  - `Faixa de Valor`: `< R$ 100`, `R$ 100–500`, `> R$ 500`.
- **Alvo (Benchmark)**:
  - Identificar precocemente 100% dos carrinhos de Alto e Crítico Risco ainda durante a sessão ativa ou nos primeiros 15 minutos pós-inatividade.

---

## 💡 Insight Esperado

- **Distribuição dos Níveis de Risco**:
  - **Alto / Crítico Risco (~15%)**: Perfil composto majoritariamente por **Clientes Novos + Dispositivo Mobile + Carrinho > R$ 500**. Alta sensibilidade a atrito e ausência de fidelidade prévia.
  - **Médio Risco (~35%)**: Perfil **Regular + Desktop + Carrinho R$ 100–500**. Clientes com histórico de compras, navegando em ambiente mais estável, mas sensíveis a frete ou promoções concorrentes.
  - **Baixo Risco (~50%)**: Perfil **Premium + Desktop + Carrinho < R$ 100**. Clientes fiéis com alta recorrência, onde o abandono geralmente decorre de interrupções momentâneas e possui taxa de retorno orgânico elevada.
- **O Ponto de Não Retorno**:
  - Sessões em mobile com carrinhos de valor elevado onde o usuário passa mais de **3 minutos parado na tela de checkout** sem digitar dados de pagamento têm probabilidade de abandono superior a **85%**.

---

## 📍 Dadosfera Config

- **Tipo**: Pipeline Analítico / View / Data App de Monitoramento em Tempo Real
- **Camada**: Enriched $\rightarrow$ Analytics
- **Dados necessários**:
  - `carrinhos`
  - `clientes`
  - `eventos_carrinho`
- **Campos necessários**:
  - `carrinhos.carrinho_id`
  - `carrinhos.cliente_id`
  - `carrinhos.valor_total`
  - `carrinhos.valor_frete`
  - `carrinhos.valor_subtotal`
  - `carrinhos.dispositivo`
  - `carrinhos.duracao_sessao_minutos`
  - `carrinhos.cliente_novo`
  - `carrinhos.status`
  - `clientes.segmento_rfm`
  - `eventos_carrinho.tipo_evento`
- **Relacionamentos**:
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)
  - `carrinhos.carrinho_id` $\rightarrow$ `eventos_carrinho.carrinho_id` (1:N)

### Passos de Transformação
1. **Enriquecimento dos Fatores de Risco**: Avaliar para cada carrinho ativo/recente os atributos de valor, canal, dispositivo, novidade do cliente e tempo de sessão.
2. **Cálculo Lógico do Score**: Aplicar a matriz de pesos e gerar os campos derivados `risk_score` e `risk_level`.
3. **Agregação e Triagem**:
   - Classificar o pipeline de prioridade de intervenção.
   - Cruzar risco calculado com a taxa real de conversão/abandono final.
4. **Visualização**:
   - Matriz de Calor (Heatmap): Nível de Risco vs Segmento RFM.
   - Gráfico de Pareto: Volume Financeiro Represado por Faixa de Risco.
   - Painel Operacional: Fila de carrinhos em risco Crítico para disparo prioritário.

---

## ✅ Como Validar

- **Escala do Score**: `RISK_SCORE` deve ser um número inteiro situado entre o valor mínimo possível (4) e o máximo (11).
- **Consistência de Classificação**: Garantir que nenhum carrinho com score $\ge 8$ seja classificado fora de `CRÍTICO`.
- **Validação Preditiva**: Comparar ex-post se os carrinhos classificados como `CRÍTICO` e `ALTO` apresentaram de fato taxa de abandono significativamente superior (ex: > 80%) aos classificados como `BAIXO` (< 35%).
- **Integridade de Chaves**: Todo registro de carrinho avaliado deve mapear para um cliente válido e manter consistência com `duracao_sessao_minutos >= 0`.

---

## 🎯 Recomendação Acionável

1. **Intervenção On-Site em Tempo Real (Antes do Abandono)**:
   - Para sessões ativas atingindo score **CRÍTICO** (ex: Cliente Novo + Mobile + > R$ 500 parado no checkout), acionar trigger de *Exit-Intent Modal* com cupom de primeira compra ou atendimento via chat/WhatsApp de suporte instantâneo.
2. **Priorização da Fila de Resgate Outbound (Pós-Abandono)**:
   - **Risco Crítico/Alto**: Disparo imediato (+15min a +1h) via canal de maior impacto (WhatsApp ou SMS) com oferta agressiva (Frete Grátis ou 10%).
   - **Risco Baixo/Médio**: Disparo espaçado (+4h a +24h) via Email com comunicação suave (lembrete sem desconto), preservando margem.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - Os 15% de carrinhos em **Alto/Crítico Risco** concentram tickets elevados (> R$ 500), respondendo por mais de **35% do valor financeiro total em risco**.
  - Evitar o abandono *in-session* ou recuperar precocemente 12% desses carrinhos críticos gera um incremento desproporcional de receita bruta.
  - Alocar incentivos financeiros (descontos/frete) **somente** nos níveis Alto e Crítico reduz em até **60% o custo de subsídio** que seria desperdiçado em clientes de Baixo Risco (que converteriam sem desconto).

---
---------sugestoes agent------

### 💡 Sugestões de Aprimoramento para o Pitch e Modelo:
1. **Regra de Inatividade vs On-Site Trigger**: Diferenciar claramente ações *in-session* (ex: pop-up após 3 min parado no checkout) de ações *outbound* (disparo de resgate após 30 min sem retorno).
2. **Flag de Sensibilidade a Frete no Score**: Como a codebase já possui a regra `valor_frete > 15% do subtotal` no `business-rules.md`, incorporar esse gatilho diretamente no termo de *sinal de fricção* do score eleva a precisão do modelo sem adicionar complexidade de Machine Learning.
3. **Preservação de Margem para Baixo Risco (Premium)**: Clientes do segmento *Premium* (Baixo Risco) não devem receber cupons na primeira abordagem de resgate para evitar habituação a descontos (*margin cannibalization*).


entender melhor essa skill
o que precisaria acontecer para isso resultar em prejuizo?