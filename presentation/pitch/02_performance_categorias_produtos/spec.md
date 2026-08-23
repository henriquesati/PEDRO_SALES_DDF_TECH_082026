# Especificação Visual & Regra de Negócio: Performance de Categorias de Produtos

## 📌 Contexto & Regra de Negócio
- **Regra de Sensibilidade de Catálogo**: O abandono varia substancialmente de acordo com a categoria e o ticket médio dos itens. Categorias de alto valor e complexidade técnica (ex: Eletrônicos) sofrem maior atrito por preço e indecisão, enquanto categorias de giro rápido e vestuário (ex: Moda) sofrem atrito com custo de frete e dúvidas sobre especificações.
- **Categorias Mapeadas**: Eletrônicos, Moda, Casa & Decoração, Esportes, Beleza, Livros, Brinquedos.

## 📊 Métricas & Fórmulas (Ancoradas em %)
- **Taxa de Abandono por Categoria (%)**: $\frac{\text{Carrinhos Abandonados com Item da Categoria } C}{\text{Total de Carrinhos com Item da Categoria } C} \times 100$.
- **Participação de Volume (% do Total de Carrinhos)**: Distribuição percentual do volume de itens no funil.
- **Conversão Incremental por Categoria**: Taxa de sucesso de campanhas de resgate estratificada por tipo de produto.

## 🎯 Objetivo no Pitch
Cumprir o requisito explícito do Item 7 (Análise de Categorias) demonstrando que a inteligência da Dadosfera permite personalizar a régua de resgate não apenas pelo cliente, mas pela sensibilidade específica de cada categoria de produto no catálogo.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Visualizar / Metabase & Pipelines.
- **Camada**: Gold (Kimball DW - `dim_produtos`, `fato_abandono`, `fato_resgate`).
- **Visão Analítica**: `v_abandonment_summary`.

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/02_performance_categorias_produtos/chart_02_performance_categorias.png)
- **Tipo de Gráfico**: Gráfico de Barras Horizontais Agrupadas / Comparativas (Abandonados vs Convertidos com Badge de Taxa %).
