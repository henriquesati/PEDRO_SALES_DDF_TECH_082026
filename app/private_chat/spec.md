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

## 🚨 4. Protocolo de Resiliência & Modal de Falha de Conexão

Caso o aplicativo Streamlit falhe ao se comunicar com o backend `http://127.0.0.1:8000`:
1. **Detecção Imediata**: O healthcheck (`check_server_health`) com timeout de 2.0s identifica a indisponibilidade.
2. **Modal / Popup de Alerta**: É disparado automaticamente um diálogo modal (`st.dialog` / popup alert) na interface informando:
   - Erro específico de conectividade (`ConnectionRefusedError` ou timeout).
   - Comando CLI para inicialização do servidor: `python make.py agent-server`.
   - Botão de ação rápida para reconexão imediata.
3. **Modo Fallback Offline**: A interface permanece funcional, permitindo a inspeção de metadados estáticos e especificações OpenAPI em cache sem quebrar a execução do Streamlit.

---

## 📂 5. Topologia dos Arquivos

```
app/
├── pages/
│   └── chat.py                     # Entrypoint nativo multi-page montado em /chat
└── private_chat/
    ├── __init__.py                 # Ponto de exportação único (render_private_chat_page)
    ├── spec.md                     # [ESTE DOCUMENTO] Especificação normativa do subsistema
    ├── client.py                   # Cliente HTTP e SSE isolado em urllib puro
    ├── styles.py                   # Injetor de CSS isolado
    ├── chat_theme.css              # Folha de estilos encapsulada com tema dark terminal
    ├── components.py               # Componentes visuais atômicos e modal de falha
    └── view.py                     # Orquestrador do ciclo de vida e estado do chat
```
