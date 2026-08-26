# 🧠 Envelope de Views: Seção [5] — Inteligência, GenAI & Data Apps (`views-05-insights-ia`)

> **Momento do Roteiro**: **Ato 4 / Seção [5] — Módulo de Inteligência, GenAI e Data Apps da Plataforma Dadosfera**  
> **Papel no Pitch**: Demonstrar a eliminação do overhead operacional de infraestrutura de Machine Learning e LLMs (AWS DIY), comprovando a facilidade de treinar modelos de negócio (Scikit-Learn, XGBoost), integrar GenAI governada com Pydantic e servir Data Apps interativos em Streamlit.  
> **Arquitetura Master**: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)

---

## 🗺️ 1. Submódulos Envelopados

1. 🧠 **[`modelos-preditivos-ml/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/modelos-preditivos-ml/)**: Modelos Preditivos de Negócio (Stepsfera, Scikit-Learn, ROC-AUC 0.9478 e 99.53% acurácia).
2. ⚖️ **[`feature-importance-ml/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/feature-importance-ml/)**: Pesos do Modelo & Explainable AI (Impacto de Ticket +38.4%, RFM VIP +26.2%, Frete +18.5%).
3. 🤖 **[`genai-extracao-copies/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/genai-extracao-copies/)**: GenAI & Extração de Features (Pydantic 100%, Validação JSON Schema e +18% de CTR).
4. 🔍 **[`similaridade-produtos/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/similaridade-produtos/)**: Busca Semântica & Embeddings de Produtos (Espaço Vetorial 2D t-SNE e +12.4% resgate).
5. 📊 **[`data-app-simulador-roi/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/data-app-simulador-roi/)**: Data Apps em Streamlit & Simulador de ROI (45x ROI e Waterfall de +R$ 167,9k).

---

## 🎯 2. Mapeamento de Artefatos Visuais

| Submódulo | Artefato Visual (300 DPI) | Mensagem Central de Pitch |
| :--- | :--- | :--- |
| **Master View** | [`chart_insights_ia_master.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/chart_insights_ia_master.png) | Síntese de IA: Eliminação de cold-start de Glue/EC2 e unificação em Stepsfera + GenAI + Streamlit. |
| **Modelos Preditivos (ML)** | [`modelos-preditivos-ml/chart_modelos_preditivos_ml.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/modelos-preditivos-ml/chart_modelos_preditivos_ml.png) | ROC-AUC 0.9478 e 99.53% de acurácia treinando in-database em 111 ms para ranquear propensão de resgate. |
| **Feature Importance (ML)** | [`feature-importance-ml/chart_feature_importance_ml.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/feature-importance-ml/chart_feature_importance_ml.png) | Transparência de IA (XAI): Ticket (+38.4%) e RFM VIP (+26.2%) orientando regras de CRM. |
| **GenAI & Copies** | [`genai-extracao-copies/chart_genai_extracao_copies.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/genai-extracao-copies/chart_genai_extracao_copies.png) | Validação 100% Pydantic em JSON Schema e aumento de +18% de CTR com copies contextuais. |
| **Similaridade Vetorial** | [`similaridade-produtos/chart_similaridade_produtos.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/similaridade-produtos/chart_similaridade_produtos.png) | Recomendação de SKUs substitutos em espaço vetorial 2D (t-SNE) gerando +12.4% de recuperação adicional. |
| **Data App & ROI** | [`data-app-simulador-roi/chart_data_app_simulador_roi.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/data-app-simulador-roi/chart_data_app_simulador_roi.png) | Simulação de sensibilidade de ROI (45x) e ganho de +R$ 167,9k líquidos com deploy em 1 clique. |

---

## ⚖️ 3. Regras de Governança

1. **Ground Truth Auditável**: 100% dos dados são consumidos de `data/mock/output_cleaned/parquet/` e relatórios de pipelines em `pipelines/`.
2. **Padrão Visual `charts-maker`**: Fundo branco puro (`#FFFFFF`), alta legibilidade, tipografia moderna (`Segoe UI`) e resolução de 300 DPI.
3. **Ausência de Pastas `assets/`**: Estrutura plana e direta em todos os subdiretórios.

---

Consulte a especificação técnica master em [`spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/views-05-insights-ia/spec.md).
