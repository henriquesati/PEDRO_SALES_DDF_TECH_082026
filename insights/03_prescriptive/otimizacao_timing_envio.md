# Otimização de Timing de Envio (Cadência por Segmento)

## ❓ Pergunta de Negócio
Qual é a janela temporal ótima (delay pós-abandono) para o primeiro disparo de resgate e qual cadência de reengajamento maximiza as taxas de abertura e conversão para cada segmento sem gerar atrito ou parecer invasivo?

---

## 📊 Métrica

- **KPI Primário**: Taxa de Conversão por Janela de Timing pós-Abandono (`%`)
- **KPIs Secundários**:
  - Taxa de Abertura por Faixa de Delay (`%`)
  - Taxa de Cliques por Faixa de Delay (`%`)
  - Tempo Médio Abandono $\rightarrow$ Conversão Efetiva (`horas`)
  - Taxa de Opt-out / Descadastro por Frequência de Disparo (`%`)
- **Fórmula**:
  - `Delay de Disparo (horas)` = `(eventos_resgate.data_envio - carrinhos.data_abandono)` expresso em horas
  - `Taxa de Abertura no Timing T (%)` = (Total de Aberturas no Delay T / Total de Envios no Delay T) * 100
  - `Taxa de Conversão no Timing T (%)` = (Total de Pedidos Convertidos no Delay T / Total de Envios no Delay T) * 100
- **Granularidade**: Semanal, Mensal, por Janela de Delay (+1h, +6h, +24h, +48h, +72h) e por Segmento RFM.
- **Dimensões**:
  - `Janela de Delay`: `+1h` (Imediato), `+6h a +8h` (Mesmo dia), `+24h` (D+1), `+48h` (D+2), `+72h` (D+3).
  - `Segmento RFM`: `clientes.segmento_rfm` (`premium`, `regular`, `dormant`, `novo`).
  - `Canal de Disparo`: `email`, `push_app`, `sms`, `whatsapp`.
- **Alvo (Benchmark)**:
  - Concentrar **65% das conversões totais de resgate** nas primeiras 24 horas pós-abandono.
  - Manter taxa de opt-out por disparo < 0.2%.

---

## 💡 Insight Esperado

### 1. Segmento PREMIUM (Lead Quente / Alta Intenção)
- **Melhor Janela de Disparo**: **1 hora** após o abandono.
- **Performance Observada**: ~40% de taxa de abertura, ~10% a 15% de taxa de conversão.
- **Comportamento & Racional**: O cliente Premium já possui fidelidade e confiança. O abandono decorre de interrupções momentâneas ou dúvidas pontuais. O contato rápido resgata o impulso imediato de compra enquanto o produto ainda está no topo da memória.

### 2. Segmento REGULAR (Maturação de Decisão)
- **Melhor Janela de Disparo**: **6 a 8 horas** após o abandono (ou início do próximo turno/noite).
- **Performance Observada**: ~32% de taxa de abertura, ~6% a 7% de conversão.
- **Comportamento & Racional**: Contatos instantâneos (< 1h) podem soar desesperados ou intrusivos para quem está apenas pesquisando. O intervalo de 6h a 8h atinge o cliente em um momento de descanso ou término do expediente com a lembrança ainda vívida.

### 3. Segmento NOVO (Ciclo Comparativo / Baixa Fidelidade)
- **Melhor Janela de Disparo**: **24 horas** após o abandono (D+1).
- **Performance Observada**: ~22% de taxa de abertura, ~3% de conversão.
- **Comportamento & Racional**: Clientes novos costumam comparar preços e condições em múltiplos sites. Um disparo em 24h atua como reengajamento no mesmo horário em que o usuário costuma navegar online, reforçando credibilidade e garantias institucionais.

---

## 📍 Dadosfera Config

- **Tipo**: Pipeline de Automação Prescritiva / View / Painel de Cadência
- **Camada**: Analytics $\rightarrow$ Prescriptive Layer
- **Dados necessários**:
  - `carrinhos`
  - `clientes`
  - `eventos_resgate`
  - `pedidos`
