# Especificação Visual: ROI e Eficiência de Campanhas de Resgate por Canal

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE BASELINE E VALORES DE NEGÓCIO**:  
> Esta especificação vincula-se diretamente ao insight canônico em [`insights/03_prescriptive/roi_campanhas_resgate.md`](../../../insights/03_prescriptive/roi_campanhas_resgate.md) e às premissas monetárias de [`presentation/pitch/pitch_spec.md`](../../pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎯 Objetivo da Visualização

Evidenciar a eficiência de conversão e rentabilidade financeira de cada canal de resgate (**E-mail**, **WhatsApp**, **SMS**, **Push Notification**), demonstrando o funil de engajamento (*Disparo $\rightarrow$ Abertura $\rightarrow$ Clique $\rightarrow$ Conversão*) e orientando a **readequação prescritiva da matriz de investimento** da Dadosfera (concentração de 85% do volume em Email e WhatsApp VIP de alta conversão, eliminando disparos frios deficitários de SMS/Push).

---

## 📐 Estrutura do Painel (Painel Duplo Integrado)

- **Resolução & Exportação**: `16.0 x 7.2 polegadas`, 300 DPI, fundo `#FFFFFF`, bordas em Slate (`#CBD5E1`).
- **Painel 1 (Funil de Eficiência & Engajamento por Canal)**:
  - **Eixo Y**: Canais de Comunicação (`E-mail Transacional`, `WhatsApp API`, `SMS Marketing`, `Push Notification`).
  - **Barras Agrupadas**:
    - 🔵 Taxa de Abertura (`%`).
    - 🟣 Taxa de Clique (`%`).
    - 🟢 Taxa de Conversão Final em Pedido (`%`).
  - **Rótulos**: Percentuais exatos e multiplicador de ROI por canal.
- **Painel 2 (Matriz Prescritiva de Rebalanceamento Orçamentário)**:
  - Tabela operacional detalhando o Canal, Custo Unitário, Alocação Atual vs Recomendada, Papel Estratégico e Ação Prescritiva da Dadosfera.

---

## 🎨 Paleta Semântica & Tipografia

- **Fontes**: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
- **Cores por Métrica**:
  - `Abertura`: `#2563EB` (Azul Royal)
  - `Clique`: `#8B5CF6` (Roxo)
  - `Conversão`: `#059669` (Verde Esmeralda)
  - `Alerta / Corte`: `#E11D48` (Rose)

---

## 📂 Fontes de Dados (Ground Truth)

- `data/mock/output_cleaned/parquet/eventos_resgate.parquet`
- `data/mock/output_cleaned/parquet/pedidos.parquet`
- `data/mock/output_cleaned/parquet/carrinhos.parquet`
