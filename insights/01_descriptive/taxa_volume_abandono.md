> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../presentation/pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)  
> **Artefato Visual Correspondente**: [`insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png`](../../insights/01_descriptive/01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png)

---

## ❓ Pergunta de Negócio
Qual é a magnitude do abandono de carrinhos na plataforma (em volume absoluto de sessões e percentual relativo ao total de carrinhos criados), qual o montante financeiro represado e como essa perda se distribui temporalmente, por canal de origem e por dispositivo?

---

## 📊 Métrica

- **KPI Primário**: Taxa de Abandono de Carrinho (`%`)
- **KPIs Secundários**:
  - Volume Total de Carrinhos Abandonados (`unidades`)
  - Valor Financeiro Represado em Abandono (`R$ Total Abandonado`)
  - Ticket Médio do Carrinho Abandonado (`R$ / carrinho`)
- **Fórmula**:
  - `Taxa de Abandono (%)` = (Total de carrinhos com status 'abandonado' / Total geral de carrinhos criados no período) * 100
  - `Valor Total Abandonado (R$)` = Soma de `valor_total` de todos os carrinhos com status 'abandonado'
  - `Ticket Médio Abandonado (R$)` = Valor Total Abandonado / Total de Carrinhos Abandonados
- **Granularidade**: Semanal, Mensal, por Canal de Aquisição e por Tipo de Dispositivo.
- **Dimensões**:
  - `Tempo`: `data_abandono` (Dia, Mês, Dia da Semana, Faixa Horária).
  - `Dispositivo`: `dispositivo` (Mobile, Desktop, Tablet).
  - `Canal de Origem`: `canal_origem` (Orgânico, Google Ads, Meta Ads, Email, Direto).
  - `Tipo de Cliente`: `cliente_novo` (Novo vs Recorrente).
- **Alvo (Benchmark)**:
  - Benchmark de mercado E-commerce (Baymard Institute): ~69.8% a 70%.
  - Alvo operacional: Reduzir taxa bruta de abandono para < 65% ou conter a perda recuperando ≥ 10% do volume abandonado.

---

## 💡 Insight Esperado
- **Volume & Taxa de Abandono**: Confirmado na faixa de **~70,0%** da base total de carrinhos criados (reconciliado com a série temporal observada no dataset).
- **Dispositivo (Mobile vs Desktop)**: Dispositivos móveis concentram a maior fatia do abandono (61% do volume total) em virtude de atrito em telas touch e preenchimento de formulários de checkout.
- **Comportamento Temporal**: Acompanhamento da curva de evolução acumulada evidenciando o lift gerado pelas réguas de recuperação Dadosfera (+498 pedidos convertidos).

---

## 📍 Dadosfera Config

- **Tipo**: Exploração & Dashboard
- **Camada**: Analytics (Consumo via Views / Tabelas Enriquecidas)
- **Dados necessários**:
  - `carrinhos`
  - `itens_carrinho` (opcional para detalhe de itens por abandono)
  - `clientes`
- **Campos necessários**:
  - `carrinhos.carrinho_id`
  - `carrinhos.cliente_id`
  - `carrinhos.status` (`'abandonado'`, `'recuperado'`, `'comprado'`, `'ativo'`, `'expirado'`)
  - `carrinhos.data_criacao`
  - `carrinhos.data_abandono`
  - `carrinhos.valor_subtotal`
  - `carrinhos.valor_frete`
  - `carrinhos.valor_desconto`
  - `carrinhos.valor_total`
  - `carrinhos.dispositivo`
  - `carrinhos.canal_origem`
  - `carrinhos.cliente_novo`
  - `clientes.segmento_rfm`
- **Relacionamentos**:
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)

### Passos de Transformação
1. **Filtragem e Limpeza**: Considerar carrinhos fechados ou com ciclo de vida estabelecido (`status IN ('abandonado', 'comprado', 'recuperado', 'expirado')`). Desconsiderar sessões ainda em andamento (`status = 'ativo'`) dentro da janela de tolerância de inatividade de 30 minutos.
2. **Agrupamento Temporal e Dimensional**: Agrupar por data de referência (`DATE(data_abandono)` ou `DATE(data_criacao)`), `dispositivo` e `canal_origem`.
3. **Cálculo de Agregações**:
   - `total_carrinhos = COUNT(carrinho_id)`
   - `total_abandonados = COUNT(CASE WHEN status = 'abandonado' THEN carrinho_id END)`
   - `taxa_abandono = (total_abandonados / total_carrinhos) * 100`
   - `montante_abandonado = SUM(CASE WHEN status = 'abandonado' THEN valor_total END)`
4. **Visualização**:
   - Gráfico de Linha temporal da Taxa de Abandono diária vs Benchmark (70%).
   - Cartões de KPI (Big Numbers): Taxa Global de Abandono (%), Volume Total Abandonado, R$ Total Represado.
   - Gráfico de Barras comparando Taxa de Abandono por Dispositivo e por Canal de Origem.

---

## ✅ Como Validar

- **Consistência de Status**: Todo carrinho com `status = 'abandonado'` deve possuir `data_abandono` não nula e `data_abandono >= data_criacao`.
- **Intervalo da Taxa**: A taxa calculada deve situar-se estritamente entre `0%` e `100%`.
- **Reconciliação Matemática**: `Total de Carrinhos = Abandonados + Comprados + Recuperados + Ativos + Expirados`.
- **Validação de Valor**: `valor_total` deve ser igual a `valor_subtotal + valor_frete - valor_desconto` para cada registro considerado.
- **Inatividade Regulatória**: Confirmar que carrinhos marcados como abandonados tiveram hiato mínimo de 30 minutos sem eventos na sessão.

---

## 🎯 Recomendação Acionável

1. **Gatilho Imediato para Motor de Resgate**: Alimentar a fila de campanhas de recuperação (`eventos_resgate`) com carrinhos que cruzaram a regra de abandono (+30min a +1h), priorizando clientes cadastrados e carrinhos de alto valor.
2. **Otimização de Checkout Mobile**: Caso o abandono mobile exceda 75%, priorizar melhorias de UX (One-Click Checkout, preenchimento automático, botão de pagamento via PIX visível acima da dobra).
3. **Transparência de Frete no Topo do Funil**: Para canais de mídia paga com alto abandono, exibir calculadora de frete ou aviso de frete grátis antes da adição ao carrinho, reduzindo a surpresa na etapa final.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - Seja $V_{abandono}$ o volume financeiro total represado em carrinhos abandonados (ex: ~R$ 600.000 a R$ 800.000 no período de 6 meses).
  - Uma recuperação de **10%** desse volume (taxa de conversão de resgate padrão de mercado) injeta diretamente **~R$ 60.000 a R$ 80.000 de receita recuperada**.
  - O custo estimado de comunicação (mix de Email a R$ 0,05, SMS a R$ 0,15 e WhatsApp a R$ 0,30) representa < 1% da receita recuperada, gerando um **ROI esperado de ~30x a 45x**.
