# 🧹 Especificação Imutável: Camada Qualify (Silver / Validação & Data Quality)

> **Doc ID:** `spec_datalake_qualify_001`  
> **Camada:** `Qualify (Silver)`  
> **Natureza:** Objeto Imutável de Validação, Contratos de Dados & Governança  
> **Banco / Schema:** Snowflake `CART_RECOVERY.*`  
> **Catálogo Dadosfera:** 7 Ativos Catalogados e Sincronizados  
> **Padrão Arquitetural:** Dual-Artifact Pipeline (DEC-006 — Qualify vs Quarentena)  
> **Status:** ✅ Homologado & Ativo  

---

## 1. 📌 Objetivo e Princípios da Camada Qualify

A camada **Qualify (Silver)** é responsável por transformar os dados brutos da camada Raw em tabelas relacionais rigorosamente tipadas, limpas, auditadas e padronizadas. É a camada onde ocorrem as validações de schema, regras de integridade contábil e de negócio, e o isolamento de registros anômalos.

### Princípios Fundamentais:
1. **Contrato Rígido de Schema:** Nenhuma linha com chave primária nula, tipos incompatíveis ou campos obrigatórios corrompidos é promovida para consumo downstream.
2. **Dual-Artifact Routing (DEC-006):** Os registros processados são bifurcados:
   - **Silver Qualify (`CART_RECOVERY.*`):** Registros 100% íntegros (taxa média de aprovação ~94.2%).
   - **Silver Anomalies (Quarentena Dead-Letter):** Registros com violação de regras de negócio ou integridade contábil (taxa ~5.8%), armazenados com metadados de diagnóstico para auditoria.
3. **Governança & Rastreabilidade de Catálogo:** Todas as entidades possuem dicionários de dados padronizados na Dadosfera com identificação de dados sensíveis (LGPD/PII).

---

## 2. 📋 Entidades Centrais da Camada Qualify

A tabela abaixo resume as 7 entidades estruturadas nesta camada, seus IDs no catálogo da Dadosfera e os arquivos de especificação detalhados:

