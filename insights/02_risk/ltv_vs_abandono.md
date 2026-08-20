# Análise de Lifetime Value (LTV) vs Abandono de Carrinho

## ❓ Pergunta de Negócio
Como o valor histórico do cliente (LTV) e o ticket do carrinho determinam o orçamento e o canal de resgate economicamente viável? Qual o retorno sobre o custo de comunicação ao alocar canais de alto impacto (WhatsApp a R$ 0,30) para clientes Premium (ticket R$ 800) versus canais de custo mínimo (Email a R$ 0,05) para clientes Novos (ticket R$ 120)?

---

## 📊 Métrica

- **KPI Primário**: Valor Financeiro em Risco por Segmento de LTV (`R$ em Risco`)
- **KPIs Secundários**:
  - Taxa de Abandono por Faixa de LTV (`%`)
  - Ticket Médio do Carrinho por Segmento de LTV (`R$ / carrinho`)
  - ROI de Resgate por Segmento (`Múltiplo: Receita Líquida / Custo de Envio`)
  - Custo de Resgate sobre o Valor do Pedido (`%`)
- **Fórmula**:
  - `Valor em Risco (R$)` = Soma de `carrinhos.valor_total` dos carrinhos abandonados no período para cada faixa de LTV
  - `Taxa de Abandono por Segmento (%)` = (Carrinhos abandonados no segmento / Total de carrinhos criados no segmento) * 100
  - `Ticket Médio no Segmento (R$)` = Valor Total Abandonado no Segmento / Total de Carrinhos Abandonados no Segmento
  - `ROI por Segmento` = `(Receita Recuperada - Descontos Concedidos - Custo de Disparos) / Custo de Disparos`
- **Granularidade**: Mensal, por Segmento de LTV/RFM e por Canal de Resgate Utilizado.
- **Dimensões**:
  - `Segmento de LTV / RFM`:
    - **Premium**: LTV > R$ 2.000 (ou R$ 5.000 em bases de alto valor) | 5+ compras.
    - **Regular**: LTV R$ 500 a R$ 2.000 | 2–4 compras.
    - **Dormant**: LTV < R$ 500 | Inativo > 90 dias.
    - **Novo**: LTV R$ 0 | Primeira sessão/compra.
  - `Canal de Resgate`: `email`, `sms`, `push_app`, `whatsapp`.
  - `Status de Conversão`: `recuperado`, `comprado`, `expirado`.
- **Alvo (Benchmark)**:
  - Recuperar $\ge 18\%$ dos carrinhos abandonados de clientes Premium.
  - Manter o custo total de comunicação abaixo de 1% do valor recuperado em todos os segmentos.

---

## 💡 Insight Esperado

- **Segmento Premium (Alto LTV / Fidelidade Consolidada)**:
  - **Taxa de Abandono**: Baixa (~35%), pois já conhecem e confiam na marca.
  - **Ticket Médio**: Alto (~R$ 800).
  - **Valor em Risco Total**: Concentração desproporcional do faturamento em risco.
  - **Sensibilidade Econômica**: Resgate com altíssimo ROI. Justifica o uso imediato de canais de custo unitário maior (WhatsApp a R$ 0,30), pois o custo representa apenas **0,037%** do valor do carrinho. Não necessita de desconto para converter.
- **Segmento Regular (LTV Intermediário)**:
  - **Taxa de Abandono**: Moderada (~70%).
  - **Ticket Médio**: Médio (~R$ 150).
  - **Valor em Risco Total**: Base de maior volume unitário de pedidos da operação.
  - **Sensibilidade Econômica**: Estratégia mista (Email + Push no 1º e 2º toques; cupom moderado de 5-10% apenas se necessário no 3º toque).
- **Segmento Novo (LTV Zero / Primeira Compra)**:
  - **Taxa de Abandono**: Elevada (~85%), devido à desconfiança, comparação de frete e ausência de histórico.
  - **Ticket Médio**: Baixo (~R$ 120).
  - **Sensibilidade Econômica**: Canais caros geram risco de margem negativa se a taxa de conversão for baixa. Devem receber Email (R$ 0,05) ou Push (R$ 0,02), combinados com cupom de primeira compra (10%) justificado pelo potencial de *LTV futuro* e não apenas pelo lucro do 1º pedido.

---

## 📍 Dadosfera Config

- **Tipo**: Exploração, View Analítica e Dashboard Executivo
- **Camada**: Analytics (Tabelas Enriquecidas / Views)
- **Dados necessários**:
  - `clientes`
  - `carrinhos`
  - `eventos_resgate`
  - `pedidos`