- **Campos necessários**:
  - `carrinhos.carrinho_id`, `carrinhos.data_abandono`, `carrinhos.status`
  - `clientes.cliente_id`, `clientes.segmento_rfm`
  - `eventos_resgate.resgate_id`, `eventos_resgate.data_envio`, `eventos_resgate.data_abertura`, `eventos_resgate.sucesso`, `eventos_resgate.canal`
- **Relacionamentos**:
  - `eventos_resgate.carrinho_id` $\rightarrow$ `carrinhos.carrinho_id` (N:1)
  - `carrinhos.cliente_id` $\rightarrow$ `clientes.cliente_id` (N:1)

### Passos de Transformação
1. **Cálculo da Diferença Temporal**: Calcular a latência exata `TIMESTAMPDIFF(HOUR, data_abandono, data_envio)`.
2. **Clusterização em Faixas de Delay**: Agrupar em buckets padronizados (`1h`, `6-8h`, `24h`, `48h`, `72h`).
3. **Agregação por Segmento**: Cruzar volume de disparos, aberturas, cliques e conversões por bucket e segmento RFM.
4. **Visualização**:
   - Curva de Degradação de Conversão no Tempo (Decay Curve: Eixo X = Horas pós-abandono, Eixo Y = Taxa de Conversão).
   - Mapa de Calor: Horário do Dia vs Taxa de Abertura por Segmento.

---

## ✅ Como Validar

- **Consistência Temporal**: `eventos_resgate.data_envio` deve ser estritamente posterior a `carrinhos.data_abandono`.
- **Intervalo Mínimo entre Disparos**: Garantir que nenhum cliente receba mais de uma comunicação dentro de uma janela de 4 horas (anti-spam policy).
- **Consistência de Status**: Carrinhos já convertidos (`status = 'comprado'`) não podem receber novos disparos da régua temporal.
- **Conferência de Decay**: A taxa de conversão deve apresentar curva decrescente natural conforme o delay aumenta (ex: Conversão em 1h > Conversão em 72h).

---

## 🎯 Recomendação Acionável (Política de 3 Ondas)

Implementar o motor de automação da Dadosfera configurado na seguinte cadência escalonada:

1. **Onda 1 (Gatilho +1h — Clientes Premium)**:
   - Disparo via WhatsApp/Email.
   - Foco: Atendimento exclusivo e reserva de estoque.
2. **Onda 2 (Gatilho +6h a +8h — Clientes Regulares)**:
   - Disparo via Email/Push App.
   - Foco: Lembrete suave de itens salvos.
3. **Onda 3 (Gatilho +24h — Clientes Novos & Inativos)**:
   - Disparo via Email com cupom de primeira compra e depoimentos de clientes (Social Proof).
4. **Onda de Reforço (+48h a +72h — Repescagem Geral)**:
   - Apenas para carrinhos que abriram as mensagens anteriores mas não converteram, aplicando oferta final de urgência.

---

## 💰 ROI & Impacto Financeiro

- **Metodologia de Impacto**:
  - Disparar para clientes Premium em 1h (ao invés de 24h) **dobra a taxa de conversão de 5% para 10%**, recuperando receita antes do esfriamento do lead.
  - Espaçar o envio de clientes regulares para 6h-8h reduz a taxa de descadastro (opt-out) em **40%**, preservando a base contatável ativa.
  - A sincronização do timing por segmento gera um incremento estimado de **+25% no volume financeiro total recuperado** com exatamente o mesmo número de disparos.

---
---------sugestoes agent------

### 💡 Sugestões de Aprimoramento para o Pitch e Modelo:
1. **Ajuste por Janela de Sono (Quiet Hours)**: Implementar trava lógica para não disparar entre 22h e 08h. Se um carrinho Premium abandonar às 23h, o gatilho de "1h" deve ser postergado automaticamente para as 08h30 do dia seguinte.
2. **Gatilho de Reativação no Horário Original de Compra**: Para clientes Novos (24h), disparar exatamente no mesmo horário em que o carrinho foi criado no dia anterior, aproveitando a rotina de navegação do usuário.
3. **Detecção de Dispositivo no Timing**: Disparos em mobile (Push/SMS) funcionam melhor em intervalos curtos (+1h a +3h), enquanto Email performa melhor em blocos de checagem (+6h ou início da manhã).
