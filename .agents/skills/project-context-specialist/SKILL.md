---
name: project-context-specialist
description: Fonte central de contexto, progresso e memória do case de Recuperação de Carrinho Abandonado (Marketplace). Mapeia etapas concluídas, decisões arquiteturais, schemas e próximos passos do projeto.
---

# Skill: Project Context Specialist

## 🎯 Objetivo & Missão
Atuar como a **fonte central de contexto e memória viva do projeto**. Esta skill armazena o histórico do case de Recuperação de Carrinho Abandonado (Marketplace), suas etapas, artefatos gerados, decisões arquiteturais e progressão contínua.

---

## 📌 Visão Geral do Case
- **Domínio**: E-commerce / Marketplace.
- **Carro-Chefe do Pitch**: Case de **Recuperação de Carrinho Abandonado** como demonstração direta de valor (ROI e conversão).
- **Prazo Executivo**: Entrega em 2 dias.
- **Tecnologias**: PostgreSQL 15+, Python (Pandas/PyArrow/Faker), Parquet, CSV, Metabase/BI, Streamlit/Dadosfera.

---

## 📈 Histórico de Etapas & Progresso do Projeto

### ✅ Etapa 1 — Modelagem Lógica & DDL SQL
- **Entidades Normalizadas (7)**: `clientes`, `produtos`, `carrinhos`, `itens_carrinho`, `eventos_carrinho`, `eventos_resgate`, `pedidos`.
- **SQL DDL**: Scripts em `data/database/sql/` (`001_create_tables.sql`, `002_constraints.sql`, `003_indexes.sql`, `004_views.sql`).
- **Relatório**: Documentado em `data/relatorio-etapa1.md`.

### ✅ Etapa 2 — Mapeamento & Gerador de Dados Mock (Parquet & CSV)
- **Pipelines Python**: Desenvolvidos em `data/mock/generators/parquet/` (`run_all.py`, `_config.py`).
- **Volume Gerado**: **116.526 registros por formato** (ultrapassando os 105k requeridos).
- **Diretórios de Saída**: `data/mock/output/parquet/` e `data/mock/output/csv/`.
- **Métricas do Dataset**: Taxa de Abandono ~70,9%, Taxa de Recuperação ~10,1%, ROI ~32,5x ([METRICS.md](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/mock/METRICS.md)).

### ⏳ Etapa 3 — Insights, Análises Preditivas/Prescritivas & Métricas de Negócio
- Elaborar análises descritivas, diagnósticas, preditivas e prescritivas em texto corrido para catalogação.
- Especificar métricas de negócio, entidades relacionadas e tomada de decisão.
- Gerar artefatos e views com base nas especificações.

### ⏳ Etapa 4 — Pipeline de Dados & Limpeza (Data Engineering)
- Implementar fluxo de ETL/ELT, tratamento de dados dirty (5% anomalias temporais/preços) e preparação para produção.

---

## 🗺️ Mapa de Artefatos & Estrutura do Repositório

```text
wheels/
├── .agents/
│   └── skills/
│       ├── datamaker/                 # Skill de modelagem e schemas
│       ├── scout/                     # Skill de mapeamento e leitura prévia
│       ├── data-strategy-analyst/     # Skill de consultoria analítica Dadosfera
│       └── project-context-specialist/# (Esta skill) Contexto e memória do case
├── data/
│   ├── models/logical/                # Entidades, cardinalidades e business rules
│   ├── database/sql/                  # DDL PostgreSQL (001 a 004)
│   ├── mock/
│   │   ├── generators/parquet/        # Scripts geradores em Python
│   │   └── output/
│   │       ├── parquet/               # 116.526 registros (.parquet)
│   │       └── csv/                   # 116.526 registros (.csv)
│   └── relatorio-etapa1.md            # Consolidado da Etapa 1
├── relatorios/decision-making/        # Pitch de vendas e árvore de decisão
└── agents_prompts_refs/               # Relatórios scout e prompts de domínio
```

---

## 📋 Diretrizes para Agentes
1. **Consulta Obrigatória**: Consulte esta skill antes de iniciar novos módulos para garantir alinhamento com o estado atual do projeto.
2. **Atualização Contínua**: Ao concluir uma nova etapa ou decisão arquitetural significativa, registre o avanço na seção de *Histórico de Etapas*.
