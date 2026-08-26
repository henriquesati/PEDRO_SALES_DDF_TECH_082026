# 🏛️ Módulo Master de Views: Insights de Negócio (`views-04-insights`)

> **Momento do Roteiro**: **Ato 3 / Seção [4]-[5] — Prova de Conceito: Insights Descritivos e Prescritivos em Recuperação de Carrinho**  
> **Diretório Envelope**: `presentation/pitch/roteiro/views-04-insights/`  
> **Padrão de Organização**: Envelopamento Lógico de Módulos Analíticos  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../roteiro.txt), [`presentation/pitch/pitch_spec.md`](../../pitch_spec.md), [`presentation/insights/README.md`](../../../insights/README.md) e [`data/mock/output_cleaned/parquet/`](../../../../data/mock/output_cleaned/parquet/).

---

## 🎯 1. Visão Geral da Seção de Insights do Roteiro

A seção de **Insights de Negócio (`views-04-insights`)** materializa o valor tangível da Plataforma Dadosfera no contexto do e-commerce através da Prova de Conceito (PoC) de **Recuperação de Carrinho Abandonado**. 

Após demonstrar a transição da arquitetura técnica legada para a Dadosfera (Ato 1) e comprovar a confiabilidade dos pipelines, governança LGPD e modelagem Kimball (Ato 2 / Seção [3]), este módulo apresenta as **respostas analíticas às duas perguntas fundamentais de negócio**:

1. **Insights Descritivos** (*O que aconteceu?*): Mapeamento do funil de conversão, série temporal semestral, decomposição das 6 causas-raiz de abandono, taxa de recuperação observada e eficiência de custo por resgate (CAC / ROI).
2. **Insights Prescritivos** (*O que devemos fazer?*): Determinação do timing ótimo de disparo (curva de decaimento temporal +1h), estratégia de abordagem por cluster RFM (preservação de margem de clientes Premium sem desconto vs. cupons para Novos), análise de catálogo por categoria e rebalanceamento orçamentário entre canais.

---

## 🗺️ 2. Estrutura e Submódulos Envelopados

```text
presentation/pitch/roteiro/views-04-insights/
├── descritivos/                        # 📈 Submódulo: Insights Descritivos (O que aconteceu)
│   ├── funilrecuperacao/               # 📊 Funil Semestral de Conversão & Diagnóstico da Operação
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_insights_descritivos.png
│   ├── motivosabandono/                # 🔍 Decomposição das 6 Causas-Raiz de Abandono
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_02_motivos_abandono.png
│   ├── custorecuperacao/               # 💰 Eficiência Financeira, CAC de Resgate & ROI
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_03_custo_recuperacao_roi.png
│   ├── spec.md                         # 📄 Especificação Índice dos Descritivos
│   └── README.md
├── prescritivos/                       # 💡 Submódulo: Insights Prescritivos (O que fazer)
│   ├── timingenvio/                    # ⏱️ Curva de Decaimento Temporal (+1h)
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   ├── chart_05_otimizacao_timing_envio.png
│   │   └── card_destaque_timing_executivo.png
│   ├── estrategiaresgate/              # 👥 Estratégia por Segmento RFM & Preservação de Margem
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_insights_prescritivos.png
│   ├── produtosabandonados/            # 📦 Categorias & Produtos Mais Abandonados
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_03_produtos_mais_abandonados.png
│   ├── roicampanhas/                   # 📈 ROI, Eficiência de Canais & Rebalanceamento de Budget
│   │   ├── spec.md
│   │   ├── generate_chart.py
│   │   └── chart_04_roi_campanhas_resgate.png
│   ├── spec.md                         # 📄 Especificação Índice dos Prescritivos
│   └── README.md
├── spec.md                             # 📄 Esta Especificação Master do Envelope
└── README.md                           # 🧭 Guia Rápido de Navegação do Módulo
```

---

## 📊 3. Resumo dos Submódulos

