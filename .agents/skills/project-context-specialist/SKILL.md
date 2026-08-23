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
| **4** | Data Quality & Anomalias | Processar | Pipeline de qualificação dual-artifact (`notebooks/pipelines/quality_report/qualification_raw.ipynb` e `pipeline_spec.md`), suíte Great Expectations (18 regras), quarentena de anomalias em Parquet e relatório gerado (`notebooks/pipelines/quality_report/outputs/data_quality_report.md`) | ✅ Concluído |
| **5** | GenAI & LLMs | Processar | Geração de copies persuasivas e enriquecimento semântico de motivos de abandono | ⏳ Planejado |
| **6** | Modelagem de Dados | Analisar | Modelagem lógica completa em 6 entidades sob o **Blueprint Canônico de 4 Divisões** com `## SCHEMA RULES` numerados e booleanos padronizados | ✅ Concluído |
| **7** | Análise de Dados & Métricas | Analisar | 6 visualizações de BI geradas (Série Temporal, Categorias, ROI, Heatmap, Scatter e DQ), script reproduzível (`pipelines/serving/generate_bi_charts.py`), catálogo declarativo (`chart_specs.py`), notebook (`07_bi_dashboards_visualizations.ipynb`) e task runner CLI (`notebook-gen`) | ✅ Concluído |
| **8** | Pipelines ETL/ML | Processar | Especificações de pipeline Silver (Qualify + Anomaly) e framework normativo (`data-pipeline-documentation`) | ⏳ Planejado |
| **9** | Data Apps | Consumir | Planejamento de Data App interativo em Streamlit para simulação de recuperação de carrinhos e cálculo de ROI | ⏳ Planejado |
| **10** | Apresentação em Vídeo | — | Roteiro de pitch ancorado em métricas de eficiência (DEC-001) e comparativo com stack legada AWS | ⏳ Planejado |
| **Bônus**| GenAI + Data Apps | IA Generativa | Geração visual de cards de produtos e vitrines dinâmicas de resgate | ⏳ Planejado |

---

## 📈 Histórico Detalhado de Etapas Concluídas

### ✅ 1. Modelagem de Dados Lógica Canônica (Item 6)
Todas as **6 entidades** do modelo de dados lógico foram reformuladas sob o padrão canônico de 4 divisões em `data/data-models/logical/entities/`:
- **`blueprint-entities-archive.md`**: Padrão canônico documentado com 4 divisões, `## SCHEMA RULES` numerado e padronização `TRUE`/`FALSE`.
- **`carrinhos.md`**: Transacional de sessão, ciclo de vida, 7 schema rules, 5 business rules, detecção de 4 anomalias e roteamento para `carrinhos_anomalies`.
- **`clientes.md`**: Cadastro mestre, conformidade LGPD (opt-ins de e-mail, SMS, push), métricas RFM, LTV, 8 schema rules e 5 business rules.
- **`produtos.md`**: Catálogo de SKUs, precificação atual/original, estoque, 4 schema rules e 5 business rules.
- **`itens_carrinho.md`**: Linhas de produtos adicionados ao carrinho, snapshot imutável de preço, conciliação de subtotal e rastreio de remoção de itens.
- **`eventos_carrinho.md`**: Telemetria comportamental de funil (`view_produto` a `retorno`), alta volumetria (`BIGINT`), payload semiestruturado `JSONB`/`VARIANT`.
- **`eventos_resgate.md`**: Régua de mensageria multicanal (E-mail, SMS, Push, WhatsApp), controle de 4 toques, cancelamento pós-conversão e cálculo de ROI.
- **`pedidos.md`**: Fechamento financeiro da conversão (relação 1:1 estrita com carrinho), meios de pagamento e atribuição de receita recuperada.

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
  - `notebooks/pipelines/quality_report/qualification_raw.ipynb`: Notebook executável e compatível com Google Colab aplicando regras sobre as 7 entidades lendo Parquet.
  - `notebooks/pipelines/quality_report/pipeline_spec.md`: Especificação normativa e documentação técnica do pipeline.
  - `notebooks/pipelines/quality_report/outputs/data_quality_report.md`: Relatório e evidências geradas de forma autocontida pelo notebook/pipeline.
  - `quality/expectations/carrinhos_suite.json` e `quality/results/validation_results.json`: Suite formal e evidências estruturadas.
- **Arquitetura Dual-Artifact (DEC-006)**: Bifurcação entre registros aprovados (`output/qualify/*.parquet` com 94.2% de conformidade) e quarentena (`output/anomalies/*.parquet` com 5.8% de registros isolados com `anomaly_reason`).

### ✅ 5. Visualizações de BI, Dashboards & CLI Runner (Item 7)
- **6 Visualizações de BI Geradas**: Série Temporal, Performance de Categorias, ROI por Canal, Heatmap RFM, Dispersão de Viabilidade e Scorecard de Data Quality salvas em `dashboards/assets/` em alta definição (300 DPI).
- **Catálogo Declarativo (`chart_specs.py`)**: Mapeamento estruturado de cada view/gráfico permitindo seleção dinâmica via chave string.
- **Task Runner Multiplataforma (`make.py` / `notebook-gen`)**: Automação por CLI permitindo rodar `.\notebook-gen` ou `python make.py notebook-gen [chart_key]`.

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
│   ├── case-internship-files/            # Materiais oficiais do estágio (specs-internship.txt)
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
│   │   └── business-rules.md             # Regras de negócio globais
│   ├── catalogo/qualify/                 # Dicionários de dados da camada Qualify
│   ├── mock/
│   │   ├── generators/parquet/           # Gerador modular (config/, core/, modules/, run_all.py)
│   │   ├── output/{parquet,csv}/         # Datasets com 115k+ linhas geradas
│   │   └── METRICS.md                    # Metadados, perfis e cotas determinísticas de anomalias
│   └── relatorio-etapa1.md              # Relatório de entrega da Etapa 1
├── insights/
│   ├── 01_descriptive/                   # Insights descritivos (conversão, volume)
│   ├── 02_risk/                          # Insights de risco (abandono por atrito)
│   ├── 03_prescriptive/                  # Insights prescritivos (melhor canal/timing)
│   └── 04_opportunity/                   # Insights de oportunidade (otimização de receita)
└── relatorios/decision-making/pitch/     # Decision records estratégicos
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

---

## 📋 Diretrizes para Agentes
1. **Consulta Obrigatória**: Consulte esta skill para entender o estado técnico do repositório e o alinhamento com as etapas do case.
2. **Separação de Contexto**:
   - Para *requisitos, critérios de avaliação e expectativas da empresa*, use `case-context-specialist`.
   - Para *estado atual dos arquivos, schemas e decisões arquiteturais do repositório*, use `project-context-specialist`.
3. **Execução sem SQL Local (DEC-004)**: Não crie novos arquivos `.sql` locais. Todas as consultas e transformações devem ser projetadas para a plataforma Dadosfera.
4. **Respeito ao Blueprint (DEC-006)**: Qualquer ajuste ou nova entidade deve obrigatoriamente cumprir o formato de 4 divisões com `SCHEMA RULES` numerados e booleanos padronizados.
