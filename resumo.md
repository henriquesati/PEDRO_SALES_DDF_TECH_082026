# 🗺️ Resumo da Topologia Arquitetural e Artefatos do Repositório

Documento normativo de mapeamento topológico por diretórios do projeto **Recuperação de Carrinho Abandonado (Marketplace / Dadosfera)**. Esta estrutura elimina a redundância de caminhos lineares, agrupando cadernos interativos (`.ipynb`), especificações normativas (`specs.md`), scripts de execução em lote (`.py`) e componentes de software conforme sua localização física e hierarquia de responsabilidade no ecossistema.

---

## 📁 1. `pipelines/` — Pipelines de Dados, Notebooks e Especificações por Item

A pasta [`pipelines/`](pipelines/) centraliza o ciclo de engenharia de dados, qualidade, inteligência artificial e visualizações correspondentes a cada requisito normativo do Case Dadosfera.

```
pipelines/
├── case-item-03/  # Ingestão e Geração de Dados Sintéticos
├── case-item-04/  # Data Quality, Quarentena e Great Expectations
├── case-item-05/  # GenAI, Extração de Features e Bônus Multimodal
├── case-item-06/  # Modelagem Dimensional Kimball DW Gold
├── case-item-07/  # BI, Dashboards Metabase e Análise de Dados
├── case-item-08/  # Pipeline Medallion, Snowpark e Stepsfera
└── case-item-09/  # Data App Streamlit e Runner Colab
```

### 📂 [`pipelines/case-item-03/`](pipelines/case-item-03/) — Ingestão, Sintéticos & Catálogo (Item 3)
*Geração dos +115k registros sintéticos com injeção controlada de ruído (dirty data) nas 7 entidades relacionais.*
- [`specs.md`](pipelines/case-item-03/specs.md): Especificação técnica normativa (`spec_data_generation_001`) da camada Bronze e regras de geração.
- Execução rápida: `python make.py mock-gen`

### 📂 [`pipelines/case-item-04/`](pipelines/case-item-04/) — Data Quality & Quarentena (Item 4)
*Auditoria de conformidade, isolamento de anomalias em quarentena e relatórios de integridade com Great Expectations.*
- [`notebooks/qualification_raw.ipynb`](pipelines/case-item-04/notebooks/qualification_raw.ipynb): Notebook oficial de qualificação, auditoria e Data Quality.
- [`specs.md`](pipelines/case-item-04/specs.md): Especificação normativa (`spec_data_quality_001`) do pipeline de qualidade e regras de quarentena.
- [`scripts/run_quality_pipeline.py`](pipelines/case-item-04/scripts/run_quality_pipeline.py): Script batch de auditoria e geração dos relatórios JSON/HTML.
- Execução rápida: `python make.py quality-eval`

### 📂 [`pipelines/case-item-05/`](pipelines/case-item-05/) — GenAI, Pydantic & Extração Multimodal (Item 5)
*Extração semântica de features não-estruturadas, transcrição de áudio com Whisper e validação de schema.*
- [`notebooks/genai_feature_extraction.ipynb`](pipelines/case-item-05/notebooks/genai_feature_extraction.ipynb): Notebook executável Google Colab com pipeline LLM e transcrição Whisper.
- [`specs.md`](pipelines/case-item-05/specs.md): Especificação técnica normativa (`spec_genai_llm_001` v1.0) do pipeline GenAI.
- [`scripts/run_genai_pipeline.py`](pipelines/case-item-05/scripts/run_genai_pipeline.py): Script batch de enriquecimento semântico e geração de copies.
- Execução rápida: `python make.py genai-extract`

