# Plano de Implementação: Pipeline de Data Quality & Quarentena de Anomalias

**Módulo:** `pipelines/case-item-04/`  
**Item do Case:** Item 4 — Sobre Data Quality  
**Framework Normativo:** Great Expectations + Medallion Architecture (Dual-Artifact Silver)  
**Status:** Concluído / Operacional  

---

## 🎯 1. Objetivos Técnicos do Item

1. Executar auditoria de Data Quality sobre as 7 entidades da camada Bronze (RAW Parquet).
2. Aplicar 18 regras formais de integridade técnica, conformidade de negócio e consistência temporal.
3. Isolar desvios em quarentena dead-letter (`output/anomalies/`) preservando o payload bruto para auditoria.
4. Promover registros íntegros para a camada Silver (`output/qualify/`).
5. Gerar automaticamente todos os outputs (relatório markdown, gráficos 300DPI e evidências JSON) em `pipelines/case-item-04/outputs/`.

---

## 📋 2. Decomposição de Tarefas (WBS / Checklist Técnico)

### Fase 1: Parametrização e Regras de Validação
- [x] **Task 1.1**: Configurar suíte de regras de nulabilidade e formato para `clientes` e `produtos`.
- [x] **Task 1.2**: Implementar validação de máquina de estados e anomalias financeiras/contábeis para `carrinhos` (`ANOM-01` a `ANOM-05`).
- [x] **Task 1.3**: Configurar integridade referencial e validação temporal para `itens_carrinho`, `eventos_carrinho`, `eventos_resgate` e `pedidos`.

### Fase 2: Construção do Motor de Qualificação Dual-Artifact
- [x] **Task 2.1**: Implementar `qualify_entity()` com captura de stack trace e enriquecimento de anomalias com `payload_raw`, `codigo_anomalia` e `severidade`.
- [x] **Task 2.2**: Exportar dados qualificados e segregados para Parquet.

### Fase 3: Geração de Relatórios e Evidências Visuais
- [x] **Task 3.1**: Gerar visualizações em alta resolução (Conformidade Global, Taxa de Rejeição por Entidade, Comparativo RAW vs Qualify) em `outputs/assets/`.
- [x] **Task 3.2**: Compilar relatório executivo `outputs/data_quality_report.md` com métricas consolidadas e embeds de gráficos.
- [x] **Task 3.3**: Salvar manifesto estruturado `outputs/validation_results.json`.

### Fase 4: Integração com Task Runner CLI
- [x] **Task 4.1**: Conectar script `pipelines/case-item-04/scripts/run_quality_pipeline.py` ao comando `python make.py quality-eval`.

---

## 🔒 3. Regras de Não-Replicação e Isolamento de Outputs

> [!IMPORTANT]
> Todos os arquivos gerados residem **estritamente** em:
> - Relatórios e gráficos: `pipelines/case-item-04/outputs/`
> - Scripts executáveis: `pipelines/case-item-04/scripts/`
> - Notebooks Google Colab: `pipelines/case-item-04/notebooks/`

---

## ✅ 4. Critérios de Aceitação (Definition of Done)

1. Execução do pipeline sem erros para todas as 7 entidades.
2. Mais de 115.000 registros avaliados com taxa de conformidade global > 90%.
3. Quarentena de anomalias devidamente populada e auditável.
4. Relatório executivo e gráficos 300 DPI gerados em `outputs/`.
