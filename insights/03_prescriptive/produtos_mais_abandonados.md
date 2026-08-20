# Análise de Produtos e Categorias Mais Abandonados

## ❓ Pergunta de Negócio
Quais categorias e produtos concentram as maiores taxas e volumes de abandono na plataforma, quais barreiras específicas de conversão afetam cada tipo de produto (confiança, incerteza de tamanho, peso de frete) e quais intervenções prescritivas por categoria desbloqueiam o checkout?

---

## 📊 Métrica

- **KPI Primário**: Taxa de Abandono por Categoria / Produto (`%`)
- **KPIs Secundários**:
  - Volume de Carrinhos Abandonados por Categoria (`unidades`)
  - Receita Represada por Categoria de Produto (`R$`)
  - Taxa de Resgate Convertido por Categoria (`%`)
  - Média de Avaliações (`avaliacao_media`) dos Itens Mais Abandonados
- **Fórmula**:
  - `Taxa de Abandono do Produto (%)` = (Total de carrinhos abandonados contendo o produto / Total de carrinhos criados com o produto) * 100
  - `Receita Represada da Categoria (R$)` = Soma de `itens_carrinho.preco_total` em carrinhos com status 'abandonado'
- **Granularidade**: Semanal, Mensal, por Categoria de Produto, Subcategoria e Produto Individual.
- **Dimensões**:
  - `Categoria`: `produtos.categoria` (`Eletrônicos`, `Moda`, `Casa & Decoração`, `Esportes`, `Beleza`, `Livros`, `Brinquedos`).
  - `Faixa de Preço`: Ticket Alto (> R$ 1.000), Médio (R$ 100–1.000), Baixo (< R$ 100).
  - `Disponibilidade`: `produtos.em_estoque`.
  - `Reputação`: `produtos.avaliacao_media` e `total_avaliacoes`.
- **Alvo (Benchmark)**:
  - Reduzir o abandono em Eletrônicos para < 68% e Moda para < 60%.
  - Recuperar $\ge 12\%$ dos carrinhos contendo itens de alto valor.

---

## 💡 Insight Esperado

### 1. Eletrônicos de Alto Valor (> R$ 1.000) — Taxa de Abandono: ~75%
- **Barreira de Conversão**: Risco percebido elevado, comparação de preços entre grandes marketplaces e medo de garantia/entrega.
- **Impacto**: Maior perda financeira unitária. Representa a maior oportunidade em R$ recuperados.

### 2. Moda & Vestuário (R$ 100 a R$ 500) — Taxa de Abandono: ~70%
- **Barreira de Conversão**: Incerteza sobre caimento, modelagem, cor real e receio de burocracia na devolução.

### 3. Casa & Decoração (R$ 50 a R$ 200) — Taxa de Abandono: ~65%
- **Barreira de Conversão**: Dúvida sobre dimensões no ambiente e custo de frete desproporcional para produtos volumosos.

### 4. Esportes & Fitness (R$ 30 a R$ 100) — Taxa de Abandono: ~60%
- **Barreira de Conversão**: Comparação de especificações técnicas e busca por cupons de desconto.

### 5. Beleza & Cuidados Pessoais (< R$ 50) — Taxa de Abandono: ~50%
- **Barreira de Conversão**: Frete que supera o valor do produto individual em compras isoladas (baixa densidade de valor).

---

## 📍 Dadosfera Config

- **Tipo**: Exploração, View Analítica (`vw_produtos_abandonados`) e Dashboard de Catálogo
- **Camada**: Analytics
- **Dados necessários**:
  - `produtos`
  - `itens_carrinho`
  - `carrinhos`
- **Campos necessários**:
  - `produtos.produto_id`, `produtos.nome`, `produtos.categoria`, `produtos.subcategoria`, `produtos.preco_atual`, `produtos.avaliacao_media`, `produtos.total_avaliacoes`
  - `itens_carrinho.carrinho_id`, `itens_carrinho.quantidade`, `itens_carrinho.preco_total`, `itens_carrinho.data_remocao`
  - `carrinhos.status`, `carrinhos.valor_frete`, `carrinhos.valor_total`
