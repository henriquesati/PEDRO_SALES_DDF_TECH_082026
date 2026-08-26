# Especificação Técnica: Processamento de Dados Desestruturados com GenAI & LLMs

**Doc ID:** `spec_genai_llm_001`  
**Versão:** 1.1  
**Módulo:** `pipelines/case-item-05/`  
**Case Oficial Dadosfera:** Item 5 — Sobre o uso de GenAI e LLMs - Processar  
**Framework Normativo:** Pydantic Validation + JSON Schema + DEC-001 (% e Ratios) + DEC-003 (Insights em Markdown) + Governança Lakehouse  
**Status:** Aprovado & Implementado  
**Público-Alvo:** Solutions Engineering & Analytics (Dadosfera)  

---

## 📋 1. Executive Summary & Contexto de Negócio

### 1.1 Objetivo
Transformar dados textuais desestruturados em linguagem natural (títulos e descrições técnicas de catálogo de produtos, complementados por feedbacks e motivos de abandono de checkout) em **features analíticas estruturadas e acionáveis**, acelerando a inteligência de CRM e recuperação de receita do marketplace na plataforma **Dadosfera**.

### 1.2 Perguntas de Negócio Respondidas com IA:
1. **Catálogo & Atrito (Insight 1)**: *Quais especificações técnicas complexas ou dúvidas de compatibilidade nas descrições estão gerando atrito e abandono no checkout?*
2. **Resgate Prescritivo (Insight 2)**: *Qual o apelo persuasivo ideal e qual copy personalizada (Email / WhatsApp) foca no benefício-chave de cada produto?*
3. **Viabilidade & Decisão (Insight 3)**: *Como enriquecer a propensão de resgate com atributos semânticos de sensibilidade a preço e urgência para o BI (Metabase)?*

---

## 🏛️ 2. Arquitetura no Lakehouse & Governança de Catálogo

Para garantir conformidade com as diretrizes de governança da Dadosfera, o dataset enriquecido gerado pelo pipeline de GenAI é catalogado e integrado diretamente na arquitetura Lakehouse:

### 2.1 Destino no Data Lakehouse:
- **Camada do Lakehouse:** **Silver Qualify**
- **Diretório no Lakehouse:** [`pipelines/datalakes/qualify/produtos_enriquecidos_qualify/`](../datalakes/qualify/produtos_enriquecidos_qualify/)
- **Documento de Metadados:** [`pipelines/datalakes/qualify/produtos_enriquecidos_qualify/metadata.md`](../datalakes/qualify/produtos_enriquecidos_qualify/metadata.md)
- **Tabela Snowflake:** `CART_RECOVERY.PRODUTOS_ENRIQUECIDOS`
- **Data Asset ID:** `78aeef12-9c41-4da2-b118-8ee12cf4da99`

### 2.2 Dicionário de Dados & Governança:
- **Dicionário de Dados Oficial:** [`data/catalogo/qualify/produtos_enriquecidos.md`](../../data/catalogo/qualify/produtos_enriquecidos.md)
- **Especificações:** 18 atributos estritamente tipados com descrições baseadas em classe ("A é um B que C"), rastreabilidade de linhagem upstream/downstream e classificação de sensibilidade LGPD (Interno / Não PII).

---

## 🏗️ 3. Contratos de Entrada e Saída (I/O)

### 3.1 Dados de Entrada (Desestruturados)
- **Catálogo de Produtos (`produtos_raw_text`)**: Título comercial e descrição detalhada de especificações técnicas, materiais e funcionalidades.
- **Feedbacks de Checkout (`checkout_feedback_text`)**: Comentários e objeções em texto livre registrados em pesquisas de saída pós-abandono e tickets de suporte SAC.

### 3.2 Schema de Saída Estruturado (Pydantic / JSON Schema)

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "ProdutoFeaturesEnriquecidas",
  "type": "object",
  "required": [
    "produto_id",
    "features_produto",
    "diagnostico_abandono",
    "acao_prescritiva_crm"
  ],
  "properties": {
    "produto_id": { "type": "integer" },
    "features_produto": {
      "type": "object",
      "required": ["categoria_normalizada", "subcategoria", "marca", "diferencial_tecnico"],
      "properties": {
        "categoria_normalizada": { "type": "string" },
        "subcategoria": { "type": "string" },
        "marca": { "type": "string" },
        "material_construcao": { "type": "string" },
        "diferencial_tecnico": { "type": "string" },
        "faixa_posicionamento": { "type": "string", "enum": ["Entrada", "Intermediario", "Premium", "Luxo"] },
        "requer_compatibilidade": { "type": "boolean" }
      }
    },
    "diagnostico_abandono": {
      "type": "object",
      "required": ["motivo_raiz", "sentimento", "sensibilidade_preco"],
      "properties": {
        "motivo_raiz": { "type": "string" },
        "sentimento": { "type": "string", "enum": ["Positivo", "Neutro", "Hesitante", "Frustrado"] },
        "nivel_urgencia": { "type": "string", "enum": ["Baixo", "Medio", "Alto"] },
        "sensibilidade_preco": { "type": "string", "enum": ["Baixa", "Media", "Alta"] }
      }
    },
    "acao_prescritiva_crm": {
      "type": "object",
      "required": ["estrategia_recomendada", "gatilho_mental", "copy_resgate_email", "copy_resgate_whatsapp"],
      "properties": {
        "estrategia_recomendada": { "type": "string" },
        "gatilho_mental": { "type": "string", "enum": ["Escassez", "Urgencia", "Prova Social", "Desconto", "Suporte", "Frete Gratis"] },
        "copy_resgate_email": { "type": "string" },
        "copy_resgate_whatsapp": { "type": "string" }
      }
    }
  }
}
```

---

## 🤖 4. Engenharia de Prompts (Template Declarativo)

```text
Você é o Especialista em Inteligência de E-commerce e IA da plataforma Dadosfera.
Sua tarefa é analisar dados desestruturados de produtos e feedbacks de clientes que abandonaram o checkout, extraindo features analíticas padronizadas e redigindo copies personalizadas de resgate.

DADOS DE ENTRADA:
- ID do Produto: {produto_id}
- Título Comercial: {nome_bruto}
- Descrição Técnica: {descricao_bruta}
- Preço Atual: R$ {preco_atual}
- Feedback / Objeção de Abandono: {feedback_abandono_cliente}

DIRETRIZES DE PROCESSAMENTO:
1. Normalize a Categoria e Subcategoria conforme a taxonomia padrão de marketplace.
2. Identifique os diferenciais técnicos e materiais principais.
3. Se o feedback indicar dúvidas de medidas/voltagem/compatibilidade, marque 'requer_compatibilidade' como True.
4. Classifique o sentimento e a sensibilidade a preço do cliente.
5. Gere copies diretas e persuasivas para Email e WhatsApp focando no principal benefício do produto e na resolução da objeção.
6. Responda ESTRITAMENTE em formato JSON aderente ao Schema fornecido.
```

---

## 🔗 5. Integração com as Camadas do Projeto

1. **Camada Silver Qualify (`pipelines/datalakes/qualify/produtos_enriquecidos_qualify/`)**:
   - As features extraídas são persistidas em `produtos_enriquecidos.parquet` e catalogadas na Dadosfera.
2. **Camada Gold / BI Metabase (Item 7)**:
   - Permite cruzar a taxa de abandono por categorias normalizadas e identificar produtos que necessitam de guias de compatibilidade.
3. **Data App Streamlit (Item 9 & Bônus)**:
   - Alimenta o simulador com copies automáticas para disparo de CRM e gera prompts para vitrines personalizadas.
