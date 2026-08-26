# 💡 Módulo de Views: Insights Prescritivos (`views-04-insights/prescritivos`)

> **Momento do Roteiro**: **Ato 3 / Seção [4.2] — Tomada de Decisão: Ações Prescritivas, Regras de Negócio e ROI**  
> **Caminho da View**: `presentation/pitch/roteiro/views-04-insights/prescritivos/`  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../../roteiro.txt), [`presentation/pitch/pitch_spec.md`](../../../pitch_spec.md#32-regras-de-negócio-e-evidências-analíticas) e [`data/mock/output_cleaned/parquet/`](../../../../../data/mock/output_cleaned/parquet/).

---

## 🎯 1. Visão Geral dos Submódulos Prescritivos

Este diretório agrupa todas as visões analíticas prescritivas para recuperação inteligente e orientada a dados na Dadosfera:

```text
presentation/pitch/roteiro/views-04-insights/prescritivos/
├── timingenvio/                        # ⏱️ Otimização de Timing & Curva de Decaimento (+1h)
│   ├── spec.md                         # 📄 Especificação técnica
│   ├── generate_chart.py               # 🐍 Script gerador 300 DPI
│   ├── chart_05_otimizacao_timing_envio.png # 📊 Curva de decaimento
│   └── card_destaque_timing_executivo.png   # 📇 Mini card executivo
├── estrategiaresgate/                  # 👥 Estratégia por Segmento RFM & Preservação de Margem
│   ├── spec.md                         # 📄 Especificação técnica
│   ├── generate_chart.py               # 🐍 Script gerador 300 DPI
│   └── chart_insights_prescritivos.png # 📊 Painel executivo de RFM & Políticas
├── produtosabandonados/                # 📦 Categorias & Produtos Mais Abandonados
│   ├── spec.md                         # 📄 Especificação técnica
│   ├── generate_chart.py               # 🐍 Script gerador 300 DPI
│   └── chart_03_produtos_mais_abandonados.png # 📊 Matriz de intervenções de catálogo
└── roicampanhas/                       # 📈 ROI, Eficiência de Canais & Rebalanceamento de Budget
    ├── spec.md                         # 📄 Especificação técnica
    ├── generate_chart.py               # 🐍 Script gerador 300 DPI
    └── chart_04_roi_campanhas_resgate.png # 📊 Funil por canal & budget ótimo
```

---

## 📊 2. Tabela de Módulos & Artefatos

| Submódulo | Foco de Apresentação | Principais Métricas | Artefatos Gráficos |
| :--- | :--- | :--- | :---: |
| [`timingenvio/`](timingenvio/) | **Janela de Ouro de Disparo** | +1h concentra 86,4% das conversões (-70% após 24h) | [`chart_05_otimizacao_timing_envio.png`](timingenvio/chart_05_otimizacao_timing_envio.png), [`card_destaque_timing_executivo.png`](timingenvio/card_destaque_timing_executivo.png) |
| [`estrategiaresgate/`](estrategiaresgate/) | **Preservação de Margem & RFM** | WhatsApp VIP 18% conversão com 0% cupom (+R$ 143,70/disparo) | [`chart_insights_prescritivos.png`](estrategiaresgate/chart_insights_prescritivos.png) |
| [`produtosabandonados/`](produtosabandonados/) | **Catálogo & UX Prescritiva** | Eletrônicos & Decoração (78,8% / R$ 7,34M represados) + Matriz de 4 Quadrantes e Top 5 SKUs | [`chart_03_produtos_mais_abandonados.png`](produtosabandonados/chart_03_produtos_mais_abandonados.png) |
| [`roicampanhas/`](roicampanhas/) | **Budget & Rebalanceamento** | 85% E-mail + 12% WhatsApp VIP (redução de dispersão SMS/Push) | [`chart_04_roi_campanhas_resgate.png`](roicampanhas/chart_04_roi_campanhas_resgate.png) |
