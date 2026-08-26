# 🏛️ Módulo Master de Views: Etapas de Qualidade, Governança & Modelagem (`view-03-dado-qualidades`)

> **Momento do Roteiro**: **Ato 2 / Seção [3] — Etapas de Qualidade e Geração de Artefatos**  
> **Diretório Envelope**: `presentation/pitch/roteiro/view-03-dado-qualidades/`  
> **Padrão de Organização**: Envelopamento Lógico de Módulos Analíticos (Consulte a arquitetura completa em [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md))  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md) e [`pipelines/datalakes/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/README.md).

---

## 🎯 1. Visão Geral da Seção [3] do Roteiro

A seção `[3]` do roteiro de pitch aborda a transição arquitetural e técnica da manipulação de dados na **Plataforma Dadosfera**, demonstrando como pipelines automatizados, governança ativa e modelagem dimensional resolvem os gargalos históricos da arquitetura legada (AWS DIY).

Este módulo atua como **container lógico de envelopamento**, agrupando 3 visões complementares descritas a seguir.

---

## 🗺️ 2. Submódulos Envelopados

| Subdiretório da View | Momento no Roteiro | Foco da Narrativa & Artefato |
| :--- | :--- | :--- |
| [`view-lake-architecture/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-lake-architecture/) | **Seção [3]: Pipelines & Data Quality** | Fluxo Medallion (Raw -> Qualify/Anomalies -> Curated), eliminação de cold start do AWS Glue (1-4 min), 18 regras de Data Quality (94.2% conformidade vs 5.8% quarentena) e persistência confiável. |
| [`view-governanca/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-governanca/) | **Seção {3.1}: Governança & LGPD** | Dicionário de dados formal ("A é um B que C"), tagging semântica `pii_sensivel`, conformidade mandatória de opt-in (`ANOM-03`), controle de acesso centralizado (RBAC) e compartilhamento seguro de Data Views. |
| [`view-model-kimball/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-model-kimball/) | **Seção {3.2}: Modelagem Kimball** | Transformação funcional Silver -> Gold, 6 Dimensões Conformadas (`_sk`) + 2 Tabelas Fato (`fato_abandono` e `fato_resgate`), 1-Hop JOINs para consultas instantâneas e visões analíticas de ROI/Abandono. |

---

## 🎨 3. Padrões Gráficos Compartilhados (`charts-maker` Standard)

* **Canvas**: Fundo Branco Puro (`#FFFFFF`), Proporção 16:9 Widescreen, 300 DPI.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`).
* **Integridade de Dados (Ground Truth)**: Conexão direta aos dados reais processados em Parquet (`data/mock/output_cleaned/parquet/`).
