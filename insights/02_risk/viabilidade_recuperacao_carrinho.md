# Viabilidade de Recuperação por Carrinho (Score de Recuperabilidade)

## ❓ Pergunta de Negócio
Dado um carrinho abandonado, qual é a sua probabilidade de ser recuperado, qual o custo estimado da campanha e qual o retorno esperado? Quais carrinhos justificam investimento ativo de resgate e quais devem ser deixados para retorno orgânico?

---

## 📊 Métrica

- **KPI Primário**: Score de Viabilidade de Recuperação por Carrinho (`RECOVERY_VIABILITY`)
- **KPIs Secundários**:
  - Probabilidade Estimada de Recuperação (`%`)
  - Custo Estimado da Campanha de Resgate (`R$`)
  - Retorno Esperado (`R$ = Probabilidade × Valor do Carrinho`)
  - ROI Esperado Unitário (`Retorno Esperado / Custo Estimado`)
  - Distribuição de Carrinhos por Faixa de Viabilidade (`%`)

- **Fórmula**:
  - **Etapa 1 — Probabilidade Base de Recuperação (`P_BASE`)**:
    - Definida pelo segmento RFM do cliente (dados empíricos do dataset):
      - `premium` → 18%
      - `novo` → 12%
      - `regular` → 10%
      - `dormant` → 6%

  - **Etapa 2 — Ajuste por Motivo de Abandono (`FATOR_MOTIVO`)**:
    - Multiplicador sobre a probabilidade base conforme o motivo:
      - `indecisao` → ×1.2 (mais recuperável — sem barreira objetiva)
      - `preco` → ×1.0 (neutro — depende de desconto)
      - `frete` → ×1.1 (recuperável com oferta de frete grátis)
      - `pagamento` → ×0.8 (barreira técnica — menor chance)
      - `estoque` → ×0.3 (baixíssima — produto indisponível)
      - `nao_informado` → ×0.9 (incerteza penaliza levemente)

  - **Etapa 3 — Ajuste por Valor do Carrinho (`FATOR_VALOR`)**:
    - Carrinhos de maior valor tendem a receber mais atenção do cliente:
      - `valor_total > R$ 500` → ×1.1
      - `R$ 100 ≤ valor_total ≤ R$ 500` → ×1.0
      - `valor_total < R$ 100` → ×0.9

  - **Etapa 4 — Ajuste por Tempo desde Abandono (`FATOR_TEMPO`)**:
    - Decay temporal (quanto mais antigo, menor a chance):
      - `< 6 horas` → ×1.2
      - `6h a 24h` → ×1.0
      - `24h a 48h` → ×0.8
      - `48h a 72h` → ×0.6
      - `> 72h` → ×0.3

  - **Probabilidade Final**:
    ```
    P_RECUPERACAO = P_BASE × FATOR_MOTIVO × FATOR_VALOR × FATOR_TEMPO
    ```
    - Capped entre 1% e 50% (limites realistas)

  - **Etapa 5 — Custo Estimado (`CUSTO_EST`)**:
    - Baseado no canal ótimo prescrito pela matriz de resgate (seção 3.1 do business-rules.md):
      - Premium → WhatsApp (R$ 0,30) + até 2 reforços Email (R$ 0,05) = ~R$ 0,40
      - Regular → Email (R$ 0,05) + Push (R$ 0,02) = ~R$ 0,07
      - Dormant → Email (R$ 0,05) + SMS (R$ 0,15) = ~R$ 0,20
      - Novo → Email (R$ 0,05) + Push (R$ 0,02) = ~R$ 0,07
    - Acrescentar custo do incentivo quando aplicável:
      - Desconto: `valor_total × %_desconto_prescrito`
      - Frete grátis: `valor_frete` (quando oferecido)

  - **Etapa 6 — Retorno Esperado e ROI**:
    ```
    RETORNO_ESPERADO = P_RECUPERACAO × valor_total
    ROI_ESPERADO = RETORNO_ESPERADO / CUSTO_EST
    ```

  - **Classificação de Viabilidade (`RECOVERY_VIABILITY`)**:
    - `🟢 ALTA`: `ROI_ESPERADO ≥ 50x` **E** `RETORNO_ESPERADO ≥ R$ 10,00`
    - `🟡 MÉDIA`: `ROI_ESPERADO ≥ 10x` **E** `RETORNO_ESPERADO ≥ R$ 2,00`
    - `🔴 BAIXA`: `ROI_ESPERADO < 10x` **OU** `RETORNO_ESPERADO < R$ 2,00`

