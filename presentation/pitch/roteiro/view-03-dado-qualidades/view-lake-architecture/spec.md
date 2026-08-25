# Especificação Visual & Técnica: Módulo Arquitetura Lakehouse & Data Quality (`view-lake-architecture`)

> **Momento do Roteiro**: **Ato 2 / Seção [3] — Etapas de Qualidade e Geração de Artefatos**  
> **Caminho da View**: `presentation/pitch/roteiro/view-lake-architecture/`  
> **Artefato Principal Previsto**: [`chart_lake_architecture.png`](chart_lake_architecture.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../roteiro.txt), [`pipelines/datalakes/README.md`](../../../pipelines/datalakes/README.md) e [`pipelines/case-item-08/specs.md`](../../../pipelines/case-item-08/specs.md).

---

## 🎯 1. Objetivo & Mensagem no Pitch

Demonstrar a superioridade da **Arquitetura Lakehouse Medallion integrada da Dadosfera** contra a complexidade fragmentada da AWS DIY, evidenciando como os pipelines declarativos e a suíte automatizada de Data Quality garantem **94.2% de conformidade de dados** e isolam anomalias em tempo real antes de qualquer impacto nas operações de negócio.

### 📌 Principais Mensagens de Fala:
1. **Fim do Cold Start e dos Custos Ocultos de Spark**:
   - *No AWS Glue*: Cada job leva de 1 a 4 minutos apenas para provisionar DPUs Spark, cobrando tempo mínimo por micro-execução e encarecendo o processamento contínuo de eventos.
   - *Na Dadosfera*: Execuções declarativas com baixo acoplamento entre ingestão, tratamento e persistência no Snowflake Lakehouse, refletindo dados limpos quase instantaneamente no catálogo.
2. **Arquitetura Dual-Artifact Silver (DEC-006)**:
   - **`_qualify` (94.2%)**: Registros validados e enriquecidos que avançam para a camada Gold/Curated.
   - **`_anomalies` (5.8%)**: Quarentena ativa que intercepta fretes negativos, e-mails malformados e divergências contábeis, armazenando o payload bruto para auditoria.
3. **Data Quality como Habilitador de Confiabilidade**:
   - A governança e a qualidade não são burocracias pós-processamento, mas barreiras ativas automatizadas que blindam réguas de marketing e decisões de diretoria.

---

## 🏛️ 2. Arquitetura Medallion dos Pipelines (Ponta a Ponta)

```text
┌─────────────────┐       ┌───────────────────────────────┐       ┌───────────────────────────────┐
│   BRONZE / RAW  │  ───► │        SILVER / QUALIFY       │  ───► │         GOLD / CURATED        │
│                 │       │                               │       │                               │
│  Ingestão Bruta │       │  • 94.2% Conformidade Rigorosa│       │  • Star Schema Kimball        │
│  Imutável       │       │  • Validação Great Expectation│       │  • 6 Dimensões / 2 Fatos      │
│  Sem Schema Lock│       │  • Higienização de PII / Email│       │  • Visões Analíticas Gold     │
└─────────────────┘       └───────────────┬───────────────┘       └───────────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────────┐
                          │       SILVER / ANOMALIES      │
                          │                               │
                          │  • 5.8% Quarentena Ativa      │
                          │  • Captura de Payload Bruto   │
                          │  • Motivo & Severidade ANOM   │
                          └───────────────────────────────┘
```

---

