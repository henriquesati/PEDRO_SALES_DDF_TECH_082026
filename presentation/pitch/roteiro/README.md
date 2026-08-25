# 📂 Diretório de Views do Roteiro de Pitch (`presentation/pitch/roteiro/`)

> **Finalidade**: Armazenar, organizar e catalogar todas as **visões visuais (views)**, mockups de slides, diagramas interativos e geradores de apresentação associados aos momentos do `roteiro.txt`.

---

## 🗺️ Estrutura de Diretórios

| Diretório / View | Momento do Roteiro | Conteúdo / Artefatos |
| :--- | :--- | :--- |
| [`arquitetura-view/arc-diagram-view/`](./arquitetura-view/arc-diagram-view) | **Ato 1: Diagramas L2R do Ciclo de Vida dos Dados (Legado vs Dadosfera)** | • Diagramas L2R (`grafico-legado-l2r.png`, `grafico-dadosfera-l2r.png`)<br/>• Templates de animação (`*-vazio.png`)<br/>• Subpasta com 26 ícones: `assets/icons/*.png`<br/>• Scripts: `generate_chart.py`, `download_high_res_icons.py`<br/>• Especificação Técnica (`spec.md`) |
| [`problema-elasticidade/`](./problema-elasticidade) | **Momento 3: Risco de Elasticidade em Picos (Black Friday)** | • Gráfico Executivo 16:9 (`chart_problema_elasticidade.png`)<br/>• Script Gerador (`generate_chart.py`)<br/>• Especificação Técnica (`spec.md`) |
| [`staff-pain-point/`](./staff-pain-point) | **Momento 4: Pain Point de Staff & Escalabilidade da Arquitetura Solta** | • Gráfico Executivo 16:9 (`chart_staff_pain_point.png`)<br/>• Comparativo TCO (`chart_custo_infra_vs_dadosfera_crossover.png`)<br/>• Scripts Geradores (`generate_chart.py`, `generate_cost_comparison_chart.py`)<br/>• Especificação Técnica (`spec.md`) |
| [`case-carrinho/views/insights/timingenvio/`](./case-carrinho/views/insights/timingenvio) | **Ato 3: Blueprint Case Carrinho (Otimização de Timing & Decaimento +1h)** | • Painel Executivo 300 DPI (`chart_05_otimizacao_timing_envio.png`)<br/>• Script Gerador (`generate_chart.py`)<br/>• Especificação Técnica (`spec.md`) |

---

## 📌 Padrão de Governança para Novas Views (Consulte [`spec.md`](./spec.md))
1. A estrutura padrão para todas as pastas de views é obrigatoriamente:
   ```
   pasta/generate_chart.py
   pasta/spec.md
   pasta/chart.png
   ```
2. **Exceção Única**: Apenas a pasta `arquitetura-view/arc-diagram-view/` possui o subdiretório `assets/` (para a biblioteca de logos e ícones de serviços da nuvem).
3. Todas as demais views mantêm estrutura normal e plana, podendo adicionar arquivos extras somente quando necessário e aprovado pelo usuário.
4. Cada view deve conter seu `spec.md` detalhando em **texto corrido** o significado de negócio do gráfico.
