# Plano de Implementação: Exploração & Catalogação de Ativos na Dadosfera

**Módulo:** `pipelines/case-item-03/`  
**Item do Case:** Item 3 — Sobre a Dadosfera: Explorar e Catalogar  
**Framework Normativo:** Dicionário de Dados Baseado em Classe + API Maestro + DEC-005  
**Status:** Concluído / Operacional  

---

## 🎯 1. Objetivos Técnicos do Item

1. Catalogar as 7 entidades do case no módulo Explorar da Dadosfera com dicionários de dados enriquecidos.
2. Definir e documentar as 3 zonas do Data Lakehouse (Raw → Qualify → Curated).
3. Aplicar técnicas de governança e mascaramento para colunas PII/LGPD (`clientes.nome`, `clientes.email`, `clientes.telefone`).
4. Automatizar a sincronização de metadados, tags e dicionários via API Maestro da Dadosfera com deduplicação preventiva (DEC-005).
5. Centralizar especificações, scripts e outputs em `pipelines/case-item-03/`.

---

## 📋 2. Decomposição de Tarefas (WBS / Checklist Técnico)

### Fase 1: Padronização de Metadados & Dicionários
- [x] **Task 1.1**: Construção do Blueprint de Dicionário de Dados com estrutura formal baseada em classe (*"A é um B que C"*).
- [x] **Task 1.2**: Mapeamento de PII e classificação de sensibilidade (Confidencial vs. Interno).
- [x] **Task 1.3**: Documentação de granularidade, chaves primárias/estrangeiras e zonas de Data Lake para as 7 entidades.

### Fase 2: Integração e Automação via API Maestro
- [x] **Task 2.1**: Implementação de autenticação via header direto `Authorization: <token>` (DEC-005).
- [x] **Task 2.2**: Construção da lógica de sincronização idempotente (`PUT /catalog/data-asset/{id}` para existentes, `POST /catalog` para novos).
- [x] **Task 2.3**: Isolamento e quarentena de duplicatas órfãs (`[DUPLICATA - IGNORAR]` + tags de lixeira).

### Fase 3: Registro de Ativos & Documentação
- [x] **Task 3.1**: Mapeamento e consolidação de Data Asset IDs oficiais da Dadosfera.
- [x] **Task 3.2**: Compilação de relatório executivo e inventário de ativos em `pipelines/case-item-03/outputs/catalog_governance_report.md`.

---

## 🔒 3. Regras de Não-Replicação e Isolamento de Outputs

> [!IMPORTANT]
> Todos os arquivos gerados residem **estritamente** em:
> - Relatórios e registros de ativos: `pipelines/case-item-03/outputs/`
> - Scripts de automação: `pipelines/case-item-03/scripts/`
> - Notebooks de exploração: `pipelines/case-item-03/notebooks/`

---

## ✅ 4. Critérios de Aceitação (Definition of Done)

1. 7 entidades catalogadas com Data Asset IDs oficiais mapeados.
2. Dicionários de dados detalhados seguindo a regra de definição baseada em classe.
3. Classificação de dados sensíveis (LGPD) explícita e consistente.
4. Script/API de sincronização documentada e validada.
