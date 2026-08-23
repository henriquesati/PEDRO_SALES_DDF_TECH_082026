# Especificação Visual & Regra de Negócio: Matriz de Viabilidade de Recuperação

## 📌 Contexto & Regra de Negócio
- **Matriz de Decisão de 3 Dimensões**:
  1. *Perfil do Cliente*: Segmento RFM (`premium`, `regular`, `dormant`, `novo`).
  2. *Valor do Carrinho*: Ticket em R$ (indica retorno financeiro potencial).
  3. *Motivo do Abandono*: Atrito diagnosticado (Frete, Pagamento, Preço, Indecisão).
- **Classificação de Viabilidade Prescritiva**:
  - `ALTA`: Alta probabilidade de conversão (> 40%) ou alto valor de carrinho (> R$ 500) com cliente engajado.
  - `MEDIA`: Probabilidade intermediária (15% a 40%) com ticket padrão.
  - `BAIXA`: Carrinhos de baixo valor com histórico frio (< 15%).

## 📊 Métricas & Fórmulas (Ancoradas em %)
- **Probabilidade de Recuperação Estimada (%)**: Score ponderado de conversão baseado no perfil do cliente e canal.
- **Concentração de Receita Viável**: Mais de **65% do valor recuperável** está concentrado nos quadrantes de ALTA e MÉDIA viabilidade.
- **Retorno Esperado Ponderado**: $\text{Retorno Esperado} = \text{Valor do Carrinho} \times \text{Probabilidade de Conversão}$.

## 🎯 Objetivo no Pitch
Apresentar a capacidade prescritiva da plataforma Dadosfera, provando que a ferramenta não apenas relata o passado, mas prioriza a fila de disparos em tempo real para maximizar o retorno da equipe de CRM e vendas.

## 📍 Mapeamento Plataforma Dadosfera
- **Módulo**: Visualizar / Metabase & Consumir / Data Apps.
- **Camada**: Gold (Kimball DW - `v_recovery_roi_by_segment` e `fato_abandono`).
- **Visão Analítica**: `vw_viabilidade_recuperacao`.

## 🖼️ Artefato Visual Gerado
- **Arquivo**: [`chart_05_dispersao_viabilidade_recuperacao.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/05_matriz_viabilidade_recuperacao/chart_05_dispersao_viabilidade_recuperacao.png)
- **Tipo de Gráfico**: Gráfico de Dispersão (Scatter Plot) com Quadrantes de Decisão e Classificação por Cores.
