# 📊 Especificação Canônica: Data Apps & Simulador de ROI (`04_data_app_simulador_roi`)

> **Módulo:** `insights/04_intelligence_ai/04_data_app_simulador_roi/`  
> **Artefato Canônico:** [`chart_data_app_simulador_roi.png`](chart_data_app_simulador_roi.png)  
> **Item do Case:** Item 9 — Data Apps em Streamlit & Bônus GenAI  
> **Framework Normativo:** [`spec_data_app_streamlit_001`](../../../pipelines/case-item-09/specs.md) • [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt)  
> **Fontes de Dados (Ground Truth):** `data/mock/output_cleaned/parquet/carrinhos.parquet`, `eventos_resgate.parquet`, `produtos.parquet`, `metrics/catalogo_kpis.md`.
> **Padrão Visual:** White Theme / `charts-maker` Standard (Fundo Branco Puro `#FFFFFF`, 16:9, 300 DPI).

---

## 🎯 1. Visão Geral e Alavancagem Analítica

O Data App Streamlit (`app/`) atua como a interface unificada de decisão executiva para o módulo **Consumir** da Dadosfera. A aplicação opera sob uma arquitetura desacoplada de 5 camadas (inspirada em React + TypeScript) com 4 abas estratégicas:

1. **Simulador Prescritivo de ROI & Rebalanceamento**: Decomposição contábil em cascata (Waterfall), curva de sensibilidade de margem e preset inteligente de canais (85% E-mail, 12% WhatsApp VIP, 2% SMS, 1% Push) gerando **+R$ 264.041,60 em receita bruta** e preservando **28.5% de margem líquida** com multiplicador de ROI de até 45.0x.
2. **Explorador Semântico & Busca Vetorial 2D**: Mapeamento de 300 SKUs em 7 categorias com centróides, trajetórias vetoriais do produto abandonado até alternativas, ranking Top-5 com score de cosseno e Card de Decisão Executiva C-Level.
3. **Copiloto Prescritivo de Resgate**: Geração de copies por canal com múltiplos tons de voz (*Urgência, Suporte, Prova Social*) e serialização contratual em Pydantic JSON Schema.
4. **Vitrine Visual de Produtos (Item Bônus)**: Card comercial estruturado com proposta de valor, pilares técnicos de materiais e prompts calibrados para DALL-E em estúdio fotográfico.