### 📂 [`pipelines/case-item-06/`](pipelines/case-item-06/) — Modelagem Dimensional Kimball Gold DW (Item 6)
*Star Schema analítico composto por 6 dimensões conformadas, 2 fatos de negócio e 2 visões analíticas Gold.*
- [`notebooks/data_modeling_kimball.ipynb`](pipelines/case-item-06/notebooks/data_modeling_kimball.ipynb): Notebook interativo de validação dimensional e cruzamento de grãos.
- [`specs.md`](pipelines/case-item-06/specs.md): Especificação técnica formal (`spec_data_modeling_001`) do Data Warehouse Kimball.
- [`scripts/generate_chart.py`](pipelines/case-item-06/scripts/generate_chart.py): Script gerador do painel dimensional no padrão visual `charts-maker`.
- Execução rápida: `python make.py data-modeling`

### 📂 [`pipelines/case-item-07/`](pipelines/case-item-07/) — BI, Dashboards Metabase & Camada Semântica (Item 7)
*Central de inteligência visual com as 6 visualizações executivas de BI, métricas de conversão e consultas Metabase SQL.*
- [`notebooks/07_bi_dashboards_visualizations.ipynb`](pipelines/case-item-07/notebooks/07_bi_dashboards_visualizations.ipynb): Notebook executável Google Colab para renderização dos gráficos e KPIs.
- [`specs.md`](pipelines/case-item-07/specs.md): Especificação técnica normativa (`spec_bi_visualizations_001` v1.0) dos dashboards.
- [`scripts/run_bi_analysis.py`](pipelines/case-item-07/scripts/run_bi_analysis.py): Script batch gerador dos 6 gráficos analíticos e resumo JSON de métricas.
- Execução rápida: `python make.py bi-analysis` ou `python make.py notebook-gen`

### 📂 [`pipelines/case-item-08/`](pipelines/case-item-08/) — Pipeline Medallion, Snowpark & Stepsfera (Item 8)
*Transformações automatizadas Bronze -> Silver -> Gold utilizando Snowpark/PySpark, modelo preditivo e Stepsfera.*
- [`notebooks/pipeline_snowpark_transformation.ipynb`](pipelines/case-item-08/notebooks/pipeline_snowpark_transformation.ipynb): Notebook executável do pipeline Medallion integrado.
- [`specs.md`](pipelines/case-item-08/specs.md): Especificação técnica formal (`spec_pipeline_orchestration_001`) e catálogo Stepsfera.
- [`scripts/run_silver_gold_pipeline.py`](pipelines/case-item-08/scripts/run_silver_gold_pipeline.py): Orquestrador do pipeline de transformação e treinamento de ML.
- [`scripts/generate_lakehouse_catalog_json.py`](pipelines/case-item-08/scripts/generate_lakehouse_catalog_json.py): Gerador do catálogo JSON estruturado do Lakehouse.
- Execução rápida: `python make.py pipeline-run`

### 📂 [`pipelines/case-item-09/`](pipelines/case-item-09/) — Data App Streamlit & Runner Colab (Item 9 & Bônus)
*Ambiente de execução e empacotamento do Data App interativo com túnel público Cloudflare/Localtunnel.*
- [`notebooks/streamlit_colab_runner.ipynb`](pipelines/case-item-09/notebooks/streamlit_colab_runner.ipynb): Notebook Google Colab para bootstrap do Streamlit em nuvem.
- [`specs.md`](pipelines/case-item-09/specs.md): Especificação técnica formal (`spec_data_app_streamlit_001` v1.0) do Data App.
- [`scripts/run_app_locally.py`](pipelines/case-item-09/scripts/run_app_locally.py): Script utilitário para inicialização local do Streamlit.
- [`scripts/export_app_assets.py`](pipelines/case-item-09/scripts/export_app_assets.py): Exportador de assets visuais compilados para a aplicação.
- Execução rápida: `python make.py data-app`

---

## 📁 2. `app/` — Data App Interativo Streamlit (5 Camadas)

A pasta [`app/`](app/) implementa a interface executiva e técnica do projeto em Streamlit puro, orientada pelo skill `streamlit-master` em arquitetura modular desacoplada.

