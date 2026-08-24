# Custo por Carrinho Recuperado (CAC de Resgate), ROI & Adjacências

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../presentation/pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)  
> **Artefato Visual Correspondente**: [`presentation/insights/01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png`](../../presentation/insights/01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png)

## ❓ Pergunta de Negócio
Qual é o custo efetivo por carrinho recuperado (CAC de Resgate) em cada canal de comunicação (Email, SMS, WhatsApp, Push) e qual o retorno sobre o investimento (ROI líquido) e margem residual gerados na esteira de recuperação da plataforma?

---

## 📊 Métrica

- **KPI Primário**: Custo por Carrinho Recuperado (`CAC de Resgate = Custo Total do Canal / Pedidos Convertidos`)
- **KPIs Secundários**:
  - Proporção do Custo de Resgate sobre o Ticket Médio (`CAC / Ticket Médio (%)`)
  - Volume Total de Disparos e Conversões Efetivas por Canal (`unidades`)
  - Receita Líquida Recuperada (`Receita Bruta - Descontos - Custos de Disparo`)
  - Múltiplo de Retorno sobre o Investimento (`ROI = Receita Líquida / Custos de Disparo`)
- **Fórmulas**:
  - `CAC de Resgate (R$)` = $\frac{\sum \text{custo\_envio}}{\sum \text{pedidos\_convertidos}}$
  - `Proporção Custo / Ticket (%)` = $\frac{\text{CAC de Resgate}}{\text{Ticket Médio Recuperado}} \times 100 \quad (\text{Alvo: } < 2,0\%)$
  - `ROI Multiplicador` = $\frac{\text{Receita Líquida}}{\text{Custo Total de Disparos}}$
- **Granularidade**: Semanal, Mensal, por Canal de Resgate (`email`, `push_app`, `sms`, `whatsapp`).
- **Dimensões**:
  - `Canal`: `eventos_resgate.canal`
  - `Tipo de Comunicação`: `eventos_resgate.tipo_comunicacao`
  - `Faixa de Valor do Carrinho`: Baixo (< R$ 100), Médio (R$ 100–250), Alto (> R$ 250)
- **Alvo (Benchmark)**:
  - Manter o custo de recuperação **abaixo de 1,5% do Ticket Médio**.
  - ROI líquido consolidado superior a **40x** (para cada R$ 1,00 investido em mensageria, retornar mais de R$ 40,00 líquidos).

---

## 💡 Insight Esperado & Distribuição Observada (Ground Truth)

> [!NOTE]
> **Foco do Projeto em Proporções (%) & Entidade Exemplo**: As métricas de eficiência são estruturadas em ratios relativos (CAC como % do Ticket Médio e Multiplicador de ROI). A *Entidade Exemplo de Baseline* (TM Geral ~R$ 375,00) exemplifica os ganhos absolutos em R$, permitindo ao cliente plugar sua própria estrutura de custos de mensageria e ticket médio.

- **Eficiência Observada por Canal (498 Carrinhos Recuperados / R$ 173,7k Resgatados)**:
  - **E-mail Transacional**: CAC de **R$ 1,02 / pedido** (apenas 0,27% do Ticket Médio) | ROI Multiplicador de **~40x a 80x** | Maior volume operacional (68% dos resgates).
  - **Push Notification**: CAC de **R$ 1,67 / pedido** (0,45% do Ticket Médio) | ROI Multiplicador de **~35x** | Canal ágil para engajamento no aplicativo.
  - **SMS Notificação**: CAC de **R$ 3,00 / pedido** (0,80% do Ticket Médio) | ROI Multiplicador de **~25x** | Recomendado para reforço qualificado de clientes com alta propensão.
  - **WhatsApp VIP**: CAC de **R$ 12,00 / pedido** (1,50% do Ticket Médio VIP) | ROI Multiplicador de **~18x a 25x** | Estratégia de alto impacto reservada para tickets > R$ 500 ou clientes Premium.
- **Consolidação Global**: Custo total de comunicação representou **menos de 1,2%** da receita resgatada, gerando mais de R$ 165k de margem líquida recuperada.

---

## 📍 Dadosfera Config

- **Tipo**: Exploração, View Analítica (`vw_performance_canais`) & Dashboard de ROI
- **Camada**: Analytics
- **Dados necessários**:
  - `eventos_resgate`
  - `pedidos`
  - `carrinhos`
- **Campos necessários**:
  - `eventos_resgate.canal`, `eventos_resgate.custo_envio`, `eventos_resgate.desconto_oferecido`, `eventos_resgate.sucesso`, `eventos_resgate.valor_pedido_final`
  - `pedidos.origem_recuperacao`, `pedidos.valor_total`, `carrinhos.valor_total`

### Passos de Transformação
1. **Agregação por Canal**: Somar total de envios, custo de disparos e pedidos convertidos (`origem_recuperacao = TRUE`).
2. **Cálculo de CAC e Margem**: Dividir o custo total pelo total de pedidos convertidos e calcular a receita líquida deduzindo cupons e custos de disparo.
3. **Visualizações Oficiais (Source of Truth)**:
   - **Painel Duplo Integrado**:
     - *Painel 1 (CAC de Resgate)*: Barras horizontais do custo por conversão em R$ e % sobre o Ticket Médio.
     - *Painel 2 (Retorno Líquido & ROI)*: Comparativo de Receita Líquida vs Custo Total com Múltiplo de ROI destacado.
   - **Artefato Gerado**: [`chart_03_custo_recuperacao_roi.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/01_descriptive/03_custo_recuperacao_roi/chart_03_custo_recuperacao_roi.png).

---

## ✅ Como Validar

- **Reconciliação de Custos**: O custo total de envio deve bater exatamente com `COUNT(*) * custo_unitario_do_canal`.
- **Integridade de Conversões**: Apenas eventos com `sucesso = TRUE` ou pedidos com `origem_recuperacao = TRUE` devem computar receita recuperada.
- **Margem Positiva**: Todos os canais ativos na esteira devem apresentar margem líquida positiva e CAC inferior a 3% do Ticket Médio da categoria.

---

## 🎯 Recomendação Acionável

1. **Email como Base Operacional**: Manter 70% a 80% da volumetria em campanhas de email automatizadas pelo custo marginal desprezível (R$ 0,05).
2. **WhatsApp Focado em Alto Ticket**: Utilizar WhatsApp para 1º toque exclusivamente em carrinhos com valor > R$ 500 ou clientes com score de risco crítico e histórico de compra prévia.
3. **Automação de Alerta de ROI**: Configurar alerta na plataforma caso o CAC de resgate de qualquer canal ultrapasse 2% do Ticket Médio da semana.
