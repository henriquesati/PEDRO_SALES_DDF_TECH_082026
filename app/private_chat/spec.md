# 📐 Especificação Técnica Normativa: Private Chat & Orquestração Multi-Agente
**Document ID:** `spec_private_chat_001`  
**Versão:** `1.0.0`  
**Status:** `APROVADO & NORMATIVO`  
**Autor:** Pedro Sales (DDF Tech Case)  
**Modelo de Linguagem:** `gemini-3.7-flash` (Google GenAI / Antigravity SDK)  
**Padrão de API:** `OpenAPI 3.1.0`  

---

## 🛡️ 1. Princípio do Isolamento Máximo (Zero Cross-Bleeding)

O módulo `app/private_chat/` opera sob o **Princípio do Isolamento Arquitetural Máximo**:
1. **Desacoplamento Absoluto**: Toda e qualquer regra, componente visual, cliente de rede, folha de estilo CSS e gerenciamento de estado referente ao chat reside exclusivamente dentro de `app/private_chat/` e `app/pages/chat.py`.
2. **Ruptura Deliberada do Princípio DRY**: Nenhuma abstração, serviço do Lakehouse (`lakehouse_service.py`), componentes de dashboard de BI (`fighter_select.py`, `insights_view.py`) ou tipos compartilhados devem ser importados pelo Private Chat. Se uma função utilitária for necessária, ela deve ser implementada localmente em `app/private_chat/` para blindar o restante da aplicação contra regressões.
3. **Escopo CSS Fechado**: Todos os seletores CSS em `chat_theme.css` possuem prefixo ou isolamento de container (`.private-chat-wrapper`, `.chat-message-*`, `.openapi-*`), impedindo qualquer efeito colateral em outras páginas do Streamlit.

---

## 🤖 2. Configuração de Inteligência & Modelo (Gemini 3.7 Flash)

- **Engine Principal**: Google GenAI via SDK `google.antigravity`.
- **Identificador do Modelo**: `gemini-3.7-flash`.
- **Modo de Operação**: 100% Autônomo (`capabilities.agent_behavior = AgentBehavior.AUTONOMOUS`).
- **Políticas de Ação**: Auto-aprovação universal (`policies = [policy.allow_all()]`) para execução ininterrupta de ferramentas e comandos sem pausas de confirmação humana.
- **Roteamento de Skills**: Injeção automática das 10 skills modulares (`.agents/skills/`) no contexto do agente.

---

## 📡 3. Padronização OpenAPI 3.1.0 & Contratos de Comunicação

O backend autônomo na raiz (`agent_server`) expõe os seguintes contratos documentados em `/docs`, `/redoc` e `/openapi.json`:

| Método | Endpoint | Tag OpenAPI | Finalidade |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | `Health` | Diagnóstico de integridade, latência em ms, agente default e contagem de ativos. |
| `GET` | `/agents` | `Discovery` | Catálogo dos 10 agentes autônomos registrados em `.agents/agents/`. |
| `GET` | `/skills` | `Discovery` | Catálogo das 10 skills modulares registradas em `.agents/skills/`. |
| `POST` | `/chat` | `Inference` | Execução síncrona de turno de inferência (`ChatInput` -> `ChatOutput`). |
| `POST` | `/stream` | `Inference` | Streaming Server-Sent Events (SSE) token a token com evento final `[DONE]`. |

---

## 🎨 4. Design de Interface Clean (Padrão ChatGPT)

1. **Minimalismo e Foco**: A interface não possui cards ruidosos, botões de chips de propensão ou inspetores visuais pesados na área principal.
2. **Layout Centrado**: As mensagens fluem em um canvas centralizado com largura de leitura ideal e bolhas discretas de conversa.
3. **Menu Lateral Contextualizado**: O menu à esquerda concentra as configurações essenciais e a descrição normativa do assistente:
   > *"Pergunte sobre o projeto e seu desenvolvimento: arquitetura do Lakehouse, modelagem dimensional, pipelines de dados, regras de negócio e simuladores de ROI."*
4. **Resiliência Transparente**: Se o servidor FastAPI estiver offline, é exibido um alerta minimalista no topo sem poluir a interface.

---

## 📂 5. Topologia dos Arquivos Isolados

```
app/
├── pages/
│   └── chat.py                     # Entrypoint nativo multi-page montado em /chat
└── private_chat/
    ├── __init__.py                 # Ponto de exportação único (render_private_chat_page)
    ├── spec.md                     # [ESTE DOCUMENTO] Especificação normativa do subsistema
    ├── client.py                   # Cliente HTTP e SSE isolado em urllib puro
    ├── styles.py                   # Injetor de CSS isolado
    ├── chat_theme.css              # Folha de estilos encapsulada com tema clean ChatGPT
    ├── components.py               # Componentes visuais atômicos, menu lateral e mensagens
    └── view.py                     # Orquestrador do ciclo de vida e estado do chat
```

