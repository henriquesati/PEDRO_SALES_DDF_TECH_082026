# Data Architecture & Schema Structure Guide

This guide establishes the standard multi-tier data architecture and file structure used by the `datamaker` skill.

---

## 1. Directory Structure

```text
data/
├── models/
│   └── logical/
│       ├── README.md                # Overview of the domain & data model
│       ├── entities/
│       │   ├── <entity_name>.md     # Attribute definitions, types, constraints, descriptions
│       │   └── ...
│       ├── relationships.md         # ER associations, cardinalities (1:1, 1:N, N:M), foreign keys
│       └── business-rules.md        # Domain rules, validations, business constraints
│
├── database/
│   ├── sql/
│   │   ├── 001_create_tables.sql    # Core table DDL statements
│   │   ├── 002_constraints.sql      # Primary & foreign keys, check constraints, unique rules
│   │   └── 003_indexes.sql          # Performance, foreign key, and unique indexes
│   └── nosql/                       # (Optional) Document/NoSQL schema definitions (e.g. MongoDB, JSON Schema)
│
└── mock/
    ├── generators/
    │   ├── <entity_name>.py         # Entity-specific Python generator scripts (Faker, random, etc.)
    │   └── ...
    └── output/                      # Generated seed and dirty datasets (CSV, JSON, SQL, Parquet)
```

---

## 2. Layer Specifications

### Layer 1: Logical Modeling (`data/models/logical/`)
- **Format**: Markdown (`.md`).
- **Goal**: Technology-agnostic conceptual and logical modeling.
- **Components**:
  - `entities/<entity_name>.md`: Detailed attribute list (Name, Data Type, Nullability, Primary/Foreign key role, Default value, Description, Business constraints).
  - `relationships.md`: Cardinality maps (e.g. Customer 1 — N Orders), deletion behaviors (CASCADE, SET NULL, RESTRICT).
  - `business-rules.md`: Invariants, calculations, state machine transitions, edge cases.


### Layer 3: Mock & Dirty Data Generation (`data/mock/`)
- **Format**: Python scripts (`generators/<entity>.py`).
- **Goal**: Generate realistic synthetic datasets reflecting real-world business distributions and intentional dirty data.
- **Output**: Populates `data/mock/output/` in requested formats (CSV, JSON, SQL inserts).

---

## 3. Dirty Data Guidelines

Synthetic data generation must incorporate intentional, realistic dirty data anomalies to test downstream data engineering, cleaning, and validation pipelines:
- **Format Inconsistencies**: Varied date formats (`YYYY-MM-DD`, `DD/MM/YYYY`), casing variations (UPPERCASE, lowercase, mixed), accented characters.
- **Domain Edge Cases**: Out-of-range dates, boundary numbers, negative values where unexpected, expired statuses.
- **Missing / Null Values**: Realistic missingness patterns (MCAR, MAR), empty strings vs nulls.
- **Reference Discrepancies**: Orphan records, slightly misspelled foreign identifiers (within controllable dirty test quotas).
- **Logical Business Violations**: Order delivery dates prior to order creation dates, discount amounts exceeding total value.

---

## 4. Consultation & Reference

When designing or updating models, the skill should check the customized project references:
- **Reference Specifications**: [data_model_specs.md](../references/data_model_specs.md)
