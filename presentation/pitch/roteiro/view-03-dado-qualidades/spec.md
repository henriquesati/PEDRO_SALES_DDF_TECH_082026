# 🏛️ Módulo Master de Views: Etapas de Qualidade, Governança & Modelagem (`view-03-dado-qualidades`)

> **Momento do Roteiro**: **Ato 2 / Seção [3] — Etapas de Qualidade e Geração de Artefatos**  
> **Diretório Envelope**: `presentation/pitch/roteiro/view-03-dado-qualidades/`  
> **Padrão de Organização**: Envelopamento Lógico de Módulos Analíticos  
> **Fonte Estratégica**: [`presentation/pitch/roteiro.txt`](../roteiro.txt), [`presentation/pitch/pitch_spec.md`](../../pitch_spec.md) e [`pipelines/datalakes/README.md`](../../../pipelines/datalakes/README.md).

---

## 🎯 1. Visão Geral da Seção [3] do Roteiro

A seção `[3]` do roteiro de pitch aborda a transição arquitetural e técnica da manipulação de dados na **Plataforma Dadosfera**, demonstrando como pipelines automatizados, governança ativa e modelagem dimensional resolvem os gargalos históricos da arquitetura legada (AWS DIY).

Para garantir máxima clareza e modularidade, este módulo atua como **container lógico de envelopamento**, agrupando 3 visões complementares:

```text
presentation/pitch/roteiro/view-03-dado-qualidades/
├── view-lake-architecture/    # 🏛️ [3] Lakehouse Medallion, Pipelines & Data Quality (Great Expectations)
├── view-governança/           # 🛡️ {3.1} Dicionário de Dados, RBAC & Blindagem LGPD / Opt-in
├── view-model-kimball/        # 📊 {3.2} Modelagem Dimensional Kimball (Star Schema 1-Hop) & Insights
├── spec.md                    # 📄 Especificação Master do Envelope
└── README.md                  # 🧭 Guia Rápido de Navegação do Módulo
```

---

## 🗺️ 2. Submódulos Envelopados

| Subdiretório da View | Momento no Roteiro | Foco da Narrativa & Artefato |
| :--- | :--- | :--- |
| [`view-lake-architecture/`](view-lake-architecture/) | **Seção [3]: Pipelines & Data Quality** | Fluxo Medallion (Raw -> Qualify/Anomalies -> Curated), eliminação de cold start do AWS Glue (1-4 min), 18 regras de Data Quality (94.2% conformidade vs 5.8% quarentena) e persistência confiável. |
| [`view-governança/`](view-governan%C3%A7a/) | **Seção {3.1}: Governança & LGPD** | Dicionário de dados formal ("A é um B que C"), tagging semântica `pii_sensivel`, conformidade mandatória de opt-in (`ANOM-03`), controle de acesso centralizado (RBAC) e compartilhamento seguro de Data Views. |
| [`view-model-kimball/`](view-model-kimball/) | **Seção {3.2}: Modelagem Kimball** | Transformação funcional Silver -> Gold, 6 Dimensões Conformadas (`_sk`) + 2 Tabelas Fato (`fato_abandono` e `fato_resgate`), 1-Hop JOINs para consultas instantâneas e visões analíticas de ROI/Abandono. |

---

## 🎨 3. Padrões Gráficos Compartilhados (`charts-maker` Standard)

* **Canvas**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen, 300 DPI.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`).
* **Integridade de Dados (Ground Truth)**: Conexão direta aos dados reais processados em Parquet (`data/mock/output_cleaned/parquet/`).
