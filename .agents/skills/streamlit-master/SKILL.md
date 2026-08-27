---
name: streamlit-master
description: >-
  Especialista supremo na arquitetura, mapeamento de navegação, componentes modulares em 5 camadas,
  injeção dinâmica de estilos e orquestração de estados do Streamlit Data App da Dadosfera.
  Centraliza os fluxos de roteamento, sincronização via query params (?nav=), hot-reloading dinâmico,
  e padrões de UX/UI para consumo executivo e técnico.
---

# Streamlit Master — Arquitetura, Navegação & Orquestração do Data App

> [!IMPORTANT]
> **PADRÃO DE DESACOPLAMENTO ARQUITETURAL EM 5 CAMADAS**  
> O Streamlit Data App do projeto adota uma arquitetura estritamente desacoplada inspirada nos padrões modernos de engenharia de software (React/TypeScript + Python Puro):
> 1. `app/types/`: Contratos de dados imutáveis e tipagem estrita (`models.py`).
> 2. `app/constants/`: Constantes centrais imutáveis (`MappingProxyType`).
> 3. `app/services/`: Lógica de negócio, leitura de Parquets (Ground Truth) e cálculo determinístico.
> 4. `app/components/`: Componentes atômicos reutilizáveis, cards de KPI, header unificado e seletores.
> 5. `app/views/`: Orquestração de telas completas, painéis executivos e dossiês de avaliação.
> 6. `app/private_chat/`: Módulo isolado de orquestração de inferência autônoma com FastAPI / OpenAPI 3.1.0.

---

## 🧭 1. Mapeamento Canônico de Navegação & Query Params

A navegação global é orquestrada em [`app/app.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/app.py) através de `st.query_params` e sincronizada com os `MODES` de navegação:

```python
MODES = (
    "🏠 Hub Central de Entrada",                          # ?nav=hub
    "🥋 Central do Avaliador (Agentes, Skills & Insights)", # ?nav=management
    "🏢 Módulo de Negócio (BI & Consumo Executivo)",       # ?nav=business
    "💬 Console de Inferência Autônoma (/chat)",           # ?nav=chat
    "🌐 Visão Unificada (Todas as Abas)"                  # ?nav=unified
)
```

### 🗺️ Matriz de Rotas, Views e Componentes

| Rota / Parâmetro | Modo de Navegação | View Principal | Sub-Abas / Recursos | Folha de Estilo Ativa |
| :--- | :--- | :--- | :--- | :--- |
| `?nav=hub` | **Hub Central de Entrada** | [`view_hub_landing.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/views/view_hub_landing.py) | Hero split-screen, CTAs diretos, Big Numbers (115k rows, 18 regras) | `hub_theme.css` |
| `?nav=management` | **Central do Avaliador** | [`tab_agents.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/views/tab_agents.py) | `Agentes`, `Skills`, Header Integrado, Leitor Dossiê (460px) + Referências (210px) | `command_center.css` |
| `?nav=business` | **Módulo de Negócios & BI** | [`app/views/`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/views/) | `1. Simulador ROI`, `2. Explorador Semântico`, `3. Copiloto Prescritivo`, `4. Vitrine`, `5. Galeria Insights` | `custom.css` / `business_theme.css` |
| `?nav=chat` | **Console Autônomo (/chat)** | [`app/private_chat/view.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/private_chat/view.py) | Multi-agente FastAPI chat, Streaming, Seletor de Agentes, Inspector OpenAPI 3.1.0 | `chat_theme.css` |
| `?nav=unified` | **Visão Unificada** | [`app/app.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/app.py) | Consolidação de todas as abas técnicas e executivas em painel único | `custom.css` |

---

## ⚡ 2. Mecanismo de Hot-Reloading Dinâmico de Submódulos

Para mitigar limitações de cacheamento interno do `sys.modules` no interpretador Python sob Windows/Streamlit, [`app/app.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/app.py) aplica um ciclo dinâmico de recarga imediata:

```python
import importlib, sys

app_modules = [mod for mod in sys.modules if mod.startswith("app.") and mod != "app.app"]
for mod_name in app_modules:
    try:
        importlib.reload(sys.modules[mod_name])
    except Exception:
        pass
```

Isso assegura que qualquer alteração em arquivos em `app/components/`, `app/views/`, `app/services/` ou `app/styles/` seja refletida no navegador instantaneamente com **`F5`**, sem necessidade de reiniciar o processo do servidor.

---

## 🎨 3. Sistema de Estilos & Isolamento Visual por Modo

A injeção de CSS é declarativa e executada em tempo de execução de acordo com o ambiente ativo:

```python
def inject_theme(mode: str) -> None:
    styles_dir = os.path.join(os.path.dirname(__file__), "styles")
    if mode == "🏠 Hub Central de Entrada":
        css_file = "hub_theme.css"
    elif mode == "🥋 Central do Avaliador (Agentes, Skills & Insights)":
        css_file = "command_center.css"
    elif mode == "🏢 Módulo de Negócio (BI & Consumo Executivo)":
        css_file = "custom.css"
    elif mode == "💬 Console de Inferência Autônoma (/chat)":
        css_file = "chat_theme.css"
    else:
        css_file = "custom.css"

    css_path = os.path.join(styles_dir, css_file)
    if os.path.exists(css_path):
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
```

### 📐 Diretrizes Visuais de Enquadramento:
1. **Zero-Top Spacing (`padding-top: 0rem !important;`)**:
   - Cabeçalhos vazios (`.stAppHeader`, `[data-testid="stHeader"]`) suprimidos (`display: none; height: 0px;`).
   - Evita rolagem fantasma para cima em espaço escuro vazio.
2. **Cards com Alinhamento Estrito à Esquerda**:
   - `text-align: left !important;` e `align-items: flex-start !important;`.
   - Indicador de seleção ativa ciano na borda esquerda (`border-left: 4px solid var(--accent-cyan)`).
3. **Containers Delimitadores Integrados**:
   - Uso de `st.container(border=True)` estilizado via marcador de classe (`.evaluator-header-marker`) para agrupar títulos e botões no mesmo bloco visual.
4. **Visualização Side-by-Side em Galeria de Insights**:
   - Gráfico de alta fidelidade 300 DPI à esquerda + Dossiê de especificação técnica Markdown à direita.

---

## 📊 4. Ground Truth & Integração de Dados

Todos os módulos de BI e visualizações conectam-se exclusivamente aos datasets persistidos em Parquet via [`app/services/lakehouse_service.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/app/services/lakehouse_service.py):
- `data/mock/output_cleaned/parquet/tb_produtos_enriquecidos.parquet`
- `data/mock/output_cleaned/parquet/tb_carrinhos_abandonados.parquet`
- `data/mock/output_cleaned/parquet/tb_intervencoes_resgate.parquet`
- `data/mock/output_cleaned/parquet/tb_clientes_metricas.parquet`

---

## 🛠️ 5. Comandos de Operação

```powershell
# Execução padrão do Data App
python make.py data-app

# Execução nativa com Streamlit
python -m streamlit run app/app.py --server.port=8501
```
