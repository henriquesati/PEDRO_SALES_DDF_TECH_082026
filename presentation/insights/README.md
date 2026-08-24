# 📊 Galeria de Gráficos de Insights: Dadosfera E-commerce

Este diretório contém a infraestrutura de especificações visuais, scripts declarativos em Python e artefatos gráficos de alta definição dedicados aos **insights descritivos, diagnósticos e prescritivos** do case de Recuperação de Carrinho de Compras.

---

## 📂 Módulos de Visualização

| # | Módulo | Status | Tema & Descrição | Tipo de Visualização | Artefatos na Pasta |
|:---:|---|:---:|---|---|---|
| **01** | [`01_bi_recuperacao_carrinhos/`](01_bi_recuperacao_carrinhos/) | ✅ Concluído | **BI de Recuperação de Carrinhos**: Evolução acumulada semestral (Jan–Jun / 7.500 un) e dinâmica semanal diária (09–15 Fev / 288 un) com pareamento 1-para-1 de mini cards executivos. | Curvas Suaves (Spline Cúbica), Fundo Branco (`#FFFFFF`), Preenchimento de Zonas (`fill_between`) e Mini Cards | [`spec.md`](01_bi_recuperacao_carrinhos/spec.md) • [`generate_chart.py`](01_bi_recuperacao_carrinhos/generate_chart.py) • [`generate_mini_tables.py`](01_bi_recuperacao_carrinhos/generate_mini_tables.py) • [`chart_bi_recuperacao_carrinhos.png`](01_bi_recuperacao_carrinhos/chart_bi_recuperacao_carrinhos.png) |
| **02** | [`02_motivos_abandono/`](02_motivos_abandono/) | ✅ Concluído | **Decomposição Descritiva de Motivos de Abandono**: Dispersão pontual de carrinhos por causa-raiz/dispositivo e gráfico separado de perda financeira represada (R$ 1.845,0k). | [1] Dispersão / Strip Plot com Jitter por Causa-Raiz & Dispositivo<br>[2] Barras Horizontais de Perda Financeira Represada | [`spec.md`](02_motivos_abandono/spec.md) • [`generate_chart.py`](02_motivos_abandono/generate_chart.py) • [`chart_02_dispersao_motivos_abandono.png`](02_motivos_abandono/chart_02_dispersao_motivos_abandono.png) • [`chart_02_perda_financeira_motivos.png`](02_motivos_abandono/chart_02_perda_financeira_motivos.png) |

| **03** | [`03_segmentacao_risco/`](03_segmentacao_risco/) | ✅ Concluído | **Matriz Diagnóstica de Risco & Atrito**: Score de Risco em Tempo de Sessão (Crítico, Alto, Médio, Baixo) cruzado com Segmentos RFM (Premium, Regular, Dormant, Novo) e taxa real de abandono observada. | Painel Integrado: Heatmap 2D de Risco RFM + Barras Horizontais de Volume & Triagem de Sessão | [`spec.md`](03_segmentacao_risco/spec.md) • [`generate_chart.py`](03_segmentacao_risco/generate_chart.py) • [`chart_03_segmentacao_risco.png`](03_segmentacao_risco/chart_03_segmentacao_risco.png) |
| **04** | [`04_estrategia_resgate_segmento/`](04_estrategia_resgate_segmento/) | ✅ Concluído | **Estratégia Prescritiva de Resgate**: Simulador de Viabilidade Econômica Líquida por Resgate (WhatsApp a R$ 0,30, SMS a R$ 0,15, Email a R$ 0,05, Push a R$ 0,02) e Matriz de Políticas por Cluster RFM. | Painel Integrado: Barras Agrupadas de Ganho Líquido Unitário + Matriz Prescritiva de Ações | [`spec.md`](04_estrategia_resgate_segmento/spec.md) • [`generate_chart.py`](04_estrategia_resgate_segmento/generate_chart.py) • [`chart_04_estrategia_resgate_segmento.png`](04_estrategia_resgate_segmento/chart_04_estrategia_resgate_segmento.png) |
| **05** | [`05_otimizacao_timing_envio/`](05_otimizacao_timing_envio/) | ✅ Concluído | **Otimização Prescritiva de Timing**: Curva de Decaimento Temporal de Conversão (Decay Curve) ao longo das réguas (+1h, +24h, +48h, +72h), destacando o Ponto Ótimo de Disparo em até +1h. | Painel Integrado: Curva Suave (Spline Cúbica) com Eixo Duplo (Abertura vs Conversão) + Barras de Volumetria | [`spec.md`](05_otimizacao_timing_envio/spec.md) • [`generate_chart.py`](05_otimizacao_timing_envio/generate_chart.py) • [`chart_05_otimizacao_timing_envio.png`](05_otimizacao_timing_envio/chart_05_otimizacao_timing_envio.png) |

