# 🎤 Pitch de Apresentação: Plataforma Dadosfera & Recuperação de Carrinho

Este diretório contém toda a infraestrutura documental, especificações visuais, scripts declarativos em Python e outputs gráficos que compõem a apresentação executiva e técnica do **Case Dadosfera (Item 10)**.

---

## 🧭 Documento Principal de Roteiro & Estrutura
- 📄 **[`pitch_spec.md`](pitch_spec.md)**: **Especificação Canônica do Pitch**
  - **[1] Apresentar Plataforma Dadosfera**: O Sistema Operacional de Dados unificado, o meio estruturante para a empresa e módulos integrados.
  - **[2] Comentar Arquitetura do Cliente e Iniciar Pitch**: Diagnóstico da stack AWS (Kinesis, Redis, S3), riscos em picos e redução de 86% no lead time.
  - **[3] Case Carrinho (PoC)**: As 5 regras de recuperação, preservação de margem de lucro, Data Quality e Data App com GenAI.
  - **[4] Diretriz Metodológica**: Foco em proporções (%) e Entidade Exemplo de baseline.
  - **[5] Governança de Dados**: Entidades canônicas unificadas e fonte da verdade.

---

## 🏛️ Arquitetura de Módulos Visuais do Pitch

> [!IMPORTANT]
> **Fonte Única da Verdade para Insights de Negócio**:  
> Todos os gráficos analíticos de negócio (Série Temporal, Motivos, CAC/ROI, Segmentação de Risco, LTV, Viabilidade, Timing e Produtos) residem canonicamente na galeria **[`presentation/insights/`](../insights/)** (`01_descriptive/`, `02_risk/`, `03_prescriptive/`).  
> O diretório `presentation/pitch/` concentra os dashboards estruturais e executivos de arquitetura, modelagem e governança da plataforma.

| # | Módulo do Pitch | Tema / Item do Case | Artefatos na Pasta |
|:---:|---|---|---|
| **06 (Item 6)** | [`views/caseitem06/`](views/caseitem06/) | **Modelagem Dimensional Kimball (Star Schema)**: Camada Gold no Snowflake Data Lakehouse, 6 dimensões conformadas, 2 fatos granulares, linhagem Medallion e 2 visões analíticas (`v_abandonment_summary` e `v_recovery_roi_by_segment`). | [`spec.md`](views/caseitem06/spec.md) • [`generate_chart.py`](views/caseitem06/generate_chart.py) • [`chart_caseitem06_kimball_model.png`](views/caseitem06/chart_caseitem06_kimball_model.png) |
| **04 (Item 4)** | [`06_data_quality_e_quarentena/`](06_data_quality_e_quarentena/) | **Governança & Data Quality (Item 4)**: Suíte Great Expectations (18 regras), conformidade global de 94.2% e quarentena Silver de Anomalias de 5.8% (DEC-006). | [`spec.md`](06_data_quality_e_quarentena/spec.md) • [`generate_chart.py`](06_data_quality_e_quarentena/generate_chart.py) • [`chart_06_scorecard_data_quality.png`](06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) |
| **10 (Item 10)** | [`07_arquitetura_dadosfera_vs_aws/`](07_arquitetura_dadosfera_vs_aws/) | **Arquitetura & Prova de Conceito (Item 10)**: Comparativo da stack legada AWS vs Plataforma Dadosfera (-86% lead time e zero risco de sharding). | [`spec.md`](07_arquitetura_dadosfera_vs_aws/spec.md) • [`generate_chart.py`](07_arquitetura_dadosfera_vs_aws/generate_chart.py) • [`chart_07_arquitetura_dadosfera_vs_aws.png`](07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png) |
| **09 (Itens 9 & Bônus)** | [`08_data_app_simulador_prescritivo_genai/`](08_data_app_simulador_prescritivo_genai/) | **Data App & GenAI (Itens 9 e Bônus)**: Simulador interativo de sensibilidade de ROI em Streamlit e personalização semântica de copywriting via LLMs. | [`spec.md`](08_data_app_simulador_prescritivo_genai/spec.md) • [`generate_chart.py`](08_data_app_simulador_prescritivo_genai/generate_chart.py) • [`chart_08_simulador_roi_data_app.png`](08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png) |

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
python presentation/insights/run_all_insights_charts.py
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