- **Granularidade**: Nível de Carrinho individual (com agregações por Segmento RFM, Motivo, Faixa de Valor).
- **Dimensões**:
  - `Segmento RFM`: `clientes.segmento_rfm`
  - `Motivo de Abandono`: `carrinhos.motivo_abandono`
  - `Faixa de Valor`: `< R$ 100`, `R$ 100–500`, `> R$ 500`
  - `Tempo desde Abandono`: `< 6h`, `6-24h`, `24-48h`, `48-72h`, `> 72h`
  - `Viabilidade`: `ALTA`, `MÉDIA`, `BAIXA`
- **Alvo (Benchmark)**:
  - Concentrar 80% do orçamento de resgate nos carrinhos com viabilidade ALTA.
  - ROI global da operação ≥ 30x ao usar a priorização por viabilidade.

---

## 💡 Insight Esperado

### Distribuição de Viabilidade Esperada

| Viabilidade | % dos Carrinhos Abandonados | Perfil Típico |
|---|---|---|
| 🟢 **ALTA** (~20%) | Carrinhos de alto valor + Cliente Premium/Regular + Abandono recente (< 24h) + Motivo tratável (indecisão, frete) | ROI esperado > 50x |
| 🟡 **MÉDIA** (~45%) | Carrinhos de valor médio + Cliente Regular/Novo + 24-48h pós-abandono | ROI esperado 10-50x |
| 🔴 **BAIXA** (~35%) | Carrinhos de baixo valor + Cliente Dormant + > 48h + Motivo estoque/pagamento | ROI esperado < 10x |

### Padrões Esperados

- **Segmento Premium + Indecisão + < 6h**: Probabilidade de ~26% (18% × 1.2 × 1.2), ROI astronômico (> 200x) pois não precisa de desconto.
- **Segmento Dormant + Estoque + > 72h**: Probabilidade de ~0.5% (6% × 0.3 × 0.3), ROI negativo se investir em canais caros. **Não resgatável ativamente.**
- **Segmento Novo + Frete + 6-24h**: Probabilidade de ~13% (12% × 1.1 × 1.0), ROI positivo com Email (R$ 0,05), mas negativo se usar WhatsApp + frete grátis em carrinho de R$ 45.

### Insight Central para o Pitch

> A priorização por viabilidade permite que a Dadosfera **aloque 80% do orçamento nos 20% de carrinhos com maior retorno**, em vez de disparar campanhas genéricas para todos. O resultado: **mesmo volume de investimento, 3x mais receita recuperada**.

---

## 📍 Dadosfera Config

- **Tipo**: View Analítica (`vw_viabilidade_recuperacao`) / Data App / Dashboard Operacional
- **Camada**: Enriched → Analytics → Prescriptive
- **Dados necessários**:
  - `carrinhos`
  - `clientes`
  - `eventos_resgate` (para custo e canal histórico)
  - `pedidos` (para validação ex-post)
- **Campos necessários**:
  - `carrinhos.carrinho_id`, `carrinhos.cliente_id`, `carrinhos.valor_total`, `carrinhos.valor_frete`, `carrinhos.motivo_abandono`, `carrinhos.status`, `carrinhos.data_abandono`
  - `clientes.cliente_id`, `clientes.segmento_rfm`, `clientes.lifetime_value`
  - `eventos_resgate.carrinho_id`, `eventos_resgate.canal`, `eventos_resgate.custo_envio`, `eventos_resgate.desconto_oferecido`, `eventos_resgate.frete_gratis_oferecido`, `eventos_resgate.sucesso`
- **Relacionamentos**:
  - `carrinhos.cliente_id` → `clientes.cliente_id` (N:1)
  - `eventos_resgate.carrinho_id` → `carrinhos.carrinho_id` (N:1)

