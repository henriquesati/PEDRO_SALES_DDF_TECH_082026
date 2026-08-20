# Data Architecture & Folder Structure Guide

This guide defines the multi-tier data architecture used by the `datamaker` skill.

---

## 1. Directory Layout

```text
data/
├── models/
│   └── logical/
│       ├── README.md
│       ├── entities/
│       │   ├── <entity_name>.md     # Attribute specifications, types, descriptions
│       │   └── ...
│       ├── relationships.md         # Entity associations (1:1, 1:N, N:M)
│       └── business-rules.md        # Domain rules & validation constraints
│
├── database/
│   ├── sql/
│   │   ├── 001_create_tables.sql    # DDL statements for tables
│   │   ├── 002_constraints.sql      # Primary & Foreign Key constraints
│   │   └── 003_indexes.sql          # Performance and unique indexes
│   └── <specialization>/            # Other database targets (NoSQL, ORMs, etc.)
│
└── mock/
    ├── generators/
    │   ├── <entity_name>.py         # Python generator scripts
    │   └── ...
    └── output/                      # Generated seed and dirty datasets
```

---

## 2. Layers Explained

### Layer 1: Logical Modeling (`data/models/logical/`)
- Written in **Markdown**.
- Database-agnostic conceptual and logical models.
- Defines domain entities, business attributes, relationships, and business rules before technology decisions.

### Layer 2: Concrete Database Implementations (`data/database/`)
- Specializes logical models into specific DBMS DDLs (e.g. PostgreSQL, MySQL, SQLite, MongoDB schemas).
- Uses clear numerical sequencing for execution order.

### Layer 3: Mock & Dirty Data Generators (`data/mock/`)
- Modular Python scripts per entity (`generators/<entity>.py`).
- Produces realistic business data and purposeful dirty data (inconsistencies, missing fields, format variants) to test downstream validation and cleaning pipelines.
