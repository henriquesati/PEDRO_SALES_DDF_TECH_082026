# Especificação Visual: Produtos e Categorias Mais Abandonados

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE BASELINE E VALORES DE NEGÓCIO**:  
> Esta especificação vincula-se diretamente ao insight canônico em [`insights/03_prescriptive/produtos_mais_abandonados.md`](../../../insights/03_prescriptive/produtos_mais_abandonados.md) e às premissas monetárias de [`presentation/pitch/pitch_spec.md`](../../pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎯 1. Objetivo da Visualização

Demonstrar a decomposição multidimensional de abandono e receita represada por **Categoria de Produto e Top SKUs**, identificando a barreira psicológica/operacional específica de cada categoria (risco financeiro em Eletrônicos, dúvida de caimento em Moda, frete volumoso em Decoração) e conectando a intervenções prescritivas customizadas no motor de resgate da Dadosfera.

---

## 📐 2. Estrutura do Painel Executivo (Widescreen 16:9)

- **Resolução & Exportação**: `16.0 x 9.0 polegadas`, 300 DPI, fundo `#FFFFFF`, bordas em Slate (`#CBD5E1`).
- **Seção Superior (Top 4 KPI Cards)**:
  1. `1. Concentração no Top 2`: R$ 7,34M (78,8%) represados em Eletrônicos & Casa & Decoração.
  2. `2. Disparidade de Ticket`: R$ 2.109 vs R$ 74 (Hesitação financeira em Tech vs Frete relativo em Livros).
  3. `3. Top 5 SKUs Críticos`: R$ 872,8k represados nos 5 principais produtos de tecnologia.
  4. `4. Lift Prescritivo`: +18% a +35% de conversão com campanhas contextualizadas.
- **Painel 1A (Matriz de Posicionamento de Catálogo - Scatter / Bubble)**:
  - **Eixo Y (Escala Logarítmica)**: Ticket Médio do Item (`R$ 50` a `R$ 2.500`).
  - **Eixo X**: Volume de Itens Abandonados (demanda represada).
  - **Tamanho da Bolha**: Proporcional à Receita Represada em Risco (`R$`).
  - **4 Quadrantes Estratégicos**: Alto Impacto (Q1), Frete Volumoso (Q2), Caimento/Tamanho (Q3), Frete Desproporcional (Q4).
- **Painel 1B (Ranking Top 5 SKUs Críticos - Eletrônicos)**:
  - Barras horizontais ordenadas dos 5 produtos que mais concentram valor represado (`Sony Headset Neo`, `Samsung Tab SPrime`, `LG IdeaPad Sport`, `Apple MacBook Max`, `Samsung iPhone Classic`).
- **Painel 2 (Matriz Prescritiva de Intervenções por Categoria)**:
  - 5 Cards Visuais Executivos estruturados com identificação da categoria, ticket médio, canal de acionamento Dadosfera, barreira crítica, ação prescritiva recomendada e impacto estimado (+XX% lift).

---

## 🎨 3. Paleta Semântica & Tipografia

- **Fontes**: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
- **Cores por Categoria**:
  - `Eletrônicos`: `#2563EB` (Azul Royal / Alto Ticket)
  - `Casa & Decoração`: `#059669` (Verde Esmeralda / Frete Volumoso)
  - `Moda`: `#7C3AED` (Violeta / Caimento & Troca)
  - `Esportes`: `#D97706` (Âmbar / Performance)
  - `Brinquedos`: `#475569` (Slate Neutro)
  - `Beleza`: `#DB2777` (Rosa)
  - `Livros`: `#0284C7` (Azul Claro)

---

## 📂 4. Fontes de Dados (Ground Truth)

- `data/mock/output_cleaned/parquet/itens_carrinho.parquet`
- `data/mock/output_cleaned/parquet/produtos.parquet`
- `data/mock/output_cleaned/parquet/carrinhos.parquet`
