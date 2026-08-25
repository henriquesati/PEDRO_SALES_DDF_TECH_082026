# Especificação Visual & Técnica: Módulo de Governança & LGPD (`view-governança`)

> **Momento do Roteiro**: **Ato 2 / Seção {3.1} — Governança e Dados: Dicionário de Dados, RBAC & Blindagem LGPD**  
> **Caminho da View**: `presentation/pitch/roteiro/view-governança/`  
> **Artefato Principal Previsto**: [`chart_governanca_lgpd.png`](chart_governanca_lgpd.png) (300 DPI, 16:9 Widescreen)  
> **Script Gerador**: [`generate_chart.py`](generate_chart.py)  
> **Padrão Visual**: Fundo Branco Puro (`#FFFFFF`), Tipografia Sem Serifa Moderna, Paleta Semântica Executiva (`charts-maker` standard).  
> **Fontes Estratégicas**: [`presentation/pitch/roteiro.txt`](../roteiro.txt), [`data/catalogo/blueprint/blueprint_dicionario.md`](../../../data/catalogo/blueprint/blueprint_dicionario.md) e [`data/data-models/logical/entities/clientes.md`](../../../data/data-models/logical/entities/clientes.md).

---

## 🎯 1. Objetivo & Mensagem no Pitch

Apresentar como a **Plataforma Dadosfera transforma segurança, compliance e governança de um gargalo de TI em um habilitador de negócios**, garantindo conformidade total com a LGPD através de opt-in mandatório, proteção de PII e documentação de catálogo estruturada sem burocracia de código de infraestrutura.

### 📌 Principais Mensagens de Fala:
1. **Dicionário de Dados Estruturado (Padrão de Classe "A é um B que C")**:
   - Cada tabela e atributo possui definição formal de negócio, tipos primitivos estritos, regras de validação e mapeamento de dependências upstream/downstream.
   - Vinculação direta aos Data Asset IDs oficiais da plataforma para descoberta autônoma por usuários de negócio.
2. **Blindagem LGPD "By Design" e Governança de Opt-in**:
   - **Tagging Semântico Automático**: Colunas sensíveis (`nome`, `email`, `telefone`) recebem classificação `Confidencial (PII / LGPD)` com políticas automáticas de anonimização/mascaramento.
   - **Opt-in Mandatório por Canal**: Disparos de recuperação exigem consentimento ativo (`permite_email = TRUE` e `permite_whatsapp = TRUE`).
   - **Interceptação Ativa (`ANOM-03`)**: Qualquer tentativa de envio sem consentimento formal é imediatamente segregada em quarentena antes de sair da plataforma, eliminando o risco de penalidades regulatórias.
3. **Fim do Gargalo de SecOps & Eliminação do "Shadow IT"**:
   - *Na AWS DIY*: Criar ou alterar acessos exige configurar políticas IAM em JSON, Lake Formation e chamados técnicos que levam de 3 a 6 semanas (induzindo equipes a exportar CSVs sem controle).
   - *Na Dadosfera*: RBAC intuitivo por perfis (Marketing, CRM, Analytics, Diretoria) em poucos cliques, liberando Data Views curadas com segurança total.

---

## 🏛️ 2. Matriz de Governança & Conformidade de Dados

| Pilar de Governança | Mecanismo na Dadosfera | Dor Eliminada da AWS DIY | Impacto no Negócio |
| :--- | :--- | :--- | :--- |
| **Dicionário de Dados** | Catálogo com definições de negócio e linhagem automática | Documentação inexistente ou dispersa em wikis desatualizadas | Descoberta autônoma e redução do tempo de onboarding |
| **Proteção de PII** | Tags semânticas e mascaramento dinâmico de atributos | Exposição acidental de dados pessoais em logs e bancos de staging | Conformidade rigorosa com a LGPD e auditoria transparente |
| **Consentimento / Opt-in** | Validação mandatória pré-disparo com bloqueio automático | Envios acidentais para usuários descadastrados gerando multas | Proteção da reputação de marca e respeito à privacidade |
| **Controle de Acesso (RBAC)** | Gestão centralizada por papéis e compartilhamento seguro de Views | Políticas IAM em JSON com lead time de 3 a 6 semanas | Time-to-data reduzido de semanas para minutos com zero risco |

---

## 📐 3. Esboço e Composição Visual Prevista

```
+---------------------------------------------------------------------------------------------------+
|  [ESPAÇO SUPERIOR LIVRE PARA TÍTULO / BULLETS NO POWERPOINT]                                      |
+---------------------------------------------------------------------------------------------------+
|  [CARD 1]                             [CARD 2]                             [CARD 3]               |
|  Ativos Catalogados com Dicionário    Conformidade LGPD / Opt-in           Lead Time de Liberação |
|  7 Entidades Canônicas                100% Blindagem PII                   Minutos (vs 3-6 semanas)|
|  Linhagem & Metadados Oficiais        Opt-in Mandatório por Canal          RBAC Centralizado      |
+---------------------------------------------------------------------------------------------------+
|  [DIAGRAMA / MATRIZ DE SEGURANÇA E GOVERNANÇA ATIVA]                                              |
|  Fluxo de Blindagem: Cadastro PII -> Tagging Semântico -> Validação Opt-in -> Data Views Seguras  |
|  - Camada de proteção ativa que impede vazamentos e bloqueia envios não autorizados               |
|  - Compartilhamento seguro com Marketing e CRM sem expor o banco de dados transacional            |
+---------------------------------------------------------------------------------------------------+
|  [RODAPÉ] Fonte: Catálogo & Governança Dadosfera | Blueprint Dicionário & Framework LGPD          |
+---------------------------------------------------------------------------------------------------+
```

---

## 📂 4. Estrutura Padrão de Arquivos do Módulo

| Arquivo | Função / Conteúdo | Status |
| :--- | :--- | :---: |
| [`spec.md`](spec.md) | Especificação técnica em texto corrido com narrativa e diretrizes. | ✅ Criado |
| [`generate_chart.py`](generate_chart.py) | Boilerplate declarativo estruturado pronto para implementação visual. | ⏳ Estruturado (Aguardando Implementação) |
| `chart_governanca_lgpd.png` | Artefato gráfico 16:9 em alta resolução (300 DPI). | ⏳ A ser gerado na etapa de implementação |
