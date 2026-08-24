---
name: project-context-specialist
description: Fonte central de contexto, progresso e memória do case de Recuperação de Carrinho Abandonado (Marketplace). Mapeia etapas concluídas, decisões arquiteturais, schemas e próximos passos do projeto correlacionados aos requisitos numerados do case Dadosfera.
---

# Skill: Project Context Specialist

## 🎯 Objetivo & Missão
Atuar como a **fonte central de contexto técnico e memória viva do projeto**. Esta skill armazena o histórico do repositório, suas etapas, artefatos gerados, decisões arquiteturais e progressão contínua, correlacionando diretamente as entregas com os **itens numerados do case oficial da Dadosfera** (gerenciados estrategicamente pela skill [`case-context-specialist`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/.agents/skills/case-context-specialist/SKILL.md)).

---

## 📌 Visão Geral do Case & Domínio
- **Domínio**: E-commerce / Marketplace.
- **Problema de Negócio**: **Recuperação de Carrinho Abandonado** (demonstração direta de ROI, conversão e redução de fricção no checkout).
- **Target de Avaliação**: Escala **Outlier** (cumprimento dos itens essenciais + Data Apps + GenAI + Case Bônus).
- **Stack & Ferramentas**: Plataforma Dadosfera (Maestro API, Catálogo, Qualify, Pipelines, Metabase), Snowflake, Python (Pandas/PyArrow/Faker), Parquet, CSV, Streamlit.

---

## 📋 Mapeamento Direto com os Itens Numerados do Case (Dadosfera)