### Passos de Transformação
1. **Enriquecimento do Carrinho**: Juntar carrinho + cliente para obter `segmento_rfm`, `lifetime_value`.
2. **Cálculo da Probabilidade Base**: Mapear `segmento_rfm` para `P_BASE` conforme tabela definida.
3. **Aplicação dos Fatores de Ajuste**: Multiplicar sequencialmente por `FATOR_MOTIVO`, `FATOR_VALOR` e `FATOR_TEMPO`.
4. **Estimativa de Custo**: Atribuir o canal ótimo e calcular custo total (comunicação + incentivo).
5. **Cálculo de Retorno e ROI Esperado**: Aplicar `P_RECUPERACAO × valor_total` e dividir pelo custo.
6. **Classificação de Viabilidade**: Aplicar as regras de corte (ALTA / MÉDIA / BAIXA).
7. **Visualização**:
   - **Tabela Operacional (Fila de Prioridade)**: Lista de carrinhos abandonados rankeados por ROI esperado, com ação prescrita (canal, timing, incentivo).
   - **Scatter Plot**: Eixo X = Probabilidade de Recuperação, Eixo Y = Valor do Carrinho, Cor = Viabilidade, Tamanho = ROI Esperado.
   - **Gauge / Big Numbers**: Total de carrinhos ALTA viabilidade hoje, R$ retorno esperado total, ROI médio esperado.
   - **Treemap**: Distribuição de viabilidade por Segmento RFM × Motivo de Abandono.

---

## ✅ Como Validar

- **Cap de Probabilidade**: `P_RECUPERACAO` deve estar estritamente entre 1% e 50% para todo carrinho.
- **Consistência de Fatores**: Cada fator multiplicador deve ser > 0. Nenhum produto de fatores pode gerar probabilidade negativa.
- **Validação Ex-Post (Backtesting)**: Comparar a viabilidade classificada com o resultado real (`eventos_resgate.sucesso`):
  - Carrinhos classificados como ALTA viabilidade devem ter taxa de recuperação empírica significativamente superior aos de BAIXA (ex: ≥ 3x).
- **Consistência de Custo**: `CUSTO_EST` nunca pode ser R$ 0 (há pelo menos 1 comunicação). Custo total do incentivo (desconto + frete grátis) não pode superar o valor do carrinho.
- **Reconciliação de ROI**: O ROI agregado da operação (soma de retornos / soma de custos) deve ser coerente com o ROI global de ~45x reportado no METRICS.md.
- **Integridade Referencial**: Todo `carrinho_id` deve corresponder a um `cliente_id` válido com `segmento_rfm` não nulo.

---

## 🎯 Recomendação Acionável

### Matriz de Ação por Viabilidade

| Viabilidade | Ação | Canal | Timing | Incentivo |
|---|---|---|---|---|
| 🟢 **ALTA** | Resgate imediato e prioritário | Canal premium do segmento (WhatsApp para Premium, Email para Regular) | Dentro de 1-4h | Conforme motivo: frete grátis se `frete`, sem desconto se `indecisão` |
| 🟡 **MÉDIA** | Resgate automatizado padrão | Email + Push | Régua padrão (1h → 24h → 48h) | Desconto condicional apenas no 3º toque |
| 🔴 **BAIXA** | **Não investir ativamente** | Nenhum disparo outbound | — | Reter na base para remarketing passivo (retargeting display) |

### Regra de Corte Financeiro

> **Não resgatável**: Se `RETORNO_ESPERADO < R$ 1,00` **OU** `ROI_ESPERADO < 5x`, o carrinho é marcado como `não resgatável ativamente`. A economia gerada por não disparar campanhas deficitárias é realocada para os carrinhos de ALTA viabilidade.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - **Sem priorização (baseline)**: Disparo de campanha genérica para 100% dos carrinhos abandonados. ROI diluído pela inclusão de carrinhos não recuperáveis, resultando em ~12x.
  - **Com priorização por viabilidade (Dadosfera)**: Concentrar 80% do orçamento nos 20% de carrinhos com viabilidade ALTA:
    - Eliminação de ~35% dos disparos deficitários (carrinhos BAIXA viabilidade).
    - Economia direta em custos de comunicação e incentivos desperdiçados.
    - ROI operacional sobe de **~12x (genérico) para ~35-45x (priorizado)**.
  - **Argumento de pitch**: _"Com a mesma verba de campanha, a Dadosfera recupera 3x mais receita ao priorizar os carrinhos certos — e evita queimar margem nos que não converteriam."_
