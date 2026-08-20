# ROI e Eficiência de Campanhas de Resgate por Canal

## ❓ Pergunta de Negócio
Qual canal de comunicação de resgate (Email, SMS, Push, WhatsApp) entrega o maior retorno financeiro sobre o investimento (ROI líquido) e como o orçamento de comunicação deve ser realocado para eliminar canais deficitários e maximizar a receita recuperada?

---

## 📊 Métrica

- **KPI Primário**: ROI por Canal de Resgate (`(Receita Líquida - Custo Total) / Custo Total`)
- **KPIs Secundários**:
  - Volume Total de Disparos por Canal (`unidades`)
  - Taxa de Conversão End-to-End por Canal (`%`)
  - Receita Total Gerada por Canal (`R$`)
  - Custo Total de Disparos por Canal (`R$`)
  - Custo Médio por Conversão Efetiva (`CAC de Resgate = Custo / Conversões`)
- **Fórmula**:
  - `Taxa de Conversão (%)` = (Total de Pedidos Convertidos pelo Canal / Total de Envios do Canal) * 100
  - `Custo Total do Canal (R$)` = Soma de `eventos_resgate.custo_envio` do canal
  - `Receita Total do Canal (R$)` = Soma de `eventos_resgate.valor_pedido_final` para envios com `sucesso = TRUE`
  - `ROI do Canal (%)` = `((Receita Total - Descontos Totais - Custo Total) / Custo Total) * 100`
- **Granularidade**: Semanal, Mensal, por Canal de Resgate (`email`, `sms`, `push_app`, `whatsapp`).
- **Dimensões**:
  - `Canal`: `eventos_resgate.canal`
  - `Tipo de Comunicação`: `eventos_resgate.tipo_comunicacao`
  - `Segmento do Cliente`: `clientes.segmento_rfm`
- **Alvo (Benchmark)**:
  - Manter ROI global de campanhas $\ge 30\text{x}$ (3.000%).
  - Eliminar 100% dos disparos em canais com ROI líquido unitário negativo.

---

## 💡 Insight Esperado

### 1. EMAIL — O Motor de Escala e Rentabilidade ✅
- **Volume**: Maior volume de envios (~24.500 disparos).
- **Conversão**: ~5% de conversão final (1.225 carrinhos recuperados).
- **Resultado Financeiro**: Receita de R$ 183.750 com custo unitário extremamente baixo (R$ 0,05).
- **Diagnóstico**: Canal mais resiliente, com menor custo por conversão e ROI consolidado altamente positivo.

### 2. SMS — Custo Unitário Elevado para Disparos Frios ❌
- **Volume**: ~7.000 envios.
- **Conversão**: ~5% (350 conversões).
- **Resultado Financeiro**: Receita de R$ 52.500 frente a um custo unitário intermediário/alto.
- **Diagnóstico**: Quando disparado de forma massiva e não qualificada, o custo cumulativo corrói o retorno, resultando em ROI comprimido ou negativo. Deve ser restrito a reforço de clientes com abertura prévia.

### 3. PUSH APP — Baixa Taxa de Entrega/Conversão em Massa ❌
- **Volume**: ~3.500 envios.
- **Conversão**: ~3% (105 conversões).
- **Resultado Financeiro**: Receita de R$ 15.750.
- **Diagnóstico**: Apresenta baixa conversão em usuários pouco engajados, gerando ROI deficitário quando atrelado a custos de manutenção de infraestrutura ou disparos redundantes.

---

## 📍 Dadosfera Config

- **Tipo**: View Analítica (`vw_performance_canais`), Dashboard de ROI e Relatório Executivo
- **Camada**: Analytics
- **Dados necessários**:
  - `eventos_resgate`
  - `pedidos`
  - `carrinhos`
- **Campos necessários**:
  - `eventos_resgate.canal`, `eventos_resgate.tipo_comunicacao`, `eventos_resgate.custo_envio`, `eventos_resgate.desconto_oferecido`, `eventos_resgate.sucesso`, `eventos_resgate.valor_pedido_final`
  - `carrinhos.valor_total`, `carrinhos.motivo_abandono`
- **Relacionamentos**:
  - `eventos_resgate.carrinho_id` $\rightarrow$ `carrinhos.carrinho_id` (N:1)

### Passos de Transformação
1. **Agregação por Canal**: Somar total de envios, aberturas, cliques e pedidos convertidos (`sucesso = TRUE`).
2. **Cálculo Financeiro Consolidado**: Calcular `custo_total`, `receita_total`, `desconto_total` e aplicar a fórmula de ROI.
3. **Classificação de Eficiência**: Rankear canais por ROI e Custo por Conversão.
4. **Visualização**:
   - Gráfico de Barras Duplas: Receita Gerada vs Custo por Canal.
   - Cartão de Indicador: ROI Comparativo por Canal (Email vs WhatsApp vs SMS vs Push).
   - Tabela de Performance de Funil (Envio $\rightarrow$ Abertura $\rightarrow$ Clique $\rightarrow$ Conversão).

---

## ✅ Como Validar

- **Reconciliação de Custos**: O custo total de envio deve bater exatamente com `COUNT(*) * custo_unitario_do_canal`.
- **Integridade de Conversões**: Apenas eventos com `sucesso = TRUE` devem somar receita em `valor_pedido_final`.
- **Coerência de ROI**: Canais onde o custo total supera a receita líquida devem obrigatoriamente exibir ROI negativo.

---

## 🎯 Recomendação Acionável

1. **Readequação da Matriz de Canais**:
   - **Canal Principal (Base)**: Concentrar **85% do volume operacional em Email**, canal com melhor equilíbrio de custo-benefício e alta capacidade de personalização.
   - **Descontinuação de Disparos Frios em SMS e Push**: Suspender envios massivos de SMS e Push para novos usuários ou carrinhos de baixo valor.
   - **Uso Seletivo de WhatsApp**: Reservar o canal WhatsApp exclusivamente para o 1º toque de clientes *Premium* ou carrinhos com valor > R$ 500.
2. **Otimização Contínua do Email (Meta 5% $\rightarrow$ 8%)**:
   - Testar variações de assunto com gatilhos de escassez e personalização com o nome do cliente.
   - Injetar fotos dos produtos abandonados e 1 avaliação real de 5 estrelas no corpo do email.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - Cortar disparos massivos em SMS/Push deficitários economiza despesas diretas imediatas de comunicação.
  - Realocar a verba economizada em testes de otimização de Email (elevando a conversão de 5% para 8%) projeta um acréscimo de **+R$ 110.000 em receita recuperada adicional**, maximizando o ROI global da operação para mais de **40x**.

---
---------sugestoes agent------

3. **Monitoramento de Custo Unitário Dinâmico**: Configurar alertas automáticos caso o custo por conversão de qualquer canal ultrapasse 5% do ticket médio recuperado.