```
app/
├── app.py              # Ponto de entrada (Entrypoint)
├── views/              # Camada de Apresentação (Abas de Negócio e Telas)
├── components/         # Camada de Componentes Reutilizáveis de UI/UX
├── services/           # Camada de Serviços, Lógica de Negócio e ML
└── constants/          # Constantes Globais, Cores e Temas
```

- [`app.py`](app/app.py): Ponto de entrada com orquestração de rotas, estado de sessão e injeção de CSS customizado.
- **Camada de Visões ([`app/views/`](app/views/)):**
  - [`view_hub_landing.py`](app/views/view_hub_landing.py): Hub central de boas-vindas e roteamento para personas técnicas e executivas.
  - [`view_business_dashboard.py`](app/views/view_business_dashboard.py): Dashboard executivo de métricas de negócio e taxas de abandono.
  - [`tab_roi.py`](app/views/tab_roi.py): Simulador interativo de ROI e sensibilidade de conversão em tempo real.
  - [`tab_similarity.py`](app/views/tab_similarity.py): Visualizador de projeção dimensional t-SNE e similaridade semântica de produtos.
  - [`tab_showcase.py`](app/views/tab_showcase.py): Vitrine interativa de enriquecimento semântico e geração de copies com LLMs.
  - [`tab_agents.py`](app/views/tab_agents.py): Central de controle, monitoramento e combate de agentes autônomos.
  - [`tab_copilot.py`](app/views/tab_copilot.py): Copilot analítico assistido por IA generativa para exploração em linguagem natural.
- **Camada de Componentes ([`app/components/`](app/components/)):**
  - [`fighter_select.py`](app/components/fighter_select.py): Seletor visual estilo arcade para confronto e seleção de agentes.
  - [`business_header.py`](app/components/business_header.py): Cabeçalho padrão corporativo com métricas de topo e badges de status.
  - [`charts.py`](app/components/charts.py): Fábrica de componentes de visualização gráfica Plotly/Altair.
  - [`insights_view.py`](app/components/insights_view.py): Renderizador modular de cards analíticos de negócio.
  - [`kpi_cards.py`](app/components/kpi_cards.py): Cards de KPIs com cálculo de delta e formatação monetária.
- **Camada de Serviços ([`app/services/`](app/services/)):**
  - [`agents_service.py`](app/services/agents_service.py): Engine de orquestração, prompts, combate e telemetria de agentes.
  - [`simulation_service.py`](app/services/simulation_service.py): Motor matemático de simulação de ROI e cálculo de viabilidade financeira.
  - [`similarity_service.py`](app/services/similarity_service.py): Serviço de projeção t-SNE e busca por vizinhos próximos (KNN).
  - [`ml_service.py`](app/services/ml_service.py): Inferência em tempo real dos modelos preditivos de propensão ao abandono.
  - [`copy_service.py`](app/services/copy_service.py): Motor de geração de copies persuasivas e templates de resgate.
  - [`insights_service.py`](app/services/insights_service.py): Provedor de dados agregados e insights estruturados para o Data App.

---

## 📁 3. `presentation/pitch/` — Apresentação Executiva & Roteiro do Pitch (Item 10)

A pasta [`presentation/pitch/`](presentation/pitch/) reúne o material executivo de defesa da solução, roteiro cronometrado e orquestradores de painéis visuais.

```
presentation/pitch/
├── pitch_spec.md             # Especificação Técnica do Pitch e Storytelling
├── roteiro.txt               # Roteiro Cronometrado (6 Minutos)
├── README.md                 # Guia Geral de Apresentação
└── run_all_pitch_charts.py   # Orquestrador de Geração dos 8 Gráficos do Pitch
```

