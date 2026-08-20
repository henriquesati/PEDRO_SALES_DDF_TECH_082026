# Motivos de Abandono de Carrinho (Categorização)

## ❓ Pergunta de Negócio
Qual razão de abandono causa a maior perda de receita na plataforma e como esses motivos se distribuem entre diferentes faixas de valor de carrinho, tipos de dispositivo e segmentos de clientes (RFM)?

---

## 📊 Métrica

- **KPI Primário**: Distribuição Percentual de Motivos de Abandono (`% do total de abandonos`)
- **KPIs Secundários**:
  - Volume de Carrinhos Abandonados por Motivo (`unidades`)
  - Receita Total Represada por Motivo (`R$`)
  - Ticket Médio Abandonado por Motivo (`R$ / carrinho`)
  - Taxa de Abandono por Pagamento no Mobile vs Desktop (`%`)
- **Fórmula**:
  - `Distribuição do Motivo (%)` = (Total de carrinhos abandonados pelo Motivo $X$ / Total de carrinhos com status 'abandonado') * 100
  - `Receita Represada por Motivo (R$)` = Soma de `valor_total` dos carrinhos abandonados agrupados por `motivo_abandono`
  - `Ticket Médio por Motivo (R$)` = Receita Represada pelo Motivo $X$ / Volume de Carrinhos do Motivo $X$
- **Granularidade**: Semanal, Mensal, por Motivo de Abandono, por Segmento RFM
- **Dimensões**:
  - `Motivo de Abandono`: `motivo_abandono` (`preco`, `frete`, `indecisao`, `pagamento`, `estoque`, `nao_informado`).
  - `Segmento RFM`: `clientes.segmento_rfm` (`premium`, `regular`, `dormant`, `novo`).
  - `Dispositivo`: `dispositivo` (`mobile`, `desktop`, `tablet`).
  - `Faixa de Valor do Carrinho`: Ticket Baixo (< R$ 100), Médio (R$ 100–250), Alto (> R$ 250).
- **Alvo (Benchmark)**:
  - Benchmark de E-commerce: Custos adicionais/frete representam ~48% dos motivos declarados; problemas de processo/pagamento representam ~15-20%.
  - Alvo: Mapear 100% dos motivos inferidos e direcionar estratégias de resgate e UX específicas para cada causa-raiz.

  <!-- granularidade por dispositivo em staging pra evitar poluição-->

---

## 💡 Insight Esperado

- **Distribuição de Motivos**:
  - **Preço Alto (~40%)**: Principal gerador de volume e perda de receita absoluta, concentrado em tickets médios e altos.
  - **Frete Caro (~30%)**: Impacta desproporcionalmente carrinhos de **ticket baixo (< R$ 100)**, onde o custo do frete ultrapassa 15-20% do subtotal.
  - **Indecisão (~20%)**: Comportamento típico de navegação comparativa, mais comum em sessões com visualização única de checkout e sem início de pagamento.
  - **Problema no Pagamento (~10%)**: Concentrado no **dispositivo mobile**, onde atritos de digitação, falhas no gateway ou lentidão no preenchimento de cartão geram cancelamentos imediatos.
- **Cruzamento com Segmento de Clientes**:
  - *Clientes Premium*: Raramente abandonam por preço ou frete; abandonos concentram-se em indecisão ou indisponibilidade de estoque.
  - *Clientes Novos & Dormant*: Altamente sensíveis a preço e custo de entrega, demandando incentivo financeiro para converter.

---

## 📍 Dadosfera Config

- **Tipo**: Exploração & Dashboard
- **Camada**: Analytics (Tabelas Enriquecidas / View `vw_abandono_analise`)
- **Dados necessários**:
  - `carrinhos`
  - `clientes`
  - `eventos_carrinho` (para inferência e validação do motivo)
