# 🛒 Dadosfera Streamlit Data App (`app/`)

> **Módulo:** Consumir & Data Apps (Item 9 & Bônus GenAI do Case Dadosfera)  
> **Padrão Visual:** White Theme / `charts-maker` Standard (Fundo Branco Puro `#FFFFFF`, Tipografia Sem Serifa Moderna)  
> **Paradigma:** Funcional & Declarativo com Tipagem Estrita (`TypeAlias`, `@dataclass(frozen=True)`, `MappingProxyType`)  
> **Arquitetura:** 5 Camadas inspirada em React + TypeScript  

---

## 🏛️ 1. Arquitetura Modular em 5 Camadas

O aplicativo foi estruturado com desacoplamento rigoroso entre contratos de dados, regras de negócio, componentes visuais e telas:

```text
app/
├── app.py                          # 🚀 Entrypoint principal (Banner Executivo & 4 Abas)
├── README.md                       # 📄 Documentação técnica da aplicação
├── styles/
│   └── custom.css                  # 🎨 Design System White Theme, Pill Badges e Cards Executivos
├── constants/
│   ├── settings.py                 # ⚙️ Benchmarks canônicos (7.500 carrinhos, R$ 348,80, Mix 85/12/2/1)
│   └── theme.py                    # 🎨 Helper de layout padronizado Plotly (White Canvas #FFFFFF)
├── types/
│   └── models.py                   # 📐 Contratos de dados imutáveis (Data Contracts)
├── services/
│   ├── lakehouse_service.py        # 📁 Leitor resiliente com cache dos Parquets Silver/Gold
│   ├── similarity_service.py       # 🔍 Busca vetorial por cosseno, PCA/t-SNE e trajetórias
│   ├── simulation_service.py       # 📊 Simulador financeiro, CAC unitário e margem preservada (28.5%)
│   ├── copy_service.py             # 🤖 Gerador de Copies com despacho funcional, Whisper e DALL-E
├── components/
│   ├── kpi_cards.py                # 🏆 Cards de métricas com badges delta semânticos e tooltips
│   ├── charts.py                   # 📈 Gráficos Plotly reutilizáveis (Waterfall, Sensibilidade, 2D)
│   └── chat_preview.py             # 💬 Visualizadores multicanais, Whisper AI e Decision Cards
└── views/
    ├── tab_roi.py                  # 📊 Aba 1: Simulador de ROI & Sensibilidade
    ├── tab_similarity.py           # 🔍 Aba 2: Explorador Semântico de Catálogo (GenAI)
    ├── tab_copilot.py              # 🤖 Aba 3: Copiloto Prescritivo de Resgate
    └── tab_showcase.py             # 🎨 Aba 4: Vitrine Visual de Produtos (Item Bônus)
```

---

## 📑 2. Especificação das 4 Abas da Aplicação

### 📊 Aba 1: Simulador de ROI & Sensibilidade (`views/tab_roi.py`)
- **Preset Inteligente Dadosfera**: Alternância de 1 clique entre o *Mix Recomendado Dadosfera* (85% E-mail, 12% WhatsApp VIP, 2% SMS, 1% Push) e *Alocação Manual*.
- **Indicadores C-Level**: Carrinhos Resgatados, Receita Bruta, Investimento Total (CAC + Cupom) e Receita Líquida Incremental com **Margem Preservada (28.5%)** e multiplicador de ROI até 45x.
- **Gráficos Interativos**:
  - *Waterfall*: Decomposição contábil da receita bruta até a receita líquida.
  - *Curva de Sensibilidade*: Impacto do desconto sobre o ROI e margem operacional.
  - *Rebalanceamento Orçamentário*: Gráfico de barras horizontais comparando mix convencional vs otimizado.

### 🔍 Aba 2: Explorador Semântico de Catálogo (`views/tab_similarity.py`)
- **Header Executivo**: 4 KPI Cards (300 SKUs Vetorizados, Similaridade Média 89.4%, Recuperação Cruzada +12.4%, Latência < 2.5 ms).
- **Espaço Vetorial 2D (t-SNE / PCA)**: Gráfico de dispersão com centróides das 7 categorias reais e trajetórias vetoriais do produto abandonado (âncora) até as 3 alternativas recomendadas.
- **Ranking Top-5 de Cosseno**: Lista detalhada com score de afinidade, delta de preço e tags estratégicas (*Substituto, Cross-sell, Acessório*).
- **Card de Decisão C-Level**: Comparativo entre *Estratégia Convencional (Queima de Cupom)* vs *Vitrine Inteligente Dadosfera (28.5% de Margem Preservada)*.

### 🤖 Aba 3: Copiloto Prescritivo de Resgate (`views/tab_copilot.py`)
- **Tons de Voz Estratégicos (GenAI)**: Seletor de *Urgência (72h)*, *Suporte Técnico (127V/instalação)* ou *Prova Social (4.9 estrelas)*.
- **Preview Multicanal Fiel**: Layouts realistas para WhatsApp Concierge, E-mail corporativo em HTML e SMS.
- **Payload Pydantic**: Visualizador do JSON Schema estruturado com validação de contrato.

### 🎨 Aba 4: Vitrine Visual de Produtos (`views/tab_showcase.py`)
- **Apresentação Comercial**: Card de proposta de valor e pilares de engenharia do produto.
- **Multimodal Whisper AI**: Módulo com transcrição de áudio do concierge técnico de suporte.
- **Engenharia de Prompts**: Prompts declarativos documentados para geração de estúdio fotográfico com DALL-E e síntese textual com LLMs.

---

## 🎨 3. Design Tokens & Paleta Semântica

| Token | Hex | Significado de Negócio |
|---|---|---|
| `--bg-canvas` | `#FFFFFF` | Fundo principal da aplicação (Pure White) |
| `--bg-light` | `#F8FAFC` | Superfície de cards e containers (Slate 50) |
| `--primary-blue` | `#2563EB` | Tráfego orgânico, modelo baseline e CTAs primários |
| `--success-green` | `#059669` | Conversão recuperada, receita líquida e margem preservada |
| `--danger-red` | `#E11D48` | Abandono de carrinho, custos de comunicação e fricção |
| `--warning-amber` | `#D97706` | Alerta de risco moderado e canal SMS |
| `--accent-purple` | `#7C3AED` | IA, busca vetorial e clientes Champions / VIP |

---

## 🚀 4. Instruções de Execução

```bash
# Execução direta via Streamlit:
streamlit run app/app.py

# Ou via Makefile do projeto:
python make.py data-app
```