- [`pitch_spec.md`](presentation/pitch/pitch_spec.md): Especificação executiva e técnica descrevendo a arquitetura do pitch, slides e métricas financeiras.
- [`roteiro.txt`](presentation/pitch/roteiro.txt): Guia de fala e roteiro verbal cronometrado para apresentação em banca de estágio.
- [`run_all_pitch_charts.py`](presentation/pitch/run_all_pitch_charts.py): Orquestrador que gera os 8 painéis e gráficos analíticos de suporte à apresentação.
- Execução rápida: `python make.py pitch`

---

## 📁 4. `insights/` — Motores de Insights Analíticos de Negócio

A pasta [`insights/`](insights/) contém a especificação metodológica e os scripts de cálculo dos 14+ insights estruturados em 4 dimensões analíticas.

```
insights/
├── 01_descriptive/       # Diagnóstico, Volume e Motivos de Abandono
├── 02_risk/              # Segmentação de Risco e LTV
├── 03_prescriptive/      # Estratégias de Resgate, Timing e ROI
├── 04_intelligence_ai/   # Modelos Preditivos, GenAI e Similaridade
└── run_all_insights_charts.py  # Orquestrador de Geração de Gráficos de Insights
```

- **01. Diagnóstico Descritivo ([`insights/01_descriptive/`](insights/01_descriptive/)):**
  - [`taxa_volume_abandono.md`](insights/01_descriptive/taxa_volume_abandono.md): Análise de volume diário e taxa macro de abandono (77,8%).
  - [`motivos_abandono.md`](insights/01_descriptive/motivos_abandono.md): Levantamento e ranqueamento das principais causas de desistência de compra.
  - [`custo_recuperacao_roi.md`](insights/01_descriptive/custo_recuperacao_roi.md): Equação de custo de aquisição vs. custo de recuperação.
- **02. Avaliação de Risco ([`insights/02_risk/`](insights/02_risk/)):**
  - [`segmentacao_risco_abandono.md`](insights/02_risk/segmentacao_risco_abandono.md): Matriz de criticidade e propensão de churn.
  - [`ltv_vs_abandono.md`](insights/02_risk/ltv_vs_abandono.md): Impacto do abandono em clientes de alto e baixo Lifetime Value.
  - [`viabilidade_recuperacao_carrinho.md`](insights/02_risk/viabilidade_recuperacao_carrinho.md): Filtros de margem para acionamento lucrativo.
- **03. Ações Prescritivas ([`insights/03_prescriptive/`](insights/03_prescriptive/)):**
  - [`estrategia_resgate_segmento.md`](insights/03_prescriptive/estrategia_resgate_segmento.md): Ações recomendadas por perfil de usuário.
  - [`otimizacao_timing_envio.md`](insights/03_prescriptive/otimizacao_timing_envio.md): Janelas ideais de disparo (30min a 2h).
  - [`produtos_mais_abandonados.md`](insights/03_prescriptive/produtos_mais_abandonados.md): Categorias com maior fricção no checkout.
  - [`roi_campanhas_resgate.md`](insights/03_prescriptive/roi_campanhas_resgate.md): Projeção de retorno financeiro sobre campanhas de resgate.
- **04. Inteligência & IA ([`insights/04_intelligence_ai/`](insights/04_intelligence_ai/)):**
  - [`spec.md`](insights/04_intelligence_ai/spec.md): Especificação de modelos preditivos, embeddings e simuladores.
  - [`generate_chart.py`](insights/04_intelligence_ai/generate_chart.py): Script de renderização do painel consolidado de IA.
- **Orquestrador Central:** [`run_all_insights_charts.py`](insights/run_all_insights_charts.py) (`python make.py insights-charts`).

---

## 📁 5. `dashboards/` & `metrics/` — Camada Semântica, KPIs & Metabase

Centralização das regras formais de métricas, catálogos de indicadores e definições para visualização no Metabase.

