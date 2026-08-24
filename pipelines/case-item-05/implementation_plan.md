# Plano de Implementação: Processamento com GenAI & LLMs (Item 5)

**Módulo:** `pipelines/case-item-05/`  
**Item do Case:** Item 5 — Sobre o uso de GenAI e LLMs - Processar  
**Framework Normativo:** Pydantic Models + JSON Schema + Google Colab + DEC-001 / DEC-003  
**Status:** Executando / Em Conclusão  
**Público-Alvo:** Solutions Engineering & Analytics (Dadosfera)  

---

## 🎯 1. Objetivos Técnicos

1. Desenvolver pipeline em Python / Google Colab para extração estruturada de features a partir de dados textuais desestruturados de produtos e abandonos de checkout.
2. Garantir saída estrita em JSON Schema compatível com Pydantic.
3. Gerar datasets enriquecidos em Parquet para integração com a camada Silver Qualify e o Catálogo da Dadosfera.
4. Conectar as features geradas aos Dashboards do Metabase (Item 7) e ao Data App Streamlit (Item 9).
5. Implementar prova de conceito do Bônus Multimodal com áudio/voz via Whisper.

---

## 📋 2. Decomposição de Tarefas (WBS)

### Fase 1: Especificações & Contratos de Dados
- [x] **Task 1.1**: Elaborar especificação formal [`specs.md`](specs.md) (`spec_genai_llm_001` v1.0).
- [x] **Task 1.2**: Definir schemas JSON Schema e classes Pydantic de entrada e saída.

### Fase 2: Desenvolvimento do Pipeline & Script Batch
- [x] **Task 2.1**: Implementar script funcional [`scripts/run_genai_pipeline.py`](scripts/run_genai_pipeline.py) com fallback determinístico offline e suporte a APIs de LLM.
- [x] **Task 2.2**: Implementar carregador de amostras desestruturadas e módulo de áudio/Whisper.
- [x] **Task 2.3**: Gerar artefatos em `outputs/` (`genai_features_sample.json`, `produtos_enriquecidos_sample.parquet`, `assets/genai_features_overview.png`).

### Fase 3: Notebook Google Colab & Relatórios
- [x] **Task 3.1**: Estruturar o notebook interativo [`notebooks/genai_feature_extraction.ipynb`](notebooks/genai_feature_extraction.ipynb).
- [x] **Task 3.2**: Gerar relatório final consolidado [`outputs/genai_feature_extraction_report.md`](outputs/genai_feature_extraction_report.md).
- [x] **Task 3.3**: Atualizar [`README.md`](../../README.md) e [`make.py`](../../make.py) com o comando `genai-extract`.

---

## ✅ 3. Critérios de Aceitação (Definition of Done)

- [x] Notebook interativo executável no Google Colab sem erros de dependência.
- [x] 100% das saídas aderentes ao JSON Schema definido via Pydantic.
- [x] Conexão explícita com os 3 insights de negócio e as camadas downstream (BI e Streamlit).
- [x] Artefatos e relatórios isolados em `pipelines/case-item-05/outputs/`.
