# 🛒 Case Técnico Dadosfera: Recuperação de Carrinho Abandonado (E-commerce)

> **Candidato:** Pedro Henrique Sales  
> **Identificador Oficial:** `PEDRO_SALES_DDF_TECH_082026`  
> **Plataforma:** [Dadosfera](https://dadosfera.ai) (Coleta, Catálogo, Qualify, Pipelines, Inteligência, Metabase & Data Apps)  
> **Domínio de Negócio:** E-commerce / Marketplace — Recuperação de Carrinho e Conversão de GMV  
> **Target de Avaliação:** Escala **Outlier** (Itens 0 a 10 + Data Apps + GenAI + Case Bônus)  

---

## 📌 1. Visão Geral do Projeto

Este repositório contém a solução completa de Engenharia, Governança, Qualidade e Inteligência de Dados para o desafio de **Recuperação de Carrinho Abandonado**, demonstrando como a plataforma **Dadosfera** substitui e supera arquiteturas legadas e dispersas (AWS Glue/Athena/Sagemaker) em produtividade, governança e ROI de negócio.

### 🎯 Principais Destaques:
- **Base de Dados Sintética Modular e Declarativa:** **115.777+ registros** em Parquet e CSV com dirty data determinístico (5%) para testes de estresse de Data Quality.
- **Arquitetura Medallion com Segregação em Quarentena:** Camada Silver bifurcada em `carrinhos_qualify` (dados conformes) e `carrinhos_anomalies` (dead-letter queue).
- **Data Quality Framework (Item 4):** Suíte de **18 expectativas Great Expectations** em 6 dimensões com relatório executivo de anomalias.
- **Dashboards & Views Analíticas (Item 7):** 6 visualizações de BI (Série Temporal, Performance de Categorias, ROI por Canal, Heatmap RFM e Matriz de Decisão) reproduzíveis via script e notebooks.
- **Contratos e Governança de Metadados:** Alinhamento rigoroso à [Data Platform Specification](docs/specifications/data-platform-specification.md) e catálogo com Data Asset IDs mapeados.

---

## 📋 2. Mapeamento de Requisitos do Case (Dadosfera)

| Item | Tema | Fase do Ciclo | Entregas no Repositório | Status |
|:---:|---|:---:|---|:---:|
| **0** | Agilidade & Planejamento | — | Planejamento iterativo entidade a entidade e matriz de decisão | ✅ Concluído |
| **1** | Base de Dados (mín. 100k) | Integrar | Gerador Python modular com 115.777+ registros em Parquet/CSV (`data/mock/`) | ✅ Concluído |
| **2.1** | Dadosfera - Integrar | Integrar | Mapeamento de carga via API Maestro e Lakehouse Snowflake | ⏳ Planejado |
| **3** | Dadosfera - Explorar | Explorar | Dicionários de dados Qualify (`data/catalogo/qualify/`) e Data Asset IDs oficiais | ✅ Concluído |
| **4** | Data Quality & Anomalias | Processar | Suíte Great Expectations e relatório gerado (`notebooks/pipelines/quality_report/outputs/data_quality_report.md`) | ✅ Concluído |
| **5** | GenAI & LLMs | Processar | Enriquecimento semântico de motivos de abandono e gerador de copy | ⏳ Planejado |
| **6** | Modelagem de Dados | Analisar | Modelagem lógica canônica (4 divisões) em 6 entidades (`data/data-models/logical/`) | ✅ Concluído |
| **7** | Análise de Dados & BI | Analisar | 6 visualizações de BI (Série Temporal, Categorias, ROI) e catálogo declarativo | ✅ Concluído |
| **8** | Pipelines ETL/ML | Processar | Especificações de pipeline Silver e Golden views na Dadosfera | ⏳ Planejado |
| **9** | Data Apps | Consumir | Planejamento de Data App em Streamlit para simulação de recuperação de ROI | ⏳ Planejado |
| **10** | Apresentação em Vídeo | — | Infraestrutura de Pitch (`presentation/pitch/`), roteiro master (`pitch_spec.md`), 8 módulos com scripts e gráficos 300 DPI | ✅ Concluído |
| **10.1** | Gráficos de Insights | Visualizações | Galeria de gráficos analíticos em `presentation/insights/`: módulo `01_bi_recuperacao_carrinhos/` concluído; módulos adicionais mapeados | 🔄 Em processo |
| **Bônus**| GenAI + Data Apps | IA Generativa | Geração visual de cards de produtos e vitrines dinâmicas de resgate | ⏳ Planejado |

---

## 📓 3. Notebooks & Geração de Artefatos Visuais

O projeto conta com notebooks reproduzíveis e um **Task Runner em Python puro (`make.py`)** com atalhos de linha de comando para Windows, permitindo inspecionar dados e gerar todos os artefatos visuais de BI e Data Quality instantaneamente.

### 📁 Estrutura da Pasta `notebooks/`:
- [`notebooks/pipelines/quality_report/qualification_raw.ipynb`](notebooks/pipelines/quality_report/qualification_raw.ipynb): Notebook oficial de qualificação e auditoria de Data Quality com Great Expectations (Item 4).
- [`notebooks/pipelines/quality_report/pipeline_spec.md`](notebooks/pipelines/quality_report/pipeline_spec.md): Especificação normativa em Markdown descrevendo o pipeline de qualidade e quarentena.
- [`notebooks/pipelines/quality_report/run_quality_pipeline.py`](notebooks/pipelines/quality_report/run_quality_pipeline.py): Script batch de execução automatizada da auditoria de qualidade.
- [`notebooks/07_bi_dashboards_visualizations.ipynb`](notebooks/07_bi_dashboards_visualizations.ipynb): Execução e inspeção dinâmica das visualizações analíticas de BI (Item 7).
- [`notebooks/pipelines/serving/generate_bi_charts.py`](notebooks/pipelines/serving/generate_bi_charts.py): Pipeline gerador de imagens e views.
- [`notebooks/pipelines/serving/chart_specs.py`](notebooks/pipelines/serving/chart_specs.py): Catálogo declarativo de especificações de gráficos.

---

### 💻 Como Executar na CLI (Windows / Linux / macOS)

Você pode gerar as imagens de visualização de BI através de 3 opções equivalentes:

#### Opção 1: Atalho Direto no Windows CLI (PowerShell / Prompt de Comando)
```powershell
# Gera todos os 6 gráficos de BI em alta resolução (300 DPI):
.\notebook-gen

# Gera apenas um gráfico específico passando o nome da view:
.\notebook-gen categories
.\notebook-gen time_series
.\notebook-gen roi_channels
```

#### Opção 2: Via Wrapper Make no Windows
```powershell
# Execução completa:
.\make notebook-gen

# Execução individual:
.\make chart time_series
```

#### Opção 3: Via Python Direto (Multiplataforma)
```bash
# Gera todas as imagens de BI:
python make.py notebook-gen

# Gera um gráfico específico por chave string:
python make.py chart categories

# Lista todas as views e gráficos disponíveis no catálogo declarativo:
python make.py list-charts

# Gera todos os 8 gráficos de alta resolução da apresentação de Pitch:
python make.py pitch-charts

# Gera todos os gráficos da galeria de Insights de Negócio (presentation/insights):
python make.py insights-charts
```

---

### 📊 Catálogo de Chaves de Gráficos Disponíveis (`chart_specs.py`):

| Chave String | ID | Tipo de Gráfico | Lugar / Painel no BI | View de Origem |
|---|:---:|---|---|---|
| `"time_series"` | `CHART-01` | `line_dual_axis` | **Painel Executivo — Topo** | `vw_metricas_resgate_diarias` |
| `"categories"` | `CHART-02` | `bar_horizontal` | **Painel de Catálogo & Produtos** | `vw_produtos_abandonados` |
| `"roi_channels"` | `CHART-03` | `combo_bar_line` | **Painel Financeiro & Marketing** | `vw_performance_canais` |
| `"rfm_heatmap"` | `CHART-04` | `heatmap_matrix` | **Painel Comportamental & CRM** | `vw_abandono_analise` |
| `"scatter_viability"` | `CHART-05` | `scatter_bubble` | **Painel Prescritivo & Operacional** | `vw_viabilidade_recuperacao` |
| `"data_quality"` | `CHART-06` | `donut_bar_split` | **Painel de Governança & DQ** | `vw_qualidade_auditoria` |

> 📁 Todas as imagens geradas são salvas automaticamente em [`dashboards/assets/`](dashboards/assets/) e [`docs/assets/charts/`](docs/assets/charts/).

---

## 🛡️ 4. Data Quality & Relatório de Anomalias (Item 4)

O pipeline de qualidade avalia **115.777 registros** em 6 dimensões fundamentais com segregação estrita entre **Detecção** e **Tratamento**:

```text
carrinhos_raw (Bronze)
       │
       ▼
[ Data Quality Gate: Great Expectations (18 Regras) ]
       │
   ┌───┴────────────────────────┐
   ▼                            ▼
carrinhos_qualify (Silver)    carrinhos_anomalies (Quarentena/Dead-Letter)
   │ (94.2% Conformes)          │ (5.8% Isolados com anomaly_reason)
   ▼                            ▼
Gold Analytics / ML / GenAI   Auditoria & Ajustes de Engenharia
```

- 📑 **Relatório de Data Quality & Anomalias:** [`notebooks/pipelines/quality_report/outputs/data_quality_report.md`](notebooks/pipelines/quality_report/outputs/data_quality_report.md)
- 📊 **Imagens e Gráficos de Qualidade:** [`notebooks/pipelines/quality_report/outputs/assets/`](notebooks/pipelines/quality_report/outputs/assets/)
- 📝 **Evidência Estruturada de Execução:** [`notebooks/pipelines/quality_report/outputs/validation_results.json`](notebooks/pipelines/quality_report/outputs/validation_results.json)

---

## 📂 5. Estrutura do Repositório

```text
wheels/
├── README.md                           # Visão geral, guia de execução e contexto do case
├── make.py                             # Task runner central multiplataforma
├── notebook-gen.cmd / .ps1             # Atalhos diretos de execução para Windows CLI
├── make.cmd                            # Wrapper para comandos make no Windows
│
├── .agents/                            # Ecossistema de IA (Agents & Skills especializadas)
│   ├── agents/                         # Agentes configurados para o projeto
│   └── skills/                         # Skills normativas (datamaker, context, dq, pipelines)
│
├── dashboards/
│   ├── dashboard_recuperacao_carrinho.md # Especificação dos Dashboards Metabase (Item 7)
│   └── assets/                         # Artefatos visuais de alta resolução (PNG / JSON)
│
├── data/
│   ├── catalogo/                       # Dicionários de dados Qualify e blueprint
│   ├── data-models/logical/            # Modelagem Lógica Canônica (4 Divisões)
│   └── mock/                           # Gerador modular e datasets gerados (Parquet/CSV)
│
├── docs/
│   ├── specifications/                 # Normas da plataforma e Data Quality
│   │   ├── data-platform-specification.md
│   │   └── data-quality-specification.md
│   ├── relatorios/                     # Relatórios executivos (Data Quality, Etapas e BI Views)
│   │   ├── data_quality_report.md
│   │   ├── bi_views_report.md
│   │   ├── relatorio-etapa1.md
│   │   ├── relatorio-etapa2.md
│   │   └── relatorio-etapa3.md
│   └── assets/charts/                  # Galeria de gráficos analíticos gerados
│
├── presentation/
│   └── pitch/                            # Infraestrutura completa da apresentação (Item 10)
│       ├── README.md                     # Visão geral e índice de navegação
│       ├── pitch_spec.md                 # Backbone Central & Guidelines de Apresentação
│       ├── run_all_pitch_charts.py       # Orquestrador consolidado dos geradores visuais
│       ├── config/chart_theme.py         # Tema visual corporativo Dadosfera (300 DPI)
│       ├── 01_abandono_vs_recuperacao_timeline/ # Spec + Script + Gráfico Série Temporal
│       ├── 02_performance_categorias_produtos/  # Spec + Script + Gráfico Categorias
│       ├── 03_roi_canais_e_comunicacao/         # Spec + Script + Gráfico ROI Canais
│       ├── 04_matriz_motivos_segmentos_rfm/     # Spec + Script + Heatmap RFM
│       ├── 05_matriz_viabilidade_recuperacao/   # Spec + Script + Scatter Viabilidade
│       ├── 06_data_quality_e_quarentena/        # Spec + Script + Scorecard DQ
│       ├── 07_arquitetura_dadosfera_vs_aws/     # Spec + Script + Comparativo AWS
│       └── 08_data_app_simulador_prescritivo_genai/ # Spec + Script + Painel GenAI
│
├── quality/
│   ├── expectations/                   # Expectativas formais Great Expectations
│   └── results/                        # Evidências JSON da validação de qualidade
```

---

## 🎤 5. Infraestrutura & Especificações do Pitch (Item 10)

Toda a infraestrutura documental e visual que suporta a gravação da apresentação em vídeo está organizada em [`presentation/pitch/`](presentation/pitch/):
- **Documentação Master (`pitch_spec.md`)**: Contém a **Parte 1 (Backbone Central)** com a cronologia em 5 blocos (00:00 a 12:30) e a **Parte 2 (Pitch Guidelines)** com falas sugeridas, dados de impacto em %, contraste Dadosfera vs AWS e respostas para objeções de C-Levels.
- **8 Subdiretórios Autocontidos**: Cada diretório de regra de negócio/ponto técnico contém a sua especificação (`spec.md`), script gerador (`generate_chart.py`) e artefato visual gerado (`chart_*.png` em 300 DPI).
- **Geração Consolidada**: `python make.py pitch-charts` ou `python presentation/pitch/run_all_pitch_charts.py`.

---

## ⚡ 6. Como Executar o Projeto Localmente

### 1. Clonar o Repositório e Instalar Dependências
```bash
git clone https://github.com/pedro-sales/PEDRO_SALES_DDF_TECH_082026.git
cd PEDRO_SALES_DDF_TECH_082026
pip install pandas pyarrow faker great_expectations matplotlib seaborn plotly
```

### 2. Gerar a Base Sintética de Dados (115k+ Registros)
```bash
python make.py mock-gen
```

### 3. Executar a Validação de Data Quality e Gerar Imagens de BI
```powershell
# No Windows:
.\notebook-gen

# Ou em qualquer SO:
python make.py notebook-gen
```

### 4. Gerar os 8 Gráficos e Painéis Visuais do Pitch
```bash
python make.py pitch-charts
```