- **Relacionamentos**:
  - `itens_carrinho.produto_id` $\rightarrow$ `produtos.produto_id` (N:1)
  - `itens_carrinho.carrinho_id` $\rightarrow$ `carrinhos.carrinho_id` (N:1)

### Passos de Transformação
1. **Filtro de Itens Ativos no Abandono**: Selecionar itens onde `itens_carrinho.data_remocao IS NULL` em carrinhos com `status = 'abandonado'`.
2. **Agrupamento por Categoria e Produto**: Contar ocorrências em carrinhos abandonados vs carrinhos convertidos.
3. **Cálculo da Taxa e Perda Financeira**: Determinar a taxa percentual de abandono e o montante em R$ represado por categoria.
4. **Visualização**:
   - Ranking (Top 10 Produtos Mais Abandonados por Volume e por R$).
   - Gráfico de Dispersão: Preço do Produto vs Taxa de Abandono com tamanho indicando Volume Financeiro.

---

## ✅ Como Validar

- **Consistência de Itens**: A soma de `itens_carrinho.preco_total` dos itens mantidos deve reconciliar com o `valor_subtotal` do carrinho.
- **Validação de Estoque**: Verificar se o abandono não foi causado por indisponibilidade posterior (`produtos.em_estoque = FALSE`).
- **Não-Duplicação**: Produtos adicionados e removidos da mesma sessão (`data_remocao IS NOT NULL`) não devem distorcer a contagem de itens presentes no momento do abandono.

---

## 🎯 Recomendação Acionável (Matriz de Ação por Categoria)

| Categoria | Dor Principal do Cliente | Gatilho Prescritivo na Régua de Resgate | Ação Corretiva na Página do Produto (UX) |
| :--- | :--- | :--- | :--- |
| **Eletrônicos (> R$ 1k)** | Medo / Risco financeiro | Oferta de **Frete Grátis com Seguro** + Garantia Estendida | Destacar selos de segurança, garantia oficial e avaliações com fotos |
| **Moda / Vestuário** | Dúvida de caimento / tamanho | Garantia de **"1ª Troca Grátis e Sem Custos"** no email de resgate | Provador virtual, tabela de medidas interativa e fotos de clientes |
| **Casa & Decoração** | Frete volumoso / medidas | **Cupom de subsídio de frete** em compras acima de R$ 150 | Calculadora de medidas e simulador de ambiente em 3D |
| **Beleza / Acessórios** | Frete caro vs item pequeno | Sugestão de **Cross-sell / Compre Junto** ("Adicione R$ 20 para frete grátis") | Kits promocionais e barra de progresso de frete no carrinho |

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - A categoria **Eletrônicos** representa ~45% de todo o valor financeiro represado. Reduzir sua taxa de abandono em apenas **5 pontos percentuais** destrava um volume expressivo de faturamento com custo de frete subsidiado totalmente coberto pela margem da venda.
  - Oferecer **"1ª Troca Grátis"** em Moda tem custo de sinistralidade baixo (< 3% dos pedidos de fato trocam), mas remove a fricção psicológica no momento da compra, elevando a conversão de resgate em até **+35%**.

---
---------sugestoes agent------

### 💡 Sugestões de Aprimoramento para o Pitch e Modelo:
1. **Gatilho de Escassez de Estoque**: Para produtos com menos de 5 unidades em estoque, disparar comunicação dinâmica com copy de urgência: *"Restam apenas X unidades de [Nome do Produto] no seu tamanho/cor"*.
2. **Recomendação de Produtos Substitutos**: Se o produto do carrinho abandonado ficar sem estoque (`em_estoque = FALSE`), o motor de resgate deve recomendar automaticamente itens similares da mesma subcategoria em vez de enviar um link quebrado.
3. **Injeção de Reviews Dinâmicos no Resgate**: Para itens com `avaliacao_media >= 4.5`, injetar no template de comunicação as 2 melhores avaliações de clientes reais para acelerar o fechamento de compras de alto valor.
