# Especificação Visual: Produtos e Categorias Mais Abandonados

> [!IMPORTANT]
> **REFERÊNCIA CANÔNICA DE BASELINE E VALORES DE NEGÓCIO**:  
> Esta especificação vincula-se diretamente ao insight canônico em [`insights/03_prescriptive/produtos_mais_abandonados.md`](../../../insights/03_prescriptive/produtos_mais_abandonados.md) e às premissas monetárias de [`presentation/pitch/pitch_spec.md`](../../pitch/pitch_spec.md) (Seções 4 e 5).

---

## 🎯 Objetivo da Visualização

Demonstrar a decomposição de abandono e receita represada por **Categoria de Produto**, identificando a barreira psicológica/operacional específica de cada categoria (risco financeiro em Eletrônicos, dúvida de caimento em Moda, frete volumoso em Decoração) e conectando a intervenções prescritivas customizadas no motor de resgate da Dadosfera.

---

## 📐 Estrutura do Painel (Painel Duplo Integrado)

- **Resolução & Exportação**: `16.0 x 7.2 polegadas`, 300 DPI, fundo `#FFFFFF`, bordas em Slate (`#CBD5E1`).
- **Painel 1 (Ranking de Categorias por Receita Represada)**:
  - **Eixo Y**: Categorias de Produtos (`Eletrônicos`, `Casa & Decoração`, `Moda`, `Esportes`, `Brinquedos`, `Beleza`, `Livros`).
  - **Eixo X**: Receita Represada em Risco (`R$ Milhares`).
  - **Rótulos**: Volume de Itens Abandonados (`un`), Taxa de Abandono (`%`) e Avaliação Média do Catálogo (`★`).
- **Painel 2 (Matriz Prescritiva de Intervenções por Categoria)**:
  - Tabela operacional detalhando a Categoria, a Dor Principal do Cliente, o Gatilho Prescritivo na Régua de Resgate e a Ação Corretiva na UX da Página do Produto.

---

## 🎨 Paleta Semântica & Tipografia

- **Fontes**: `Segoe UI`, `DejaVu Sans`, `Helvetica`, `Arial`, `sans-serif`.
- **Cores por Categoria**:
  - `Eletrônicos`: `#2563EB` (Azul Royal / Alto Ticket)
  - `Casa & Decoração`: `#059669` (Verde Esmeralda / Frete Volumoso)
  - `Moda`: `#D97706` (Âmbar / Caimento & Troca)
  - `Esportes`: `#7C3AED` (Roxo / Performance)
  - `Demais Categorias`: `#64748B` (Slate Neutro)

---

## 📂 Fontes de Dados (Ground Truth)

- `data/mock/output_cleaned/parquet/itens_carrinho.parquet`
- `data/mock/output_cleaned/parquet/produtos.parquet`
- `data/mock/output_cleaned/parquet/carrinhos.parquet`
