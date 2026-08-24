# Otimização de Timing de Envio (Cadência por Segmento)

> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../presentation/pitch/pitch_spec.md) (Seções 4 e 5)  
> **Base de Dados Unificada**: `data/mock/output_cleaned/parquet/*.parquet` (Ground Truth)  
> **Artefato Visual Correspondente**: [`presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png`](../../presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png)

---

## ❓ Pergunta de Negócio
Qual é a janela temporal inicial candidata e qual a cadência de reengajamento que maximiza a recuperação de receita sem provocar atrito ou descadastros, validada empiricamente através dos dados de telemetria de disparos?

---

## 📊 Métrica

- **KPI Primário**: Taxa de Conversão por Janela de Timing pós-Abandono (`% sobre envios da régua`).
- **KPIs Secundários**:
  - Taxa de Abertura por Janela de Delay (`%`).
  - Concentração Relativa do Total de Conversões por Onda (`% do volume recuperado`).
  - Taxa de Opt-out / Descadastro por Frequência de Disparo (`%`).
- **Fórmulas de Telemetria (Ground Truth)**:
  - `Delay de Disparo (horas)` = `TIMESTAMPDIFF(HOUR, carrinhos.data_abandono, eventos_resgate.data_envio)`.
  - `Taxa de Abertura no Timing T (%)` = $\frac{\text{Aberturas com data\_abertura NOT NULL no Timing } T}{\text{Total de Envios no Timing } T} \times 100$.
  - `Taxa de Conversão no Timing T (%)` = $\frac{\text{Conversões com sucesso = TRUE no Timing } T}{\text{Total de Envios no Timing } T} \times 100$.
  - `Concentração no Timing T (%)` = $\frac{\text{Conversões no Timing } T}{\text{Total Geral de Conversões de Réguas}} \times 100$.
- **Granularidade**: Nível de disparo individual (`eventos_resgate`), agregado por Régua Temporal (`lembrete_1h`, `lembrete_24h`, `desconto_48h`, `urgencia_72h`) e por Segmento RFM.
- **Dimensões**:
  - `Régua Temporal`: `lembrete_1h` (+1h), `lembrete_24h` (+24h), `desconto_48h` (+48h), `urgencia_72h` (+72h).
  - `Segmento RFM`: `clientes.segmento_rfm` (`premium`, `regular`, `dormant`, `novo`).
  - `Canal de Disparo`: `whatsapp`, `email`, `sms`, `push_app`.

---

## 💡 Evidência Empírica & Hipóteses Comportamentais

> [!IMPORTANT]
> **GOVERNANÇA METODOLÓGICA DE DADOS: NENHUMA SUPOSIÇÃO ARBITRÁRIA**
> - **Evidência Medida no Dataset**: A análise empírica dos dados persistidos em `eventos_resgate.parquet` e plotados em [`chart_05_otimizacao_timing_envio.png`](../../presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) demonstra que a **janela de +1h concentrou 86,4% do total de conversões de réguas**, apresentando a maior taxa unitária de conversão por disparo (1,04%) e taxa de abertura de 44,3%.
> - **Ressalva Metodológica para o Pitch**: Em vez de assumir percentuais especulativos ou declarar categoricamente que *"o horário ótimo é +1h"*, a formulação rigorosa é:  
> > *"Nos dados observados, a janela de +1h apresentou a maior taxa de conversão e concentrou a esmagadora maioria das conversões (86,4%), indicando +1h como a janela inicial candidata prioritária para calibração contínua via testes A/B na plataforma Dadosfera."*

### 1. Dinâmica Comportamental por Segmento (Hipóteses a Calibrar)

- **Segmento PREMIUM (Alta Propensão & Memória Recente)**:
  - *Comportamento*: Clientes fiéis com alta recorrência. O abandono frequentemente decorre de interrupção externa momentânea ou dúvida técnica pontual.
  - *Estratégia de Cadência*: Priorizar abordagem na **janela inicial candidata (+1h)** via canal direto/humano (WhatsApp/Suporte VIP), restabelecendo o contato enquanto o interesse de compra está ativo, sem necessidade de descontos.
- **Segmento REGULAR (Maturação de Decisão & Comparação)**:
  - *Comportamento*: Navegação mais deliberada, sensível a condições de frete e prazos.
  - *Estratégia de Cadência*: Disparo inicial espaçado (+6h a +24h) via Email Transacional ou Push Notification para evitar sensação de pressão excessiva no primeiro momento.
- **Segmento NOVO / DORMANT (Baixa Fidelidade & Exploração)**:
  - *Comportamento*: Visitantes em primeira jornada de compra ou inativos de longa data.
  - *Estratégia de Cadência*: Disparos cadenciados em D+1 (+24h) e D+2 (+48h) com incentivos condicionais e elementos de prova social para construir credibilidade institucional.

---

## 📍 Dadosfera Config

- **Tipo**: Pipeline de Automação Prescritiva / View / Painel de Cadência
- **Camada**: Lakehouse `Silver (Qualify)` $\rightarrow$ `Gold (Curated Kimball)`
- **Dados necessários**:
  - `carrinhos.parquet` (`carrinho_id`, `data_abandono`, `status`)
  - `clientes.parquet` (`cliente_id`, `segmento_rfm`)
  - `eventos_resgate.parquet` (`resgate_id`, `tipo_comunicacao`, `data_envio`, `data_abertura`, `sucesso`, `canal`, `custo_envio`)
  - `pedidos.parquet` (`carrinho_id`, `origem_recuperacao`, `valor_total`)

### Passos de Transformação
1. **Cálculo da Latência de Disparo**: `TIMESTAMPDIFF(HOUR, carrinhos.data_abandono, eventos_resgate.data_envio)`.
2. **Agrupamento por Onda Temporal**: Mapear para réguas padronizadas (`lembrete_1h`, `lembrete_24h`, `desconto_48h`, `urgencia_72h`).
3. **Métricas Empíricas**: Calcular taxas reais de abertura, cliques e conversões observadas diretamente nos logs.
4. **Visualização**: Curva de decaimento temporal conectando os vértices reais de resposta ([`chart_05_otimizacao_timing_envio.png`](../../presentation/insights/03_prescriptive/02_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png)).

---

## ✅ Como Validar (Definition of Done)

- **Integridade Cronológica**: Todo `data_envio` deve ser estritamente posterior a `data_abandono`.
- **Concordância com o Gráfico**: Nenhuma métrica descrita na especificação pode divergir dos números calculados a partir dos dados do dataset (1,04% de conversão por disparo em +1h / 86,4% de concentração).
- **Consistência de Status**: Carrinhos que já converteram não continuam no pipeline de réguas subsequentes.
- **Prevenção de Fadiga de Canal**: Limite de segurança de no máximo 3 toques em 72 horas para um mesmo carrinho.

---

## 🎯 Recomendação Acionável (Política de Cadência em 3 Ondas)

1. **Onda 1 (Gatilho Inicial Candidato: +1h)**:
   - Foco em carrinhos de alto valor e clientes Premium/Regular com abordagem consultiva e suporte direto.
2. **Onda 2 (Lembrete D+1: +24h)**:
   - Email inbound automático destacando itens salvos e avaliações de outros compradores.
3. **Onda 3 (Repescagem Final D+2: +48h a +72h)**:
   - Apenas para carrinhos que demonstraram engajamento prévio (abertura/clique), com gatilho condicional de urgência.
