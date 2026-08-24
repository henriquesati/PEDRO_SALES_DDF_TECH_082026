---
name: datamaker
description: >-
  Creates and organizes data models and schema definitions, including database
  schemas, SQL/DDL structures, relationships, and data-model files. Utilizes python scripts to generate realistic mock datasets that should represent real business data. Use this skill when the user requests database modeling, schema
  definition, structuring of data entities and it's relationships, files and directories structure related to the topic.
---

# DataMaker Skill

The **DataMaker** skill is responsible for modeling business data entities, defining schemas (such as SQL/DDL structures, relationships, and ORM/data-model definitions), specific schemas per database type, and organizing directories and files related to database architecture. Additionally, it leverages **Python scripts** to generate realistic mock datasets that as close to reality as possible represent real-world business data.

---

## 1. Recommended Directory Structure

The structure begins with technology-agnostic logical modeling in Markdown under `data/data-models/logical/`, followed by concrete database implementations (`data/database/`) and mock data generation scripts (`data/mock/`):

```text
data/
├── data-models/
│   └── logical/
│       ├── entities/
│       │   ├── blueprint-entities-archive.md # Canonical 4-division entity blueprint
│       │   ├── carrinhos.md                  # Attribute definitions, anomalies, validations
│       │   ├── clientes.md
│       │   └── produtos.md
│       ├── relationships.md                  # Cardinalities & ER associations
│       └── business-rules.md                 # Domain rules, validation, constraints
│
├── database/
│   ├── sql/
│   │   ├── 001_create_tables.sql
│   │   ├── 002_constraints.sql
│   │   └── 003_indexes.sql
│   └── nosql/                                # (Optional) Specialized schemas
│
└── mock/
    ├── generators/parquet/                   # Geradores modulares em Python
    │   ├── config/                           # Constantes, settings e perfis (standard, rich, dev)
    │   ├── core/                             # BaseGenerator e AnomalyEngine determinístico
    │   ├── modules/                          # Módulos por entidade (clientes, produtos, carrinhos...)
    │   └── run_all.py                        # Orquestrador CLI com suporte a perfis e cotas
    └── output/                               # Datasets gerados (parquet/, csv/)
```

---

## 2. Workflow & Procedure

When requested to create or update data models and schemas:

0. **Context & Consultation**:
   - Check `data/data-models/logical/entities/blueprint-entities-archive.md` for the canonical entity specification standard (4 divisions: Data Definition, Business Definition & Rules, Data Quality & Anomalies, Governance).
1. **Logical Modeling (Markdown Base)**:
   - Create foundational, database-agnostic models under `data/data-models/logical/`.
   - Document each entity in `entities/<entity>.md` following strictly `blueprint-entities-archive.md`.
   - Define entity associations in `relationships.md` and domain constraints in `business-rules.md`.
2. **Specialized Database Implementations**:
   - Translate logical models into target database schemas under `data/database/` (e.g., `sql/001_create_tables.sql`, `002_constraints.sql`, `003_indexes.sql`).
3. **Mock & Dirty Data Generation (Python)**:
   - Develop modular Python generators under `data/mock/generators/<entity>.py` (using `faker`, `random`, etc.).
   - Include realistic business-oriented dirty data and edge cases as specified in Section 4.
   - Output datasets to `data/mock/output/` or export formats.
4. **Validation**:
   - Verify consistency across logical models, database DDLs, and Python generator outputs.

---

## 3. Best Practices & Guidelines

- **Logical Models in Markdown**:
  - Keep logical entities clear, self-contained, and business-focused before writing SQL.
  - Document domain rules and edge cases in `business-rules.md`.
- **Database Specializations**:
  - Use clear sequential naming for migration/DDL scripts (`001_...`, `002_...`).
  - Maintain strict referential integrity (PK/FK constraints) and performance indexes in dedicated files or steps.
- **Realistic Mock Datasets**:
  - Use Python scripts to generate business-accurate data (e.g., valid document IDs, realistic emails, plausible dates, coherent financial values).
- **Resource & Reference Documents**:
  - Consult project-specific model rules in [data_model_specs.md](./references/data_model_specs.md).
  - Reference the schema organization guide in [schema_structure.md](./resources/schema_structure.md).

---

## 4. Dirty Data

The data generation must include dirty data in the sense that it should contain realistic errors and inconsistencies that will be cleaned and fixed further on the pipeline. These errors and inconsistencies should be related to the business logic and rules that govern the data generation.

---

## 5. 📊 Data Visualization & Chart Generation Standard (Default Style)

> [!IMPORTANT]
> **INTEGRAÇÃO OBRIGATÓRIA COM A SKILL `charts-maker` (DEFAULT STYLE)**:  
> Sempre que houver necessidade de gerar gráficos, visualizações de volumetria de dados, distribuições estatísticas, perfis de qualidade ou mini cards analíticos para acompanhar modelos e datasets, **o estilo de estilização padrão (Default) DEVE ser rigorosamente idêntico ao padrão corporativo de [`presentation/insights/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/insights/)**, a não ser que explicitamente especificado de outra forma.
>
> **Atributos Canônicos Padrão**:
> - **Canvas & Eixos**: Fundo Branco Puro (`#FFFFFF`), `dpi=300`, `bbox_inches="tight"`.
> - **Tipografia**: `["Segoe UI", "DejaVu Sans", "Helvetica", "Arial", "sans-serif"]`, títulos `#0F172A` (Bold).
> - **Spines & Grade**: Spines superior/direita ocultas (`set_visible(False)`), bordas e grid em `#CBD5E1` (`alpha=0.45`).
> - **Paleta Semântica**:
>   - 🔵 Conversão Orgânica / Base Total: `#2563EB`
>   - 🟢 Resgate Dadosfera / Sucesso: `#059669`
>   - 🔴 Atrito / Abandono / Perda: `#E11D48`
>   - 🟡 Alerta / Risco Médio: `#F59E0B`
>   - 🟣 IA / Canais Especiais: `#8B5CF6`
> - **Cards Executivos**: Containers em `#F8FAFC` com bordas `#94A3B8`.
> - **Ground Truth**: Dados 100% lidos dos arquivos Parquet gerados (`data/mock/output_cleaned/parquet/*.parquet` ou `data/mock/output/parquet/*.parquet`), proibindo multiplicadores visuais manuais.
>
> Consulte as especificações completas em [`charts-maker/SKILL.md`](../charts-maker/SKILL.md) e no guia de estilo [`presentation_insights_style_guide.md`](../charts-maker/references/presentation_insights_style_guide.md).