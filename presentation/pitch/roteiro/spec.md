# 🧭 Especificação Arquitetural & Padrão de Governança do Roteiro (`presentation/pitch/roteiro/`)

> **Finalidade**: Centralizar as diretrizes, padrões de estrutura de pastas, governança de views visuais e mapeamento de todos os artefatos de apoio ao roteiro de apresentação do pitch ([`roteiro.txt`](roteiro.txt)).

---

## 🏛️ 1. Padrão Arquitetural de Diretórios de Views

A organização de diretórios visuais do roteiro segue a convenção estruturada por blocos temáticos e momentos da fala:

$$\text{presentation/pitch/roteiro/} \longrightarrow \mathbf{arquitetura\text{-}view/[diretorio\text{-}nomeado\text{-}view]}$$

### 📌 Regras Obrigatórias de Governança para cada View:
1. **Documento `spec.md` Obrigatório**: Cada subdiretório de view DEVE conter um arquivo `spec.md` detalhando em **texto corrido e executivo** o que a visualização representa, qual momento do roteiro ela ilustra e qual argumento de negócio ela sustenta.
2. **Padrões de Implementação do Gerador (`generate_chart.py`)**:
   * **Opção 1 (Implementação Direta)**: O diretório implementa seu próprio script `generate_chart.py` declarativo e funcional, que lê o Ground Truth em Parquet e renderiza a imagem no próprio diretório.
   * **Opção 2 (Importação de Script Existente)**: Se o gráfico/diagrama já foi definido em outro local do ecossistema, o diretório deve conter um `generate_chart.py` que **importa o script gerador original e o executa**, garantindo a persistência do artefato no diretório da view sem duplicar lógica complexa.

---

## 🗺️ 2. Mapeamento de Diretórios de Views

| Diretório da View | Momento / Ato do Roteiro | Tipo de Implementação | Artefatos Gerados |
| :--- | :--- | :---: | :--- |
| [`arquitetura-view/arc-diagram-view/`](arquitetura-view/arc-diagram-view/) | **Ato 1: Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Dadosfera** | Importa e executa `generate_l2r_charts.py` | • `grafico-legado-l2r.png`<br/>• `grafico-dadosfera-l2r.png`<br/>• `grafico-legado-l2r-vazio.png`<br/>• `grafico-dadosfera-l2r-vazio.png` |
| [`problema-elasticidade/`](problema-elasticidade/) | **Momento 3: Risco de Elasticidade e Downtime em Picos (Black Friday)** | Implementação Direta (`generate_chart.py`) | • `chart_problema_elasticidade.png` (Painel Executivo 16:9) |
| [`staff-pain-point/`](staff-pain-point/) | **Momento 4: Headcount Linear & Escalabilidade de Equipe** | Implementação Direta (`generate_chart.py` e `generate_cost_comparison_chart.py`) | • `chart_staff_pain_point.png`<br/>• `chart_custo_infra_vs_dadosfera_crossover.png` |
| [`case-carrinho/views/insights/timingenvio/`](case-carrinho/views/insights/timingenvio/) | **Ato 3: Blueprint Case Carrinho — Otimização de Timing (+1h & Decay Curve)** | Implementação Direta (`generate_chart.py`) | • `chart_05_otimizacao_timing_envio.png` (300 DPI) |

---

## 🎨 3. Padrão Visual Global (`charts-maker` Standard)

Todos os geradores e saídas gráficas do diretório `roteiro/` devem obrigatoriamente respeitar os seguintes princípios:
* **Fundo Branco Puro**: `#FFFFFF` em 100% dos painéis e canvas.
* **Resolução**: Exportação a **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`).
* **Integridade dos Dados**: Conexão exclusiva aos dados reais em Parquet (`data/mock/output_cleaned/parquet/`).