> Cruzamento entre o status técnico do repositório e os requisitos formais de [`case-context-specialist`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/.agents/skills/case-context-specialist/SKILL.md) / [`specs-internship.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/specs-internship.txt).

| Item | Requisito do Case | Fase Dadosfera | Entregas Técnicas no Repositório | Status |
|:---:|---|:---:|---|:---:|
| **0** | Agilidade & Planejamento | — | Planejamento iterativo entidade a entidade, matriz de decisão e registro de progresso | ✅ Concluído |
| **1** | Base de Dados (mín. 100k) | Integrar | Gerador Python modular e declarativo com 115.777+ registros (`data/mock/output/parquet/` e `csv/`), arquitetura DAG em cascata, perfis (`standard`, `rich`, `dev`) e motor determinístico de anomalias/dirty data | ✅ Concluído |
| **2.1** | Dadosfera - Integrar | Integrar | Scripts de carga via API Maestro e Data Lakehouse Snowflake | ⏳ Planejado |
| **3** | Dadosfera - Explorar & Catalogar | Explorar | Dicionários de Dados das 7 entidades no Qualify (`data/catalogo/qualify/`) e mapeamento de Data Asset IDs oficiais (`assets_registry.md` / `assets_registry.json`) | ✅ Concluído |
| **4** | Data Quality & Anomalias | Processar | Pipeline de qualificação dual-artifact (`pipelines/case-item-04/notebooks/qualification_raw.ipynb` e `specs.md`), suíte Great Expectations (18 regras), quarentena de anomalias em Parquet e relatório gerado (`pipelines/case-item-04/outputs/data_quality_report.md`) | ✅ Concluído |
| **5** | GenAI & LLMs | Processar | Geração de copies persuasivas e enriquecimento semântico de motivos de abandono | ⏳ Planejado |
| **6** | Modelagem de Dados | Analisar | Modelagem dimensional Kimball Star Schema (6 dimensões conformadas, 2 fatos granulares, 2 visões analíticas Gold, diagrama DW em camadas Medallion e relatório em `pipelines/case-item-06/outputs/data_modeling_report.md` sob DEC-008) | ✅ Concluído |
| **7** | Análise de Dados & Métricas | Analisar | 6 visualizações de BI geradas (Série Temporal, Categorias, ROI, Heatmap, Scatter e DQ), script reproduzível (`pipelines/serving/generate_bi_charts.py`), catálogo declarativo (`chart_specs.py`), notebook (`07_bi_dashboards_visualizations.ipynb`) e task runner CLI (`notebook-gen`) | ✅ Concluído |
| **8** | Pipelines ETL/ML | Processar | Especificações de pipeline Silver (Qualify + Anomaly) e framework normativo (`data-pipeline-documentation`) | ⏳ Planejado |
| **9** | Data Apps | Consumir | Planejamento de Data App interativo em Streamlit para simulação de recuperação de carrinhos e cálculo de ROI | ⏳ Planejado |
| **10** | Apresentação em Vídeo | — | Infraestrutura completa de Pitch (`presentation/pitch/`), roteiro cronológico (Backbone Central & Guidelines em `pitch_spec.md`), 8 subdiretórios com specs/scripts funcionais e artefatos visuais (300 DPI) | ✅ Concluído |
| **Bônus**| GenAI + Data Apps | IA Generativa | Geração visual de cards de produtos e vitrines dinâmicas de resgate | ⏳ Planejado |

---

## 📈 Histórico Detalhado de Etapas Concluídas

### ✅ 1. Modelagem de Dados Lógica Canônica & Dimensional Kimball (Item 6)
- **Modelagem Lógica Canônica (4 Divisões)**: Todas as **7 entidades** do modelo de dados lógico estruturadas em `data/data-models/logical/entities/` (`carrinhos.md`, `clientes.md`, `produtos.md`, `itens_carrinho.md`, `eventos_carrinho.md`, `eventos_resgate.md`, `pedidos.md`), integridade referencial em `relationships.md` e o documento central [`business-rules.md`](data/data-models/logical/business-rules.md) consolidado como o **Master Single Source of Truth (SSOT)** de Regras de Negócio, Invariantes Contábeis, Políticas de Automação de Resgate e Lógicas Analíticas de BI.
- **Modelagem Dimensional Gold (Kimball Star Schema - DEC-008)**:
  - 6 Dimensões Conformadas (`dim_clientes`, `dim_tempo`, `dim_dispositivo`, `dim_motivo_abandono`, `dim_canal_resgate`, `dim_segmento_rfm`) com chaves surrogate (`_sk`).
  - 2 Tabelas de Fatos Granulares (`fato_abandono` com 6.525 linhas e `fato_resgate` com 6.289 linhas).
  - 2 Visões Analíticas Gold (`v_abandonment_summary` para perfil/risco e `v_recovery_roi_by_segment` para conversão/ROI de CRM).
  - Relatório de Gap Analysis em `pipelines/case-item-06/outputs/canonical_structure_gaps_report.md`.
  - Diagrama de Arquitetura DW em camadas Medallion (`pipelines/case-item-06/outputs/assets/data_warehouse_architecture.png` e `.mmd`).
  - Relatório técnico final consolidado em `pipelines/case-item-06/outputs/data_modeling_report.md`.

### ✅ 2. Geração de Base de Dados Sintética Modular e Declarativa (Item 1)
- **Arquitetura Modular**: Decomposição em camadas desacopladas (`config/` para constantes e settings, `core/` para `BaseGenerator` e `AnomalyEngine`, `modules/` para geradores de entidade e `run_all.py` como orquestrador CLI).
- **Perfis de Volumetria**: Suporte nativo a perfis (`standard` com **115.777 registros**, `rich` com **~161.600 registros** e `dev` com **~12.100 registros** em <3s).
- **Geração em Cascata (DAG)**: Execução encadeada respeitando integridade referencial (`clientes` & `produtos` → `carrinhos` → `itens_carrinho`, `eventos_carrinho`, `eventos_resgate` → `pedidos`), suportando execução individual de módulos com auto-resolução de dependências.
- **Motor Determinístico de Anomalias (`AnomalyEngine`)**: Garantia matemática de cotas mínimas de dirty data e anomalias de negócio (e-mails nulos em 5%, sintaxe inválida em 3%, telefones sem máscara em 5%, frete negativo ANOM-01 em 4%, total inconsistente ANOM-04 em 5%, subtotal zerado ANOM-02 em 2%, desconto excessivo ANOM-03 em 2%, carrinhos sem itens/órfãos em 2%, promoções invertidas em 5%, inversões temporais em 5%).
- **Métricas e Benchmarks Validados (DEC-001)**: ~69,7% de abandono (Baymard ~69,8%), ~9,5% de recuperação (Klaviyo/Salesforce 6-15%) e ROI financeiro de ~31,3x.

### ✅ 3. Catalogação de Ativos na Plataforma Dadosfera (Item 3)
- Dicionários de dados detalhados na camada Qualify (Silver) para todas as entidades em `data/catalogo/qualify/`.
- Sincronização e mapeamento de Data Asset IDs oficiais da Dadosfera via API Maestro registrados em `agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md`.

### ✅ 4. Auditoria de Data Quality & Quarentena de Anomalias (Item 4)
- **Tripé de Entrega Implementado**:
  - `pipelines/case-item-04/notebooks/qualification_raw.ipynb`: Notebook executável e compatível com Google Colab aplicando regras sobre as 7 entidades lendo Parquet.
  - `pipelines/case-item-04/specs.md` & `pipelines/case-item-04/implementation_plan.md`: Especificação normativa e documentação técnica do pipeline.
  - `pipelines/case-item-04/outputs/data_quality_report.md`: Relatório e evidências geradas de forma autocontida pelo pipeline.
  - `quality/expectations/carrinhos_suite.json` e `quality/results/validation_results.json`: Suite formal e evidências estruturadas.
- **Arquitetura Dual-Artifact (DEC-006)**: Bifurcação entre registros aprovados (`pipelines/case-item-04/outputs/qualify/*.parquet` com 94.2% de conformidade) e quarentena (`pipelines/case-item-04/outputs/anomalies/*.parquet` com 5.8% de registros isolados com `anomaly_reason`).

### ✅ 5. Visualizações de BI, Dashboards & CLI Runner (Item 7)
- **6 Visualizações de BI Geradas**: Série Temporal, Performance de Categorias, ROI por Canal, Heatmap RFM, Dispersão de Viabilidade e Scorecard de Data Quality salvas em `dashboards/assets/` em alta definição (300 DPI).
- **Catálogo Declarativo (`chart_specs.py`)**: Mapeamento estruturado de cada view/gráfico permitindo seleção dinâmica via chave string.
- **Task Runner Multiplataforma (`make.py` / `notebook-gen`)**: Automação por CLI permitindo rodar `.\notebook-gen` ou `python make.py notebook-gen [chart_key]`.

### ✅ 6. Infraestrutura Documental, Roteiro & Gráficos do Pitch (Item 10)
- **Estrutura Centralizada (`presentation/pitch/`)**: Todos os artefatos de apresentação, especificações de negócio e geradores visuais organizados e autocontidos.
- **Documentação Canônica (`pitch_spec.md` & `README.md`)**:
  - **Parte 1 — Backbone Central**: Ordem cronológica da apresentação (Blocos 1 a 5, minutagem estimada, entregas levantadas e mensagem central).
  - **Parte 2 — Pitch Guidelines**: Roteiro detalhado com falas sugeridas para cada slide/tópico, dados de impacto ancorados em taxas e percentuais (DEC-001/007), contraste Dadosfera vs AWS e tratamento de objeções de C-Levels.
- **8 Módulos Autocontidos com Gráficos em 300 DPI**:
  - `01_abandono_vs_recuperacao_timeline/` (Série Temporal & Ciclo de Vida do Carrinho)
  - `02_performance_categorias_produtos/` (Performance de Catálogo & Categorias com Atrito)
  - `03_roi_canais_e_comunicacao/` (Topologia de Canais, Custos & ROI Multiplicador de ~45x)
  - `04_matriz_motivos_segmentos_rfm/` (Causas-Raiz vs Segmentação RFM - Ratio 3x)
  - `05_matriz_viabilidade_recuperacao/` (Matriz Prescritiva de Viabilidade & Priorização)
  - `06_data_quality_e_quarentena/` (Governança & Quarentena Silver de Anomalias - Great Expectations 18 regras)
  - `07_arquitetura_dadosfera_vs_aws/` (Comparativo Arquitetural & -86% Lead Time)
  - `08_data_app_simulador_prescritivo_genai/` (Data App Streamlit & GenAI com LLMs)
- **Orquestrador Central (`run_all_pitch_charts.py`)**: Script funcional para execução ponta a ponta dos geradores visuais.

### ✅ 7. Arquitetura de Data Lakehouse & Catálogo de Metadados por Entidade (`pipelines/datalakes/`)
- **Arquitetura em 4 Camadas**: Estruturação formal do Lakehouse Medallion com Quarentena de Anomalias em:
  - **`raw/` (Bronze)**: Ingestão bruta e preservação integral *as-is* com replayability e rastreabilidade (`spec_datalake_raw_001`).
  - **`qualify/` (Silver)**: Limpeza técnica, padronização tipológica e execução de contratos rígidos (`spec_datalake_qualify_001`).
  - **`anomaly/` (Silver Quarentena de Anomalias - DEC-006)**: Isolamento de falhas contábeis e de negócio com diagnóstico de causa-raiz e severidades sem interrupção do pipeline (`spec_datalake_anomaly_001`).
  - **`curated/` (Gold Kimball - DEC-008)**: Modelagem dimensional analítica com medidas aditivas e cálculo de taxas em tempo de consulta (`spec_datalake_curated_001`).
- **Padrão Diretório por Entidade**: Organização de 28 subdiretórios individuais nas 4 camadas (`[entidade]_raw/`, `[entidade]_qualify/`, `[entidade]_anomalies/`, `[entidade]_curated/`), contendo o respectivo arquivo `metadata.md`.
- **Formato Híbrido e Texto Corrido Fluido**:
  - Cabeçalho YAML Frontmatter para leitura automatizada por parsers e integração de catálogo.
  - Narrativa em texto corrido abordando a visão de negócio, granularidade e papel da tabela na camada.
  - Referência única: todas as regras de tipos, chaves e restrições são citadas como **"validações declaradas no corpo da entidade"**, eliminando duplicação de dados ou schemas.
- **Atualização da Especificação Central do Catálogo**: [`data/catalogo/business-catalog-classification.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/business-catalog-classification.md) evoluído para a versão 2.0 (Active).

### ✅ 8. Gráficos de Insights de Negócio (`presentation/insights/`)
- **Objetivo**: Fornecer visualizações analíticas focadas para os insights de negócio do case de Carrinho Abandonado (`insights/`), com estética refinada (300 DPI, fundo branco `#FFFFFF`, curvas suaves spline e preenchimento de zonas coloridas `fill_between`), governadas pela **Fonte Canônica Master em `presentation/pitch/pitch_spec.md`**.
- **Módulos Concluídos (100% Ground Truth Parquet)**:
  - ✅ `01_descriptive/01_bi_recuperacao_carrinhos/`: Evolução temporal acumulada (início em 0 até 7.500 no topo), linha basal de compras diretas (1.731 un), resgate Dadosfera (498 un) e total comprado (2.229 un) com mini cards pareados 1-para-1.
  - ✅ `01_descriptive/02_motivos_abandono/`: Treemap proporcional de causas-raiz (5.231 un) e painel duplo de perda financeira bruta vs resgate Dadosfera (+R$ 173,7k).
  - ✅ `01_descriptive/03_custo_recuperacao_roi/`: Eficiência de CAC de resgate por canal (Email R$ 1,02, Push R$ 1,67, SMS R$ 3,00, WhatsApp R$ 12,00) e ROI multiplicador de ~45x.
  - ✅ `02_risk/01_segmentacao_risco/`: Matriz diagnóstica de risco (Score de Sessão vs RFM) e distribuição de volume/receita represada.
  - ✅ `03_prescriptive/01_estrategia_resgate_segmento/`: Simulador de viabilidade econômica líquida por canal/cluster RFM e matriz prescritiva de políticas.
  - ✅ `03_prescriptive/02_otimizacao_timing_envio/`: Curva de decaimento temporal de conversão (Decay Curve) com ponto ótimo de disparo em até +1h.
- **Orquestração**: Orquestrador em lote `presentation/insights/run_all_insights_charts.py` e comando integrado no Makefile `python make.py insights-charts`.

---

## 🗺️ Mapa Atualizado de Artefatos do Repositório

```text
wheels/
├── .agents/
│   ├── agents/                           # Definições de agentes (read-only)
│   │   ├── case-context-specialist.md    # Guardião estratégico do case
│   │   ├── project-context-specialist.md # Guardião técnico e memória do repo
│   │   ├── cart-recovery-insights.md     # Especialista em insights de negócio
│   │   ├── platform-registry-consultant.md # Guardião de Data Assets & IDs
│   │   ├── data-pipeline-documentation.md # Documentação & Lineage Medallion
│   │   └── declarative-functional-coding.md # Paradigma funcional e pipelines
│   └── skills/
│       ├── case-context-specialist/      # Skill: Requisitos, expectativas e specs
│       ├── project-context-specialist/   # (Esta skill) Memória técnica & progresso
│       ├── cart-recovery-insights/       # Skill: Especificação de insights
│       ├── data-pipeline-documentation/  # Skill: Documentação Medallion, DQ e Lineage
│       ├── data-strategy-analyst/        # Skill: Framework analítico Dadosfera
│       ├── datamaker/                    # Skill: Modelagem lógica e schemas
│       ├── declarative-functional-coding/ # Skill: Paradigma funcional & tipagem
│       ├── platform-registry-consultant/ # Skill: Mapeamento de Data Assets & IDs
│       └── scout/                        # Skill: Mapeamento de repositório
├── agents_prompts_refs/
│   ├── case-internship-files/            # Materiais do estágio (specs-internship.txt, user-case-raw-analyses.md)
│   ├── dadosfera-api/                    # Documentação técnica e endpoints da API Maestro
│   │   ├── output-mappers/               # assets_registry.md / assets_registry.json
│   │   └── endpoints/                    # Mapeamento detalhado de rotas
│   └── data_domain/                      # Contexto de negócio do case
├── data/
│   ├── data-models/logical/
│   │   ├── entities/                     # Modelagem Lógica Canônica (4 Divisões)
│   │   │   ├── blueprint-entities-archive.md # Blueprint canônico padronizado
│   │   │   ├── carrinhos.md              # Entidade carrinhos
│   │   │   ├── clientes.md               # Entidade clientes
│   │   │   ├── produtos.md               # Entidade produtos
│   │   │   ├── itens_carrinho.md         # Entidade itens_carrinho
│   │   │   ├── eventos_carrinho.md       # Entidade eventos_carrinho
│   │   │   ├── eventos_resgate.md        # Entidade eventos_resgate
│   │   │   └── pedidos.md                # Entidade pedidos
│   │   ├── relationships.md              # Cardinalidades e grafo ERD
│   │   └── business-rules.md             # Master SSOT de Regras de Negócio, Invariantes e Lógicas de BI
│   ├── catalogo/
│   │   ├── business-catalog-classification.md # Especificação v2.0 do Catálogo & Lakehouse
│   │   └── qualify/                      # Dicionários de dados da camada Qualify
│   ├── mock/
│   │   ├── generators/parquet/           # Gerador modular (config/, core/, modules/, run_all.py)
│   │   ├── output/{parquet,csv}/         # Datasets brutos com 115k+ linhas geradas
│   │   ├── output_cleaned/{parquet,csv}/ # Datasets higienizados e scripts de limpeza
│   │   └── METRICS.md                    # Metadados, perfis e cotas determinísticas de anomalias
│   └── relatorio-etapa1.md              # Relatório de entrega da Etapa 1
├── pipelines/
│   ├── datalakes/                        # Arquitetura Lakehouse & Catálogo por Entidade
│   │   ├── README.md                     # Visão Geral das 4 Camadas
│   │   ├── raw/                          # Bronze: spec.md + 7 pastas com metadata.md
│   │   ├── qualify/                      # Silver: spec.md + 7 pastas com metadata.md
│   │   ├── anomaly/                      # Quarentena DEC-006: spec.md + 7 pastas com metadata.md
│   │   └── curated/                      # Gold Kimball: spec.md + 7 pastas com metadata.md
│   ├── case-item-03/                     # Catalogação e Exploração na Dadosfera
│   ├── case-item-04/                     # Data Quality Pipeline (Notebook + Specs + Report)
│   └── case-item-06/                     # Modelagem Dimensional Kimball (DW Gold)
├── insights/
│   ├── 01_descriptive/                   # Insights descritivos (conversão, volume)
│   ├── 02_risk/                          # Insights de risco (abandono por atrito)
│   ├── 03_prescriptive/                  # Insights prescritivos (melhor canal/timing)
│   └── 04_opportunity/                   # Insights de oportunidade (otimização de receita)
├── presentation/
│   ├── pitch/                            # Infraestrutura completa da apresentação (Item 10)
│   │   ├── README.md                     # Visão geral e índice de navegação
│   │   ├── pitch_spec.md                 # Backbone Central & Guidelines de Apresentação
│   │   ├── run_all_pitch_charts.py       # Orquestrador central dos geradores
│   │   ├── config/chart_theme.py         # Tema visual corporativo Dadosfera (300 DPI)
│   │   └── 01 a 08/                      # Módulos com spec, script e chart
│   └── insights/                         # Gráficos e visualizações dos insights de negócio
│       ├── README.md                     # Galeria de gráficos de insights
│       ├── run_all_insights_charts.py    # Orquestrador em lote de insights
│       └── 01_bi_recuperacao_carrinhos/  # Spec + Script + Gráfico BI (curvas, fundo branco, fill_between)
└── docs/relatorios/
    ├── decision-making/                  # DEC-007, DEC-008
    └── pitch/
        └── decision-making/              # pitch.txt, relatorio-pitch-01.md
```

---

## 🧭 Decisões Arquiteturais e Estratégicas Ativas

- **DEC-001 (Pitch Ancorado em %)**: Foco em taxas, ratios e eficiência relativa para máxima transferibilidade de valor.
- **DEC-002 (Base Mock Sintética Própria)**: 116k+ registros aderentes ao domínio com dirty data controlado (5%).
- **DEC-003 (Insights em Markdown)**: Especificações desacopladas da implementação física.
- **DEC-004 (Proibição de .SQL Locais)**: Criação e execução de views/queries analíticas restritas à plataforma Dadosfera.
- **DEC-005 (Governança Maestro API)**: Token JWT sem prefixo Bearer e isolamento de duplicatas órfãs via PUT.
- **DEC-006 (Dual-Artifact Pipeline & 4-Division Blueprint)**: Bifurcação Silver (`[entidade]_qualify` vs `[entidade]_anomalies`) com fronteira clara entre Plataforma (evidência/detecção) e Domínio (resolução/ação), com `## SCHEMA RULES` numerados e booleanos padronizados em `TRUE`/`FALSE`.
- **DEC-007 (Taxas Quebradas e Distribuições Naturais no Mock Engine)**: Adoção de percentuais fracionários não-redondos em `config/settings.py` e `core/anomaly_engine.py` para máxima verossimilhança estatística de telemetria nos dashboards e Data Apps.
- **DEC-008 (Kimball Star Schema por Simplicidade e Performance)**: Adoção do modelo dimensional Kimball (6 dimensões conformadas, 2 fatos granulares e 2 visões analíticas Gold) na camada Gold, eliminando complexidade desnecessária de Data Vault e maximizando a performance analítica para Metabase (Item 7) e Streamlit (Item 9).

---

## 📋 Diretrizes para Agentes
1. **Consulta Obrigatória**: Consulte esta skill para entender o estado técnico do repositório e o alinhamento com as etapas do case.
2. **Separação de Contexto**:
   - Para *requisitos, critérios de avaliação e expectativas da empresa*, use `case-context-specialist`.
   - Para *estado atual dos arquivos, schemas e decisões arquiteturais do repositório*, use `project-context-specialist`.
3. **Execução sem SQL Local (DEC-004)**: Não crie novos arquivos `.sql` locais. Todas as consultas e transformações devem ser projetadas para a plataforma Dadosfera.
4. **Respeito ao Blueprint (DEC-006)**: Qualquer ajuste ou nova entidade deve obrigatoriamente cumprir o formato de 4 divisões com `SCHEMA RULES` numerados e booleanos padronizados.
