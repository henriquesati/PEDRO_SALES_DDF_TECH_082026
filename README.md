# 🛒 Case Técnico Dadosfera: Recuperação de Carrinho Abandonado (E-commerce)

> **Candidato:** Pedro Henrique Sales  
> **Identificador Oficial:** `PEDRO_SALES_DDF_TECH_082026`  
> **Plataforma:** [Dadosfera](https://dadosfera.ai) (Coleta, Catálogo, Qualify, Pipelines, Inteligência, Metabase & Data Apps)  
> **Domínio de Negócio:** E-commerce / Marketplace — Recuperação de Carrinho e Conversão de GMV   

---

## 📌 1. Visão Geral do Projeto

Este repositório contém a solução completa de Engenharia, Governança, Qualidade e Inteligência de Dados para o desafio de **Recuperação de Carrinho Abandonado**, demonstrando como a plataforma **Dadosfera** substitui e supera arquiteturas legadas e dispersas (AWS Glue/Athena/Sagemaker) em produtividade, governança e ROI de negócio.

### 🎯 Principais Destaques em resumo:
- **Base de Dados Sintética Modular e Declarativa:** **115.777+ registros** em Parquet e CSV com dirty data determinístico (5%) para testes de estresse de Data Quality.
- **Arquitetura Medallion com Segregação em Quarentena:** Camada Silver bifurcada em `carrinhos_qualify` (dados conformes) e `carrinhos_anomalies` (dados anômalos).
- **Data Quality Framework (Item 4):** Suíte de **18 expectativas Great Expectations** em 6 dimensões com relatório executivo de anomalias.
- **Dashboards & Views Analíticas (Item 7):** 6 visualizações de BI (Série Temporal, Performance de Categorias, ROI por Canal, Heatmap RFM e Matriz de Decisão) reproduzíveis via script e notebooks.
- **Contratos e Governança de Metadados:** Alinhamento rigoroso à [Data Platform Specification](docs/specifications/data-platform-specification.md) e catálogo com Data Asset IDs mapeados.

---
## 📋 2. Mapeamento de Tarefas do Case (Dadosfera)

| Item | Tema | Fase do Ciclo | Entregas no Repositório | Status |
|:---:|---|:---:|---|:---:|
| **0** | Agilidade & Planejamento | — | Planejamento iterativo entidade a entidade e matriz de decisão | ✅ Concluído |
| **1** | Base de Dados (mín. 100k) | Integrar | Gerador Python modular com 115.777+ registros em Parquet/CSV (`data/mock/`) | ✅ Concluído |
| **2.1** | Dadosfera - Integrar | Integrar | Ingestão de 115k+ registros via Módulo de Coleta, API Maestro e mapeamento em `output-mappers/` | ✅ Concluído |
| **3** | Dadosfera - Explorar & Catalogar | Explorar | Especificação de governança (`pipelines/case-item-03/`), Lakehouse Medallion (`pipelines/datalakes/`), dicionários (`data/catalogo/`) e Data Asset IDs oficiais | ✅ Concluído |
| **4** | Data Quality & Anomalias | Processar | Suíte Great Expectations e relatório gerado (`notebooks/pipelines/quality_report/outputs/data_quality_report.md`) | ✅ Concluído |
| **5** | GenAI & LLMs | Processar | Enriquecimento semântico de motivos de abandono e gerador de copy | ⏳ Planejado |
| **6** | Modelagem de Dados | Analisar | Modelagem lógica canônica (4 divisões) em 6 entidades (`data/data-models/logical/`) | ✅ Concluído |
| **7** | Análise de Dados & BI | Analisar | 6 visualizações de BI (Série Temporal, Categorias, ROI) e catálogo declarativo | ✅ Concluído |
| **8** | Pipelines ETL/ML | Processar | Especificações de pipeline Silver e Golden views na Dadosfera | ⏳ Planejado |
| **9** | Data Apps | Consumir | Planejamento de Data App em Streamlit para simulação de recuperação de ROI | ⏳ Planejado |
| **10** | Apresentação em Vídeo | — | Infraestrutura de Pitch (`presentation/pitch/`), roteiro master (`pitch_spec.md`), 8 módulos com scripts e gráficos 300 DPI | ✅ Concluído |
| **10.1** | Gráficos de Insights | Visualizações | Galeria de gráficos analíticos em `presentation/insights/`: módulo `01_bi_recuperacao_carrinhos/` concluído; módulos adicionais mapeados | 🔄 Em processo |
| **Bônus**| GenAI + Data Apps | IA Generativa | Geração visual de cards de produtos e vitrines dinâmicas de resgate | ⏳ Planejado |

### 🗂️ Mapeamento Detalhado de Tarefas por Entregável

<div style="opacity: 0.60; color: #8c92a4;">

- [x] ~~**[X] [case-01] Definição da base de dados**~~
  - **escolha de case carrinho** (*Recuperação de Carrinho Abandonado no Marketplace / E-commerce*)
  - **📁 Definições de entidade:**
    - [`data/data-models/logical/entities/`](data/data-models/logical/entities/) — *Especificações de entidades canônicas ([`carrinhos.md`](data/data-models/logical/entities/carrinhos.md), [`itens_carrinho.md`](data/data-models/logical/entities/itens_carrinho.md), [`eventos_carrinho.md`](data/data-models/logical/entities/eventos_carrinho.md), [`eventos_resgate.md`](data/data-models/logical/entities/eventos_resgate.md), [`clientes.md`](data/data-models/logical/entities/clientes.md), [`produtos.md`](data/data-models/logical/entities/produtos.md), [`pedidos.md`](data/data-models/logical/entities/pedidos.md))*
    - [`data/data-models/logical/relationships.md`](data/data-models/logical/relationships.md) — *Matriz de cardinalidade, integridade referencial e chaves*
    - [`data/data-models/logical/business-rules.md`](data/data-models/logical/business-rules.md) — *specificações de Regras de negócio, temporalidade de abandono (15 min) e status*
  - **📁 Diretórios de geração de carga e output:**
    - [`data/mock/generators/`](data/mock/generators/) — *Geradores modulares em Python com injeção determinística de dirty data*
    - [`data/mock/generators/parquet/config/`](data/mock/generators/parquet/config/) (`_config.py`) — *Engine central de configuração: controla parâmetros de injeção de dirty data (taxas de anomalias contábeis e de integridade) e garante métricas positivas de conversão, canais e ROI para a narrativa do Pitch*
    - [`data/mock/output/`](data/mock/output/) — *Datasets sintéticos brutos (+115.777 registros), organizados estritamente por formato de arquivo (`parquet/` e `csv/`)*
    - [`data/mock/output_cleaned/`](data/mock/output_cleaned/) — *Datasets higienizados e tratados (Ground Truth para BI e Pitch), organizados por formato (`parquet/` e `csv/`) com scripts de limpeza (`clean_all.py`)*
    - [`data/mock/METRICS.md`](data/mock/METRICS.md) — *Métricas de volumetria, distribuição e conformidade quantitativa*

- [x] ~~**[X] [case-02.1] Dadosfera - Integrar (Módulo de Coleta & Integração API Maestro) [X]**~~
  - **carga e ingestão da base de dados** (*Ingestão de 115.777+ registros nas 7 entidades canônicas, superando a meta mínima de 100k do case*)
  - **📁 Diretórios de interação com API, endpoints e mapeamento de ativos:**
    - [`agents_prompts_refs/dadosfera-api/`](agents_prompts_refs/dadosfera-api/) — *Documentação técnica e base de orquestração de scripts para integração com a API Maestro da Dadosfera, mantendo a documentação próxima do ambiente de contexto e execução*
    - [`agents_prompts_refs/dadosfera-api/referencia/endpoints.md`](agents_prompts_refs/dadosfera-api/referencia/endpoints.md) — *Catálogo de referência completa dos endpoints Maestro (Auth, Storage Explorer, Tables e Catalog)*
    - [`agents_prompts_refs/dadosfera-api/output-mappers/`](agents_prompts_refs/dadosfera-api/output-mappers/) — *Mapeamento oficial dos 7 Data Asset IDs, URLs da UI Dadosfera e schemas das tabelas Snowflake, serve como uma referencia em memória dos ativos e suas modificações realizadas na plataforma via API ([`assets_registry.md`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md), [`assets_registry.json`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json))*
  - **🤖 Agentes e Skills desenvolvidos/utilizados nesta etapa:**
    - [`platform-registry-consultant`](.agents/skills/platform-registry-consultant/SKILL.md) ([`.agents/agents/platform-registry-consultant.md`](.agents/agents/platform-registry-consultant.md)) — *Especialista e guardião do registro de ativos, metadados, Data Asset IDs oficiais e mapeamentos da plataforma Dadosfera no diretório `output-mappers`*
    - [`case-context-specialist`](.agents/skills/case-context-specialist/SKILL.md) ([`.agents/agents/case-context-specialist.md`](.agents/agents/case-context-specialist.md)) — *Fonte central de contexto estratégico, validação de requisitos do case de estágio e diretrizes de autenticação e governança*
    - [`agents_prompts_refs/dadosfera-api/referencia/solved-errors.md`](agents_prompts_refs/dadosfera-api/referencia/solved-errors.md) — *Relatório documentando os erros técnicos identificados na API e soluções/workarounds aplicados (envio de token puro sem prefixo `Bearer` no header, tratamento de payload no `sign-in`, contorno de permissão `403 Forbidden` no storage via Coleta Web, prevenção de duplicatas via `PUT` no catálogo e tratamento de charset no console Windows)*

- [x] ~~**[X] [case-03] Dadosfera - Explorar & Catalogar (Dicionário de Dados, Arquitetura Lakehouse & Governança) [X]**~~
  - **exploração, carga e catalogação com governança** (*Carga e catalogação dos datasets das 7 entidades no módulo Explorar da Dadosfera, estruturação de Dicionários de Dados baseados em classe ("A é um B que C"), conformidade LGPD/PII e organização do Data Lakehouse em 4 zonas Medallion com Dead-Letter/Quarentena. Automação via API Maestro e vinculação direta aos 7 Data Asset IDs oficiais*)
  - **🏛️ Arquitetura de Zonas do Data Lakehouse (Dadosfera):**
    ```text
                      ┌──────────────────────────────────────────────┐
                      │          ZONAS DO DATA LAKEHOUSE             │
                      └──────────────────────┬───────────────────────┘
                                             │
            ┌────────────────────────────────┼────────────────────────────────┐
            ▼                                ▼                                ▼
      [ ZONA RAW ]                  [ ZONA QUALIFY ]                 [ ZONA CURATED ]
      • Formato: Parquet / CSV      • Formato: Tabela Snowflake      • Formato: Snowflake Views
      • Origem: Ingestão Bruta      • Tratamento: Tipagem, DQ        • Consumo: BI (Metabase)
      • Storage: S3 Explorer        • Governança: Catalogado         • Lógica: RFM, KPIs, ROI
    ```
    *(+ Camada **Anomaly / Silver Dead-Letter** para segregação de dirty data e quarentena contábil DEC-006)*
  - **📁 Especificações Normativas & Blueprints de Governança:**
    - [`data/catalogo/business-catalog-classification.md`](data/catalogo/business-catalog-classification.md) — *Blueprint normativo e especificação v2.0 de governança e arquitetura Lakehouse em 4 zonas (Raw/Bronze, Qualify/Silver, Anomaly/Quarentena e Curated/Gold). Define a convenção de diretório por entidade (`metadata.md`), dicionário de dados rico, linhagem upstream/downstream, stewardship (owners) e conformidade LGPD*
    - [`data/catalogo/blueprint/blueprint_dicionario.md`](data/catalogo/blueprint/blueprint_dicionario.md) — *Modelo padronizado de dicionário de dados contendo identificação, visão de negócio, visão técnica, governança, atributos baseados em classe ("A é um B que C") e regras de Data Quality*
    - [`pipelines/case-item-03/specs.md`](pipelines/case-item-03/specs.md) — *Especificação técnica formal do módulo de exploração e catalogação (`spec_catalog_governance_001`), critérios de avaliação e integração com a API Maestro*
    - [`pipelines/case-item-03/implementation_plan.md`](pipelines/case-item-03/implementation_plan.md) — *Plano de implementação técnico e checklist de aceitação WBS para exploração e catalogação*
  - **📁 Dicionários de Dados & Governança por Entidade:**
    - [`data/catalogo/qualify/`](data/catalogo/qualify/) — *Dicionários de dados detalhados para as 7 entidades canônicas (`clientes`, `produtos`, `carrinhos`, `itens_carrinho`, `eventos_carrinho`, `eventos_resgate`, `pedidos`). Cada entidade possui arquivo dedicado estruturado no blueprint normativo, documentando descrições baseadas em classe ("A é um B que C"), granularidade, regras de validação e classificação de sensibilidade LGPD (com colunas de PII `nome`, `email` e `telefone` isoladas como 🔴 Confidencial em `clientes`)*
  - **📁 Arquitetura de Data Lakehouse por Entidade (`pipelines/datalakes/`):**
    - [`pipelines/datalakes/`](pipelines/datalakes/) — *Padrão arquitetural Lakehouse Medallion modular com diretório dedicado por entidade em cada camada (`pipelines/datalakes/[camada]/[entidade]_[camada]/`), onde coabitam o dataset físico e seu documento de metadados (`metadata.md`)*
    - [`pipelines/datalakes/README.md`](pipelines/datalakes/README.md) — *Guia arquitetural de referência do Lakehouse com fluxo de maturidade entre as 4 camadas*
    - [`pipelines/datalakes/raw/spec.md`](pipelines/datalakes/raw/spec.md) — *Diretrizes da Camada Raw (Bronze: Ingestão Bruta e Preservação As-Is)*
    - [`pipelines/datalakes/qualify/spec.md`](pipelines/datalakes/qualify/spec.md) — *Diretrizes da Camada Qualify (Silver: Limpeza Técnica e Contratos de Dados)*
    - [`pipelines/datalakes/anomaly/spec.md`](pipelines/datalakes/anomaly/spec.md) — *Diretrizes da Camada Anomaly (Silver Dead-Letter: Quarentena e Diagnóstico DEC-006)*
    - [`pipelines/datalakes/curated/spec.md`](pipelines/datalakes/curated/spec.md) — *Diretrizes da Camada Curated (Gold: Modelagem Dimensional Kimball e Analytics)*
  - **📁 Mapeamento Oficial de Ativos & Outputs (`output-mappers/`):**
    - [`agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md) ([`assets_registry.json`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json)) — *Mapeamento oficial dos 7 Data Asset IDs vinculados, URLs diretas e schemas sincronizados na Dadosfera*
    - [`pipelines/case-item-03/outputs/catalog_governance_report.md`](pipelines/case-item-03/outputs/catalog_governance_report.md) — *Inventário consolidado dos ativos e data lakes catalogados e evidências técnicas de governança*
  - **Skills e Agentes Criados nesta etapa:**
    - [`data-pipeline-documentation`](.agents/skills/data-pipeline-documentation/SKILL.md) ([`.agents/agents/data-pipeline-documentation.md`](.agents/agents/data-pipeline-documentation.md)) — *Especialista em documentação, catálogo e linhagem de pipelines no padrão Medallion (Bronze -> Silver -> Gold), contratos de dados, Data Quality e governança ágil sem over-engineering*
    - [`platform-registry-consultant`](.agents/skills/platform-registry-consultant/SKILL.md) ([`.agents/agents/platform-registry-consultant.md`](.agents/agents/platform-registry-consultant.md)) — *Guardião do registro de ativos, metadados, Data Asset IDs oficiais da Dadosfera (`output-mappers`) e sincronização via API Maestro*
</div>

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
│   ├── catalogo/                       # Blueprint normativo de catálogo de negócios e dicionários
│   │   ├── business-catalog-classification.md # Especificação v2.0 do Catálogo & Lakehouse
│   │   ├── blueprint/                  # Blueprint de dicionário de dados ("A é um B que C")
│   │   └── qualify/                    # Dicionários de dados detalhados das 7 entidades
│   ├── data-models/logical/            # Modelagem Lógica Canônica (4 Divisões)
│   └── mock/                           # Gerador modular e datasets gerados (Parquet/CSV)
│       ├── generators/                 # Geradores Python e engine declarativa de configuração (config.py)
│       ├── output/                     # Datasets sintéticos brutos por formato (csv/ e parquet/)
│       └── output_cleaned/             # Datasets higienizados por formato (csv/ e parquet/) e scripts
│
├── docs/
│   ├── specifications/                 # Normas da plataforma e Data Quality
│   │   ├── data-platform-specification.md
│   │   └── data-quality-specification.md
│   ├── relatorios/                     # Relatórios executivos (Data Quality, Etapas e BI Views)
│   │   ├── 03_explorar_catalogacao.md
│   │   ├── data_quality_report.md
│   │   ├── bi_views_report.md
│   │   ├── relatorio-etapa1.md
│   │   ├── relatorio-etapa2.md
│   │   └── relatorio-etapa3.md
│   └── assets/charts/                  # Galeria de gráficos analíticos gerados
│
├── pipelines/
│   ├── case-item-03/                   # Exploração & Catalogação de Ativos (Item 3)
│   │   ├── specs.md                    # Especificação formal do módulo
│   │   ├── implementation_plan.md      # Plano de implementação técnico
│   │   └── outputs/                    # Relatório de governança e catálogo consolidado
│   ├── case-item-04/                   # Data Quality Pipeline & Quarentena (Item 4)
│   ├── case-item-06/                   # Modelagem Dimensional Kimball DW Gold (Item 6)
│   └── datalakes/                      # Arquitetura Lakehouse Medallion (Raw, Qualify, Anomaly, Curated)
│       ├── README.md                   # Visão geral das 4 camadas com diagrama
│       ├── raw/                        # Bronze: spec.md + 7 pastas com metadata.md
│       ├── qualify/                    # Silver: spec.md + 7 pastas com metadata.md
│       ├── anomaly/                    # Quarentena DEC-006: spec.md + 7 pastas com metadata.md
│       └── curated/                    # Gold Kimball: spec.md + 7 pastas com metadata.md
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

## 🎤 6. Infraestrutura & Especificações do Pitch (Item 10)

Toda a infraestrutura documental e visual que suporta a gravação da apresentação em vídeo está organizada em [`presentation/pitch/`](presentation/pitch/):
- **Documentação Master (`pitch_spec.md`)**: Contém a **Parte 1 (Backbone Central)** com a cronologia em 5 blocos (00:00 a 12:30) e a **Parte 2 (Pitch Guidelines)** com falas sugeridas, dados de impacto em %, contraste Dadosfera vs AWS e respostas para objeções de C-Levels.
- **8 Subdiretórios Autocontidos**: Cada diretório de regra de negócio/ponto técnico contém a sua especificação (`spec.md`), script gerador (`generate_chart.py`) e artefato visual gerado (`chart_*.png` em 300 DPI).
- **Geração Consolidada**: `python make.py pitch-charts` ou `python presentation/pitch/run_all_pitch_charts.py`.

---

## ⚡ 7. Como Executar o Projeto Localmente

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
