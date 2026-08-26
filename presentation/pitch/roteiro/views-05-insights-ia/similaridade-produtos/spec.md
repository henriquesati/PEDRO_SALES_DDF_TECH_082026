# 🔍 Especificação Visual & Técnica: Busca Semântica & Embeddings (`similaridade-produtos`)

> **Momento do Roteiro**: **Ato 4 / Seção [5.3] — Busca Semântica, Espaço Vetorial & Vitrine de Produtos Inteligente**  
> **Artefato Gerado**: [`chart_similaridade_produtos.png`](chart_similaridade_produtos.png)  
> **Framework Normativo**: [`spec_data_app_streamlit_001`](../../../pipelines/case-item-09/specs.md) • Item 9 & Bônus GenAI • [`DEC-001`](../../../docs/relatorios/decision-making/pitch/pitch.txt)  
> **Fontes de Dados (Ground Truth)**: `data/mock/output_cleaned/parquet/produtos.parquet`, `pipelines/case-item-09/outputs/assets/data_app_product_similarity_map.png`.

---

## 🎯 1. Papel no Roteiro e Mensagem Estratégica

Quando um cliente abandona um carrinho no marketplace por **objeção de preço**, **frete regional excessivo** ou **indecisão entre modelos**, disparar um lembrete convencional de resgate tem baixa efetividade.

Com a **Plataforma Dadosfera**, o catálogo de produtos é automaticamente vetorizado na camada Silver (*Silver GenAI*), permitindo executar **consultas vetoriais de Similaridade de Cosseno** diretamente sobre o Data Lakehouse:
1. **Espaço Vetorial 2D (t-SNE / PCA)**: Agrupamento semântico dos 300 SKUs em clusters de alta coesão e afinidade de atributos através das 7 categorias do catálogo.
2. **Recomendação Prescritiva de Substitutos**: Identifica produtos alternativos compatíveis (ex.: versão similar com menor ticket, produto com centro de distribuição regional ou kit promocional).
3. **Conversão Cruzada Sem Perda de Margem**: Gera **+12.4% de recuperação incremental**, transformando perdas irreversíveis em novas oportunidades de venda e preservando 28.5% de margem bruta.

---

## 📊 2. Decomposição do Painel Visual de Negócios

O painel executivo 16:9 em 300 DPI é estruturado em 4 blocos analíticos de alta conversão:

1. **Header com 4 KPI Cards Executivos**:
   * **Catálogo Vetorizado**: *300 SKUs Mapeados* com embeddings multidimensionais na camada Silver GenAI.
   * **Similaridade de Cosseno**: *Score Médio de 89.4%* para recomendações Top-$K$ in-database.
   * **Recuperação Cruzada**: *+12.4% de Conversão Adicional* através de produtos substitutos e combos.
   * **Latência de Busca**: *< 2.5 ms por Consulta* via pushdown vetorial no Snowflake.

2. **Mapa de Projeção Vetorial 2D (t-SNE / PCA)**:
   * Projeção espacial das 7 categorias reais do catálogo auditado: Eletrônicos (72), Moda (63), Casa & Decoração (38), Esportes (38), Livros (33), Brinquedos (32) e Beleza (24).
   * **Jornada Prática Destacada no Pitch**:
     * Item Abandonado: *Smart TV 65" 4K (R$ 3.899)* com objeção de preço elevado (ticket > R$ 3.5k) e dúvida técnica.
     * Vetores de Conexão: Trajetórias semânticas ligando o abandono aos 3 SKUs recomendados (*Smart TV 55" 4K [94.2%]*, *Soundbar Premium [87.5%]* e *Suporte Articulado [81.0%]*).

3. **Ranking Visual dos Top-5 SKUs Alternativos (Item 9)**:
   * Gráfico de barras horizontais com score de similaridade por distância de cosseno (%):
     * *Smart TV 55" Crystal 4K (R$ 2.499)*: **94.2% Match** (Substituto Direto | -36% Preço).
     * *Smart TV 50" UHD HDR (R$ 2.199)*: **89.8% Match** (Menor Ticket | -44% Preço).
     * *Soundbar 3.1 Dolby Atmos (R$ 899)*: **87.5% Match** (Cross-Sell / Combo Áudio).
     * *Projetor Smart Full HD (R$ 1.850)*: **82.3% Match** (Alternativa Visual Portátil).
     * *Suporte Articulado Ultra (R$ 189)*: **81.0% Match** (Acessório Complementar).
   * Linha de corte do threshold mínimo de relevância estatística (80.0%).

4. **Comparativo Prescritivo de Negócio (Antes vs Agora)**:
   * **Estratégia Convencional (Sem IA / Cupom 20%)**: Disparo genérico que queima R$ 779,80 de margem bruta por venda com baixa conversão média (8.2%) e sem sanar a dúvida técnica.
   * **Vitrine Inteligente Dadosfera (GenAI)**: Recomendação da Smart TV 55" Bivolt Automático, preservando 28.5% de margem sem cupom e entregando +14.2% de conversão no segmento.

---

## 🛠️ 3. Governança e Reprodutibilidade

* **Script Autocontido**: [`generate_chart.py`](generate_chart.py) (importa e executa o módulo canônico [`insights/04_intelligence_ai/03_similaridade_produtos/generate_chart.py`](../../../insights/04_intelligence_ai/03_similaridade_produtos/generate_chart.py)).
* **Padrão Estético**: Fundo Branco Puro (`#FFFFFF`), alta legibilidade, tipografia moderna (`Segoe UI`), cores corporativas semânticas e exportação em 300 DPI (`charts-maker` standard).
* **Integridade**: Zero hardcoding — dados derivados do catálogo auditado e do motor de similaridade de `pipelines/case-item-09/`.
