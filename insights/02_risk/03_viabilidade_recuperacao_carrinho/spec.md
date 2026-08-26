# Especificação Visual: Score de Viabilidade de Recuperação (Recovery Viability)

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE BASELINE E VALORES DE NEGÓCIO**:  
> Esta especificação vincula-se diretamente ao insight canônico em [`insights/02_risk/viabilidade_recuperacao_carrinho.md`](../../../insights/02_risk/viabilidade_recuperacao_carrinho.md) e às premissas monetárias de [`presentation/pitch/pitch_spec.md`](../../pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎯 Objetivo da Visualização

Apresentar o modelo de **Score de Viabilidade de Recuperação de Carrinhos**, que combina a **Probabilidade Empírica de Recuperação** (baseada em RFM do cliente, motivo de abandono, valor da cesta e latência temporal) com o **Custo Unitário de Intervenção**, calculando o **Expected ROI** de cada sessão de compra abandonada.

Essa priorização permite à Dadosfera **alocar 80% do orçamento nos carrinhos de maior retorno**, eliminando até 35% de disparos deficitários em carrinhos não recuperáveis.

---

## 📐 Estrutura do Painel (Painel Duplo Integrado)

- **Resolução & Exportação**: `15.5 x 7.2 polegadas`, 300 DPI, fundo `#FFFFFF`, bordas em Slate (`#CBD5E1`).
- **Painel 1 (Scatter Plot de Dispersão de Viabilidade)**:
  - **Eixo X**: Probabilidade Estimada de Recuperação (`%`).
  - **Eixo Y**: Valor do Carrinho Abandonado (`R$`).
  - **Classificação & Cores**:
    - 🟢 **Alta Viabilidade** (`#059669`): ROI $\ge 50\text{x}$ e Retorno $\ge \text{R\$ } 10$.
    - 🟡 **Média Viabilidade** (`#F59E0B`): ROI $\ge 10\text{x}$ e Retorno $\ge \text{R\$ } 2$.
    - 🔴 **Baixa Viabilidade** (`#E11D48`): ROI $< 10\text{x}$ ou Retorno $< \text{R\$ } 2$.
  - **Tamanho dos Pontos**: Proporcional ao Expected ROI da intervenção.
- **Painel 2 (Decomposição Operacional & Retorno Financeiro)**:
  - Barras horizontais agrupadas com Volume (`un`), Retorno Esperado Total (`R$ k`), Custo Total de Disparo (`R$`) e Matriz de Ação Prescrita por Faixa.

---

## 🎨 Paleta Semântica & Tipografia

- **Fontes**: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
- **Cores Semânticas**:
  - `Alta Viabilidade`: `#059669` (Verde Esmeralda)
  - `Média Viabilidade`: `#F59E0B` (Âmbar)
  - `Baixa Viabilidade`: `#E11D48` (Rose/Alerta)
  - `Fundo e Bordas`: `#FFFFFF` e `#CBD5E1`

---

## 📂 Fontes de Dados (Ground Truth)

- `data/mock/output_cleaned/parquet/carrinhos.parquet`
- `data/mock/output_cleaned/parquet/clientes.parquet`
- `data/mock/output_cleaned/parquet/eventos_resgate.parquet`
