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

The structure begins with technology-agnostic logical modeling in Markdown under `data/models/logical/`, followed by concrete database implementations (`data/database/`) and mock data generation scripts (`data/mock/`):

```text
data/
├── models/
│   └── logical/
│       ├── README.md
│       ├── entities/
│       │   ├── customer.md      # Attribute definitions, types, constraints
│       │   ├── order.md
│       │   └── product.md
│       ├── relationships.md     # Cardinalities & ER associations
│       └── business-rules.md    # Domain rules, validation, constraints
│
├── database/
│   ├── sql/
│   │   ├── 001_create_tables.sql
│   │   ├── 002_constraints.sql
│   │   └── 003_indexes.sql
│   └── nosql/                   # (Optional) Specialized schemas (e.g., MongoDB, JSON Schema)
│
└── mock/
    ├── generators/
    │   ├── customer.py          # Entity-specific generator scripts (Python)
    │   ├── order.py
    │   └── product.py
    └── output/                  # Generated seed datasets (CSV, JSON, SQL)
```

---

## 2. Workflow & Procedure

When requested to create or update data models and schemas:

0. **Context & Consultation**:
   - Check [data_model_specs.md](./references/data_model_specs.md) for custom business rules, domain entities, database specifications, and dirty data requirements provided for the project.
1. **Logical Modeling (Markdown Base)**:
   - Create foundational, database-agnostic models under `data/models/logical/`.
   - Document each entity in `entities/<entity>.md` (attributes, types, descriptions, nullability).
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