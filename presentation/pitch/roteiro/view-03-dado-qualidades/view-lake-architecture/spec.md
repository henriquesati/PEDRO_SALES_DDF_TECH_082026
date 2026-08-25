# Especificação Visual & Técnica: Módulo Arquitetura Lakehouse & Data Quality (`view-lake-architecture`)

> **Momento do Roteiro**: **Ato 2 / Seção [3] — Etapas de Qualidade e Geração de Artefatos**  
> **Caminho da View**: `presentation/pitch/roteiro/view-lake-architecture/`  
> **Artefato Principal Previsto**: [`chart_lake_architecture.png`](chart_lake_architecture.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../roteiro.txt), [`pipelines/datalakes/README.md`](../../../pipelines/datalakes/README.md) e [`pipelines/case-item-08/specs.md`](../../../pipelines/case-item-08/specs.md).

---

## 🎯 1. Objetivo & Mensagem no Pitch

Demonstrar a superioridade da **Arquitetura Lakehouse Medallion integrada da Dadosfera** contra a complexidade fragmentada da AWS DIY, evidenciando como os pipelines declarativos e a suíte automatizada de Data Quality garantem **94.2% de conformidade de dados** e isolam anomalias em tempo real antes de qualquer impacto nas operações de negócio.

### 📌 Principais Mensagens de Fala:
1. **Fim do Cold Start e dos Custos Ocultos de Spark**:
   - *No AWS Glue*: Cada job leva de 1 a 4 minutos apenas para provisionar DPUs Spark, cobrando tempo mínimo por micro-execução e encarecendo o processamento contínuo de eventos.
   - *Na Dadosfera*: Execuções declarativas com baixo acoplamento entre ingestão, tratamento e persistência no Snowflake Lakehouse, refletindo dados limpos quase instantaneamente no catálogo.
2. **Arquitetura Dual-Artifact Silver (DEC-006)**:
   - **`_qualify` (94.2%)**: Registros validados e enriquecidos que avançam para a camada Gold/Curated.
   - **`_anomalies` (5.8%)**: Quarentena ativa que intercepta fretes negativos, e-mails malformados e divergências contábeis, armazenando o payload bruto para auditoria.
3. **Data Quality como Habilitador de Confiabilidade**:
   - A governança e a qualidade não são burocracias pós-processamento, mas barreiras ativas automatizadas que blindam réguas de marketing e decisões de diretoria.

---

## 🏛️ 2. Arquitetura Medallion dos Pipelines (Ponta a Ponta)

```text
┌─────────────────┐       ┌───────────────────────────────┐       ┌───────────────────────────────┐
│   BRONZE / RAW  │  ───► │        SILVER / QUALIFY       │  ───► │         GOLD / CURATED        │
│                 │       │                               │       │                               │
│  Ingestão Bruta │       │  • 94.2% Conformidade Rigorosa│       │  • Star Schema Kimball        │
│  Imutável       │       │  • Validação Great Expectation│       │  • 6 Dimensões / 2 Fatos      │
│  Sem Schema Lock│       │  • Higienização de PII / Email│       │  • Visões Analíticas Gold     │
└─────────────────┘       └───────────────┬───────────────┘       └───────────────────────────────┘
                                          │
                                          ▼
                          ┌───────────────────────────────┐
                          │       SILVER / ANOMALIES      │
                          │                               │
                          │  • 5.8% Quarentena Ativa      │
                          │  • Captura de Payload Bruto   │
                          │  • Motivo & Severidade ANOM   │
                          └───────────────────────────────┘
```

---

## 📐 3. Esboço e Composição Visual Prevista

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO POWERPOINT]                                      |
+---------------------------------------------------------------------------------------------------+
|  [CARD 1]                             [CARD 2]                             [CARD 3]               |
|  Taxa de Conformidade Silver          Isolamento em Quarentena             Regras Great Expectations|
|  94.2%                                5.8%                                 18 Regras Automatizadas |
|  Registros Prontos para Gold          Interceptados Pré-Envio              Validação Sintática & Neg|
+---------------------------------------------------------------------------------------------------+
|  [DIAGRAMA / PAINEL COMPARATIVO DE PIPELINES]                                                     |
|  Fluxo Medallion: Bronze (Raw) -> Silver (Qualify + Anomaly) -> Gold (Curated DW)                 |
|  - Desacoplamento operacional e eliminação de 1-4 min de cold start do AWS Glue                   |
|  - Rastreabilidade ponta a ponta e geração de artefatos confiáveis para consumo imediato          |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: Pipelines Datalakes Dadosfera | Framework Normativo DEC-006 & DEC-008           |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 4. Estrutura Padrão de Arquivos do Módulo

| Arquivo | Função / Conteúdo | Status |
| :--- | :--- | :---: |
| [`spec.md`](spec.md) | Especificação técnica em texto corrido com diretrizes e narrativa. | ✅ Criado |
| [`generate_chart.py`](generate_chart.py) | Boilerplate declarativo estruturado pronto para implementação visual. | ⏳ Estruturado (Aguardando Implementação) |
| `chart_lake_architecture.png` | Artefato gráfico 16:9 em alta resolução (300 DPI). | ⏳ A ser gerado na etapa de implementação |