---

## 📐 Diretriz Metodológica: Foco em Proporções (%) & Entidade Exemplo

### 1. Foco Estrutural em Porcentagens (%)
> [!IMPORTANT]
> **O foco primordial de todas as análises e gráficos de Insights é a modelagem em PORCENTAGENS (%) e TAXAS RELATIVAS.**
> As dinâmicas de conversão de funil, curvas de decaimento temporal (+1h a +72h), segmentação de risco RFM e distribuição de atritos são desenhadas de forma agnóstica de ticket. Isso permite que qualquer cliente ou prospect conecte sua própria operação e **adeque seu próprio Ticket Médio e volumetria**, recalculando o ROI financeiro diretamente sobre as proporções validadas.

### 2. Entidade Exemplo de Negócio (Baseline Mock para Demonstrações)
Para momentos em que for estritamente necessário exemplificar projeções em moeda corrente (R$), adota-se o seguinte **Baseline da Entidade Exemplo (Varejo / Marketplace Padrão)**:

| Métrica / Dimensão | Valor Baseline Exemplo | Finalidade no Pitch / Insights |
|---|:---:|---|
| **Volume Semestral de Carrinhos** | `7.500 un` (~1.250 un/mês) | Base amostral da PoC |
| **Taxa Global de Abandono** | `~70,3% a 70,9%` | Benchmark de mercado (Baymard) |
| **Taxa de Conversão Direta** | `23,1%` | Conversão pura no checkout |
| **Taxa de Recuperação de Carrinho** | `10,6% s/ abandono` (6,6% total) | Recuperação com motor de resgate |
| **Ticket Médio Global da Operação** | `R$ 375,00` | Baseline médio ponderado |
| **Ticket Médio: Segmento PREMIUM** | `R$ 800,00` | Alta fidelidade / atendimento VIP (WhatsApp) |
| **Ticket Médio: Segmento REGULAR** | `R$ 360,00` | Compras recorrentes (Email + Push) |
| **Ticket Médio: Segmento NOVO** | `R$ 250,00` | Primeira compra / incentivo moderado |
| **Ticket Médio: Segmento DORMANT** | `R$ 200,00` | Reativação seletiva |
| **Custo por Disparo (WhatsApp)** | `R$ 0,30` | Canal nobre / conversão alta |
| **Custo por Disparo (Email / Push)** | `R$ 0,05 / R$ 0,02` | Canais de alta escala e custo mínimo |

---

## ⚙️ Como Executar os Geradores

### 1. Execução Consolidada
Para regerar todos os artefatos de visualização de uma só vez:
```bash
python presentation/insights/run_all_insights_charts.py
```
Ou via Make:
```bash
python make.py insights-charts
```

### 2. Execução Individual por Módulo
Você pode entrar em qualquer subdiretório e executar seu script isoladamente:
```bash
python presentation/insights/01_bi_recuperacao_carrinhos/generate_chart.py
python presentation/insights/02_motivos_abandono/generate_chart.py
python presentation/insights/03_segmentacao_risco/generate_chart.py
python presentation/insights/04_estrategia_resgate_segmento/generate_chart.py
python presentation/insights/05_otimizacao_timing_envio/generate_chart.py
```
*Cada script lê diretamente os datasets limpos em Parquet (`data/mock/output_cleaned/parquet/`) e salva a imagem correspondente em 300 DPI dentro do próprio diretório.*