| Submódulo da View | Momento no Roteiro | Pergunta de Negócio | Foco da Narrativa & Artefatos |
| :--- | :--- | :---: | :--- |
| [`descritivos/funilrecuperacao/`](descritivos/funilrecuperacao/) | **Ato 3 / Seção [4.1] — Diagnóstico da Operação** | *O que aconteceu?* | • **7.500 carrinhos semestrais** com **69,7% de abandono basal**.<br/>• **+10,1% de recuperação** com réguas Dadosfera (+R$ 167,9k recuperados e lift de conversão total de 23,1% para 29,7%).<br/>• Artefato: `chart_insights_descritivos.png`. |
| [`descritivos/motivosabandono/`](descritivos/motivosabandono/) | **Ato 3 / Seção [4.1] — Causas de Abandono** | *Por que abandonaram?* | • Decomposição das 6 causas-raiz: Frete Caro (38,2%), Indecisão (24,1%), Erro no Pagamento (18,3%).<br/>• Concentração financeira por faixa de ticket.<br/>• Artefato: `chart_02_motivos_abandono.png`. |
| [`descritivos/custorecuperacao/`](descritivos/custorecuperacao/) | **Ato 3 / Seção [4.1] — CAC & ROI** | *Qual foi o custo?* | • CAC Unitário de Resgate: E-mail R$ 1,02/resgate, Push R$ 1,67, SMS R$ 3,00, WhatsApp R$ 12,00.<br/>• Multiplicador de ROI consolidado em 45x.<br/>• Artefato: `chart_03_custo_recuperacao_roi.png`. |
| [`prescritivos/timingenvio/`](prescritivos/timingenvio/) | **Ato 3 / Seção [4.2] — Timing de Disparo** | *Quando agir?* | • **Janela de Ouro (+1h)**: A 1ª hora após o abandono concentra **86,4% de todas as conversões observadas** (-70% após 24h).<br/>• Artefatos: `chart_05_otimizacao_timing_envio.png` e `card_destaque_timing_executivo.png`. |
| [`prescritivos/estrategiaresgate/`](prescritivos/estrategiaresgate/) | **Ato 3 / Seção [4.2] — Segmentação RFM** | *O que oferecer para quem?* | • **Preservação de Margem**: Clientes Premium convertem 18% via WhatsApp VIP **sem conceder desconto** (100% da margem protegida).<br/>• Artefato: `chart_insights_prescritivos.png`. |
| [`prescritivos/produtosabandonados/`](prescritivos/produtosabandonados/) | **Ato 3 / Seção [4.2] — Ações de Catálogo** | *Quais produtos otimizar?* | • Eletrônicos & Decoração (78,8% / R$ 7,34M represados).<br/>• Matriz Multidimensional de Posicionamento (Scatter Log + 4 Quadrantes), Top 5 SKUs Críticos e 5 Cards Prescritivos de Intervenção de Catálogo.<br/>• Artefato: `chart_03_produtos_mais_abandonados.png`. |
| [`prescritivos/roicampanhas/`](prescritivos/roicampanhas/) | **Ato 3 / Seção [4.2] — Alocação de Budget** | *Como balancear o orçamento?* | • Rebalanceamento orçamentário: 85% E-mail + 12% WhatsApp VIP (reduzindo dispersão em SMS/Push).<br/>• Artefato: `chart_04_roi_campanhas_resgate.png`. |

---

## 🎨 4. Padrões Gráficos Compartilhados (`charts-maker` Standard)

* **Canvas & Fundo**: `#FFFFFF` (Branco Puro) em 100% dos painéis, eixos e canvas.
* **Proporção & Resolução**: **16:9 Widescreen** exportado a **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`).
* **Integridade Absoluta (Ground Truth)**: Todos os dados plotados são carregados diretamente dos arquivos Parquet em `data/mock/output_cleaned/parquet/`.
* **Ausência de Pasta `assets/`**: Estrutura de pastas limpa e padronizada.