## 📐 3. Esboço e Composição Visual Prevista

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO POWERPOINT]                                      |
+---------------------------------------------------------------------------------------------------+
|  [CARD 1]                             [CARD 2]                             [CARD 3]               |
|  Taxa de Conformidade Silver          Isolamento em Quarentena             Regras Great Expectations|
|  94.2%                                5.8%                                 18 Regras Automatizadas |
|  Registros Prontos para Gold          Interceptados Pré-Envio              Validação Sintática & Neg|
+---------------------------------------------------------------------------------------------------+
|  [DIAGRAMA / PAINEL COMPARATIVO DE PIPELINES]                                                     |
|  Fluxo Medallion: Bronze (Raw) -> Silver (Qualify + Anomaly) -> Gold (Curated DW)                 |
|  - Desacoplamento operacional e eliminação de 1-4 min de cold start do AWS Glue                   |
|  - Rastreabilidade ponta a ponta e geração de artefatos confiáveis para consumo imediato          |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: Pipelines Datalakes Dadosfera | Framework Normativo DEC-006 & DEC-008           |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 4. Mapeamento Canônico de Scripts e Artefatos do Ecossistema (DRY)

Para evitar duplicidade de código e garantir uma única fonte da verdade, este submódulo atua como **Hub de Visualização & Referência**, conectando-se diretamente aos scripts, modelos e relatórios já homologados no ecossistema:

| Pilar da Arquitetura | Script Canônico de Origem | Artefatos Gerados / Relatórios | Status |
| :--- | :--- | :--- | :---: |
| **Data Quality & Quarentena (DEC-006)** | [`pipelines/case-item-04/scripts/run_quality_pipeline.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-04/scripts/run_quality_pipeline.py) | [`chart_01_global_compliance_and_quarantine.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-04/outputs/assets/chart_01_global_compliance_and_quarantine.png)<br>[`data_quality_report.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-04/outputs/data_quality_report.md) | ✅ Homologado |
| **Scorecard Executivo Silver** | [`presentation/pitch/06_data_quality_e_quarentena/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/generate_chart.py) | [`chart_06_scorecard_data_quality.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) | ✅ Homologado |
| **Modelagem Kimball Gold (DEC-008)** | [`pipelines/case-item-06/scripts/generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/scripts/generate_chart.py) | [`chart_caseitem06_kimball_model.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/outputs/assets/chart_caseitem06_kimball_model.png)<br>[`data_warehouse_architecture.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/outputs/assets/data_warehouse_architecture.png) | ✅ Homologado |
| **Pipelines Stepsfera Medallion** | [`pipelines/case-item-08/scripts/run_silver_gold_pipeline.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/scripts/run_silver_gold_pipeline.py) | [`stepsfera/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/stepsfera/) (Steps 01 a 05)<br>[`pipeline_execution_report.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/outputs/pipeline_execution_report.md) | ✅ Homologado |
| **Especificações Datalakes** | [`pipelines/datalakes/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/README.md) | 4 Zonas: `raw/`, `qualify/`, `anomaly/`, `curated/` | ✅ Homologado |
| **View Consolidada do Pitch (Painel Completo)** | [`generate_chart.py`](generate_chart.py) | [`chart_lake_architecture.png`](chart_lake_architecture.png) (300 DPI, 16:9) | ✅ Ativo |
| **View Estilo PowerPoint (3 Camadas + Qualidade)** | [`powerpoint-medallion.py`](powerpoint-medallion.py) | [`chart_powerpoint_medallion.png`](chart_powerpoint_medallion.png) (300 DPI, 16:9) | ✅ Ativo |

---

## 🎨 5. Variantes Visuais Disponíveis no Módulo

1. **Painel Executivo Multicamadas (`chart_lake_architecture.png`)**:
   - Ideal para relatórios técnicos e visão aprofundada: inclui Top KPI Cards (94.2% conformidade / 5.8% quarentena / 18 regras DQ), fluxo detalhado de 4 blocos e quadro comparativo de eficiência operacional (AWS Glue vs Dadosfera).
2. **Slide Limpo PowerPoint / Keynote (`chart_powerpoint_medallion.png`)**:
   - Ideal para apresentação dinâmica de slides: fundo em curva vermelha ergonômica, 3 cards metálicos (Bronze, Silver, Gold) com ícones tridimensionais de banco de dados, setas tracejadas de transição e faixa de base destacando a evolução contínua da **Qualidade**.
