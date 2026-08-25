# ⏱️ View de Roteiro: Otimização de Timing & Curva de Decaimento (Janela +1h)

> **Caminho da View**: `presentation/pitch/roteiro/case-carrinho/views/insights/timingenvio/`  
> **Momento do Roteiro**: **Ato 3 / Blueprint Case Carrinho — Otimização de Timing & Cadência de Disparos**  
> **Referência Canônica Master**: [`presentation/pitch/pitch_spec.md`](../../../../pitch_spec.md#regra-6-otimização-de-timing--curva-de-decaimento-decay-curve)  
> **Base de Dados**: `data/mock/output_cleaned/parquet/eventos_resgate.parquet` (Ground Truth 100% Auditável)

---

## 🎯 Objetivo & Mensagem no Pitch

Demonstrar visualmente como a inteligência e os pipelines da **Dadosfera** identificam a **janela temporal ideal de disparo** para resgatar carrinhos abandonados, comprovando que a velocidade de resposta é o fator mais determinante para a conversão.

### 📌 Principais Descobertas:
1. **Curva de Decaimento Acentuada (Decay Curve)**: A probabilidade de conversão do comprador despenca drasticamente com o passar das horas.
2. **Concentração na Janela de +1h**: A primeira régua de contato disparada em até **1 hora pós-abandono concentra 86,4% de todas as conversões observadas**.
3. **Rigor Metodológico no Pitch**: A defesa analítica formal é:
   > *"Nos dados observados, a janela de +1h apresentou a maior taxa de conversão e concentrou 86,4% dos resgates, indicando +1h como a janela inicial prioritária para testes A/B contínuos dentro da plataforma."*

---

## 📊 Métricas & Fórmulas (Ground Truth)

| Régua de Comunicação | Latência Pós-Abandono | Total de Envios | Total de Conversões | % do Total Convertido | Taxa de Abertura (%) | Taxa de Conversão (%) |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **Onda 1** | **+1 hora** | **3.671** | **38** | **86,4%** | **44,3%** | **1,04%** |
| **Onda 2** | +24 horas | 1.631 | 5 | 11,4% | 39,2% | 0,31% |
| **Onda 3** | +48 horas | 793 | 1 | 2,3% | 45,8% | 0,13% |
| **Onda 4** | +72 horas | 332 | 0 | 0,0% | 57,2% | 0,00% |

---

## 🎨 Especificações do Painel Visual

* **Painel Esquerdo**: Curva suave (Spline Cúbica) de Decaimento Temporal com duplo eixo Y (Abertura em azul `#2563EB` vs Conversão em verde `#059669`), com anotação executiva destacando a Janela Candidata Inicial (+1h).
* **Painel Direito**: Barras horizontais comparando o Volume Total de Mensagens Enviadas com as Conversões Efetivas (em escala x60 ampliada), sem sobreposição de textos e legenda em posição limpa (`upper right`).
* **Resolução**: 300 DPI, fundo branco puro (`#FFFFFF`), tipografia sem serifa moderna (`charts-maker` standard).

---

## 📂 Artefatos do Módulo

| Arquivo | Descrição |
| :--- | :--- |
| [`chart_05_otimizacao_timing_envio.png`](chart_05_otimizacao_timing_envio.png) | Painel visual executivo renderizado em alta resolução (300 DPI). |
| [`generate_chart.py`](generate_chart.py) | Script declarativo e funcional em Python para reprodução imediata. |
| [`spec.md`](spec.md) | Especificação técnica e guia de narrativa para o apresentador. |
