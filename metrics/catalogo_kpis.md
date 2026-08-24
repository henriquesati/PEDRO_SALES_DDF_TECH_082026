# Catálogo de KPIs e Métricas de Negócio

> **Domínio**: Recuperação de Carrinho Abandonado (E-commerce / Marketplace)  
> **Status**: Consolidado com o Modelo Lógico, Generators Mock e Views SQL

---

## 📐 Hierarquia de Métricas

O modelo analítico do projeto está estruturado em 5 camadas hierárquicas, priorizando **taxas, proporções e eficiência** (em conformidade com a decisão estratégica DEC-001):

```
┌─────────────────────────────────────────────────────────────┐
│  Camada 1: Conversão & Recuperação (Métricas Globais)       │
├─────────────────────────────────────────────────────────────┤
│  Camada 2: Eficiência por Canal de Resgate                  │
├─────────────────────────────────────────────────────────────┤
│  Camada 3: Eficiência por Segmento de Cliente (RFM & LTV)   │
├─────────────────────────────────────────────────────────────┤
│  Camada 4: Eficiência Operacional & Financeira (ROI)        │
├─────────────────────────────────────────────────────────────┤
│  Camada 5: Timing & Cadência de Sequência                   │
└─────────────────────────────────────────────────────────────┘
```

---

## 1. Camada 1: Conversão & Recuperação

### KPI-01: Taxa de Abandono de Carrinho
- **Definição**: Percentual de carrinhos criados que resultaram em abandono de sessão.
- **Fórmula**:
  $$\text{Taxa de Abandono (\%)} = \left( \frac{\text{Total de Carrinhos com status 'abandonado'}}{\text{Total Geral de Carrinhos Criados}} \right) \times 100$$
- **Granularidade**: Diária, Semanal, Mensal, por Dispositivo, por Canal de Origem.
- **Target / Benchmark**: ~70.9% (Benchmark Baymard: ~69.8%).
- **Entidades Envolvidas**: `carrinhos`.

### KPI-02: Taxa de Recuperação de Carrinhos Abandonados
- **Definição**: Percentual de carrinhos abandonados que foram convertidos em compra via campanha de resgate.
- **Fórmula**:
  $$\text{Taxa de Recuperação (\%)} = \left( \frac{\text{Carrinhos com status 'recuperado' / 'comprado' e origem\_recuperacao = TRUE}}{\text{Total de Carrinhos Abandonados}} \right) \times 100$$
- **Granularidade**: Semanal, Mensal, por Canal de Resgate, por Segmento RFM.
- **Target / Benchmark**: ~10.1% dos abandonados (Benchmark de Mercado: 5% a 15%).
- **Entidades Envolvidas**: `carrinhos`, `eventos_resgate`, `pedidos`.

### KPI-03: Lift de Conversão de Resgate
- **Definição**: Incremento percentual de conversão gerado pelo resgate ativo em relação ao baseline de retorno orgânico.
- **Fórmula**:
  $$\text{Lift (\%)} = \left( \frac{\text{Taxa de Conversão com Resgate} - \text{Taxa de Retorno Orgânico}}{\text{Taxa de Retorno Orgânico}} \right) \times 100$$
- **Target**: $+50\%$ de incremento sobre a taxa base.

---

## 2. Camada 2: Eficiência por Canal de Resgate

### KPI-04: Taxas do Funil de Engajamento de Resgate
- **Fórmulas**:
  - **Taxa de Abertura**: $\frac{\text{Total de Aberturas}}{\text{Total de Envios}} \times 100$
  - **Taxa de Clique (CTR)**: $\frac{\text{Total de Cliques}}{\text{Total de Aberturas}} \times 100$
  - **Taxa de Conversão Final**: $\frac{\text{Total de Pedidos Convertidos}}{\text{Total de Envios}} \times 100$
- **Benchmarks por Canal no Dataset**:
  | Canal | Custo/Envio | Abertura | Clique | Conversão Final |
  |---|---|---|---|---|
  | **Email** | R$ 0,05 | ~42% | ~28% | ~4.5% |
  | **WhatsApp** | R$ 0,30 | ~68% | ~35% | ~2.5% |
  | **SMS** | R$ 0,15 | ~55% | ~22% | ~1.8% |
  | **Push App** | R$ 0,02 | ~30% | ~18% | ~1.2% |