- **Campos necessários**:
  - `carrinhos.carrinho_id`
  - `carrinhos.status`
  - `carrinhos.motivo_abandono`
  - `carrinhos.valor_subtotal`
  - `carrinhos.valor_frete`
  - `carrinhos.valor_total`
  - `carrinhos.dispositivo`
  - `carrinhos.data_abandono`
  - `clientes.cliente_id`
  - `clientes.segmento_rfm`
- **Relacionamentos**:
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)

### Passos de Transformação
1. **Filtro de Escopo**: Selecionar registros onde `carrinhos.status IN ('abandonado', 'recuperado', 'expirado')` e `data_abandono IS NOT NULL`.
2. **Classificação de Faixas de Ticket**: Categorizar `valor_total` em faixas (Baixo, Médio, Alto) para cruzar com `motivo_abandono`.
3. **Agregações Multidimensionais**:
   - Agrupar por `motivo_abandono`, `segmento_rfm` e `dispositivo`.
   - Calcular contagem de carrinhos, soma do `valor_total` e média do `valor_frete`.
4. **Visualização**:
   - Gráfico de Rosca/Donut com a distribuição percentual dos motivos de abandono.
   - Gráfico de Barras Empilhadas: Motivos de Abandono por Segmento RFM e por Dispositivo.
   - Grafico de Impacto Financeiro: 1 linha mostrando total de carrinhos, 1 mostrando carrinhos perdidos e outra mostrando os recuperados 
   - Gráfico auxiliar de impacto financeiro complementando o gráfico anterior mostrandoPerda Total em R$, valor recuperado

---

## ✅ Como Validar

- **Domínio de Valores**: O campo `motivo_abandono` deve conter apenas valores válidos do enum do negócio (`preco`, `frete`, `pagamento`, `indecisao`, `estoque`, `nao_informado`).
- **Completude**: A soma dos percentuais de todos os motivos deve totalizar exatamente **100%**.
- **Coerência da Regra de Frete**: Carrinhos classificados com motivo `'frete'` devem apresentar `valor_frete > 15% do valor_subtotal` ou evento explícito de cálculo de frete sem avanço.
- **Coerência de Pagamento**: Carrinhos com motivo `'pagamento'` devem possuir evento prévio de `'erro_pagamento'` ou abandono na etapa de checkout.
- **Reconciliação de Receita**: A soma do `valor_total` de todos os motivos deve ser idêntica ao montante total de carrinhos abandonados da análise de volume.

---

## 🎯 Recomendação Acionável

1. **Estratégia Diferenciada no Motor de Resgate**:
   - **Abandono por Frete**: Disparar comunicação com oferta de **Frete Grátis** (ou desconto equivalente ao frete) em vez de cupom percentual.
   - **Abandono por Preço**: Acionar sequência de desconto progressivo (5% no 3º toque, 10% no 4º toque).
   - **Abandono por Pagamento**: Enviar link direto de recuperação com opção facilitada de **PIX com aprovação instantânea** ou troca de método.
   - **Abandono por Indecisão**: Comunicação baseada em *Social Proof* (avaliações 5 estrelas, "Mais de X clientes compraram este item") sem erosão de margem com descontos.
2. **Ações Corretivas no Produto / UX**:
   - Otimizar o fluxo de pagamento mobile (One-Click checkout, teclado numérico nativo para cartão, PIX Copia e Cola em 1 toque).
   - Criar régua de frete grátis dinâmica ("Faltam R$ X para frete grátis") para reduzir desistências de ticket baixo.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - Abandono por **Preço (40%)** e **Frete (30%)** respondem por **~70% da perda total**.
  - Tratar especificamente a dor do frete com cupom de entrega recupera até **12-15% dos carrinhos de frete**, com custo marginal coberto pela margem do produto.
  - Reduzir o atrito de pagamento mobile (recuperando 1 em cada 5 falhas de pagamento) gera conversão imediata de carrinhos com alta intenção de compra, sem concessão de desconto, maximizando a margem líquida.