- [`dashboards/dashboard_recuperacao_carrinho.md`](dashboards/dashboard_recuperacao_carrinho.md): Especificação completa do painel Metabase com perguntas SQL, filtros e layouts.
- [`metrics/catalogo_kpis.md`](metrics/catalogo_kpis.md): Catálogo de KPIs de negócio (Taxa de Abandono, Taxa de Recuperação, Ticket Médio, ROI).
- [`metrics/arvore_metricas_driver_tree.md`](metrics/arvore_metricas_driver_tree.md): Driver Tree decompondo a receita recuperável em alavancas operacionais.
- [`metrics/matriz_metricas_dimensoes.md`](metrics/matriz_metricas_dimensoes.md): Matriz de granularidade cruzando métricas contra as dimensões Kimball.
- [`metrics/metricas_data_quality_slo.md`](metrics/metricas_data_quality_slo.md): SLOs e SLAs de qualidade de dados na camada Silver.
- [`metrics/metricas_ml_genai.md`](metrics/metricas_ml_genai.md): Métricas de acurácia, ROC-AUC e tempo de inferência dos modelos.

---

## 📁 6. `data/` — Modelagem de Dados, Schemas SQL & Datalake

Estrutura de dados relacional e dimensional que alimenta o ecossistema.

- **Schemas e DDLs ([`data/database/sql/`](data/database/sql/)):**
  - [`001_create_tables.sql`](data/database/sql/001_create_tables.sql): DDL completo das tabelas relacionais do Marketplace.
  - [`002_constraints.sql`](data/database/sql/002_constraints.sql): Chaves primárias, estrangeiras e regras de integridade referencial.
  - [`003_indexes.sql`](data/database/sql/003_indexes.sql): Estratégia de indexação para consultas analíticas de alta performance.
  - [`004_views.sql`](data/database/sql/004_views.sql): Camada de visões SQL consolidadas para consumo em BI.
- **Catálogo de Metadados ([`data/catalogo/qualify/`](data/catalogo/qualify/)):** Dicionários de dados detalhados para cada entidade (`clientes.md`, `produtos.md`, `carrinhos.md`, `itens_carrinho.md`, `eventos_carrinho.md`, `pagamentos.md`, `notificacoes_resgate.md`).

---

## 📁 7. `agents_prompts_refs/` — Registro de Ativos Dadosfera & Prompts de IA

Mapeamentos oficiais de infraestrutura na plataforma Dadosfera e templates para os agentes inteligentes.

- [`agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md`](agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md): Mapeamento oficial dos **7 Data Asset IDs**, links diretos na plataforma Dadosfera e volumetria real.
- [`agents_prompts_refs/case-internship-files/`](agents_prompts_refs/case-internship-files/): Documentos de requisitos originais do processo seletivo.

---

## ⚡ 8. Guia Unificado de Comandos do Task Runner (`make.py`)

Abaixo estão os comandos diretos para executar qualquer pipeline ou gerar artefatos a partir da raiz:

| Comando | Descrição do Pipeline / Ação | Item do Case |
| :--- | :--- | :---: |
| `python make.py mock-gen` | Gera +115k dados sintéticos nas 7 entidades Bronze | **Item 3** |
| `python make.py quality-eval` | Executa a suíte de auditoria Great Expectations e Quarentena | **Item 4** |
| `python make.py genai-extract` | Executa extração semântica com Pydantic e Whisper | **Item 5** |
| `python make.py data-modeling` | Deriva o DW Kimball Gold (6 dims / 2 fatos) e gera dashboard | **Item 6** |
| `python make.py bi-analysis` | Processa e renderiza as 6 visualizações de BI executivas | **Item 7** |
| `python make.py pipeline-run` | Executa o pipeline Medallion Snowpark e modelo de ML | **Item 8** |
| `python make.py data-app` | Inicializa a aplicação Streamlit interativa | **Item 9** |
| `python make.py pitch` | Compila e gera os 8 gráficos da apresentação de Pitch | **Item 10** |
| `python make.py insights-charts` | Gera todos os gráficos analíticos da pasta `insights/` | **Transversal** |
| `python make.py all` | Executa a regeneração de todos os pipelines e gráficos | **Geral** |
