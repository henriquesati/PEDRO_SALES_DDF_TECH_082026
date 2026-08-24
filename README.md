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
| **2.1** | Integrar (Coleta & API Maestro) | Integrar | Ingestão de 115k+ registros via Módulo de Coleta, API Maestro e mapeamento em `output-mappers/` | ✅ Concluído |
| **3** | Explorar & Catalogar | Explorar | Especificação de governança (`pipelines/case-item-03/`), Lakehouse Medallion (`pipelines/datalakes/`), dicionários (`data/catalogo/`) e Data Asset IDs oficiais | ✅ Concluído |
| **4** | Data Quality & Anomalias | Processar | Pipeline Dual-Artifact, suíte Great Expectations (18 regras), quarentena Parquet e relatório em [`pipelines/case-item-04/outputs/data_quality_report.md`](pipelines/case-item-04/outputs/data_quality_report.md) | ✅ Concluído |
| **5** | GenAI & LLMs | Processar | Enriquecimento semântico de motivos de abandono e gerador de copy | ⏳ Planejado |
| **6** | Modelagem de Dados | Analisar | Modelagem lógica canônica (4 divisões) em 6 entidades (`data/data-models/logical/`) | ✅ Concluído |
| **7** | Análise de Dados & BI | Analisar | 6 visualizações de BI (Série Temporal, Categorias, ROI) e catálogo declarativo | ✅ Concluído |
| **8** | Pipelines ETL/ML | Processar | Especificações de pipeline Silver e Golden views no Lakehouse | ⏳ Planejado |
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

- [x] ~~**[X] [case-02.1] Integrar (Módulo de Coleta & API Maestro) [X]**~~
  - **carga e ingestão da base de dados** (*Ingestão de 115.777+ registros nas 7 entidades canônicas, superando a meta mínima de 100k do case*)
  - **📁 Diretórios de interação com API, endpoints e mapeamento de ativos:**
    - [`agents_prompts_refs/dadosfera-api/`](agents_prompts_refs/dadosfera-api/) — *Documentação técnica e base de orquestração de scripts para integração com a API Maestro, mantendo a documentação próxima do ambiente de contexto e execução*
    - [`agents_prompts_refs/dadosfera-api/referencia/endpoints.md`](agents_prompts_refs/dadosfera-api/referencia/endpoints.md) — *Catálogo de referência completa dos endpoints Maestro (Auth, Storage Explorer, Tables e Catalog)*
    - [`agents_prompts_refs/dadosfera-api/output-mappers/`](agents_prompts_refs/dadosfera-api/output-mappers/) — *Mapeamento oficial dos 7 Data Asset IDs, URLs da UI e schemas das tabelas Snowflake, servindo como referência em memória dos ativos e suas modificações realizadas via API ([`assets_registry.md`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md), [`assets_registry.json`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json))*
  - **🤖 Agentes e Skills desenvolvidos/utilizados nesta etapa:**
    - [`platform-registry-consultant`](.agents/skills/platform-registry-consultant/SKILL.md) ([`.agents/agents/platform-registry-consultant.md`](.agents/agents/platform-registry-consultant.md)) — *Especialista e guardião do registro de ativos, metadados, Data Asset IDs oficiais e mapeamentos no diretório `output-mappers`*
    - [`case-context-specialist`](.agents/skills/case-context-specialist/SKILL.md) ([`.agents/agents/case-context-specialist.md`](.agents/agents/case-context-specialist.md)) — *Fonte central de contexto estratégico, validação de requisitos do case de estágio e diretrizes de autenticação e governança*
    - [`agents_prompts_refs/dadosfera-api/referencia/solved-errors.md`](agents_prompts_refs/dadosfera-api/referencia/solved-errors.md) — *Relatório documentando os erros técnicos identificados na API e soluções/workarounds aplicados (envio de token puro sem prefixo `Bearer` no header, tratamento de payload no `sign-in`, contorno de permissão `403 Forbidden` no storage via Coleta Web, prevenção de duplicatas via `PUT` no catálogo e tratamento de charset no console Windows)*

