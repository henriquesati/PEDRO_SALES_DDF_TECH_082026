# Recomendação: Estratégia de Resgate por Segmento

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../presentation/pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)  
> **Artefato Visual Correspondente**: [`insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png`](../../insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png)

---

## ❓ Pergunta de Negócio
Qual é a política ótima de resgate (canal de comunicação e incentivo financeiro) para cada segmento de cliente que maximiza a receita recuperada líquida e impede o desperdício de margem com descontos desnecessários ou canais inviáveis?

---

## 📊 Métrica

- **KPI Primário**: Índice de Viabilidade Econômica Líquida por Resgate (`R$ / carrinho`).
- **KPIs Secundários**:
  - Ganho Líquido Esperado por Abordagem (`R$`).
  - Custo Efetivo de Resgate por Conversão (`CAC de Resgate`).
  - Expected ROI Prescritivo por Abordagem (`Multiplicador`).
- **Fórmula de Viabilidade Unitária**:
  $$\text{Viabilidade Líquida (R\$)} = (\text{Taxa de Conversão Esperada} \times \text{Valor do Carrinho} \times \text{Margem Operacional}) - (\text{Custo do Canal} + \text{Custo do Incentivo})$$
- **Onde**:
  - `Custo do Canal`: WhatsApp (R$ 0,30), SMS (R$ 0,15), Email (R$ 0,05), Push App (R$ 0,02).
  - `Margem Operacional`: 35% (Baseline de referência).
  - `Custo do Incentivo`: `(Valor do Carrinho * % Desconto) + Custo do Frete` (quando concedido).
- **Decisão Prescritiva**:
  - Se $\text{Viabilidade Líquida} > 0$ e $\text{Expected ROI} \ge 1.0\text{x}$ $\rightarrow$ **Aprovar Disparo Ativo**.
  - Se $\text{Viabilidade Líquida} \le 0$ $\rightarrow$ **Migrar para Canal de Custo Zero (Push/Email Inbound) ou Abortar Resgate Pago**.
- **Granularidade**: Nível de Carrinho / Cliente, agregado por Segmento RFM (`Premium`, `Regular`, `Dormant`, `Novo`) e por Canal.

---

## 💡 Diretrizes Estratégicas por Segmento

> [!IMPORTANT]
> **GOVERNANÇA METODOLÓGICA: DADOS ORIUNDOS DO SIMULADOR E DATASET**
> As decisões de alocação de canal não assumem percentuais arbitrários a priori; elas derivam da equação de viabilidade econômica líquida calculada sobre o Ticket Médio de cada segmento e custos reais de canais, conforme visualizado em [`chart_04_estrategia_resgate_segmento.png`](../../insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png).

### 1. Segmento PREMIUM (Ticket Médio R$ 800,00)
- **Diagnóstico Comportamental**: Clientes fiéis e de alto valor. O abandono decorre predominantemente de dúvidas pontuais ou interrupções de navegação.
- **Diretriz de Canal**: **Máximo Esforço / Canal VIP (WhatsApp API / Suporte Consultivo)**.
- **Política de Desconto**: **Desconto Zero (Cupom 0%)**. O ticket elevado absorve com facilidade o custo de R$ 0,30 do WhatsApp, gerando o maior ganho líquido unitário sem canibalizar margem.

### 2. Segmento REGULAR (Ticket Médio R$ 360,00)
- **Diagnóstico Comportamental**: Compradores recorrentes com sensibilidade moderada a prazos e condições comerciais.
- **Diretriz de Canal**: **Automação em Escala (Email Inbound / Push App)** com opção de WhatsApp apenas para cestas acima de R$ 500.
- **Política de Desconto**: **Desconto Condicionado (Cupom 5% apenas acima de R$ 200)**, preservando a rentabilidade da operação.

### 3. Segmento NOVO / DORMANT (Ticket Médio R$ 200,00 a R$ 250,00)
- **Diagnóstico Comportamental**: Visitantes em estágio comparativo ou clientes inativos com menor propensão espontânea de retorno.
- **Diretriz de Canal**: **Automação Zero Cost (Email Transacional / Push App)**.
- **Política de Desconto**: **Incentivo de Primeira Compra Condicionado a Frete**, vedando disparos via WhatsApp ou SMS pagos que gerariam viabilidade líquida negativa (custo do canal superior à margem residual).

---

## 📍 Dadosfera Config

- **Tipo**: Pipeline Prescritivo / Decision Engine / View Analítica
- **Camada**: Lakehouse `Silver (Qualify)` $\rightarrow$ `Gold (Curated Kimball)`
- **Dados necessários**:
  - `carrinhos.parquet` (`carrinho_id`, `valor_total`, `cliente_id`, `status`)
  - `clientes.parquet` (`cliente_id`, `segmento_rfm`, `lifetime_value`)
  - `eventos_resgate.parquet` (`canal`, `custo_envio`, `sucesso`, `valor_pedido_final`)

---

## ✅ Como Validar (Definition of Done)

- **Viabilidade Estrita**: Nenhum acionamento via canal com custo $\ge \text{R\$} 0,15$ pode ser aprovado para cestas onde a margem líquida esperada resulte em prejuízo financeiro.
- **Alinhamento com o Gráfico**: A matriz prescritiva de canais deve corresponder integralmente às zonas de viabilidade plotadas em [`chart_04_estrategia_resgate_segmento.png`](../../insights/03_prescriptive/01_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png).
- **Proteção de Margem**: Validar a regra de Cupom Zero para clientes Premium em 100% das simulações.
