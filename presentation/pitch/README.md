# 🎤 Pitch de Apresentação: Plataforma Dadosfera & Recuperação de Carrinho

Este diretório contém toda a infraestrutura documental, especificações visuais, scripts declarativos em Python e outputs gráficos que compõem a apresentação executiva e técnica do **Case Dadosfera (Item 10)**.

---

## 🧭 Governança & Documentos Centrais do Pitch

> [!IMPORTANT]
> **Fonte Única da Verdade para o Pitch e Narrativa de Negócio**:  
> - **[`pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md)**: **Especificação Master do Pitch** (Seções [1] a [5]), contendo todas as regras de negócio, princípios metodológicos em % (DEC-001), Entidade Exemplo de Negócio (Baseline Mock de 7.500 carrinhos, R$ 375 ticket e ROI 45x) e governança de dados (Ground Truth Parquet).
> - **[`roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt)**: **Roteiro Falado & Notas Cronológicas de Apresentação** (Atos 1 a 4 com contraste AWS DIY vs Dadosfera).
> - **[`roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)**: **Arquitetura Centralizada das Views do Roteiro**, detalhando a árvore completa e modular de todas as visões (Atos 1, 2, 3 e 4).
> - **[`roteiro/catalogo_graficos_referencias.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/catalogo_graficos_referencias.md)**: **Catálogo Mestre de Gráficos** com links diretos para 100% dos PNGs em 300 DPI gerados no ecossistema.

---

## 🏛️ Módulos Executivos de Apresentação Técnica do Pitch

| # | Módulo do Pitch | Tema / Item do Case | Artefatos na Pasta |
|:---:|---|---|---|
| **06 (Item 6)** | [`views/caseitem06/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/) | **Modelagem Dimensional Kimball (Star Schema)**: Camada Gold no Snowflake Data Lakehouse, 6 dimensões conformadas, 2 fatos granulares, linhagem Medallion e 2 visões analíticas (`v_abandonment_summary` e `v_recovery_roi_by_segment`). | [`spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/spec.md) • [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/generate_chart.py) • [`chart_caseitem06_kimball_model.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/views/caseitem06/chart_caseitem06_kimball_model.png) |
| **04 (Item 4)** | [`06_data_quality_e_quarentena/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/) | **Governança & Data Quality (Item 4)**: Suíte Great Expectations (18 regras), conformidade global de 94.2% e quarentena Silver de Anomalias de 5.8% (DEC-006). | [`spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/spec.md) • [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/generate_chart.py) • [`chart_06_scorecard_data_quality.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) |
| **10 (Item 10)** | [`07_arquitetura_dadosfera_vs_aws/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/) | **Arquitetura & Prova de Conceito (Item 10)**: Comparativo da stack legada AWS vs Plataforma Dadosfera (-86% lead time e zero risco de sharding). | [`spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/spec.md) • [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/generate_chart.py) • [`chart_07_arquitetura_dadosfera_vs_aws.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png) |
| **09 (Itens 9 & Bônus)** | [`08_data_app_simulador_prescritivo_genai/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/08_data_app_simulador_prescritivo_genai/) | **Data App & GenAI (Itens 9 e Bônus)**: Simulador interativo de sensibilidade de ROI em Streamlit e personalização semântica de copywriting via LLMs. | [`spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/08_data_app_simulador_prescritivo_genai/spec.md) • [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/08_data_app_simulador_prescritivo_genai/generate_chart.py) • [`chart_08_simulador_roi_data_app.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png) |

---

## 🎬 Camada de Views do Roteiro Narrativo

A infraestrutura completa de visões cronológicas do roteiro está centralizada e documentada em:
👉 **[`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)**

- **🏛️ Ato 1 (Arquitetura, Riscos & TCO)**: [`roteiro/arquitetura-view/arc-diagram-view/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/), [`roteiro/problema-elasticidade/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/problema-elasticidade/), [`roteiro/staff-pain-point/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/staff-pain-point/).
- **🛡️ Ato 2 (Fundamentos de Dados)**: [`roteiro/view-03-dado-qualidades/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/) (`view-lake-architecture/`, `view-governanca/`, `view-model-kimball/`).
- **📈 Ato 3 (Insights de Negócio)**: [`roteiro/views-04-insights/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-04-insights/) (`descritivos/` e `prescritivos/`).
- **🧠 Ato 4 (Inteligência & Data Apps)**: [`roteiro/views-05-insights-ia/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/) (`modelos-preditivos-ml/`, `genai-extracao-copies/`, `similaridade-produtos/`, `data-app-simulador-roi/`).

---

## ⚙️ Como Executar os Geradores Visuais

### 1. Execução Consolidada dos Dashboards do Pitch
Para gerar todos os 4 artefatos de infraestrutura e arquitetura do pitch:
```bash
python presentation/pitch/run_all_pitch_charts.py
```

### 2. Execução Consolidada da Galeria de Insights de Negócio
Para gerar toda a suíte de 10+ gráficos analíticos de negócio:
```bash
python insights/run_all_insights_charts.py
```

### 3. Execução Individual por Módulo
Você pode entrar em qualquer subdiretório e executar seu script isoladamente:
```bash
python presentation/pitch/views/caseitem06/generate_chart.py
python presentation/pitch/06_data_quality_e_quarentena/generate_chart.py
python presentation/pitch/07_arquitetura_dadosfera_vs_aws/generate_chart.py
python presentation/pitch/08_data_app_simulador_prescritivo_genai/generate_chart.py
```
*Cada script consome os datasets estruturados em Parquet (`data/mock/output_cleaned/parquet/`) e salva a imagem correspondente em alta resolução (300 DPI) dentro do próprio diretório.*
