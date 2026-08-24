# Dashboard: Painel Executivo & Operacional de Recuperação de Carrinho

## 🎯 Objetivo
Centralizar a visão executiva e operacional de abandono e resgate de carrinhos no marketplace, permitindo aos gestores de e-commerce e growth:
1. Acompanhar a evolução temporal do abandono vs recuperação de receita.
2. Analisar o desempenho por categoria de produtos e identificar gargalos no catálogo.
3. Avaliar a rentabilidade (ROI) de cada canal de comunicação (WhatsApp, Email, SMS, Push).
4. Operar a fila de carrinhos prioritários via Score de Viabilidade de Recuperação.

---

## 👥 Público-Alvo
- **Head de E-commerce / C-Level**: Acompanhamento de ROI global, faturamento recuperado e taxa de conversão incremental.
- **Gerente de CRM / Growth Marketing**: Otimização de canais, réguas de timing e calibragem de descontos.
- **Equipe de Atendimento / Vendas**: Fila de resgate prioritário de clientes Premium (WhatsApp).

---

## 📊 KPIs Principais (Cards / Big Numbers)
1. **Taxa Global de Abandono**: ~70.9% (com indicador de tendência semanal)
2. **Taxa de Recuperação de Carrinhos**: ~10.1% dos abandonados
3. **Receita Bruta Recuperada**: Total em R$ gerado por campanhas de resgate com sucesso
4. **ROI Consolidado de Campanhas**: Múltiplo de retorno líquido sobre custo de envio (~45x)
5. **Volume de Carrinhos em Alta Viabilidade**: Total de carrinhos ativos com ROI esperado > 50x

---

## 🔍 Filtros Globais
- **Período Temporal**: Filtro de data (`data_criacao` / `data_abandono`) com presets: Últimos 7 dias, 30 dias, 6 meses (Jan–Jun 2026).
- **Segmento RFM**: `premium`, `regular`, `dormant`, `novo`, `Todos`.
- **Canal de Resgate**: `email`, `sms`, `push_app`, `whatsapp`, `Todos`.
- **Categoria de Produto**: `Eletrônicos`, `Moda`, `Casa & Decoração`, `Esportes`, `Beleza`, `Livros`, `Brinquedos`, `Todas`.
- **Dispositivo**: `mobile`, `desktop`, `tablet`, `Todos`.

---

## 📈 Visualizações (Mínimo de 5 Tipos Distintos)

### Visualização 1: Série Temporal — Evolução Diária de Abandono vs Recuperação
- **Tipo**: **Gráfico de Linha (Time Series com 2 Eixos Y / Múltiplas Linhas)**
- **Artefato Gerado**: [`chart_01_serie_temporal_abandono_resgate.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_01_serie_temporal_abandono_resgate.png)
- **Fonte**: `vw_metricas_resgate_diarias`
- **Eixo X**: `data` (diário/semanal)
- **Eixo Y (Esquerda)**: Taxa de Abandono (%) e Taxa de Recuperação (%)
- **Eixo Y (Direita)**: Valor Total Abandonado (R$) vs Valor Total Recuperado (R$)
- **Objetivo**: Atender ao requisito explícito de análise de série temporal do case, monitorando picos e sazonalidade.

![Série Temporal](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_01_serie_temporal_abandono_resgate.png)

---

### Visualização 2: Performance de Catálogo — Abandono e Conversão por Categoria
- **Tipo**: **Gráfico de Barras Horizontais Empilhadas / Agrupadas**
- **Artefato Gerado**: [`chart_02_performance_categorias.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_02_performance_categorias.png)
- **Fonte**: `vw_produtos_abandonados`
- **Eixo Y**: `categoria` (Eletrônicos, Moda, Casa & Decoração, etc.)
- **Eixo X**: Volume de Carrinhos Abandonados vs Volume de Carrinhos Convertidos
- **Tooltip / Métrica Secundária**: Taxa de Abandono (%) e Ticket Médio da Categoria
- **Objetivo**: Atender ao requisito explícito de análise de categorias do case.

![Performance Categorias](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_02_performance_categorias.png)

---