---

## 3. Camada 3: Eficiência por Segmento (RFM & LTV)

### KPI-05: Taxa de Recuperação por Segmento RFM
- **Fórmula**:
  $$\text{Taxa Segmento (\%)} = \left( \frac{\text{Carrinhos Recuperados no Segmento}}{\text{Carrinhos Abandonados no Segmento}} \right) \times 100$$
- **Distribuição Observada**:
  - `Premium`: ~18% (alta responsividade, resgate imediato)
  - `Novo`: ~12% (reatividade com cupom 1ª compra)
  - `Regular`: ~10% (maior volume absoluto)
  - `Dormant`: ~6% (reativação de cliente inativo)
- **Ratio Premium / Dormant**: **3.0x** (comprova o ganho de segmentar).

### KPI-06: Valor Financeiro em Risco por LTV
- **Definição**: Montante em R$ total represado em carrinhos abandonados agrupado por faixa histórica de LTV do cliente.
- **Fórmula**: $\sum \text{carrinhos.valor\_total}$ para `status = 'abandonado'` agrupado por `clientes.segmento_rfm`.

---

## 4. Camada 4: Eficiência Operacional & Financeira (ROI)

### KPI-07: Retorno sobre Investimento de Resgate (ROI)
- **Definição**: Múltiplo financeiro líquido gerado para cada R$ 1,00 gasto em comunicação de resgate.
- **Fórmula**:
  $$\text{ROI} = \frac{\text{Receita dos Pedidos Recuperados} - \text{Descontos Concedidos} - \text{Custo Total de Disparos}}{\text{Custo Total de Disparos}}$$
- **Target**: ROI Global $\ge 30\text{x}$ (Dataset atinge ~45x).

### KPI-08: Custo Médio por Conversão Efetiva (CAC de Resgate)
- **Definição**: Custo direto de comunicação necessário para gerar 1 pedido recuperado.
- **Fórmula**: $\frac{\text{Custo Total de Disparos}}{\text{Total de Pedidos Convertidos}}$
- **Target**: $< 1\%$ do ticket médio recuperado.

---

## 5. Camada 5: Timing & Cadência de Sequência

### KPI-09: Distribuição de Conversões por Toque da Régua
- **Fórmula**: $\frac{\text{Conversões no Toque } T}{\text{Total de Conversões de Resgate}} \times 100$
- **Distribuição Alvo**:
  - `1º Toque (lembrete_1h)`: ~35% das conversões
  - `2º Toque (lembrete_24h)`: ~30% das conversões
  - `3º Toque (desconto_48h)`: ~25% das conversões
  - `4º Toque (urgencia_72h)`: ~10% das conversões

### KPI-10: Tempo Médio Abandono → Conversão
- **Definição**: Tempo médio decorrido entre a detecção do abandono e a confirmação do pedido resgatado.
- **Target**: ~28 horas.

---

## 6. Métrica Prescritiva: Score de Viabilidade de Recuperação

### KPI-11: Score de Viabilidade por Carrinho (`RECOVERY_VIABILITY`)
- **Fórmula**:
  $$\text{P\_RECUPERACAO} = \text{P\_BASE(RFM)} \times \text{FATOR\_MOTIVO} \times \text{FATOR\_VALOR} \times \text{FATOR\_TEMPO}$$
  $$\text{RETORNO\_ESPERADO} = \text{P\_RECUPERACAO} \times \text{valor\_total}$$
  $$\text{ROI\_ESPERADO} = \frac{\text{RETORNO\_ESPERADO}}{\text{CUSTO\_ESTIMADO\_CANAL}}$$
- **Categorização**:
  - 🟢 `ALTA`: $\text{ROI\_ESPERADO} \ge 50\text{x}$ e $\text{RETORNO\_ESPERADO} \ge \text{R\$ 10,00}$
  - 🟡 `MEDIA`: $\text{ROI\_ESPERADO} \ge 10\text{x}$ e $\text{RETORNO\_ESPERADO} \ge \text{R\$ 2,00}$
  - 🔴 `BAIXA`: $\text{ROI\_ESPERADO} < 10\text{x}$ ou $\text{RETORNO\_ESPERADO} < \text{R\$ 2,00}$
- **View SQL**: `vw_viabilidade_recuperacao`
