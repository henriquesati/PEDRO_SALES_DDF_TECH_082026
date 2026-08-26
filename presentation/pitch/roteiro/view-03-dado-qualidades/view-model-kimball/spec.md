# Especificação Visual & Técnica: Módulo Modelagem Dimensional Kimball (`view-model-kimball`)

> **Momento do Roteiro**: **Ato 2 / Seção {3.2} — Modelagem Kimball: Transformação dos Dados & Geração de Insights**  
> **Caminho da View**: `presentation/pitch/roteiro/view-03-dado-qualidades/view-model-kimball/`  
> **Arquitetura Master**: [`presentation/pitch/roteiro/README.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/README.md)  
> **Artefato Principal Previsto**: [`chart_modelagem_kimball.png`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-model-kimball/chart_modelagem_kimball.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro/view-03-dado-qualidades/view-model-kimball/generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/roteiro.txt), [`pipelines/case-item-06/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-06/specs.md) e [`pipelines/case-item-08/specs.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/case-item-08/specs.md).

---

## 🎯 1. Objetivo & Mensagem no Pitch

Apresentar a modelagem dimensional **Kimball Star Schema (1-Hop)** implementada na camada Gold do Snowflake Data Lakehouse, comprovando que esta arquitetura é a mais simples de compreender pelos times de negócio e a mais rápida de responder a consultas analíticas em ferramentas de visualização (Metabase / PowerBI) e Data Apps.

### 📌 Principais Mensagens de Fala:
1. **Transformação Funcional & Confiável (Silver -> Gold)**:
   - Os dados purificados da Silver Qualify são transformados por pipelines funcionais modulares (Step 4 da Stepsfera), gerando chaves surrogate (`_sk`), integridade dimensional e métricas pré-calculadas.
2. **Star Schema Centralizado (6 Dimensões Conformadas & 2 Fatos)**:
   - **Dimensões Conformadas**: `dim_cliente`, `dim_produto`, `dim_tempo`, `dim_canal`, `dim_dispositivo` e `dim_motivo_abandono`.
   - **Tabelas Fato Granulares**: `fato_abandono` (eventos no checkout) e `fato_resgate` (disparos e conversões de réguas).
   - **Eficiência 1-Hop**: Consultas analíticas exigem apenas 1 salto de junção (JOIN direto entre Fato e Dimensão), eliminando a latência e a complexidade de cascata de tabelas normalizadas (3NF) ou pontes de Data Vault.
3. **Derivação Imediata de Visões Analíticas Gold & Insights de Negócio**:
   - **`v_abandonment_summary`**: Visão executiva consolidando abandono por motivo, categoria e dispositivo.
   - **`v_recovery_roi_by_segment`**: Visão tática de performance cruzando segmentação RFM com eficiência de canais (WhatsApp vs Email), comprovando o ROI de 45x e a taxa de recuperação de 10.1%.

---

## 🏛️ 2. Arquitetura do Star Schema Kimball (Camada Gold DW)

```text
       ┌────────────────────────┐         ┌────────────────────────┐
       │      dim_cliente       │         │      dim_produto       │
       │  --------------------  │         │  --------------------  │
       │  • cliente_sk (PK)     │         │  • produto_sk (PK)     │
       │  • segmento_rfm        │         │  • categoria / preco   │
       └───────────┬────────────┘         └───────────┬────────────┘
                   │                                  │
                   ▼                                  ▼
       ┌───────────────────────────────────────────────────────────┐
       │                 FATO PRINCIPAL: fato_abandono             │
       │  -------------------------------------------------------  │
       │  • abandono_id (PK)      • cliente_sk (FK)                │
       │  • produto_sk (FK)       • tempo_sk (FK)                  │
       │  • canal_sk (FK)         • dispositivo_sk (FK)            │
       │  • motivo_sk (FK)        • valor_carrinho (Métrica)       │
       │  • tempo_sessao_seg      • recuperado_flag (0/1)          │
       └───────────────────────────┬───────────────────────────────┘
                                   │
                                   ▼
       ┌───────────────────────────────────────────────────────────┐
       │                  FATO DERIVADO: fato_resgate              │
       │  -------------------------------------------------------  │
       │  • resgate_id (PK)       • abandono_id (FK)               │
       │  • canal_disparo         • custo_envio_brl                │
       │  • convertido_flag (0/1) • valor_recuperado_brl           │
       │  • roi_multiplicador     • latencia_disparo_horas         │
       └───────────────────────────────────────────────────────────┘
```

---

## 📐 3. Esboço e Composição Visual Prevista

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO POWERPOINT]                                      |
+---------------------------------------------------------------------------------------------------+
|  [CARD 1]                             [CARD 2]                             [CARD 3]               |
|  Dimensões Conformadas                Tabelas Fato Granulares              Visões Analíticas Gold |
|  6 Dimensões (Chaves _sk)             2 Fatos (Abandono & Resgate)         v_abandonment_summary  |
|  1-Hop JOINs Otimizados               Granularidade Transacional           v_recovery_roi_segment |
+---------------------------------------------------------------------------------------------------+
|  [DIAGRAMA STAR SCHEMA EXPANDIDO / MODELO VISUAL KIMBALL]                                         |
|  Visualização das 6 Dimensões conectadas radialmente às Tabelas Fato                              |
|  - Relações 1-Hop sem nós intermediários para máxima performance no Snowflake                     |
|  - Habilitação direta de relatórios no Metabase e simuladores no Streamlit Data App               |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: Snowflake Lakehouse Dadosfera | Modelagem Dimensional Ralph Kimball (Gold DW)    |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 4. Estrutura Padrão de Arquivos do Módulo

| Arquivo | Função / Conteúdo | Status |
| :--- | :--- | :---: |
| [`spec.md`](spec.md) | Especificação técnica em texto corrido com narrativa e modelo de dados. | ✅ Criado |
| [`generate_chart.py`](generate_chart.py) | Boilerplate declarativo estruturado pronto para implementação visual. | ⏳ Estruturado (Aguardando Implementação) |
| `chart_modelagem_kimball.png` | Artefato gráfico 16:9 em alta resolução (300 DPI). | ⏳ A ser gerado na etapa de implementação |