| Entidade | Tabela Snowflake | Data Asset ID (Dadosfera) | Sensibilidade | Dicionário de Dados |
|:---|:---|:---|:---:|:---|
| **`carrinhos`** | `CART_RECOVERY.CARRINHOS` | `e2d3b1bb-bf22-456e-bc66-4ac843deec82` | 🟢 Interno | [`carrinhos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/carrinhos.md) |
| **`pedidos`** | `CART_RECOVERY.PEDIDOS` | `7f82a988-8e68-416a-b6fa-5007c4789d1a` | 🟢 Interno | [`pedidos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/pedidos.md) |
| **`clientes`** | `CART_RECOVERY.CLIENTES` | `0327fecc-f826-48fb-bb0a-1493fe18a32c` | 🔴 Confidencial (PII) | [`clientes.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/clientes.md) |
| **`produtos`** | `CART_RECOVERY.PRODUTOS` | `65fcfa25-a6f3-4cb8-a444-7fd23df3fa84` | 🟢 Interno | [`produtos.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/produtos.md) |
| **`itens_carrinho`** | `CART_RECOVERY.ITENS_CARRINHO` | `7649755a-c6e8-4b56-a092-be9eefde1dab` | 🟢 Interno | [`itens_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/itens_carrinho.md) |
| **`eventos_carrinho`** | `CART_RECOVERY.EVENTOS_CARRINHO` | `397c3ebc-15cb-42d2-a717-a3b5d150c3ea` | 🟢 Interno | [`eventos_carrinho.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_carrinho.md) |
| **`eventos_resgate`** | `CART_RECOVERY.EVENTOS_RESGATE` | `04739f6d-e8c3-4d6f-80b7-0f98c12a5798` | 🟢 Interno | [`eventos_resgate.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/data/catalogo/qualify/eventos_resgate.md) |

---

## 3. 🔍 Validações em Texto Corrido por Entidade

Abaixo é descrito em detalhe o conjunto de validações técnicas, contábeis e de regras de negócio executadas pelo motor de Data Quality para cada entidade antes da promoção para a camada Qualify:

### 3.1 Entidade `carrinhos` (Ativo Central)
- **Validação de Schema & Chaves:** É validada a obrigatoriedade da chave primária `carrinho_id` (`ERR_CAR_001`) e da chave estrangeira `cliente_id` (`ERR_CAR_002`), garantindo que não existam sessões anônimas sem vínculo de cliente na base de recuperação. Os campos monetários são convertidos e tipados estritamente como `FLOAT / DECIMAL(12,2)`.
- **Validação de Domínio de Status:** O campo `status` é validado contra o conjunto estrito de valores permitidos (`ERR_CAR_003`): `['comprado', 'abandonado', 'expirado', 'ativo', 'recuperado']`. Valores fora deste conjunto são rejeitados.
- **Validações Contábeis & Anomalias:**
  - `ANOM-01`: Valida que o valor do frete seja estritamente não-negativo (`valor_frete >= 0.0`).
  - `ANOM-02`: Valida que o subtotal do carrinho seja maior que zero (`valor_subtotal > 0.0`), impedindo carrinhos vazios faturáveis.
  - `ANOM-03`: Valida que o valor de desconto nunca ultrapasse o valor subtotal do carrinho (`valor_desconto <= valor_subtotal`), bloqueando anomalias de desconto abusivo (> 100%).
  - `ANOM-04`: Validação da equação contábil de fechamento: `valor_total == round(valor_subtotal + valor_frete - valor_desconto, 2)`. Qualquer desvio aritmético roteia o registro para anomalias.
- **Validação Temporal:** `ANOM-05` valida a coerência cronológica de abandono, exigindo que a data de abandono seja maior ou igual à data de criação do carrinho (`data_abandono >= data_criacao`).

### 3.2 Entidade `pedidos` (Conversões e Faturamento)
- **Validação de Schema & Integridade Referencial:** A validação confere a unicidade e não-nulidade do `pedido_id` (`ERR_PED_001`) e a presença do `cliente_id` (`ERR_PED_002`).
- **Validação Financeira:** O montante faturado `valor_total` deve ser positivo (`valor_total > 0`). O `status_pedido` é validado para garantir conformidade com o ciclo de vida de pagamento (`'pago'`, `'cancelado'`, `'estornado'`, `'processando'`).
- **Consistência de Resgate:** Pedidos originados de carrinhos abandonados devem correlacionar o `carrinho_id` com histórico de disparo de resgate prévio para validação de atribuição de receita recuperada.

### 3.3 Entidade `clientes` (Cadastro & LGPD)
- **Validação de Schema & Unicidade:** O identificador `cliente_id` é verificado como chave primária não-nula e única (`ERR_CLI_001`). O campo de e-mail é validado como obrigatório (`ERR_CLI_002`).
- **Validação Sintática por Expressão Regular:** O endereço de e-mail é validado via regex (`ERR_CLI_003`): `^[^@]+@[^@]+\.[^@]+$`. Registros com sintaxe inválida são marcados para quarentena ou correção de canal.
- **Tratamento de Privacidade (LGPD/PII):** Os atributos `nome`, `email` e `telefone` recebem tags de governança de alta sensibilidade no catálogo da Dadosfera, restringindo a visibilidade em consultas analíticas abertas e exigindo mascaramento dinâmico em relatórios executivos.

### 3.4 Entidade `produtos` (Catálogo de SKUs)
- **Validação de Schema & Chaves:** Validação de não-nulidade da PK `produto_id` (`ERR_PROD_001`).
- **Validação de Sanidade de Preços:** 
  - `ERR_PROD_002`: Valida que o `preco_atual` seja estritamente superior a zero (`preco_atual > 0`).
  - `ERR_PROD_003`: Valida que o preço promocional atual seja menor ou igual ao preço original (`preco_atual <= preco_original`), evitando o erro de "promoção invertida" no catálogo de marketplace.

### 3.5 Entidade `itens_carrinho` (Detalhe Granular)
- **Validação de Schema & Chaves:** Valida a presença de `item_id` (`ERR_ITM_001`) e da chave estrangeira `carrinho_id` (`ERR_ITM_002`).
- **Validação de Quantidade & Preço:**
  - `ERR_ITM_003`: Quantidade de itens deve ser um número inteiro estritamente positivo (`quantidade > 0`).
  - `ERR_ITM_004`: Preço unitário do item adicionado deve ser maior que zero (`preco_unitario > 0`).
- **Validação Temporal:** `ERR_ITM_005` valida que, caso o item tenha sido removido do carrinho, a `data_remocao` seja posterior ou igual à `data_adicao`.

### 3.6 Entidade `eventos_carrinho` (Telemetria)
- **Validação de Schema & Chaves:** Validação de `evento_id` (`ERR_EVC_001`) e vinculação à sessão de carrinho via `carrinho_id` (`ERR_EVC_002`).
- **Consistência de Navegação:** Validação de ordenação cronológica das etapas de checkout (`'visualizacao_carrinho'`, `'preenchimento_endereco'`, `'selecao_frete'`, `'escolha_pagamento'`).

### 3.7 Entidade `eventos_resgate` (Régua de CRM)
- **Validação de Schema & Chaves:** Validação de `resgate_id` (`ERR_RES_001`) e `carrinho_id` (`ERR_RES_002`).
- **Validação de Funil de Engajamento & Tempo:** `ERR_RES_003` valida que a data de abertura da mensagem seja cronologicamente igual ou posterior à data de envio (`data_abertura >= data_envio`). As flags booleanas de funil (`flag_entregue`, `flag_aberto`, `flag_clicado`, `flag_convertido`) são validadas para garantir a progressão lógica do funil de marketing.

---

## 4. 🔀 Quarentena de Anomalias (Dual-Artifact - DEC-006)

Registros que falham em qualquer uma das regras acima são extraídos e armazenados na pasta de anomalias com a seguinte estrutura de auditoria:

```json
{
  "anomalia_id": "UUID-V4",
  "entidade": "carrinhos",
  "codigo_erro": "ANOM-04",
  "descricao": "Total contábil inconsistente (valor_total != subtotal + frete - desconto)",
  "severidade": "ALTA",
  "registro_id": "carrinho_784920",
  "detected_at": "2026-08-23T14:30:00Z",
  "payload_original": { ... }
}
```

> **Próxima Etapa:** Os dados 100% aprovados desta camada alimentam o Data Warehouse dimensional conforme detalhado na [Especificação da Camada Curated](file:///c:/Users/pedro/OneDrive/Desktop/wheels/pipelines/datalakes/curated/spec.md).
