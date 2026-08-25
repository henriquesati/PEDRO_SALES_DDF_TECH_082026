## 🏛️ 1. Padrão Arquitetural de Diretórios de Views

A organização de diretórios visuais do roteiro segue a convenção estruturada:

$$\text{presentation/pitch/roteiro/} \longrightarrow \mathbf{arquitetura\text{-}view/[diretorio\text{-}nomeado\text{-}view]}$$

### 📌 Regras Obrigatórias de Estrutura de Pastas:
1. **Estrutura Padrão (Enxuta / Canônica)**:
   A estrutura padrão para todas as pastas de views é obrigatoriamente:
   ```
   pasta/
   ├── generate_chart.py    # 🐍 Script declarativo de renderização a partir do Parquet
   ├── spec.md              # 📄 Especificação técnica em texto corrido
   └── chart.png            # 📊 Imagem gerada em alta resolução (300 DPI)
   ```
2. **Exceção Única para Subpasta `assets/`**:
   * **Somente a pasta `arc-diagram-view/`** possui um subdiretório `assets/` (dedicado exclusivamente a armazenar os 26 logos e ícones de serviços da AWS e da Dadosfera) e scripts utilitários adicionais (`download_high_res_icons.py`).
   * **Todas as demais pastas de views devem ser normais e sem pasta `assets/`**, mantendo seus scripts e saídas gráficos diretamente na raiz do diretório.
   * As pastas só podem ter arquivos e scripts adicionais quando estritamente **necessário e aprovado pelo usuário**.
3. **Documento `spec.md` em Texto Corrido**:
   Cada diretório DEVE conter uma `spec.md` explicando em **texto corrido** o que a view representa no roteiro, qual momento da narrativa ela apoia e qual o diagnóstico/insight de negócio transmitido.

---

## 🗺️ 2. Mapeamento dos Módulos de Views do Roteiro

| Diretório da View | Momento / Ato do Roteiro | Estrutura de Arquivos | Artefatos Gerados |
| :--- | :--- | :---: | :--- |
| [`arquitetura-view/arc-diagram-view/`](arquitetura-view/arc-diagram-view/) | **Ato 1: Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Dadosfera** | `assets/icons/` + Scripts | • `grafico-legado-l2r.png`<br/>• `grafico-dadosfera-l2r.png`<br/>• `grafico-legado-l2r-vazio.png`<br/>• `grafico-dadosfera-l2r-vazio.png` |
| [`problema-elasticidade/`](problema-elasticidade/) | **Momento 3: Risco de Elasticidade e Downtime em Picos (Black Friday)** | Padrão Enxuto | • `chart_problema_elasticidade.png` (Painel Executivo 16:9) |
| [`staff-pain-point/`](staff-pain-point/) | **Momento 4: Headcount Linear & Escalabilidade de Equipe** | Padrão com 2 Scripts Aprovados | • `chart_staff_pain_point.png`<br/>• `chart_custo_infra_vs_dadosfera_crossover.png` |
| [`case-carrinho/views/insights/timingenvio/`](case-carrinho/views/insights/timingenvio/) | **Ato 3: Blueprint Case Carrinho — Otimização de Timing (+1h & Decay Curve)** | Padrão Enxuto | • `chart_05_otimizacao_timing_envio.png` (300 DPI) |

---

## 🎨 3. Padrão Visual Global (`charts-maker` Standard)

Todos os geradores e saídas gráficas do diretório `roteiro/` devem obrigatoriamente respeitar os seguintes princípios:
* **Fundo Branco Puro**: `#FFFFFF` em 100% dos painéis e canvas.
* **Resolução**: Exportação a **300 DPI** com `bbox_inches="tight"`.
* **Tipografia**: Família sem serifa moderna (`Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`).
* **Integridade dos Dados**: Conexão exclusiva aos dados reais em Parquet (`data/mock/output_cleaned/parquet/`).
