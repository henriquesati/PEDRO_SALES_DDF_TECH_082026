# 🏗️ Arquitetura de Datalakes — Pipelines de Dados (Medallion Architecture)

> **Módulo:** `pipelines/datalakes/`  
> **Padrão:** Lakehouse Medallion (Raw -> Qualify -> Curated)  
> **Framework Normativo:** DEC-001 (Métricas em Tempo de Execução) + DEC-004 (Sem SQL Local) + DEC-006 (Dual-Artifact Qualify/Anomalies)  
> **Status:** Objeto Imutável de Especificação Centralizada  

---

## 📌 Visão Geral do Diretório

Este diretório centraliza os contratos de dados e especificações imutáveis das três camadas do Data Lakehouse para o case de **Recuperação de Carrinho Abandonado**:

```text
pipelines/datalakes/
├── raw/
│   └── spec.md          # Especificação Imutável da Camada Raw (Bronze / Ingestão Bruta)
├── qualify/
│   └── spec.md          # Especificação Imutável da Camada Qualify (Silver / Validação & DQ)
└── curated/
    └── spec.md          # Especificação Imutável da Camada Curated (Gold / Modelagem Dimensional)
```

---

## 🔄 Fluxo de Maturidade dos Dados

```mermaid
flowchart LR
    subgraph Raw [Zona Raw - Bronze]
        R1[raw_pedidos]
        R2[raw_carrinhos]
        R3[raw_itens_carrinho]
        R4[raw_clientes]
        R5[raw_produtos]
        R6[raw_eventos_carrinho]
        R7[raw_eventos_resgate]
    end

    subgraph Qualify [Zona Qualify - Silver]
        Q1[pedidos]
        Q2[carrinhos]
        Q3[itens_carrinho]
        Q4[clientes]
        Q5[produtos]
        Q6[eventos_carrinho]
        Q7[eventos_resgate]
        ANOM[Quarentena de Anomalias]
    end

    subgraph Curated [Zona Curated - Gold]
        D1[dim_clientes]
        D2[dim_tempo]
        D3[dim_dispositivo]
        D4[dim_motivo_abandono]
        D5[dim_canal_resgate]
        D6[dim_segmento_rfm]
        F1[fato_abandono]
        F2[fato_resgate]
        V1[v_abandonment_summary]
        V2[v_recovery_roi_by_segment]
    end

    Raw -->|Validação de Schema & Regras DQ| Qualify
    Qualify -->|Registros Conformes| Curated
    Qualify -->|Registros com Desvios| ANOM
```

---

## 📚 Navegação Rápida

- 📥 [Especificação da Camada Raw](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/raw/spec.md)
- 🧹 [Especificação da Camada Qualify](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/qualify/spec.md)
- 📊 [Especificação da Camada Curated](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/curated/spec.md)