- [x] ~~**[X] [case-03] Explorar & Catalogar (Dicionário de Dados, Arquitetura Lakehouse & Governança) [X]**~~
  - **exploração, carga e catalogação com governança** (*Carga e catalogação dos datasets das 7 entidades no módulo Explorar, estruturação de Dicionários de Dados baseados em classe ("A é um B que C"), conformidade LGPD/PII e organização do Data Lakehouse em 4 zonas Medallion com Quarentena de Anomalias. Automação via API Maestro e vinculação direta aos 7 Data Asset IDs oficiais*)
  - **🏛️ Arquitetura de Zonas do Data Lakehouse:**
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
    *(+ Camada **Anomaly / Silver Quarentena** para segregação e armazenamento de anomalias contábeis e dirty data DEC-006)*
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
    - [`pipelines/datalakes/anomaly/spec.md`](pipelines/datalakes/anomaly/spec.md) — *Diretrizes da Camada Anomaly (Silver Quarentena: Armazenamento e Diagnóstico de Anomalias DEC-006)*
    - [`pipelines/datalakes/curated/spec.md`](pipelines/datalakes/curated/spec.md) — *Diretrizes da Camada Curated (Gold: Modelagem Dimensional Kimball e Analytics)*
  - **📁 Mapeamento Oficial de Ativos & Outputs (`output-mappers/`):**
    - [`agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md) ([`assets_registry.json`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.json)) — *Mapeamento oficial dos 7 Data Asset IDs vinculados, URLs diretas e schemas sincronizados*
    - [`pipelines/case-item-03/outputs/catalog_governance_report.md`](pipelines/case-item-03/outputs/catalog_governance_report.md) — *Inventário consolidado dos ativos e data lakes catalogados e evidências técnicas de governança*
  - **Skills e Agentes Criados nesta etapa:**
    - [`data-pipeline-documentation`](.agents/skills/data-pipeline-documentation/SKILL.md) ([`.agents/agents/data-pipeline-documentation.md`](.agents/agents/data-pipeline-documentation.md)) — *Especialista em documentação, catálogo e linhagem de pipelines no padrão Medallion (Bronze -> Silver -> Gold), contratos de dados, Data Quality e governança ágil sem over-engineering*
    - [`platform-registry-consultant`](.agents/skills/platform-registry-consultant/SKILL.md) ([`.agents/agents/platform-registry-consultant.md`](.agents/agents/platform-registry-consultant.md)) — *Guardião do registro de ativos, metadados, Data Asset IDs oficiais (`output-mappers`) e sincronização via API Maestro*

- [x] ~~**[X] [case-04] Data Quality, Quarentena de Anomalias & Common Data Model (Great Expectations & Relatório) [X]**~~
  - **governança de data quality, quarentena de anomalias e common data model** (*Auditoria completa de qualidade sobre 115.777+ registros em Parquet da camada Bronze, aplicação de suíte declarativa no Great Expectations com 18 expectativas em 6 dimensões fundamentais, segregação de qualidade na camada Silver (DEC-006) e implementação do Common Data Model (CDM) canônico em 7 entidades para garantir integridade e confiabilidade nas análises de BI*)
  - **🛡️ Arquitetura Dual-Artifact & Quarentena de Anomalias (DEC-006):**
    ```text
                      ┌──────────────────────────────────────────────┐
                      │             CAMADA BRONZE (RAW)              │
                      │         115.777+ Registros em Parquet        │
                      └──────────────────────┬───────────────────────┘
                                             │
                                             ▼
                      ┌──────────────────────────────────────────────┐
                      │    DATA QUALITY GATE: GREAT EXPECTATIONS     │
                      │       Regras Parametrizadas por Entidade     │
                      └──────────────────────┬───────────────────────┘
                                             │
                    ┌────────────────────────┴────────────────────────┐
                    ▼                                                 ▼
      ┌───────────────────────────┐                     ┌───────────────────────────┐
      │   SILVER QUALIFY (98.8%)  │                     │  SILVER ANOMALIES (1.2%)  │
      │  • Registros Higienizados │                     │  • Quarentena de Anomalias│
      │  • Contratos Cumpridos    │                     │  • Snapshot de Auditoria  │
      │  • Promovido para Análise │                     │  • Log de Desvios e Riscos│
      └─────────────┬─────────────┘                     └─────────────┬─────────────┘
                    │                                                 │
                    ▼                                                 ▼
      ┌───────────────────────────┐                     ┌───────────────────────────┐
      │     CONSUMO ANALÍTICO     │                     │   AUDITORIA DE QUALIDADE  │
      │  • Dashboards no Metabase │                     │  • Diagnóstico de Desvios │
      │  • Análise de Abandono/BI │                     │  • Relatório Executivo    │
      │  • Métricas Consolidadas  │                     │  • Rastreabilidade Silver │
      └───────────────────────────┘                     └───────────────────────────┘
    ```
  - **📁 Especificações Normativas e Blueprints de Data Quality:**
    - [`docs/specifications/data-quality-specification.md`](docs/specifications/data-quality-specification.md) — *Especificação normativa do Item 4 contendo contextualização, tripé de artefatos, as 6 dimensões de qualidade (Completeness, Uniqueness, Validity, Consistency, Integrity, Temporal Consistency), taxonomia detalhada de anomalias (ANOM-01 a ANOM-05) e estrutura de 13 seções do relatório*
    - [`docs/specifications/data-platform-specification.md`](docs/specifications/data-platform-specification.md) — *Diretrizes globais de governança, arquitetura, e contratos de dados*
    - [`pipelines/case-item-04/specs.md`](pipelines/case-item-04/specs.md) — *Especificação técnica formal do pipeline de Data Quality (`spec_data_quality_001` v1.1), mapeamento com requisitos oficiais do case, matriz de 18 regras e catálogo de severidades*
    - [`pipelines/case-item-04/implementation_plan.md`](pipelines/case-item-04/implementation_plan.md) — *Plano de implementação técnico, decomposição em fases WBS, regras de não-replicação e critérios de aceitação (Definition of Done)*
  - **📁 Suíte Declarativa de Expectativas e Execução:**
    - [`pipelines/case-item-04/notebooks/qualification_raw.ipynb`](pipelines/case-item-04/notebooks/qualification_raw.ipynb) — *Notebook executável aplicando as regras de validação sobre as entidades*
    - [`pipelines/case-item-04/scripts/run_quality_pipeline.py`](pipelines/case-item-04/scripts/run_quality_pipeline.py) — *Script batch automatizado (`python make.py quality-eval`)*
    - [`pipelines/case-item-04/quality/`](pipelines/case-item-04/quality/) — *Suíte declarativa de expectativas (`carrinhos_suite.json`) e log estruturado de validação*
  - **📁 Arquitetura de Outputs & Views:**
    - [`pipelines/case-item-04/outputs/`](pipelines/case-item-04/outputs/) — *Estrutura abstrata de diretórios de saída:*
      - `outputs/qualify/[entidade]/` — *Datasets higienizados e conformes promovidos para a camada Gold*
      - `outputs/anomalies/[entidade]/[rule]/` — *Quarentena de anomalias segregada por entidade e código de anomalia*
      - `outputs/assets/` — *Gráficos gerados pelo notebook e suas respectivas regras de validação*
      - `outputs/data_quality_report.md` — *Relatório executivo consolidado de qualidade e anomalias*
      - `outputs/validation_results.json` — *Manifesto estruturado de auditoria da validação*
  - **🌟 Bônus: Common Data Model (CDM) Implementado:**
    - **Modelo de Dados Padronizado (CDM)**: Padronização das 7 entidades de e-commerce para garantir que todo o Lakehouse e os dashboards analíticos compartilhem o mesmo schema e regras:
      - [`data/data-models/logical/entities/`](data/data-models/logical/entities/) — *Especificação das 7 entidades canônicas ([`clientes.md`](data/data-models/logical/entities/clientes.md), [`produtos.md`](data/data-models/logical/entities/produtos.md), [`carrinhos.md`](data/data-models/logical/entities/carrinhos.md), [`itens_carrinho.md`](data/data-models/logical/entities/itens_carrinho.md), [`eventos_carrinho.md`](data/data-models/logical/entities/eventos_carrinho.md), [`eventos_resgate.md`](data/data-models/logical/entities/eventos_resgate.md), [`pedidos.md`](data/data-models/logical/entities/pedidos.md))*
      - [`data/data-models/logical/relationships.md`](data/data-models/logical/relationships.md) — *Relacionamentos, cardinalidades e grafo ERD entre as tabelas*
      - [`data/data-models/logical/business-rules.md`](data/data-models/logical/business-rules.md) — *Regras de negócio e fórmulas contábeis unificadas*
  - **🤖 Agentes e Skills desenvolvidos/utilizados nesta etapa:**
    - [`data-pipeline-documentation`](.agents/skills/data-pipeline-documentation/SKILL.md) ([`.agents/agents/data-pipeline-documentation.md`](.agents/agents/data-pipeline-documentation.md)) — *Especialista em documentação, catálogo e linhagem de pipelines no padrão Medallion (Bronze -> Silver -> Gold), contratos de dados, Data Quality e governança ágil sem over-engineering*
    - [`declarative-functional-coding`](.agents/skills/declarative-functional-coding/SKILL.md) ([`.agents/agents/declarative-functional-coding.md`](.agents/agents/declarative-functional-coding.md)) — *Especialista na implementação de pipelines sob o paradigma funcional e declarativo, sequências de funções puras de validação/higienização (`validar_pk`, `sanitizar_frete`, etc.) e tipagem estrita*
    - [`datamaker`](.agents/skills/datamaker/SKILL.md) — *Especialista em modelagem lógica de dados, Common Data Model (CDM), schemas relacionais e injeção determinística de dirty data no mock engine*
    - [`charts-maker`](.agents/skills/charts-maker/SKILL.md) — *Especialista na geração de gráficos analíticos e visualizações com rigor absoluto de Ground Truth e preservação de evidências em 300 DPI*
    - [`case-context-specialist`](.agents/skills/case-context-specialist/SKILL.md) ([`.agents/agents/case-context-specialist.md`](.agents/agents/case-context-specialist.md)) — *Fonte central de contexto estratégico, validação de requisitos do case de estágio e diretrizes de autenticação e governança*
    - [`project-context-specialist`](.agents/skills/project-context-specialist/SKILL.md) ([`.agents/agents/project-context-specialist.md`](.agents/agents/project-context-specialist.md)) — *Guardião da memória técnica, arquitetura dual-artifact (DEC-006) e rastreabilidade de artefatos do repositório*
</div>

---

## 📓 3. Notebooks & Geração de Artefatos Visuais

O projeto conta com notebooks reproduzíveis e um **Task Runner em Python puro (`make.py`)** com atalhos de linha de comando para Windows, permitindo inspecionar dados e gerar todos os artefatos visuais de BI e Data Quality instantaneamente.

### 📁 Estrutura de Notebooks & Pipelines Executáveis:
- [`pipelines/case-item-04/notebooks/qualification_raw.ipynb`](pipelines/case-item-04/notebooks/qualification_raw.ipynb): Notebook oficial de qualificação e auditoria de Data Quality com Great Expectations (Item 4).
- [`pipelines/case-item-04/specs.md`](pipelines/case-item-04/specs.md): Especificação técnica normativa descrevendo o pipeline de qualidade e quarentena.
- [`pipelines/case-item-04/scripts/run_quality_pipeline.py`](pipelines/case-item-04/scripts/run_quality_pipeline.py): Script batch de execução automatizada da auditoria de qualidade (`python make.py quality-eval`).
- [`presentation/pitch/run_all_pitch_charts.py`](presentation/pitch/run_all_pitch_charts.py): Orquestrador de geração dos 8 painéis e gráficos visuais do Pitch (Item 10).
- [`presentation/insights/run_all_insights_charts.py`](presentation/insights/run_all_insights_charts.py): Orquestrador de geração de gráficos analíticos de insights de negócio.

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

# Executa o pipeline de Data Quality e gera o relatório (Item 4):
python make.py quality-eval

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
carrinhos_qualify (Silver)    carrinhos_anomalies (Quarentena de Anomalias)
   │ (98.8% Conformes)          │ (1.2% Isolados com anomaly_reason)
   ▼                            ▼
Gold Analytics / ML / GenAI   Auditoria & Ajustes de Engenharia
```

- 📑 **Relatório de Data Quality & Anomalias:** [`pipelines/case-item-04/outputs/data_quality_report.md`](pipelines/case-item-04/outputs/data_quality_report.md)
- 📊 **Imagens e Gráficos de Qualidade:** [`pipelines/case-item-04/outputs/assets/`](pipelines/case-item-04/outputs/assets/)
- 📝 **Evidência Estruturada de Execução:** [`pipelines/case-item-04/outputs/validation_results.json`](pipelines/case-item-04/outputs/validation_results.json)
- 📐 **Especificação Técnica do Item 4:** [`pipelines/case-item-04/specs.md`](pipelines/case-item-04/specs.md)
- 📓 **Notebook Interativo (Google Colab):** [`pipelines/case-item-04/notebooks/qualification_raw.ipynb`](pipelines/case-item-04/notebooks/qualification_raw.ipynb)

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
│   ├── data-models/logical/            # Modelagem Lógica Canônica / Common Data Model (4 Divisões)
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
│   │   ├── specs.md                    # Especificação técnica normativa
│   │   ├── implementation_plan.md      # Plano de execução WBS
│   │   ├── notebooks/                  # Notebook Google Colab executável
│   │   ├── scripts/                    # Script batch de execução automatizada (run_quality_pipeline.py)
│   │   ├── quality/                    # Expectativas Great Expectations & resultados JSON
│   │   └── outputs/                    # Relatório Markdown, datasets Parquet e gráficos 300 DPI
│   ├── case-item-06/                   # Modelagem Dimensional Kimball DW Gold (Item 6)
│   └── datalakes/                      # Arquitetura Lakehouse Medallion (Raw, Qualify, Anomaly, Curated)
│       ├── README.md                   # Visão geral das 4 camadas com diagrama
│       ├── raw/                        # Bronze: spec.md + 7 pastas com metadata.md
│       ├── qualify/                    # Silver: spec.md + 7 pastas com metadata.md
│       ├── anomaly/                    # Quarentena DEC-006: spec.md + 7 pastas com metadata.md
│       └── curated/                    # Gold Kimball: spec.md + 7 pastas com metadata.md
│
└── presentation/
    ├── pitch/                          # Infraestrutura completa da apresentação (Item 10)
    │   ├── README.md                   # Visão geral e índice de navegação
    │   ├── pitch_spec.md               # Backbone Central & Guidelines de Apresentação
    │   ├── run_all_pitch_charts.py     # Orquestrador consolidado dos geradores visuais
    │   ├── config/chart_theme.py       # Tema visual corporativo Dadosfera (300 DPI)
    │   └── 01 a 08/                    # Módulos com spec, script e artefatos visuais
    └── insights/                       # Visualizações de insights de negócio (01_bi_recuperacao_carrinhos)
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
