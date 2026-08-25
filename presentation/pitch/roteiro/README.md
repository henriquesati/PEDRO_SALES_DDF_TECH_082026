# 📂 Diretório de Views do Roteiro de Pitch (`presentation/pitch/roteiro/`)

> **Finalidade**: Armazenar, organizar e catalogar todas as **visões visuais (views)**, mockups de slides, diagramas interativos e geradores de apresentação associados aos momentos do `roteiro.txt`.

---

## 🗺️ Estrutura de Diretórios

| Diretório / View | Momento do Roteiro | Conteúdo / Artefatos |
| :--- | :--- | :--- |
| [`arquitetura-view/`](./arquitetura-view) | **Ato 1: Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Dadosfera** | • Gerador de PowerPoint (`generate_architecture_deck.py`)<br/>• Apresentação PPTX (`arquitetura_dadosfera.pptx`)<br/>• Pacote de 26 ícones oficiais em vetor/PNG (`assets/icons/*.png`)<br/>• Submódulo: [`arc-diagram-view/`](./arquitetura-view/arc-diagram-view/) |
| [`arquitetura-view/arc-diagram-view/`](./arquitetura-view/arc-diagram-view) | **Ato 1: Diagramas L2R do Ciclo de Vida dos Dados (Legado vs Dadosfera)** | • Diagramas L2R (`grafico-legado-l2r.png`, `grafico-dadosfera-l2r.png`)<br/>• Templates vazios de animação (`*-vazio.png`)<br/>• Wrapper gerador (`generate_chart.py`)<br/>• Especificação Técnica (`spec.md`) |
| [`problema-elasticidade/`](./problema-elasticidade) | **Momento 3: Risco de Elasticidade em Picos (Black Friday)** | • Gráfico Executivo 16:9 (`chart_problema_elasticidade.png`)<br/>• Script Gerador (`generate_chart.py`)<br/>• Especificação Técnica (`spec.md`) |
| [`staff-pain-point/`](./staff-pain-point) | **Momento 4: Pain Point de Staff & Escalabilidade da Arquitetura Solta** | • Gráfico Executivo 16:9 (`chart_staff_pain_point.png`)<br/>• Comparativo TCO (`chart_custo_infra_vs_dadosfera_crossover.png`)<br/>• Scripts Geradores (`generate_chart.py`, `generate_cost_comparison_chart.py`)<br/>• Especificação Técnica (`spec.md`) |
| [`case-carrinho/views/insights/timingenvio/`](./case-carrinho/views/insights/timingenvio) | **Ato 3: Blueprint Case Carrinho (Otimização de Timing & Decaimento +1h)** | • Painel Executivo 300 DPI (`chart_05_otimizacao_timing_envio.png`)<br/>• Script Gerador (`generate_chart.py`)<br/>• Especificação Técnica (`spec.md`) |

---

## 📌 Padrão de Governança para Novas Views (Consulte [`spec.md`](./spec.md))
1. Cada momento-chave do roteiro com necessidade de suporte visual dedicado segue a convenção:
   - `presentation/pitch/roteiro/arquitetura-view/[diretorio-nomeado-view]/`
   - `presentation/pitch/roteiro/case-carrinho/views/<categoria>/<nome-da-view>/`
2. Cada view deve conter:
   - `spec.md`: Especificação técnica e narrativa da view em texto corrido explicativo.
   - Artefatos gráficos exportados (PNG, SVG, PPTX) em padrão 300 DPI.
   - Script gerador `generate_chart.py` (implementação direta ou wrapper que importa e executa o original).
