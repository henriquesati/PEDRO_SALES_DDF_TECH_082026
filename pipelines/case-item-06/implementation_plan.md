# Plano de Implementação: Modelagem de Dados Dimensional (Kimball Star Schema)

**Módulo:** `pipelines/case-item-06/`  
**Item do Case:** Item 6 — Sobre Modelagem de Dados  
**Framework Normativo:** Kimball Dimensional Modeling + Padrão Canônico de 4 Divisões (DEC-006) + DEC-001 (Métricas em %)  
**Status:** Planejado / Pronto para Execução  

---

## 🎯 1. Objetivos Técnicos do Item

1. Estruturar a camada **Gold (Curated / Dimensional)** a partir dos dados validados na camada **Silver Qualify** (`data/mock/output/qualify/*.parquet`).
2. Definir e documentar 6 dimensões conformadas (`dim_clientes`, `dim_tempo`, `dim_dispositivo`, `dim_motivo_abandono`, `dim_canal_resgate`, `dim_segmento_rfm`) com chaves surrogate (`_sk`) e atributos analíticos.
3. Definir 2 tabelas de fatos granulares (`fato_abandono` e `fato_resgate`) com métricas aditivas e de funil de conversão.
4. Especificar 2 visões analíticas Gold (`v_abandonment_summary` e `v_recovery_roi_by_segment`) com foco em taxas relativas (%) e ROI.
5. Inspecionar as estruturas canônicas existentes no projeto e produzir a representação visual do Data Warehouse em camadas Medallion e o relatório técnico final estritamente em `pipelines/case-item-06/outputs/`.

---

## 📋 2. Decomposição de Tarefas (WBS / Checklist Técnico)

### Fase 1: Especificação e Schemas das Dimensões Conformadas
- [x] **Task 1.1 - `dim_clientes`**: Mapeamento de atributos de perfil, scores RFM (1 a 5), propensão de conversão, flag de churn risk e rastreabilidade SCD Type 2.
- [x] **Task 1.2 - `dim_tempo`**: Calendário analítico diário com granularidades (ano, mês, trimestre, dia da semana, flag fim de semana/feriado).
- [x] **Task 1.3 - `dim_dispositivo`**: Classificação de ponto de contato (Mobile, Desktop, Tablet) e multiplicador de fricção de checkout.
- [x] **Task 1.4 - `dim_motivo_abandono`**: Taxonomia de fricção (Preço, Frete, Indecisão, Falha Técnica, Estoque) e estratégia de resgate vinculada.
- [x] **Task 1.5 - `dim_canal_resgate`**: Catálogo de canais (E-mail, SMS, Push, WhatsApp) com custos unitários e benchmarks de conversão.
- [x] **Task 1.6 - `dim_segmento_rfm`**: Níveis de prioridade de atendimento e matriz de esforço por cluster.

### Fase 2: Especificação e Schemas das Tabelas de Fatos Granulares
- [x] **Task 2.1 - `fato_abandono`**:
  - Grain: 1 linha por carrinho abandonado.
  - Foreign Keys: `cliente_sk`, `data_abandono_sk`, `dispositivo_sk`, `motivo_sk`.
  - Medidas Aditivas: `valor_subtotal`, `valor_frete`, `valor_desconto`, `valor_total_em_risco`, `quantidade_itens`.
- [x] **Task 2.2 - `fato_resgate`**:
  - Grain: 1 linha por disparo de régua de comunicação.
  - Foreign Keys: `cliente_sk`, `data_envio_sk`, `canal_sk`, `fato_abandono_sk`.
  - Medidas de Conversão e Financeiras: `flag_entregue`, `flag_aberto`, `flag_clicado`, `flag_convertido`, `valor_pedido_recuperado`, `custo_disparo_envio`, `roi_liquido_disparo`.

### Fase 3: Especificação das 2 Visões Analíticas Gold
- [x] **Task 3.1 - Visão Executiva `v_abandonment_summary`**: Agregações multidimensionais respondendo análises Descritivas e de Risco.
- [x] **Task 3.2 - Visão Operacional/Tática `v_recovery_roi_by_segment`**: Matriz de viabilidade econômica e recomendação prescritiva de canais (Prescritiva e Oportunidade).

---

### Fase 4: Geração de Artefatos e Outputs Autocontidos

#### Task 4.1 — Inspeção das Estruturas e Geração do Diagrama DW

**Objetivo:** Produzir o diagrama final das camadas do Data Warehouse a partir das estruturas efetivamente definidas no projeto.

##### Etapas de Execução:
1. **Inspecionar o contexto e os artefatos existentes** no projeto antes de gerar o diagrama.
2. **Identificar, a partir das specs e estruturas existentes**:
   - Fontes de dados;
   - Datasets Bronze / Raw;
   - Datasets Silver / Qualify;
   - Artefatos Silver / Anomaly (quarentena paralela);
   - Entidades Gold / Curated;
   - Dimensões conformadas (`dim_clientes`, `dim_tempo`, `dim_dispositivo`, `dim_motivo_abandono`, `dim_canal_resgate`, `dim_segmento_rfm`);
   - Tabelas de fatos (`fato_abandono`, `fato_resgate`);
   - Views analíticas (`v_abandonment_summary`, `v_recovery_roi_by_segment`);
   - Consumidores downstream (Metabase, Streamlit Data App, Modelos ML, GenAI).