### Visualização 3: Eficiência Financeira — Receita Recuperada vs Custo por Canal (ROI)
- **Tipo**: **Gráfico de Barras Duplas com Linha de Tendência (Combo Chart)**
- **Artefato Gerado**: [`chart_03_roi_eficiencia_canais.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_03_roi_eficiencia_canais.png)
- **Fonte**: `vw_performance_canais`
- **Eixo X**: `canal` (`email`, `whatsapp`, `sms`, `push_app`)
- **Eixo Y1 (Barras)**: Receita Total Gerada (R$) e Custo Total de Disparos (R$)
- **Eixo Y2 (Linha / Pontos)**: Múltiplo de ROI Líquido por Canal
- **Objetivo**: Demonstrar visualmente por que o Email escala com baixo custo e o WhatsApp gera alto valor unitário.

![ROI Canais](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_03_roi_eficiencia_canais.png)

---

### Visualização 4: Matriz de Causas-Raiz — Distribuição de Motivos por Segmento RFM
- **Tipo**: **Mapa de Calor (Heatmap) / Gráfico de Rosca (Donut)**
- **Artefato Gerado**: [`chart_04_matriz_motivos_rfm_heatmap.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_04_matriz_motivos_rfm_heatmap.png)
- **Fonte**: `vw_abandono_analise`
- **Dimensões**: `motivo_abandono` (Preço, Frete, Indecisão, Pagamento, Estoque) × `segmento_rfm`
- **Valor**: Volume de Carrinhos e Valor Represado em R$
- **Objetivo**: Identificar rapidamente que Premium abandona por Indecisão e Novos por Frete/Preço.

![Heatmap RFM](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_04_matriz_motivos_rfm_heatmap.png)

---

### Visualização 5: Matriz de Decisão — Dispersão de Viabilidade de Recuperação
- **Tipo**: **Gráfico de Dispersão (Scatter Plot / Bubble Chart)**
- **Artefato Gerado**: [`chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_05_dispersao_viabilidade_recuperacao.png)
- **Fonte**: `vw_viabilidade_recuperacao`
- **Eixo X**: Probabilidade de Recuperação (`prob_recuperacao_pct`)
- **Eixo Y**: Valor do Carrinho (`valor_total`)
- **Cor da Bolha**: Nível de Viabilidade (`ALTA` em Verde, `MEDIA` em Amarelo, `BAIXA` em Vermelho)
- **Tamanho da Bolha**: Retorno Esperado em R$
- **Objetivo**: Fornecer a visão prescritiva dos carrinhos que geram o maior retorno com o menor risco.

![Scatter Viabilidade](file:///c:/Users/pedro/OneDrive/Desktop/wheels/dashboards/assets/chart_05_dispersao_viabilidade_recuperacao.png)

---

### Visualização 6 (Operacional): Fila de Priorização de Resgate em Tempo Real
- **Tipo**: **Tabela Interativa (Data Grid com Formatação Condicional)**
- **Fonte**: `vw_viabilidade_recuperacao`
- **Colunas**: `carrinho_id`, `segmento_rfm`, `valor_total`, `motivo_abandono`, `prob_recuperacao_pct`, `roi_esperado`, `viabilidade_recuperacao`, `acao_prescrita`
- **Ordenação Default**: `retorno_esperado DESC`
- **Objetivo**: Servir de interface direta de acionamento para o motor de envio ou equipe de atendimento.

---

## 🔗 Insights Relacionados
- [Taxa e Volume de Abandono](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/01_descriptive/taxa_volume_abandono.md)
- [Motivos de Abandono](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/01_descriptive/motivos_abandono.md)
- [LTV vs Abandono](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/02_risk/ltv_vs_abandono.md)
- [Viabilidade de Recuperação por Carrinho](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/02_risk/viabilidade_recuperacao_carrinho.md)
- [ROI de Campanhas](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/03_prescriptive/roi_campanhas_resgate.md)
- [Produtos Mais Abandonados](file:///c:/Users/pedro/OneDrive/Desktop/wheels/insights/03_prescriptive/produtos_mais_abandonados.md)

---

## 🔄 Regras de Atualização
- **Frequência de Carga/Refresh**:
  - Camada de Monitoramento Geral: Atualização a cada 1 hora.
  - Fila de Viabilidade de Recuperação (Operacional): Atualização em tempo real (micro-batch de 5 minutos).
- **Janela Histórica**: 6 meses contínuos com retenção de dados agregados para comparação ano contra ano.

---

## 🚨 Alertas & Monitoramento Inteligente (Metabase Alerts)
1. **Alerta de Anomalia de Abandono**: Notificar via Slack/Email se a taxa diária de abandono ultrapassar **78%** (+2 desvios padrão).
2. **Alerta de Fricção de Pagamento**: Disparar alerta imediato se o motivo `'pagamento'` no dispositivo `mobile` representar > 20% dos abandonos da última hora.
3. **Alerta de ROI Negativo**: Alerta crítico se o ROI de qualquer canal cair abaixo de **5x** no acumulado semanal.
4. **Alerta de Carrinho Baleia (Whale Cart)**: Notificar equipe de vendas se um cliente `premium` abandonar carrinho com valor > R$ 1.500.

---

## 🏆 Critérios de Sucesso
- Aderência aos requisitos do Item 7: análise de categorias + série temporal + 5 visualizações de 5 tipos distintos.
- Facilidade de navegação: tempo de resposta das consultas nas views inferior a 1.5 segundos.
- Capacidade de acionamento direto: a tabela operacional permite selecionar e disparar campanhas diretamente na Dadosfera.
