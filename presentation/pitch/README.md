# 🎤 Pitch de Apresentação: Plataforma Dadosfera & Recuperação de Carrinho

Este diretório contém toda a infraestrutura documental, especificações visuais, scripts declarativos em Python e outputs gráficos que compõem a apresentação executiva e técnica do **Case Dadosfera (Item 10)**.

---

## 🧭 Documento Principal de Roteiro & Estrutura
- 📄 **[pitch_spec.md](pitch_spec.md)**: **Documentação Canônica do Pitch**
  - **Parte 1 — Backbone Central**: Ordem cronológica da apresentação (Blocos 1 a 5, minutagem, entregas levantadas e mensagem central).
  - **Parte 2 — Pitch Guidelines**: Roteiro aprofundado com falas sugeridas para cada slide/tópico, dados de impacto ancorados em taxas e percentuais (DEC-001/007), contraste Dadosfera vs AWS e tratamento de objeções de C-Levels.

---

## 📂 Arquitetura de Diretórios & Artefatos Visuais

Cada diretório abaixo agrupa de forma autocontida a **especificação (`spec.md`)**, o **script gerador em Python (`generate_chart.py`)** e o **artefato visual gerado (`chart_*.png`)**:

| # | Diretório do Módulo | Tema / Regra de Negócio | Artefatos na Pasta |
|:---:|---|---|---|
| **01** | [`01_abandono_vs_recuperacao_timeline/`](01_abandono_vs_recuperacao_timeline/) | **Ciclo de Vida & Série Temporal**: Transição de status (30min inatividade), sazonalidade Jan–Jun 2026 e taxa de recuperação (~10.1%). | [`spec.md`](01_abandono_vs_recuperacao_timeline/spec.md) • [`generate_chart.py`](01_abandono_vs_recuperacao_timeline/generate_chart.py) • [`chart_01_*.png`](01_abandono_vs_recuperacao_timeline/chart_01_serie_temporal_abandono_resgate.png) |
| **02** | [`02_performance_categorias_produtos/`](02_performance_categorias_produtos/) | **Performance de Catálogo**: Sensibilidade de categorias (Eletrônicos, Moda, Beleza), atrito de preço e volume represado. | [`spec.md`](02_performance_categorias_produtos/spec.md) • [`generate_chart.py`](02_performance_categorias_produtos/generate_chart.py) • [`chart_02_*.png`](02_performance_categorias_produtos/chart_02_performance_categorias.png) |
| **03** | [`03_roi_canais_e_comunicacao/`](03_roi_canais_e_comunicacao/) | **Topologia de Canais & ROI**: Custo unitário (Email R$0,05 vs WhatsApp R$0,30) e ROI multiplicador de **~45x**. | [`spec.md`](03_roi_canais_e_comunicacao/spec.md) • [`generate_chart.py`](03_roi_canais_e_comunicacao/generate_chart.py) • [`chart_03_*.png`](03_roi_canais_e_comunicacao/chart_03_roi_eficiencia_canais.png) |
| **04** | [`04_matriz_motivos_segmentos_rfm/`](04_matriz_motivos_segmentos_rfm/) | **Causas-Raiz vs Segmentação RFM**: Frete > 15%, Pagamento, Indecisão, e validação de que segmentar compensa (Ratio 3x). | [`spec.md`](04_matriz_motivos_segmentos_rfm/spec.md) • [`generate_chart.py`](04_matriz_motivos_segmentos_rfm/generate_chart.py) • [`chart_04_*.png`](04_matriz_motivos_segmentos_rfm/chart_04_matriz_motivos_rfm_heatmap.png) |
| **05** | [`05_matriz_viabilidade_recuperacao/`](05_matriz_viabilidade_recuperacao/) | **Matriz Prescritiva de Decisão**: Dispersão probabilidade x valor do carrinho e fila de priorização em tempo real. | [`spec.md`](05_matriz_viabilidade_recuperacao/spec.md) • [`generate_chart.py`](05_matriz_viabilidade_recuperacao/generate_chart.py) • [`chart_05_*.png`](05_matriz_viabilidade_recuperacao/chart_05_dispersao_viabilidade_recuperacao.png) |
| **06** | [`06_data_quality_e_quarentena/`](06_data_quality_e_quarentena/) | **Governança & Data Quality (Item 4)**: Suíte Great Expectations (18 regras), conformidade 94.2% e quarentena Silver 5.8%. | [`spec.md`](06_data_quality_e_quarentena/spec.md) • [`generate_chart.py`](06_data_quality_e_quarentena/generate_chart.py) • [`chart_06_*.png`](06_data_quality_e_quarentena/chart_06_scorecard_data_quality.png) |
| **07** | [`07_arquitetura_dadosfera_vs_aws/`](07_arquitetura_dadosfera_vs_aws/) | **Arquitetura & Prova de Conceito (Item 10)**: Comparativo da stack legada AWS vs Dadosfera (-86% lead time). | [`spec.md`](07_arquitetura_dadosfera_vs_aws/spec.md) • [`generate_chart.py`](07_arquitetura_dadosfera_vs_aws/generate_chart.py) • [`chart_07_*.png`](07_arquitetura_dadosfera_vs_aws/chart_07_arquitetura_dadosfera_vs_aws.png) |
| **08** | [`08_data_app_simulador_prescritivo_genai/`](08_data_app_simulador_prescritivo_genai/) | **Data App & GenAI (Itens 9 e Bônus)**: Simulador interativo de ROI em Streamlit e copywriting semântico dinâmico. | [`spec.md`](08_data_app_simulador_prescritivo_genai/spec.md) • [`generate_chart.py`](08_data_app_simulador_prescritivo_genai/generate_chart.py) • [`chart_08_*.png`](08_data_app_simulador_prescritivo_genai/chart_08_simulador_roi_data_app.png) |

---

## ⚙️ Como Executar os Geradores Visuais

### 1. Execução Consolidada (Todos os Gráficos)
Para gerar todos os 8 artefatos visuais de uma só vez:
```bash
python presentation/pitch/run_all_pitch_charts.py
```

### 2. Execução Individual por Módulo
Você pode entrar em qualquer subdiretório e executar seu script isoladamente:
```bash
python presentation/pitch/01_abandono_vs_recuperacao_timeline/generate_chart.py
python presentation/pitch/03_roi_canais_e_comunicacao/generate_chart.py
```
*Cada script lê os datasets estruturados em Parquet e salva a imagem correspondente em alta resolução (300 DPI) dentro do próprio diretório.*