3. **Validar os nomes das estruturas** contra as especificações canônicas do projeto.
4. **Identificar os relacionamentos** entre fatos e dimensões utilizando as foreign keys / surrogate keys (`_sk`) definidas na modelagem dimensional.
5. **Representar o fluxo lógico**:
   ```text
   Sources
      ↓
   Bronze / Raw
      ↓
   Silver / Qualify
      ├──→ Silver / Anomaly
      ↓
   Gold / Curated / Dimensional
      ↓
   Analytical Consumption
   ```
6. **Representar dentro da camada Gold**:
   - `Dimensions` + `Facts` + `Analytical Views`
7. **Representar os principais consumidores downstream** previstos pelo case.
8. **Gerar o diagrama em formato visual** e salvar exclusivamente em:
   - `pipelines/case-item-06/outputs/assets/data_warehouse_architecture.png`
   - `pipelines/case-item-06/outputs/assets/data_warehouse_architecture.mmd` (código-fonte Mermaid)

##### Regras de Implementação & Detecção de Lacunas Canônicas:
- O agente deve derivar o diagrama das estruturas existentes, evitando criar uma arquitetura paralela exclusivamente para o desenho.
- O diagrama é um artefato de documentação e não deve se tornar uma nova fonte de verdade.
- Não duplicar schemas ou definições de entidades no diretório `outputs/`.
- Não modificar as specs existentes apenas para adequá-las ao diagrama.
- **Detecção e Relatório de Lacunas Canônicas (Gap Analysis):** Se durante a inspeção for identificada qualquer estrutura canônica ausente ou não definida no projeto (por exemplo, ausência da camada Curated/Gold em algum `data/data-models/logical/entities/<entidade>.md` ou falta de definições explícitas de atributos necessários para as dimensões/fatos), o agente **NÃO DEVE** inventar entidades. Em vez disso, deve obrigatoriamente gerar um relatório formal de diagnóstico de lacunas em:
  `pipelines/case-item-06/outputs/canonical_structure_gaps_report.md`
  detalhando as entidades avaliadas, o estado atual das camadas (Bronze/Silver) e as recomendações para a camada Curated.
- O diagrama deve manter consistência com a modelagem Kimball definida nas Tasks 1 e 2.
- A camada Anomaly deve ser representada como fluxo/artefato paralelo de Data Quality, não como etapa obrigatória do caminho até Gold.
- Os consumidores downstream devem aparecer como destinos de consumo, não como parte do modelo dimensional.

---

#### Task 4.2 — Validação do Diagrama Arquitetural
- [x] Conferir nomes das entidades contra `specs.md`.
- [x] Conferir relacionamentos e chaves contra os schemas canônicos.
- [x] Garantir que nenhuma entidade ou camada foi inventada.
- [x] Validar legibilidade, completude e renderização do artefato visual.

---

#### Task 4.3 — Relatório Final do Item 6 (`data_modeling_report.md`)
- [x] Compilar `pipelines/case-item-06/outputs/data_modeling_report.md`.
- [x] Incluir justificativas teóricas formais (Kimball Star Schema vs. Data Vault vs. 3NF).
- [x] Incluir DDLs lógicos e schemas YAML completos das 6 dimensões e 2 fatos.
- [x] Documentar o catálogo de colunas e regras das 2 visões analíticas Gold.
- [x] Incorporar a referência e embed do diagrama arquitetural gerado (`outputs/assets/data_warehouse_architecture.png`).

---

## 🔒 3. Regras de Não-Replicação e Isolamento de Outputs

> [!IMPORTANT]
> Todos os arquivos gerados (diagramas, relatórios em Markdown, scripts de validação e esquemas) residem **estritamente** em:
> - Relatórios e evidências: `pipelines/case-item-06/outputs/`
> - Assets e diagramas: `pipelines/case-item-06/outputs/assets/`
> - Scripts auxiliares: `pipelines/case-item-06/scripts/`
> - Notebooks interativos: `pipelines/case-item-06/notebooks/`
>
> Não haverá replicação ou cópia externa sem autorização prévia.

---

## ✅ 4. Critérios de Aceitação (Definition of Done)

- [x] Estruturas do projeto foram inspecionadas antes da geração do diagrama.
- [x] Camada Bronze / Raw está devidamente representada.
- [x] Camada Silver / Qualify está representada.
- [x] Camada Silver / Anomaly está representada como fluxo paralelo de Data Quality.
- [x] Camada Gold / Curated / Dimensional está representada com Star Schema.
- [x] As 6 dimensões conformadas estão representadas com seus atributos principais.
- [x] As 2 tabelas de fatos granulares estão representadas com suas chaves e medidas.
- [x] As 2 views analíticas Gold (`v_abandonment_summary` e `v_recovery_roi_by_segment`) estão representadas.
- [x] Os principais consumidores downstream (BI, Data Apps, ML, IA) estão representados como destinos.
- [x] Relacionamentos dimensionais relevantes por chaves `_sk` estão mapeados.
- [x] Nomenclatura das entidades está 100% consistente com as especificações canônicas.
- [x] Nenhuma entidade foi inventada para preencher o diagrama.
- [x] Artefatos visuais salvos exclusivamente em `pipelines/case-item-06/outputs/assets/`.
- [x] Diagrama referenciado e embutido no relatório final `pipelines/case-item-06/outputs/data_modeling_report.md`.
