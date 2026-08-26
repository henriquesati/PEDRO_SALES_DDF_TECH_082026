# 📂 Arquitetura de Diretórios do Roteiro (`presentation/pitch/roteiro/`)

> **Objetivo**: Organizar e centralizar como Fonte Única da Verdade toda a infraestrutura de visões visuais (*views*), especificações técnicas e scripts geradores que compõem a apresentação executiva do case no [`roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt) e no [`pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md).

---

## 🏛️ 1. Estrutura Modular Completa

```text
presentation/pitch/roteiro/
├── roteiro.txt                                # 📜 Roteiro Narrativo Completo (Atos 1, 2, 3 e 4)
├── spec.md                                    # 📄 Especificação Master de Governança das Views
├── catalogo_graficos_referencias.md          # 📊 Catálogo Geral com Links Diretos a todos os PNGs
├── README.md                                  # 🧭 Este Guia Canônico de Arquitetura das Views
│
├── 🏛️ Ato 1: Arquitetura, Riscos & TCO
│   ├── arquitetura-view/arc-diagram-view/     # Diagramas L2R Legado vs Dadosfera (*única com assets/icons*)
│   ├── problema-elasticidade/                 # Risco de Downtime em Picos (Black Friday: R$ 50k-100k/min)
│   └── staff-pain-point/                      # Escalabilidade de Equipe & Curva de TCO (Crossover Break-even)
│
├── 🛡️ Ato 2: Fundamentos de Dados (Seção [3])
│   └── view-03-dado-qualidades/               # Master Envelope de Qualidade e Governança
│       ├── view-lake-architecture/            # Lakehouse Medallion & 18 Regras Great Expectations (94.2% Conformidade)
│       ├── view-governanca/                   # Catálogo Vivo, Contrato de Metadados & Blindagem LGPD / Opt-in
│       └── view-model-kimball/                # Modelagem Dimensional Gold (Star Schema 1-Hop: 6 Dim / 2 Fatos)
│
├── 📈 Ato 3: Insights de Negócio (Seção [4])
│   └── views-04-insights/                     # Master Envelope de Insights Analíticos
│       ├── descritivos/                       # Submódulos Descritivos (O que aconteceu?)
│       │   ├── funilrecuperacao/              # Funil Semestral (7.500 carrinhos / +10,1% resgate / +R$ 167,9k)
│       │   ├── motivosabandono/               # Concentração por Ticket & 6 Causas-Raiz de Abandono
│       │   └── custorecuperacao/              # CAC Unitário por Canal & ROI 45x Multiplicador
│       └── prescritivos/                      # Submódulos Prescritivos (O que fazer?)
│           ├── timingenvio/                   # Curva de Decaimento & Janela de Ouro (+1h com 86,4% de resgate)
│           ├── estrategiaresgate/             # Segmentação RFM & Margem VIP sem Desconto (18% conv. WhatsApp)
│           ├── produtosabandonados/           # Receita Represada & Matriz de Intervenções de Catálogo
│           └── roicampanhas/                  # Funil por Canal & Rebalanceamento de Budget (85% E-mail / 12% WhatsApp)
│
└── 🧠 Ato 4: Inteligência & Data Apps (Seção [5])
    └── views-05-insights-ia/                  # Master Envelope de Inteligência, GenAI & Data Apps
        ├── modelos-preditivos-ml/             # Machine Learning Supervisionado (ROC-AUC 0.9478 / 99.53% acurácia)
        ├── feature-importance-ml/             # Pesos do Modelo & XAI (Ticket +38.4%, RFM VIP +26.2%, Frete +18.5%)
        ├── genai-extracao-copies/             # GenAI, Pydantic 100% & Copywriting Personalizado (+18% CTR)
        ├── similaridade-produtos/             # Embeddings, Espaço 2D (t-SNE) & Recomendação de SKUs (+12.4% resgate)
        └── data-app-simulador-roi/            # Data App Streamlit, Simulação de ROI (45x) & Waterfall Contábil
```

---

## 📐 2. Padrão Canônico da Tríade por Subdiretório

Cada subdiretório analítico segue estritamente a tríade de arquivos:

```text
pasta-do-modulo/
├── generate_chart.py    # 🐍 Script declarativo puro (Ground Truth Parquet -> 300 DPI)
├── spec.md              # 📄 Especificação técnica, métricas canônicas e narrativa de negócio
└── chart_*.png          # 📊 Painel visual executivo (16:9, fundo branco #FFFFFF, 300 DPI)
```

---

## ⚖️ 3. Regras Globais de Governança

1. **Ausência de Pastas `assets/`**: Toda pasta de view mantém estrutura plana e direta. A **única exceção** autorizada em todo o projeto é [`arquitetura-view/arc-diagram-view/assets/icons/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/arquitetura-view/arc-diagram-view/assets/icons/) para a biblioteca de logos transparentes de nuvem.
2. **Ground Truth Auditável**: 100% dos dados dos gráficos são consumidos diretamente dos arquivos Parquet em `data/mock/output_cleaned/parquet/` e dos relatórios de pipelines auditados (zero hardcoding).
3. **Padrão Visual `charts-maker`**: Fundo branco puro (`#FFFFFF`), alta legibilidade, tipografia sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Arial`) e renderização em 300 DPI com `bbox_inches="tight"`.
4. **Hierarquia Documental**:
   - Master Source of Truth de Negócio e Pitch: [`presentation/pitch/pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md).
   - Roteiro Falado e Cronologia: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt).
   - Catálogo Geral de Links dos Gráficos: [`catalogo_graficos_referencias.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/catalogo_graficos_referencias.md).
   - Arquitetura de Diretórios das Views: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md) (Este Arquivo).