- **Campos necessários**:
  - `clientes.cliente_id`, `clientes.segmento_rfm`, `clientes.lifetime_value`, `clientes.total_compras`
  - `carrinhos.carrinho_id`, `carrinhos.status`, `carrinhos.valor_total`, `carrinhos.data_abandono`
  - `eventos_resgate.canal`, `eventos_resgate.custo_envio`, `eventos_resgate.sucesso`, `eventos_resgate.valor_pedido_final`
- **Relacionamentos**:
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)
  - `eventos_resgate.carrinho_id` $\rightarrow$ `carrinhos.carrinho_id` (N:1)

### Passos de Transformação
1. **Junção e Enriquecimento**: Associar cada carrinho abandonado aos dados históricos do cliente (`lifetime_value` e `segmento_rfm`).
2. **Agrupamento por Faixa de LTV**:
   - Totalizar carrinhos criados vs abandonados por faixa de LTV.
   - Calcular taxa de abandono, ticket médio e montante acumulado em risco.
3. **Cruzamento de Custos e Retorno de Campanha**:
   - Somar os custos de envio (`custo_envio`) e receitas de conversão (`valor_pedido_final`) por segmento RFM.
   - Calcular ROI unitário e ROI agregado.
4. **Visualização**:
   - Gráfico de Bolhas: Eixo X (Taxa de Abandono), Eixo Y (Ticket Médio), Tamanho da Bolha (Valor Total em Risco).
   - Tabela de Decisão Financeira: Comparativo de ROI por Canal vs Segmento de LTV.

---

## ✅ Como Validar

- **Consistência de LTV**: O `lifetime_value` do cliente deve ser igual à soma histórica de `pedidos.valor_total` confirmados anteriores.
- **Validação de Margem Unitária**: Em nenhum cenário o `custo_envio + desconto_concedido` pode superar a margem bruta estimada do pedido recuperado.
- **Coerência da Taxa de Abandono**: `Taxa_Abandono(Novos) > Taxa_Abandono(Regulares) > Taxa_Abandono(Premium)`.
- **Reconciliação de Valores em Risco**: A soma do valor em risco de todas as faixas de LTV deve fechar exatamente com o valor total de carrinhos abandonados da plataforma.

---

## 🎯 Recomendação Acionável

1. **Priorização e Matriz de Canais por LTV**:
   - **Clientes Premium**: Disparo imediato via **WhatsApp (R$ 0,30)** com atendimento consultivo ("Olá, notamos que você não concluiu seu pedido. Precisa de ajuda?"). **Proibido conceder desconto no 1º contato**.
   - **Clientes Regulares**: Disparo automático via **Email (R$ 0,05)** e **Push (R$ 0,02)** no D+0 e D+1. Desconto condicionado apenas a carrinhos acima de R$ 200 no 3º toque.
   - **Clientes Novos**: Disparo via **Email (R$ 0,05)** destacando garantias, segurança do site e cupom exclusivo de primeira compra (`BEMVINDO10`).
2. **Cap de Custo por Segmento**:
   - Estabelecer teto de gasto de recuperação por carrinho de **no máximo 1% do ticket do carrinho** para clientes regulares e **até 3% para clientes novos** (encarado como Custo de Aquisição de Cliente - CAC).

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - No segmento **Premium**, recuperar 18% dos carrinhos de ticket R$ 800 com custo de R$ 0,30 gera um retorno bruto de **R$ 144,00 por real investido** (ROI ~480x).
  - No segmento **Novo**, recuperar 12% dos carrinhos de ticket R$ 120 via Email (R$ 0,05) gera **R$ 288,00 por real investido**, além de destravar o LTV futuro do cliente (que comprará novamente sem custo de mídia).
  - A segmentação inteligente evita queimar margem dando cupom para clientes Premium e evita queimar verba de WhatsApp em carrinhos de baixo valor sem intenção de compra.

---
---------sugestoes agent------

### 💡 Sugestões de Aprimoramento para o Pitch e Modelo:
1. **LTV Futuro como Métrica de Decisão**: Para clientes novos, o ROI não deve ser medido apenas pelo lucro do 1º carrinho recuperado, mas sim pelo *LTV projetado nos próximos 12 meses* (Payback do CAC de Resgate).
2. **Prevenção de Canibalização**: Adicionar uma regra de negócio que impede o disparo de cupons de desconto para clientes com `lifetime_value > R$ 2.000`, a menos que o motivo do abandono tenha sido explicitamente `'preco'` ou `'frete'`.
3. **Escalonamento Inteligente de Canais**: Se o cliente Premium não abrir o WhatsApp em 2 horas, acionar fallback automático para Email; se o cliente Novo abrir o Email e clicar, aí sim justificar um SMS de reforço.
