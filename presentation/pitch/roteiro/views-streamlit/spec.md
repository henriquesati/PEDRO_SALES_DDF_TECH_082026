# 🖥️ Módulo de Views: Data App Streamlit (`views-streamlit`)

> **Momento do Roteiro**: **Ato 4 / Seção [5.4] — Consumo, Analytics & Data App Integrado**  
> **Caminho da View**: `presentation/pitch/roteiro/views-streamlit/`  
> **Arquitetura Master**: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)  
> **Código da Aplicação Real**: [`app/app.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/app.py) • [`app/views/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/views/)  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md), [`pipelines/case-item-09/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-09/specs.md).

---

## 🎯 1. Visão Geral do Módulo

Este módulo reúne as visões executivas em alta resolução (16:9, 300 DPI) da aplicação interativa **Data App Streamlit** desenvolvida no projeto para demonstração na apresentação do pitch.

A aplicação foi construída sobre a camada curada de dados do Data Lakehouse (Snowflake / Parquet) e materializa o consumo analítico e prescritivo em 4 telas modulares (React/TypeScript pattern):

```
views-streamlit/
├── 01-simulador-roi/          # 📊 1. Simulador de ROI & Sensibilidade Orçamentária
├── 02-explorador-catalogo/     # 🔍 2. Explorador Semântico & Projeção Vetorial 2D (t-SNE/PCA)
├── 03-copiloto-resgate/        # 🤖 3. Copiloto Prescritivo de Resgate com IA Generativa
├── 04-vitrine-produtos/        # 🎨 4. Vitrine Visual de Produtos Enriquecidos (GenAI)
├── generate_chart.py           # 🐍 Gerador do Painel Consolidado do Data App
├── chart_streamlit_data_app_overview.png # 🖼️ Painel Executivo Master (300 DPI)
└── spec.md                     # 📄 Especificação deste módulo
```

---

## 📊 2. Submódulos e Telas da Apresentação

| Submódulo / View | Tela da Aplicação Streamlit | Foco no Roteiro / Pitch | Artefato Gráfico |
|---|---|---|---|
| [`01-simulador-roi/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-streamlit/01-simulador-roi/) | **Aba 1: Simulador de ROI & Sensibilidade** | Simulação em tempo real de mix de canais (Email, WhatsApp, SMS, Push) e retorno de R$ 314,5k GMV resgatado (ROI 45.2x). | `chart_streamlit_simulador_roi.png` |
| [`02-explorador-catalogo/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-streamlit/02-explorador-catalogo/) | **Aba 2: Explorador Vetorial (t-SNE/PCA)** | Clusterização semântica de 300 produtos e recomendação instantânea de SKUs alternativos para carrinhos abandonados. | `chart_streamlit_explorador_catalogo.png` |
| [`03-copiloto-resgate/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-streamlit/03-copiloto-resgate/) | **Aba 3: Copiloto Prescritivo de Resgate** | Assistente de IA que diagnostica a causa-raiz e gera copies personalizadas em tempo real com schema Pydantic. | `chart_streamlit_copiloto_resgate.png` |
| [`04-vitrine-produtos/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-streamlit/04-vitrine-produtos/) | **Aba 4: Vitrine de Produtos Enriquecidos** | Catálogo interativo com filtros e destaque para atributos técnicos e diferenciais semânticos extraídos por LLM. | `chart_streamlit_vitrine_produtos.png` |
| **Painel Master** | **Visão Consolidada do Data App** | Envelopamento visual master mostrando a interface completa do Streamlit integrada ao Data Lakehouse Dadosfera. | `chart_streamlit_data_app_overview.png` |

---

## 🚀 3. Como Executar a Aplicação Interativa

Para rodar a aplicação Streamlit interativa ao vivo no navegador durante a apresentação:

```bash
streamlit run app/app.py
```
