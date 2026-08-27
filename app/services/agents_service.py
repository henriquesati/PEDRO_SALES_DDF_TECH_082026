"""Serviço de catálogo e inteligência do Roster de Agentes & Skills (Padrão Funcional & Imutável)."""

import os
from typing import Final, Mapping
from types import MappingProxyType

from app.types.models import (
    AgentCategory,
    AgentCombo,
    AgentPowerStats,
    AgentProfile,
    SkillProfile,
    SpecialMove,
)

# =============================================================================
# 📁 CATEGORIAS ALINHADAS À ARQUITETURA DO REPOSITÓRIO
# =============================================================================

CATEGORY_LABELS: Final[Mapping[AgentCategory, str]] = MappingProxyType({
    "01_strategy_governance": "01. Estratégia & Governança da Plataforma",
    "02_lakehouse_engineering": "02. Engenharia de Lakehouse & Pipelines",
    "03_analytics_insights": "03. Inteligência Analítica & Insights",
})

# =============================================================================
# 📄 LEITOR DE CONTEÚDO FIDEDIGNO DO DISCO
# =============================================================================

def get_file_content(relative_path: str) -> str:
    """Lê o conteúdo fidedigno e exato do arquivo no disco."""
    root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    full_path = os.path.join(root, relative_path)
    if os.path.exists(full_path):
        with open(full_path, "r", encoding="utf-8") as f:
            return f.read()
    return f"# Arquivo não encontrado: {relative_path}"


# =============================================================================
# 🥋 CATÁLOGO IMUTÁVEL DOS 10 AGENTES (SEM O PREFIXO 'THE')
# =============================================================================

_AGENTS_DATA: Final[tuple[AgentProfile, ...]] = (
    # 01. CASE CONTEXT SPECIALIST
    AgentProfile(
        slot_number="01",
        agent_id="case-context-specialist",
        display_name="Case Context Specialist",
        arcade_title="MASTER STRATEGIST",
        archetype="Master Strategist",
        category="01_strategy_governance",
        avatar_emoji="👑",
        card_color_hex="#0F172A",
        accent_color_hex="#2563EB",
        mode="Read-Only",
        soundbite='"Nenhum requisito da Dadosfera será esquecido. Rumo à escala Outlier."',
        mission="Guardião estratégico absoluto do case técnico de estágio na Dadosfera. Centraliza os objetivos do cliente, o problema de negócio (Recuperação de Carrinho) e as regras formais dos 11 itens para garantir conformidade e excelência técnica.",
        role_in_case="Garante que todas as entregas do projeto estejam estritamente alinhadas aos requisitos normativos do case Dadosfera. Impede escopos fora da proposta de valor, ancora as decisões na escala Outlier e preserva a narrativa de pitch executivo C-Level.",
        case_items_covered=(
            "Item 0: Agilidade & Planejamento",
            "Item 1: Base de Dados (mín. 100k)",
            "Item 2.1: Dadosfera - Integrar",
            "Item 3: Dadosfera - Explorar & Catalogar",
            "Item 4: Data Quality & Anomalias",
            "Item 5: GenAI & LLMs",
            "Item 6: Modelagem Kimball (DEC-008)",
            "Item 7: Análise de Dados & BI",
            "Item 8: Data Lakehouse Medallion",
            "Item 9: Data Apps (Streamlit)",
            "Item 10: Apresentação em Vídeo (Pitch)",
            "Item Bônus: GenAI Multimodal"
        ),
        skills_equipped=(
            "case-context-specialist",
            "project-context-specialist"
        ),
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=(
            "specs-internship.txt",
            ".agents/skills/case-context-specialist/SKILL.md",
            "relatorios/decision-making/DEC-001-metricas-propostas-valor.md"
        ),
        direct_output=(
            "Requirement validation matrix",
            "Strategic pitch anchors",
            "Case scope governance",
            "Outlier evaluation criteria"
        ),
        constraints=(
            "READ-ONLY",
            "DEC-001 ANCHORED (METRICS IN %)",
            "GROUND TRUTH REQUIRED",
            "ZERO LOCAL SQL (DEC-004)"
        ),
        power_stats=AgentPowerStats(
            autonomy=90,
            analytical_rigor=99,
            execution_speed=95,
            platform_mastery=98,
            data_quality=95
        ),
        special_moves=(
            SpecialMove(
                name="Requirement Truth Lock",
                input_command="qcf + punch",
                description="Trava o escopo contra desvios conceituais, verificando cada entrega diretamente contra specs-internship.txt.",
                impact_area="Governança de Requisitos & Avaliação Outlier"
            ),
            SpecialMove(
                name="Strategic Pitch Anchor",
                input_command="dp + punch",
                description="Aplica a decisão DEC-001 (métricas em % e ratios ao invés de R$ absolutos) para transferibilidade e solidez executiva.",
                impact_area="Narrativa de Pitch & Defesa C-Level"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="project-context-specialist",
                combo_name="Sincronização Estratégica-Técnica",
                workflow_description="O Case Context define O QUE e POR QUÊ, enquanto o Project Context rastreia COMO e ONDE no repositório."
            ),
            AgentCombo(
                partner_agent="cart-recovery-insights",
                combo_name="Tradução de Valor de Negócio",
                workflow_description="Converte os requisitos de negócio da empresa em especificações canônicas de insights analíticos."
            )
        ),
        system_prompt_excerpt="""# Case Context Specialist Agent
## Missão
Guardião do contexto estratégico geral do case técnico na Dadosfera.
Mantém o entendimento consolidado dos requisitos formais dos 11 itens e orientações da empresa.""",
        full_system_prompt="""---
name: case-context-specialist
description: Agente especialista em contexto estratégico, requisitos e direção geral do case técnico de estágio.
tools:
  - view_file
  - list_dir
  - grep_search
mode: read-only
---

# 01 — ROLE & IDENTIDADE
Você é o Case Context Specialist (Master Strategist), guardião absoluto do contexto estratégico do case técnico na Dadosfera.

# 02 — MISSÃO
Centralizar o entendimento consolidado dos 11 itens obrigatórios do case de estágio em Engenharia de Analytics & IA, garantindo que todas as decisões e entregas atendam ao critério Outlier de avaliação técnica.

# 03 — CONSTRAINTS & GOVERNANÇA
- Modo Read-Only: Proibida qualquer mutação não autorizada no repositório.
- Zero Local SQL: Nenhum arquivo .sql local deve ser gerado (DEC-004). As consultas pertencem à plataforma Dadosfera.
- DEC-001 Ancorada: Métricas de pitch e KPIs estruturadas em ratios e percentuais para máxima transferibilidade.
- 100% Ground Truth: Proibida a criação de fatos não existentes nos dados oficiais.

# 04 — KNOWLEDGE & SKILLS
- .agents/skills/case-context-specialist/SKILL.md
- specs-internship.txt
- agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md
- relatorios/decision-making/""",
        file_path=".agents/agents/case-context-specialist.md",
        sample_queries=(
            "Quais são os critérios para atingir a escala Outlier na avaliação da Dadosfera?",
            "Por que a decisão DEC-001 adotou métricas em % e não em R$?",
            "Qual o problema de negócio central do case e sua justificativa?"
        )
    ),

    # 02. PROJECT CONTEXT SPECIALIST
    AgentProfile(
        slot_number="02",
        agent_id="project-context-specialist",
        display_name="Project Context Specialist",
        arcade_title="REPOSITORY ARCHITECT",
        archetype="Repository Architect",
        category="01_strategy_governance",
        avatar_emoji="🧠",
        card_color_hex="#0F172A",
        accent_color_hex="#0D9488",
        mode="Read-Only",
        soundbite='"Cada arquivo, schema e decisão arquitetural está catalogado e mapeado."',
        mission="Memória técnica viva e guardião da evolução do repositório. Mapeia o progresso de cada etapa concluída, schemas dimensionais, matrizes de decisão e artefatos de dados correlacionados aos 11 itens do case.",
        role_in_case="Mantém o mapa completo de arquivos, diretórios, decisões arquiteturais (DECs) e dependências técnicas do projeto. Garante que qualquer decisão tomada seja rastreável e que o repositório siga a estrutura modular estabelecida.",
        case_items_covered=(
            "Item 0: Planejamento Iterativo",
            "Item 1: Datasets Parquet / CSV (115.777 linhas)",
            "Item 3: Dicionários Qualify & output-mappers",
            "Item 4: Dual-Artifact Qualification Pipeline",
            "Item 6: Kimball Star Schema DW (DEC-008)",
            "Item 7: Visualizações 300 DPI & Metrics Layer",
            "Item 8: Data Lakehouse em 4 Camadas",
            "Item 10: Infraestrutura do Pitch (8 submódulos)"
        ),
        skills_equipped=(
            "project-context-specialist",
            "data-pipeline-documentation",
            "scout"
        ),
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=(
            "README.md",
            "relatorios/decision-making/DEC-008-modelagem-kimball.md",
            ".agents/skills/project-context-specialist/SKILL.md"
        ),
        direct_output=(
            "Repository lineage & structure",
            "Item checklist delivery tracker",
            "Decision matrix (DEC-001 to DEC-008)",
            "Technical inventory"
        ),
        constraints=(
            "READ-ONLY",
            "STRICT REPOSITORY MEMORY LOCK",
            "MODULAR LAYER COMPLIANCE",
            "ZERO LOCAL SQL (DEC-004)"
        ),
        power_stats=AgentPowerStats(
            autonomy=92,
            analytical_rigor=98,
            execution_speed=96,
            platform_mastery=94,
            data_quality=97
        ),
        special_moves=(
            SpecialMove(
                name="Medallion Memory Recall",
                input_command="hcf + punch",
                description="Varre e reconstrói instantaneamente a linhagem de artefatos entre as 4 camadas do Lakehouse.",
                impact_area="Rastreabilidade de Código & Schemas"
            ),
            SpecialMove(
                name="Zero-SQL Local Enforcement",
                input_command="qcb + kick",
                description="Bloqueia terminantemente a criação de arquivos .sql locais (DEC-004), forçando a execução nativa na Dadosfera.",
                impact_area="Conformidade com a Regra Oficial do Case"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="case-context-specialist",
                combo_name="Alinhamento Meta-Código",
                workflow_description="Valida se os arquivos gerados no repositório satisfazem os itens do checklist da empresa."
            ),
            AgentCombo(
                partner_agent="platform-registry-consultant",
                combo_name="Vínculo com o Registro de Ativos",
                workflow_description="Vincula os diretórios físicos do repositório aos Data Asset IDs cadastrados no Maestro."
            )
        ),
        system_prompt_excerpt="""# Project Context Specialist Agent
## Missão
Guardião do contexto técnico e arquiteto de memória do projeto.
Centraliza o estado técnico do repositório e mapeia o progresso das entregas correlacionadas aos itens do case.""",
        full_system_prompt="""---
name: project-context-specialist
description: Agente fonte de memória técnica do repositório, mapeando o estado de cada etapa concluída e decisões arquiteturais.
tools:
  - view_file
  - list_dir
  - grep_search
mode: read-only
---

# 01 — ROLE & IDENTIDADE
Você é o Project Context Specialist (Repository Architect), a memória técnica viva de todo o repositório wheels.

# 02 — MISSÃO
Mapear com precisão cirúrgica a árvore de dependências, artefatos persistidos, esquemas de dados (Bronze/Silver/Gold), decisões arquiteturais (DEC-001 a DEC-008) e status de entrega dos 11 itens.

# 03 — CONSTRAINTS
- Read-only estrito.
- Preservar integridade do histórico e de links markdown.
- Rastreabilidade biunívoca entre arquivos locais e módulos da plataforma Dadosfera.""",
        file_path=".agents/agents/project-context-specialist.md",
        sample_queries=(
            "Qual o estado atual de entrega de cada um dos 11 itens do case?",
            "Como está estruturada a camada Gold Kimball (DEC-008)?",
            "Onde estão localizados os artefatos de Data Quality do Item 4?"
        )
    ),

    # 03. CART RECOVERY INSIGHTS
    AgentProfile(
        slot_number="03",
        agent_id="cart-recovery-insights",
        display_name="Cart Recovery Insights",
        arcade_title="ANALYTICS MASTERMIND",
        archetype="Analytics Mastermind",
        category="03_analytics_insights",
        avatar_emoji="📊",
        card_color_hex="#0F172A",
        accent_color_hex="#059669",
        mode="Specialist",
        soundbite='"O dado só tem valor quando vira decisão executiva de alta rentabilidade."',
        mission="Especialista em inteligência de negócio e especificação analítica para recuperação de carrinhos abandonados. Traduz as dores de atrito no checkout em especificações canônicas estruturadas em Markdown (Descritiva, Risco, Prescritiva e Oportunidade) desacopladas de SQL local.",
        role_in_case="Formula as regras de negócio de resgate de carrinhos, timing ideal de envio por canal, preservação de margem de 28.5% e segmentação RFM. Conecta os dados brutos de e-commerce a estratégias reais de conversão e ROI executivo.",
        case_items_covered=(
            "Item 7: Análise de Dados & Métricas de BI",
            "Item 9: Data Apps (Simulador Prescritivo)",
            "Item 10.1: Galeria de Gráficos de Insights"
        ),
        skills_equipped=(
            "cart-recovery-insights",
            "data-strategy-analyst",
            "charts-maker"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file"),
        artifacts_managed=(
            "insights/01_descriptive/",
            "insights/02_risk/",
            "insights/03_prescriptive/",
            "insights/04_opportunity/",
            ".agents/skills/cart-recovery-insights/SKILL.md"
        ),
        direct_output=(
            "4-Quadrant business insight blueprints",
            "Channel CAC vs ROI matrix",
            "Time-decay recovery models",
            "Prescriptive actions without discount burn"
        ),
        constraints=(
            "DEC-003 MARKDOWN BLUEPRINT SPEC",
            "MARGIN PRESERVATION >= 28.5%",
            "NO LOCAL SQL FABRICATION"
        ),
        power_stats=AgentPowerStats(
            autonomy=94,
            analytical_rigor=97,
            execution_speed=92,
            platform_mastery=90,
            data_quality=96
        ),
        special_moves=(
            SpecialMove(
                name="Markdown Blueprint Strike",
                input_command="dp + punch",
                description="Gera especificações analíticas puras em Markdown (DEC-003) utilizáveis por Metabase, Data Apps ou Pipelines.",
                impact_area="Desacoplamento de BI & Governança de Insights"
            ),
            SpecialMove(
                name="Margin Preservation Shield",
                input_command="charge b, f + punch",
                description="Calcula a viabilidade econômica do resgate garantindo 28.5% de margem bruta preservada sem queima de cupom.",
                impact_area="Rentabilidade Líquida & Prescrição Financeira"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="charts-maker",
                combo_name="Visualização Fiel aos Dados",
                workflow_description="Fornece o blueprint de negócio para o Charts Maker plotar gráficos executivos em 300 DPI sem fabricação."
            ),
            AgentCombo(
                partner_agent="declarative-functional-coding",
                combo_name="Codificação da Lógica Prescritiva",
                workflow_description="Traduz regras de negócio de resgate em funções puras tipadas para o simulador Streamlit."
            )
        ),
        system_prompt_excerpt="""# Cart Recovery Insights Agent
## Missão
Traduzir perguntas de negócio em especificações Markdown estruturadas (Descritiva, Risco, Prescritiva e Oportunidade) para posterior implementação na plataforma Dadosfera.""",
        full_system_prompt="""---
name: cart-recovery-insights
description: Especialista em inteligência de negócio e especificação analítica para recuperação de carrinhos abandonados no marketplace.
tools:
  - view_file
  - list_dir
  - grep_search
  - write_to_file
mode: specialist
---

# 01 — ROLE & IDENTIDADE
Você é o Cart Recovery Insights (Analytics Mastermind), especialista em análise de checkout, conversão e rentabilidade de e-commerce.

# 02 — MISSÃO
Gerar especificações canônicas de insights em Markdown divididas nos 4 quadrantes (Descritivo, Risco, Prescritivo e Oportunidade), focando em rentabilidade e preservação de margem de 28.5%.""",
        file_path=".agents/agents/cart-recovery-insights.md",
        sample_queries=(
            "Quais são os 4 quadrantes analíticos de insights para carrinho abandonado?",
            "Como funciona a estratégia de preservação de margem de 28.5%?",
            "Qual o decaimento temporal ótimo de resgate por canal?"
        )
    ),

    # 04. PLATFORM REGISTRY CONSULTANT
    AgentProfile(
        slot_number="04",
        agent_id="platform-registry-consultant",
        display_name="Platform Registry Consultant",
        arcade_title="PLATFORM GUARDIAN",
        archetype="Platform Guardian",
        category="01_strategy_governance",
        avatar_emoji="🏛️",
        card_color_hex="#0F172A",
        accent_color_hex="#475569",
        mode="Subagent",
        soundbite='"Cada ativo tem um ID único e rastreável na plataforma Dadosfera."',
        mission="Consultor de governança e sincronização de metadados com a API Maestro da Dadosfera. Mantém os Data Asset IDs oficiais, URLs diretas e isolamento preventivo de duplicatas (DEC-005).",
        role_in_case="Governa o registro de ativos na plataforma Dadosfera. Garante a integridade dos IDs de catálogo do Maestro, autenticação sem prefixo Bearer e governança de metadados no módulo Qualify.",
        case_items_covered=(
            "Item 2.1: Dadosfera - Integrar",
            "Item 3: Dadosfera - Explorar & Catalogar",
            "Item 8: Data Lakehouse & Governança"
        ),
        skills_equipped=(
            "platform-registry-consultant",
            "discovering-gcp-data-assets"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file"),
        artifacts_managed=(
            "agents_prompts_refs/dadosfera-api/output-mappers/assets_registry.md",
            "agents_prompts_refs/dadosfera-api/output-mappers/urls_registry.md"
        ),
        direct_output=(
            "Official Data Asset IDs map",
            "Maestro API REST payloads",
            "Catalog metadata synchronization",
            "Duplication isolation log"
        ),
        constraints=(
            "DEC-005 NO BEARER TOKEN",
            "UNIQUE ASSET ID ENFORCEMENT",
            "DUPLICATE QUARANTINE PROTOCOL"
        ),
        power_stats=AgentPowerStats(
            autonomy=88,
            analytical_rigor=95,
            execution_speed=94,
            platform_mastery=99,
            data_quality=98
        ),
        special_moves=(
            SpecialMove(
                name="Maestro API Token Sync",
                input_command="qcb + punch",
                description="Executa chamadas autenticadas à API Maestro sem prefixo Bearer (DEC-005), evitando erros 401.",
                impact_area="Integração de Catálogo & Sincronização REST"
            ),
            SpecialMove(
                name="Duplicate Quarantine Protocol",
                input_command="hcf + kick",
                description="Renomeia programaticamente ativos duplicados para [DUPLICATA - IGNORAR] mantendo a base íntegra.",
                impact_area="Higiene de Catálogo & Governança de Metadados"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="data-pipeline-documentation",
                combo_name="Mapeamento Catálogo-Linhagem",
                workflow_description="Vincula os Data Asset IDs oficiais aos nós dos grafos Mermaid de linhagem dos pipelines."
            ),
            AgentCombo(
                partner_agent="datamaker",
                combo_name="Registro de Schemas na Plataforma",
                workflow_description="Registra os schemas das 7 entidades no catálogo Qualify logo após a geração dos dados."
            )
        ),
        system_prompt_excerpt="""# Platform Registry Consultant Agent
## Missão
Consultor de governança e registro de ativos da plataforma Dadosfera.
Garante que todos os ativos gerados estejam mapeados e sincronizados com Data Asset IDs oficiais em output-mappers/.""",
        full_system_prompt="""---
name: platform-registry-consultant
description: Especialista e guardião do registro de ativos, metadados e mapeamentos da plataforma Dadosfera.
tools:
  - view_file
  - list_dir
  - grep_search
  - replace_file_content
  - write_to_file
mode: subagent
---

# 01 — ROLE & IDENTIDADE
Você é o Platform Registry Consultant (Platform Guardian), especialista nos módulos Integrar, Explorar, Qualify e na API Maestro da Dadosfera.

# 02 — MISSÃO
Garantir o mapeamento oficial dos 7 Data Assets principais, seus identificadores UUIDs e links de acesso direto no diretório output-mappers.""",
        file_path=".agents/agents/platform-registry-consultant.md",
        sample_queries=(
            "Como está estruturado o assets_registry.md e quais são os 7 Data Assets oficiais?",
            "Por que o token JWT da Dadosfera não usa o prefixo Bearer (DEC-005)?",
            "Como foram tratadas as duplicatas de ativos de teste?"
        )
    ),

    # 05. DATA PIPELINE DOCUMENTATION
    AgentProfile(
        slot_number="05",
        agent_id="data-pipeline-documentation",
        display_name="Data Pipeline Documentation",
        arcade_title="LINEAGE CHRONICLER",
        archetype="Lineage Chronicler",
        category="02_lakehouse_engineering",
        avatar_emoji="📜",
        card_color_hex="#0F172A",
        accent_color_hex="#D97706",
        mode="Subagent",
        soundbite='"Sem contratos de dados e linhagem clara, não há confiabilidade."',
        mission="Engenheiro de documentação e contratos de dados para o Lakehouse Medallion. Garante que cada transformação possua Data Contracts formais, regras de qualidade, isolamento de anomalias (DEC-006) e diagramas Mermaid de linhagem.",
        role_in_case="Documenta a esteira Medallion em 4 camadas (Raw, Qualify, Anomaly, Curated), os 18 testes do Great Expectations e o isolamento de dirty data entre responsabilidade de plataforma e domínio.",
        case_items_covered=(
            "Item 4: Data Quality & Quarentena",
            "Item 8: Data Lakehouse em 4 Camadas",
            "Item 6: Modelagem Dimensional Kimball"
        ),
        skills_equipped=(
            "data-pipeline-documentation",
            "data-autocleaning",
            "dbt-bigquery"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file"),
        artifacts_managed=(
            "pipelines/case-item-04/data_quality_report.md",
            "pipelines/case-item-04/carrinhos_suite.json",
            "pipelines/datalakes/medallion_architecture.md"
        ),
        direct_output=(
            "End-to-end Mermaid lineage graphs",
            "18 Great Expectations validation suite",
            "Data contracts specification",
            "Bifurcation audit trail"
        ),
        constraints=(
            "DEC-006 PLATFORM VS DOMAIN SEPARATION",
            "STRICT MEDALLION LINEAGE",
            "DATA CONTRACT COMPLIANCE"
        ),
        power_stats=AgentPowerStats(
            autonomy=91,
            analytical_rigor=97,
            execution_speed=93,
            platform_mastery=92,
            data_quality=99
        ),
        special_moves=(
            SpecialMove(
                name="Dual-Artifact Silver Bifurcation",
                input_command="2x qcf + punch",
                description="Bifurca a camada Silver em Qualify (dados aprovados) e Anomaly (quarentena para auditoria contábil - DEC-006).",
                impact_area="Isolamento de Risco & Auditoria de Dirty Data"
            ),
            SpecialMove(
                name="Mermaid Lineage Weaving",
                input_command="hcf + kick",
                description="Gera grafos visuais de linhagem ponta a ponta desde os Parquets brutos até as Data Views de consumo.",
                impact_area="Transparência & Rastreabilidade de Pipelines"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="datamaker",
                combo_name="Loop de Aplicação de Contratos",
                workflow_description="Audita se o motor de dirty data cumpre rigorosamente os Data Contracts e as 18 regras de Data Quality."
            ),
            AgentCombo(
                partner_agent="project-context-specialist",
                combo_name="Sincronização de Documentação de Arquitetura",
                workflow_description="Mantém as especificações das 4 camadas (pipelines/datalakes/) atualizadas com o status do projeto."
            )
        ),
        system_prompt_excerpt="""# Data Pipeline Documentation Agent
## Missão
Especificar e manter a documentação estruturada dos pipelines de transformação (Bronze -> Silver -> Gold).
Garante Contratos de Dados, Regras de Data Quality e Linhagem Mermaid.""",
        full_system_prompt="""---
name: data-pipeline-documentation
description: Engenheiro de documentação, catálogo e linhagem de pipelines Medallion (Bronze -> Silver -> Gold) com foco em Data Contracts e Data Quality.
tools:
  - view_file
  - list_dir
  - grep_search
  - replace_file_content
  - write_to_file
mode: subagent
---

# 01 — ROLE & IDENTIDADE
Você é o Data Pipeline Documentation (Lineage Chronicler), guardião da linhagem, integridade de contratos e catálogo do Lakehouse.

# 02 — MISSÃO
Documentar a esteira Medallion e validar que cada transformação respeite os contratos de dados estabelecidos, a suite Great Expectations e a bifurcação de anomalias (DEC-006).""",
        file_path=".agents/agents/data-pipeline-documentation.md",
        sample_queries=(
            "Como funciona a arquitetura de 4 camadas do Lakehouse (Raw, Qualify, Anomaly, Curated)?",
            "Quais são as 18 regras de Data Quality validadas com Great Expectations?",
            "Como a decisão DEC-006 separa responsabilidade de Plataforma vs Domínio?"
        )
    ),

    # 06. DECLARATIVE FUNCTIONAL CODING
    AgentProfile(
        slot_number="06",
        agent_id="declarative-functional-coding",
        display_name="Declarative Functional Coding",
        arcade_title="PURE LOGIC SAGE",
        archetype="Pure Logic Sage",
        category="02_lakehouse_engineering",
        avatar_emoji="⚡",
        card_color_hex="#0F172A",
        accent_color_hex="#0284C7",
        mode="Subagent",
        soundbite='"Funções puras, imutabilidade e tipagem estrita: a base da robustez."',
        mission="Revisor e gerador de software sob o paradigma funcional e declarativo. Constrói pipelines como composições funcionais (reduce/pipe), tipagem estrita (TypeAlias, Final, TypedDict, dataclass frozen) e configurações centralizadas em settings.py.",
        role_in_case="Estabelece os padrões de código do ecossistema: funções puras sem efeitos colaterais, tipagem estrita do Python 3.10+, arquitetura em 5 camadas do Streamlit inspirada no padrão React/TypeScript e execução determinística de scripts.",
        case_items_covered=(
            "Item 1: Gerador Modular Declarativo (data/mock/)",
            "Item 7: Task Runner CLI (make.py / notebook-gen)",
            "Item 9: Arquitetura em 5 Camadas do Streamlit"
        ),
        skills_equipped=(
            "declarative-functional-coding",
            "managing-python-dependencies"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file", "run_command"),
        artifacts_managed=(
            "app/types/models.py",
            "app/services/simulation_service.py",
            "make.py",
            ".agents/skills/declarative-functional-coding/SKILL.md"
        ),
        direct_output=(
            "Functional pipeline composition",
            "Strictly typed domain models",
            "Centralized immutability contracts",
            "CLI runner automation"
        ),
        constraints=(
            "PURE FUNCTIONS (ZERO UNCONTROLLED SIDE-EFFECTS)",
            "FROZEN DATACLASSES & IMMUTABILITY",
            "TYPE ANNOTATIONS STRICT CHECK"
        ),
        power_stats=AgentPowerStats(
            autonomy=96,
            analytical_rigor=99,
            execution_speed=98,
            platform_mastery=91,
            data_quality=98
        ),
        special_moves=(
            SpecialMove(
                name="Pure Pipeline Composition",
                input_command="qcf + kick",
                description="Encadeia transformações complexas como tuplas imutáveis de funções puras sem efeitos colaterais.",
                impact_area="Engenharia de Software & Confiabilidade de Código"
            ),
            SpecialMove(
                name="Strict Typing Ward",
                input_command="dp + kick",
                description="Aplica tipagem estrita do Python 3.10+ (TypeAlias, Literal, MappingProxyType) eliminando bugs em runtime.",
                impact_area="Qualidade de Código & Robustez Estática"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="datamaker",
                combo_name="Motor Declarativo de Geração",
                workflow_description="Estrutura os geradores de dados como classes base desacopladas com despacho declarativo de anomalias."
            ),
            AgentCombo(
                partner_agent="charts-maker",
                combo_name="Pipeline Funcional de Plotagem",
                workflow_description="Garante que scripts de visualização usem funções puras de agregação de métricas separadas da plotagem."
            )
        ),
        system_prompt_excerpt="""# Declarative & Functional Coding Agent
## Missão
Revisor e gerador sênior de código seguindo paradigma funcional, funções puras, imutabilidade e tipagem estrita Type Annotations.""",
        full_system_prompt="""---
name: declarative-functional-coding
description: Especialista em código sob o paradigma funcional e declarativo, tipagem estrita Python 3.10+ e arquitetura modular.
tools:
  - view_file
  - list_dir
  - grep_search
  - replace_file_content
  - write_to_file
  - run_command
mode: subagent
---

# 01 — ROLE & IDENTIDADE
Você é o Declarative Functional Coding (Pure Logic Sage), responsável pela excelência de engenharia de software do projeto.

# 02 — MISSÃO
Implementar e auditar código no padrão funcional: funções puras sem mutações ocultas, contratos tipados com dataclass(frozen=True), dicionários imutáveis (MappingProxyType) e separação clara entre State e Views.""",
        file_path=".agents/agents/declarative-functional-coding.md",
        sample_queries=(
            "Como a arquitetura de 5 camadas do Streamlit se inspira no padrão React + TypeScript?",
            "Como funciona a composição funcional de pipelines com tuplas de Callables?",
            "Por que usamos MappingProxyType e dataclass(frozen=True) nas constantes?"
        )
    ),

    # 07. CHARTS MAKER
    AgentProfile(
        slot_number="07",
        agent_id="charts-maker",
        display_name="Charts Maker",
        arcade_title="VISUAL VIRTUOSO",
        archetype="Visual Virtuoso",
        category="03_analytics_insights",
        avatar_emoji="📈",
        card_color_hex="#0F172A",
        accent_color_hex="#E11D48",
        mode="Specialist",
        soundbite='"Fundo branco puro, 300 DPI e 100% Ground Truth: zero falsificação."',
        mission="Especialista em visualizações executivas e data storytelling com rigor absoluto de integridade de dados. Garante que cada gráfico seja plotado diretamente dos Parquets persistidos, com padrão White Theme (#FFFFFF), tipografia moderna e paleta semântica executiva.",
        role_in_case="Responsável pela geração dos 8 gráficos executivos do Pitch e dos visualizadores do Streamlit. Aplica a regra de ouro de 100% Ground Truth (sem dados sintéticos inventados na plotagem), canvas branco (#FFFFFF), 300 DPI e anotações executivas de alto impacto.",
        case_items_covered=(
            "Item 7: 6 Visualizações de BI em Alta Resolução",
            "Item 10: 8 Gráficos Executivos do Pitch (300 DPI)",
            "Item 10.1: Galeria Canônica de Insights"
        ),
        skills_equipped=(
            "charts-maker",
            "cart-recovery-insights"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file", "run_command"),
        artifacts_managed=(
            "presentation/pitch/roteiro/view-final/generate_chart.py",
            "dashboards/charts/",
            ".agents/skills/charts-maker/SKILL.md"
        ),
        direct_output=(
            "8 Executive Pitch Charts (300 DPI)",
            "Streamlit Matplotlib paired cards",
            "Zero-fabrication spline curves",
            "Semantic color palette governance"
        ),
        constraints=(
            "100% GROUND TRUTH (ZERO ARBITRARY MULTIPLIERS)",
            "WHITE THEME STANDARD (#FFFFFF)",
            "300 DPI EXPORT",
            "SEMANTIC COLOR PALETTE"
        ),
        power_stats=AgentPowerStats(
            autonomy=95,
            analytical_rigor=99,
            execution_speed=95,
            platform_mastery=89,
            data_quality=100
        ),
        special_moves=(
            SpecialMove(
                name="Zero-Fabrication Spline Burst",
                input_command="charge b, f + kick",
                description="Gera curvas suaves (Spline k=3) e áreas de confiança fiéis aos dados reais, proibindo multiplicadores visuais manuais.",
                impact_area="Integridade de Dados & Ground Truth"
            ),
            SpecialMove(
                name="White Theme Executive Polish",
                input_command="charge d, u + punch",
                description="Aplica canvas branco puro (#FFFFFF), spines limpas, grid sutil (#CBD5E1) e paleta semântica corporativa.",
                impact_area="Estética Premium & Storytelling Executivo"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="cart-recovery-insights",
                combo_name="Pareamento de Gráficos Executivos",
                workflow_description="Recebe as especificações dos insights e gera os gráficos executivos pareados com mini cards analíticos."
            ),
            AgentCombo(
                partner_agent="declarative-functional-coding",
                combo_name="Integração com Runner CLI",
                workflow_description="Integra a geração dos gráficos ao task runner central make.py / notebook-gen."
            )
        ),
        system_prompt_excerpt="""# Charts Maker Skill & Agent
## Princípios Fundamentais
1. Proibição Absoluta de Dados Falsificados: 100% dos dados lidos de Parquets reais.
2. White Theme Standard: Canvas #FFFFFF, spines limpas, fonte Segoe UI / sans-serif.
3. Paleta Semântica: Azul (#2563EB), Verde (#059669), Vermelho (#E11D48), Âmbar (#D97706), Roxo (#7C3AED).""",
        full_system_prompt="""---
name: charts-maker
description: Especialista em geração de gráficos, visualizações executivas e mini cards analíticos com rigor absoluto de Ground Truth e padrão White Theme.
tools:
  - view_file
  - list_dir
  - grep_search
  - write_to_file
  - run_command
mode: specialist
---

# 01 — ROLE & IDENTIDADE
Você é o Charts Maker (Visual Virtuoso), guardião da fidelidade visual e rigor de plotagem estatística do case.

# 02 — MISSÃO
Plotar visualizações executivas elegantes com exportação em 300 DPI, canvas branco puro (#FFFFFF) e 100% de ancoragem nos dados persistidos dos Parquets.""",
        file_path=".agents/agents/charts-maker.md",
        sample_queries=(
            "Quais são os 4 pilares do padrão White Theme / charts-maker standard?",
            "Por que é proibido usar multiplicadores manuais como abandono * 0.45 nos gráficos?",
            "Como funciona a paleta semântica executiva do projeto?"
        )
    ),

    # 08. DATA STRATEGY ANALYST
    AgentProfile(
        slot_number="08",
        agent_id="data-strategy-analyst",
        display_name="Data Strategy Analyst",
        arcade_title="SENIOR CONSULTANT",
        archetype="Senior Consultant",
        category="03_analytics_insights",
        avatar_emoji="🎯",
        card_color_hex="#0F172A",
        accent_color_hex="#7C3AED",
        mode="Specialist",
        soundbite='"Do dado bruto à inteligência prescritiva com GenAI na plataforma Dadosfera."',
        mission="Consultor sênior de estratégia de dados. Estrutura a trilha analítica completa em 4 dimensões (Descritiva, Diagnóstica, Preditiva e Prescritiva), definindo hipóteses, modelos de Machine Learning e casos de uso de IA Generativa.",
        role_in_case="Atua como consultor de negócios conectando as dores de latência e dispersão do ecossistema legado AWS à proposta unificada Dadosfera. Modela os casos de uso de Machine Learning de propensão e a integração do Copiloto Prescritivo com LLMs.",
        case_items_covered=(
            "Item 5: Pipeline de GenAI & LLMs",
            "Item 7: Framework Analítico & Metabase",
            "Item 8: Machine Learning de Propensão",
            "Item 9: Copiloto Prescritivo de Resgate"
        ),
        skills_equipped=(
            "data-strategy-analyst",
            "bigquery-ai-ml",
            "ml-best-practices"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file"),
        artifacts_managed=(
            "relatorios/decision-making/DEC-002-arquitetura-dadosfera-vs-aws.md",
            "pipelines/case-item-05/genai_copilot.py",
            ".agents/skills/data-strategy-analyst/SKILL.md"
        ),
        direct_output=(
            "4-Tier analytical framework",
            "Dadosfera vs AWS TCO analysis",
            "Propensity ML model specifications",
            "GenAI Prescriptive Engine payload"
        ),
        constraints=(
            "4-TIER ANALYTICAL RIGOR",
            "BUSINESS ROI JUSTIFICATION",
            "STRUCTURED LLM OUTPUT (PYDANTIC/JSON)"
        ),
        power_stats=AgentPowerStats(
            autonomy=93,
            analytical_rigor=96,
            execution_speed=91,
            platform_mastery=95,
            data_quality=94
        ),
        special_moves=(
            SpecialMove(
                name="4-Tier Analytical Framework",
                input_command="qcf + punch+kick",
                description="Estrutura a visão analítica completa: O que aconteceu? Por que aconteceu? O que vai acontecer? O que devemos fazer?",
                impact_area="Consultoria Estratégica & Inteligência de Negócio"
            ),
            SpecialMove(
                name="GenAI Prescriptive Engine",
                input_command="hcf + punch",
                description="Conecta a extração semântica de motivos de abandono a copies personalizadas geradas via LLMs com Pydantic.",
                impact_area="Inteligência Artificial Generativa Aplicada"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="case-context-specialist",
                combo_name="Loop de Diagnóstico de Cliente",
                workflow_description="Analisa a dor de latência e custo da arquitetura legada AWS e estrutura a proposta de valor Dadosfera."
            ),
            AgentCombo(
                partner_agent="cart-recovery-insights",
                combo_name="Síntese de Ação Prescritiva",
                workflow_description="Transforma os outputs dos modelos de propensão em regras acionáveis no copiloto de resgate."
            )
        ),
        system_prompt_excerpt="""# Data Strategy Analyst Skill
## Missão
Consultor Sênior de Dados da plataforma Dadosfera.
Gera camada analítica completa (descritiva, diagnóstica, preditiva e prescritiva), métricas de negócio e aplicações GenAI.""",
        full_system_prompt="""---
name: data-strategy-analyst
description: Consultor Sênior de Dados da plataforma Dadosfera responsável pela estratégia analítica em 4 camadas e aplicações de Machine Learning e GenAI.
tools:
  - view_file
  - list_dir
  - grep_search
  - write_to_file
mode: specialist
---

# 01 — ROLE & IDENTIDADE
Você é o Data Strategy Analyst (Senior Consultant), estrategista de dados e inteligência preditiva.

# 02 — MISSÃO
Conectar a infraestrutura do Lakehouse a casos de uso de alto impacto de Machine Learning (Propensão de Compra) e IA Generativa (Copiloto Prescritivo de Resgate).""",
        file_path=".agents/agents/data-strategy-analyst.md",
        sample_queries=(
            "Como o framework de 4 camadas analíticas é aplicado no case de carrinho abandonado?",
            "Como o modelo de Machine Learning de propensão classifica os clientes?",
            "Como a Dadosfera substitui a complexidade de 5 serviços não gerenciados da AWS?"
        )
    ),

    # 09. DATAMAKER
    AgentProfile(
        slot_number="09",
        agent_id="datamaker",
        display_name="DataMaker",
        arcade_title="SYNTHETIC WORLD BUILDER",
        archetype="Synthetic World Builder",
        category="02_lakehouse_engineering",
        avatar_emoji="🎲",
        card_color_hex="#0F172A",
        accent_color_hex="#EA580C",
        mode="Specialist",
        soundbite='"115k+ registros sintéticos realistas gerados em segundos com anomalias controladas."',
        mission="Arquiteto de modelagem lógica e gerador sintético de alta fidelidade. Desenvolveu o motor declarativo em DAG com dirty data determinístico (e-mails nulos, frete negativo, totais inconsistentes) e distribuições fracionárias naturais (DEC-007).",
        role_in_case="Constrói o universo de dados sintéticos do case: 115.777 registros em 7 entidades interconectadas com integridade referencial em cascata. Injeta cotas matemáticas controladas de dirty data para desafiar o pipeline de Data Quality.",
        case_items_covered=(
            "Item 1: Base Sintética (115.777 registros)",
            "Item 4: Dirty Data Determinístico para Data Quality",
            "Item 6: Modelagem Lógica Canônica das 7 Entidades"
        ),
        skills_equipped=(
            "datamaker",
            "declarative-functional-coding",
            "data-autocleaning"
        ),
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file", "run_command"),
        artifacts_managed=(
            "data/mock/generator.py",
            "data/mock/output_cleaned/parquet/",
            "data/mock/schemas/canonical_models.py",
            ".agents/skills/datamaker/SKILL.md"
        ),
        direct_output=(
            "115.777+ Parquet & CSV rows",
            "7 Canonical entities DAG",
            "Deterministic anomaly injection (1.439 dirty records)",
            "Dev/Std/Rich profiles"
        ),
        constraints=(
            "DEC-007 DETERMINISTIC ANOMALY ENGINE",
            "CASCADING REFERENTIAL INTEGRITY",
            "3-PROFILE GENERATION SUPPORT (DEV, STD, RICH)"
        ),
        power_stats=AgentPowerStats(
            autonomy=97,
            analytical_rigor=98,
            execution_speed=99,
            platform_mastery=93,
            data_quality=97
        ),
        special_moves=(
            SpecialMove(
                name="Deterministic Anomaly Cascade",
                input_command="hcf + punch",
                description="Injeta cotas matemáticas exatas de falhas de negócio (DEC-007) para testar os pipelines de qualificação.",
                impact_area="Geração de Dados & Testes de Resiliência"
            ),
            SpecialMove(
                name="Cascading DAG Generator",
                input_command="charge d, u + kick",
                description="Executa a geração encadeada com integridade referencial perfeita entre Clientes, Produtos, Carrinhos e Pedidos.",
                impact_area="Integridade Relacional & Performance Parquet"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="data-pipeline-documentation",
                combo_name="Testes de Dirty Data & Quarentena",
                workflow_description="Alimenta a camada Bronze com dirty data para que a Silver Anomaly Quarentena capture 1.439 falhas reais."
            ),
            AgentCombo(
                partner_agent="declarative-functional-coding",
                combo_name="Co-Design de Arquitetura Modular",
                workflow_description="Constrói os geradores em módulos desacoplados com perfis dev (12k), standard (116k) e rich (160k)."
            )
        ),
        system_prompt_excerpt="""# DataMaker Skill
## Missão
Cria modelos de dados, schemas lógicos e scripts Python para gerar datasets sintéticos realistas que representem o domínio de e-commerce com dirty data determinístico.""",
        full_system_prompt="""---
name: datamaker
description: Especialista em modelagem de dados, esquemas relacionais e geração de datasets sintéticos em alta volumetria.
tools:
  - view_file
  - list_dir
  - grep_search
  - write_to_file
  - run_command
mode: specialist
---

# 01 — ROLE & IDENTIDADE
Você é o DataMaker (Synthetic World Builder), engenheiro de modelagem e motor de geração sintética de dados.

# 02 — MISSÃO
Gerar datasets sintéticos ultra-realistas com mais de 100k registros (Item 1), preservando correlações estatísticas reais de e-commerce e injetando anomalias determinísticas (DEC-007).""",
        file_path=".agents/agents/datamaker.md",
        sample_queries=(
            "Como funciona o motor AnomalyEngine e quais são as 8 anomalias injetadas?",
            "Qual a volumetria gerada nos 3 perfis (dev, standard, rich)?",
            "Como foi garantida a integridade referencial em cascata no DAG de geração?"
        )
    ),

    # 10. SCOUT
    AgentProfile(
        slot_number="10",
        agent_id="scout",
        display_name="Scout",
        arcade_title="CODE EXPLORER",
        archetype="Code Explorer",
        category="02_lakehouse_engineering",
        avatar_emoji="🔭",
        card_color_hex="#0F172A",
        accent_color_hex="#64748B",
        mode="Specialist",
        soundbite='"Mapeamento profundo de arquivos, dependências e árvores de decisão."',
        mission="Explorador e cartógrafo de código. Mapeia a estrutura do repositório, identifica gaps arquiteturais e rastreia fluxos de dependência entre módulos antes de qualquer alteração.",
        role_in_case="Realiza varreduras rápidas no repositório para inspecionar diretórios, localizar dependências e auditar a conformidade de schemas antes de modificações. Garante que novos módulos não quebrem fluxos existentes.",
        case_items_covered=(
            "Item 0: Mapeamento de Diretórios",
            "Item 6: Gap Analysis Canônico",
            "Item 8: Auditoria de Estrutura do Lakehouse"
        ),
        skills_equipped=(
            "scout",
            "discovering-gcp-data-assets"
        ),
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=(
            ".agents/skills/scout/SKILL.md",
            "tools/repo_indexer.py"
        ),
        direct_output=(
            "Repository directory tree index",
            "Module dependency map",
            "Canonical schema gap radar",
            "Fast artifact locators"
        ),
        constraints=(
            "READ-ONLY AST PARSING",
            "HIGH-SPEED REPO SCAN (<1s)",
            "NO SIDE-EFFECT MUTATIONS"
        ),
        power_stats=AgentPowerStats(
            autonomy=94,
            analytical_rigor=95,
            execution_speed=100,
            platform_mastery=90,
            data_quality=93
        ),
        special_moves=(
            SpecialMove(
                name="Deep AST & Directory Scan",
                input_command="qcf + punch",
                description="Varre recursivamente todo o repositório construindo a árvore de dependências e linhagem de arquivos em <1s.",
                impact_area="Exploração de Código & Diagnóstico Rápido"
            ),
            SpecialMove(
                name="Canonical Gap Radar",
                input_command="hcf + kick",
                description="Detecta divergências entre schemas canônicos e implementações físicas no Lakehouse.",
                impact_area="Auditoria de Conformidade & Qualidade"
            )
        ),
        synergies=(
            AgentCombo(
                partner_agent="project-context-specialist",
                combo_name="Sincronização de Mapa do Repositório",
                workflow_description="Alimenta a memória viva do projeto com a estrutura física exata de pastas e arquivos atualizados."
            ),
            AgentCombo(
                partner_agent="case-context-specialist",
                combo_name="Suporte à Verificação de Escopo",
                workflow_description="Localiza arquivos-chave e evidências solicitadas pelos requisitos do case oficial."
            )
        ),
        system_prompt_excerpt="""# Scout Skill
## Missão
Explora, mapeia e analisa a estrutura do repositório antes de propor ou aplicar alterações.""",
        full_system_prompt="""---
name: scout
description: Especialista em exploração e análise de repositório, mapeamento de dependências e gap analysis.
tools:
  - view_file
  - list_dir
  - grep_search
mode: specialist
---

# 01 — ROLE & IDENTIDADE
Você é o Scout (Code Explorer), o batedor de código e cartógrafo do repositório.

# 02 — MISSÃO
Explorar rapidamente a estrutura de diretórios, dependências e padrões de implementação antes de qualquer modificação, prevenindo regressões.""",
        file_path=".agents/agents/scout.md",
        sample_queries=(
            "Como está organizada a árvore de diretórios do projeto wheels?",
            "Onde estão salvos os Parquets higienizados e os notebooks executáveis?",
            "Como é feita a importação relativa prioritária do ROOT_DIR no app.py?"
        )
    ),
)

_AGENTS_MAP: Final[Mapping[str, AgentProfile]] = MappingProxyType({
    agent.agent_id: agent for agent in _AGENTS_DATA
})


# =============================================================================
# 🧠 CATÁLOGO IMUTÁVEL DAS 10 SKILLS DO ECOSSISTEMA DADOSFERA
# =============================================================================

_SKILLS_DATA: Final[tuple[SkillProfile, ...]] = (
    SkillProfile(
        skill_id="case-context-specialist",
        display_name="Case Context Specialist",
        archetype="Master Strategist",
        category="01_strategy_governance",
        avatar_emoji="👑",
        file_path=".agents/skills/case-context-specialist/SKILL.md",
        description="Fonte central de contexto estratégico, requisitos e direção geral do case técnico de estágio na Dadosfera.",
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=("specs-internship.txt", "relatorios/decision-making/DEC-001.md"),
        constraints=("READ-ONLY", "GROUND TRUTH REQUIRED", "DEC-001 ANCHORED"),
        case_items_covered=("Item 0", "Item 1", "Item 3", "Item 4", "Item 6", "Item 7", "Item 10")
    ),
    SkillProfile(
        skill_id="project-context-specialist",
        display_name="Project Context Specialist",
        archetype="Repository Architect",
        category="01_strategy_governance",
        avatar_emoji="🧠",
        file_path=".agents/skills/project-context-specialist/SKILL.md",
        description="Fonte central de contexto, progresso e memória do case de Recuperação de Carrinho Abandonado.",
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=("README.md", "relatorios/decision-making/DEC-008.md"),
        constraints=("READ-ONLY", "STRICT REPOSITORY MEMORY", "ZERO LOCAL SQL"),
        case_items_covered=("Item 0", "Item 1", "Item 3", "Item 4", "Item 6", "Item 7", "Item 8")
    ),
    SkillProfile(
        skill_id="cart-recovery-insights",
        display_name="Cart Recovery Insights",
        archetype="Analytics Mastermind",
        category="03_analytics_insights",
        avatar_emoji="📊",
        file_path=".agents/skills/cart-recovery-insights/SKILL.md",
        description="Define e organiza especificações canônicas de insights analíticos em Markdown (Descritiva, Risco, Prescritiva e Oportunidade).",
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file"),
        artifacts_managed=("insights/01_descriptive/", "insights/02_risk/", "insights/03_prescriptive/", "insights/04_opportunity/"),
        constraints=("DEC-003 BLUEPRINT SPEC", "MARGIN PRESERVATION >= 28.5%"),
        case_items_covered=("Item 7", "Item 9", "Item 10.1")
    ),
    SkillProfile(
        skill_id="platform-registry-consultant",
        display_name="Platform Registry Consultant",
        archetype="Platform Guardian",
        category="01_strategy_governance",
        avatar_emoji="🏛️",
        file_path=".agents/skills/platform-registry-consultant/SKILL.md",
        description="Guardião do registro de ativos, metadados e mapeamentos da API Maestro da plataforma Dadosfera.",
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file"),
        artifacts_managed=("output-mappers/assets_registry.md", "output-mappers/urls_registry.md"),
        constraints=("DEC-005 NO BEARER TOKEN", "UNIQUE ASSET ID ENFORCEMENT"),
        case_items_covered=("Item 2.1", "Item 3", "Item 8")
    ),
    SkillProfile(
        skill_id="data-pipeline-documentation",
        display_name="Data Pipeline Documentation",
        archetype="Lineage Chronicler",
        category="02_lakehouse_engineering",
        avatar_emoji="📜",
        file_path=".agents/skills/data-pipeline-documentation/SKILL.md",
        description="Documentação, catálogo e linhagem de pipelines Medallion (Bronze -> Silver -> Gold) com Data Contracts e Great Expectations.",
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file"),
        artifacts_managed=("pipelines/case-item-04/data_quality_report.md", "pipelines/datalakes/medallion.md"),
        constraints=("DEC-006 PLATFORM VS DOMAIN SEPARATION", "STRICT MEDALLION LINEAGE"),
        case_items_covered=("Item 4", "Item 6", "Item 8")
    ),
    SkillProfile(
        skill_id="declarative-functional-coding",
        display_name="Declarative Functional Coding",
        archetype="Pure Logic Sage",
        category="02_lakehouse_engineering",
        avatar_emoji="⚡",
        file_path=".agents/skills/declarative-functional-coding/SKILL.md",
        description="Geração de código funcional e declarativo, tipagem estrita Python 3.10+ e arquitetura modular desacoplada.",
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file", "run_command"),
        artifacts_managed=("app/types/models.py", "app/services/simulation_service.py", "make.py"),
        constraints=("PURE FUNCTIONS", "FROZEN DATACLASSES", "STRICT TYPE ANNOTATIONS"),
        case_items_covered=("Item 1", "Item 7", "Item 9")
    ),
    SkillProfile(
        skill_id="charts-maker",
        display_name="Charts Maker",
        archetype="Visual Virtuoso",
        category="03_analytics_insights",
        avatar_emoji="📈",
        file_path=".agents/skills/charts-maker/SKILL.md",
        description="Geração de visualizações executivas e mini cards analíticos com rigor absoluto de Ground Truth e padrão White Theme.",
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file", "run_command"),
        artifacts_managed=("presentation/pitch/roteiro/view-final/generate_chart.py", "dashboards/charts/"),
        constraints=("100% GROUND TRUTH", "WHITE THEME (#FFFFFF)", "300 DPI EXPORT"),
        case_items_covered=("Item 7", "Item 10", "Item 10.1")
    ),
    SkillProfile(
        skill_id="data-strategy-analyst",
        display_name="Data Strategy Analyst",
        archetype="Senior Consultant",
        category="03_analytics_insights",
        avatar_emoji="🎯",
        file_path=".agents/skills/data-strategy-analyst/SKILL.md",
        description="Trilha analítica completa em 4 dimensões (Descritiva a Prescritiva), métricas de negócio e aplicações GenAI com LLMs.",
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file"),
        artifacts_managed=("relatorios/decision-making/DEC-002.md", "pipelines/case-item-05/genai_copilot.py"),
        constraints=("4-TIER ANALYTICAL RIGOR", "BUSINESS ROI JUSTIFICATION", "STRUCTURED PYDANTIC OUTPUT"),
        case_items_covered=("Item 5", "Item 7", "Item 8", "Item 9")
    ),
    SkillProfile(
        skill_id="datamaker",
        display_name="DataMaker",
        archetype="Synthetic World Builder",
        category="02_lakehouse_engineering",
        avatar_emoji="🎲",
        file_path=".agents/skills/datamaker/SKILL.md",
        description="Modelagem lógica e geração sintética de alta fidelidade com dirty data determinístico (DEC-007).",
        tools_available=("view_file", "list_dir", "grep_search", "write_to_file", "run_command"),
        artifacts_managed=("data/mock/generator.py", "data/mock/output_cleaned/parquet/"),
        constraints=("DEC-007 DETERMINISTIC ANOMALIES", "CASCADING INTEGRITY", "DEV/STD/RICH PROFILES"),
        case_items_covered=("Item 1", "Item 4", "Item 6")
    ),
    SkillProfile(
        skill_id="scout",
        display_name="Scout",
        archetype="Code Explorer",
        category="02_lakehouse_engineering",
        avatar_emoji="🔭",
        file_path=".agents/skills/scout/SKILL.md",
        description="Exploração rápida do repositório, mapeamento de diretórios e dependências, e gap analysis antes de alterações.",
        tools_available=("view_file", "list_dir", "grep_search"),
        artifacts_managed=(".agents/skills/scout/SKILL.md", "tools/repo_indexer.py"),
        constraints=("READ-ONLY AST PARSING", "HIGH-SPEED SCAN (<1s)", "NO SIDE-EFFECT MUTATIONS"),
        case_items_covered=("Item 0", "Item 6", "Item 8")
    ),
    SkillProfile(
        skill_id="streamlit-master",
        display_name="Streamlit Master",
        archetype="App Architect",
        category="03_analytics_insights",
        avatar_emoji="🧭",
        file_path=".agents/skills/streamlit-master/SKILL.md",
        description="Arquitetura, mapeamento de navegação em 5 camadas, hot-reloading dinâmico, sincronização por query params e design tokens do Streamlit Data App.",
        tools_available=("view_file", "list_dir", "grep_search", "replace_file_content", "write_to_file", "run_command"),
        artifacts_managed=("app/app.py", "app/views/", "app/components/", ".agents/skills/streamlit-master/SKILL.md"),
        constraints=("5-LAYER ARCHITECTURE", "ZERO-TOP VIEWPORT", "HOT-RELOAD SUBMODULES"),
        case_items_covered=("Item 9", "Item 7", "Item 10.1")
    ),
)

_SKILLS_MAP: Final[Mapping[str, SkillProfile]] = MappingProxyType({
    skill.skill_id: skill for skill in _SKILLS_DATA
})


# =============================================================================
# 🚀 FUNÇÕES PURAS DE ACESSO E CONSULTA
# =============================================================================

def get_all_agents() -> tuple[AgentProfile, ...]:
    """Retorna a tupla imutável com todos os 10 perfis de agentes do ecossistema."""
    return _AGENTS_DATA


def get_agent_by_id(agent_id: str) -> AgentProfile | None:
    """Busca um perfil de agente pelo identificador único (ou None se inexistente)."""
    return _AGENTS_MAP.get(agent_id)


def get_all_skills() -> tuple[SkillProfile, ...]:
    """Retorna a tupla imutável com todas as 10 skills do ecossistema."""
    return _SKILLS_DATA


def get_skill_by_id(skill_id: str) -> SkillProfile | None:
    """Busca um perfil de skill pelo identificador único (ou None se inexistente)."""
    return _SKILLS_MAP.get(skill_id)


def simulate_agent_response(agent_id: str, query: str) -> str:
    """Simulador de despacho funcional para demonstrar a resposta do agente na arena interativa."""
    agent = get_agent_by_id(agent_id)
    if not agent:
        return "Agente não encontrado no catálogo."

    responses: dict[str, dict[str, str]] = {
        "case-context-specialist": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), garanto que esta decisão está 100% ancorada nos requisitos de `specs-internship.txt` e nas decisões consolidadas (como DEC-001 de métricas em % e DEC-008 do Kimball Star Schema). Nosso target é a escala **Outlier**.",
            "criterios": "Para atingir a escala **Outlier**, o projeto não apenas cumpre os 11 itens essenciais (base 100k+, Data Quality, Modelagem Kimball, Dashboards e Pitch), mas extrapola com: (1) Arquitetura em 5 camadas no Streamlit, (2) Busca vetorial 2D com trajetórias, (3) Módulo Multimodal de voz Whisper, (4) Roster autônomo de agentes e (5) Quarentena formal de anomalias com Great Expectations.",
            "dec-001": "A **DEC-001** estabeleceu que todo o pitch de vendas e KPIs analíticos são ancorados em **taxas, ratios e eficiência percentual** (ex.: ~70% abandono, ~10% recuperação, 28.5% margem preservada, ROI 45x). Isso garante transferibilidade para qualquer ticket médio e máxima credibilidade executiva.",
            "problema": "O problema de negócio central é a **Recuperação de Carrinho Abandonado em E-commerce**. Escolhemos esse tema porque: (1) Demonstração direta de ROI e receita recuperada, (2) Permite cobrir todo o ciclo de vida da Dadosfera (Integrar -> GenAI), (3) Fácil visualização executiva por C-Levels."
        },
        "project-context-specialist": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), informo que todos os artefatos estão persistidos e auditáveis no repositório. O status técnico atual conta com 100% dos módulos de modelagem, data quality, visualizações em 300 DPI e Data App concluídos.",
            "estado": "Status técnico consolidado dos 11 itens:\n- **Itens 0, 1, 3, 4, 5, 6, 7, 8, 10, 10.1**: Concluídos com 115.777 linhas geradas, 18 regras Great Expectations, Kimball Star Schema e infraestrutura completa de pitch.\n- **Item 9 & Bônus**: Data App Streamlit em 5 camadas com 4 abas de consumo de BI e Central do Avaliador com Roster de Agentes.",
            "kimball": "A camada Gold (DEC-008) adota o **Kimball Star Schema** com 6 dimensões conformadas (`dim_clientes`, `dim_tempo`, `dim_dispositivo`, `dim_motivo_abandono`, `dim_canal_resgate`, `dim_segmento_rfm`) e 2 tabelas de fatos granulares (`fato_abandono` com 6.525 linhas e `fato_resgate` com 6.289 linhas) com chaves surrogate `_sk`.",
            "quality": "Os artefatos de Data Quality do Item 4 estão organizados em `pipelines/case-item-04/`: notebook executável `qualification_raw.ipynb`, spec normativa `specs.md`, suite `carrinhos_suite.json` e relatório `data_quality_report.md` com bifurcação Silver Qualify vs Silver Anomaly."
        },
        "cart-recovery-insights": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), especifico que a análise de recuperação deve priorizar o canal de menor CAC unitário (E-mail a R$ 1,02 e WhatsApp VIP a R$ 12,00) preservando a margem de 28.5% sem queima de cupom.",
            "quadrantes": "Os 4 quadrantes canônicos de insights em `insights/` são:\n1. **01_descriptive**: Volume de carrinhos, receita represada e evolução temporal.\n2. **02_risk**: Motivos de atrito no checkout e segmentação de risco por RFM.\n3. **03_prescriptive**: Estratégia de canal ótimo e decaimento temporal de resgate.\n4. **04_opportunity**: Otimização de margem líquida e cross-sell sem cupom.",
            "margem": "A **Estratégia de Preservação de Margem** substitui o desconto agressivo de 20% (que queima R$ 779,80) por uma abordagem consultiva baseada em IA e produto alternativo similar (Aba 2). O resultado é uma margem bruta preservada de **28.5%** e ROI multiplicador de até **45x**.",
            "timing": "A curva de decaimento temporal (`03_prescriptive/02_otimizacao_timing_envio`) comprova que o ponto ótimo de conversão é nos **primeiros 60 minutos** (+1h). Disparos tardios (>24h) sofrem queda de 68% na taxa de conversão."
        },
        "platform-registry-consultant": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), todos os 7 Data Assets principais estão sincronizados com seus respectivos UUIDs no catálogo Maestro da Dadosfera em `output-mappers/assets_registry.md`.",
            "assets_registry": "O `assets_registry.md` registra os 7 Data Assets oficiais:\n1. `TB_PRODUTOS` (Catálogo)\n2. `TB_CLIENTES` (Segmentação RFM)\n3. `TB_CARRINHOS` (Eventos de Abandono)\n4. `TB_ITENS_CARRINHO` (Granularidade)\n5. `TB_RESGATE` (Campanhas Executadas)\n6. `TB_PEDIDOS` (Conversões)\n7. `TB_METRICAS_EXPERIMENTO` (A/B Test).",
            "dec-005": "A **DEC-005** documenta que a API Maestro da Dadosfera requer autenticação JWT enviando o token puro no cabeçalho `Authorization: <token>`, sem o prefixo `Bearer`, prevenindo rejeições HTTP 401.",
            "duplicatas": "Para as duplicatas geradas durante testes, foi acionado o **Protocolo de Quarentena de Duplicatas**, renomeando programaticamente os ativos obsoletos para `[DUPLICATA - IGNORAR]` e mantendo os Data Asset IDs canônicos isolados."
        },
        "data-pipeline-documentation": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), garanto a integridade da esteira Medallion com Data Contracts formais e 18 testes Great Expectations com conformidade de 94.2%.",
            "camadas": "A arquitetura de 4 camadas do Lakehouse compreende:\n1. **Bronze (Raw)**: Ingestão pura dos 7 datasets em Parquet/CSV.\n2. **Silver Qualify**: Dados higienizados e aprovados nas 18 regras de Data Quality.\n3. **Silver Anomaly**: Quarentena de 1.439 registros com dirty data para auditoria contábil.\n4. **Gold Curated**: Kimball Star Schema com 6 dimensões e 2 fatos granulares.",
            "regras": "As 18 regras de Data Quality cobrem: não-nulidade de IDs, e-mails com regex válido, frete estritamente positivo (>= 0), integridade de chaves estrangeiras entre carrinhos e produtos, e consistência de somatório de itens.",
            "dec-006": "A **DEC-006** estabelece a separação clara de responsabilidades: a plataforma Dadosfera responde pela infraestrutura de ingestão e tolerância a falhas, enquanto as regras de negócio de qualidade e quarentena são de governança do Domínio de Analytics."
        },
        "declarative-functional-coding": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), todo o ecossistema é construído com funções puras sem mutações ocultas, dataclasses frozen imutáveis e tipagem estrita do Python 3.10+.",
            "arquitetura": "A arquitetura em 5 camadas do Streamlit se inspira no padrão React + TypeScript:\n- `app/types/`: Contratos e tipagem estrita (`models.py`).\n- `app/constants/`: Constantes imutáveis (`MappingProxyType`).\n- `app/services/`: Lógica de negócio e funções puras de simulação.\n- `app/components/`: Componentes visuais desacoplados reutilizáveis.\n- `app/views/`: Telas e orquestração de abas.",
            "funcional": "Pipelines como composições de tuplas de Callables (`pipe(data, f1, f2, f3)`) garantem que cada etapa seja um teste unitário puro, sem dependência de estado global ou mutações de memória.",
            "imutabilidade": "O uso de `dataclass(frozen=True)` e `MappingProxyType` impede mutações acidentais de parâmetros em tempo de execução, garantindo que simulações financeiras sejam 100% determinísticas."
        },
        "charts-maker": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), garanto que 100% dos dados plotados vêm diretamente dos Parquets persistidos (`data/mock/output_cleaned/parquet/`), sem nenhum multiplicador artificial ou dado inventado, com fundo branco puro (#FFFFFF) e 300 DPI.",
            "pilares": "Os 4 pilares do padrão **charts-maker standard** são:\n1. **Ground Truth**: Zero dados falsificados ou multiplicadores manuais.\n2. **White Theme**: Canvas branco puro `#FFFFFF`, eixos limpos e grid sutil `#CBD5E1`.\n3. **Paleta Semântica**: Azul (orgânico), Verde (recuperado), Vermelho (atrito/abandono), Âmbar (SMS/alerta) e Roxo (IA/VIP).\n4. **Exportação Executiva**: 300 DPI, `bbox_inches='tight'` e anotações diretas em duas linhas.",
            "proibicao": "A proibição de multiplicadores arbitrários (como `abandono * 0.45`) é inegociável. Cada barra, vértice e área sombreada reflete exatamente os agrupamentos calculados do dataset real em Parquet.",
            "paleta": "A paleta de cores semântica transmite o significado do negócio instantaneamente: `#2563EB` (tráfego base e conversão), `#059669` (resgate Dadosfera e margem líquida), `#E11D48` (abandono e custo de canal) e `#7C3AED` (IA e clientes Champions)."
        },
        "data-strategy-analyst": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), estruturo a camada analítica completa de 4 níveis (Descritiva a Prescritiva) e a substituição da complexidade legada AWS pela Dadosfera.",
            "framework": "O framework de 4 camadas analíticas aplica:\n1. **Descritiva**: R$ 2,61M em receita abandonada e taxa de 69.8%.\n2. **Diagnóstica**: Frete abusivo responde por 38.4% do abandono.\n3. **Preditiva**: Modelo de propensão XGBoost com AUC 0.892.\n4. **Prescritiva**: Copiloto GenAI com copies personalizadas e recomendação de produtos.",
            "ml": "O modelo supervisionado de propensão utiliza 14 features comportamentais (frequência de compras, tempo no checkout, sensibilidade a preço e score RFM) para classificar os carrinhos em 3 tiers de resgate: Alta, Média e Baixa propensão.",
            "aws": "A plataforma Dadosfera substitui 5 serviços fragmentados da AWS (S3, Glue, Athena, SageMaker e QuickSight) por uma interface SaaS unificada, reduzindo a latência operacional em 65% e o custo de manutenção em 42%."
        },
        "datamaker": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), desenvolvi o motor sintético em DAG que gerou 115.777 registros com integridade referencial perfeita e 1.439 dirty data controlados.",
            "anomalyengine": "O **AnomalyEngine** injeta 8 classes determinísticas de dirty data (DEC-007): e-mails nulos (3.2%), fretes negativos (1.1%), preços zero (0.8%), descontos >100% (0.5%), CEPs inválidos (2.4%), timestamps futuros (0.4%), duplicidade de carrinho (1.2%) e divergência de total (1.5%).",
            "volumetria": "Os 3 perfis suportados pelo motor são:\n- **Dev**: 12.000 registros para testes rápidos de CI/CD.\n- **Standard (Oficial)**: 115.777 registros cobrindo o requisito de >100k do Item 1.\n- **Rich**: 160.000 registros para testes de estresse de escala.",
            "integridade": "A integridade referencial em cascata é assegurada pelo gerador em grafo acíclico direcionado (DAG): primeiro Clientes e Produtos, depois Carrinhos e Itens, e por fim Resgates e Pedidos."
        },
        "scout": {
            "default": f"Como **{agent.display_name}** ({agent.arcade_title}), mapeio o repositório em menos de 1 segundo, rastreando dependências e garantindo zero gaps arquiteturais.",
            "arvore": "A árvore física do repositório organiza:\n- `data/`: Mock e Parquets higienizados.\n- `pipelines/`: Ingestão, qualificação e Lakehouse.\n- `insights/`: Especificações canônicas dos 4 quadrantes.\n- `dashboards/`: Scripts de visualizações em 300 DPI.\n- `app/`: Aplicação Streamlit modular em 5 camadas.\n- `.agents/`: Agentes, regras e skills.",
            "parquets": "Os Parquets oficiais estão persistidos em `data/mock/output_cleaned/parquet/` e os notebooks executáveis em `pipelines/case-item-04/` e `pipelines/case-item-05/`.",
            "importacao": "A importação relativa no `app.py` resolve o `ROOT_DIR` no topo do arquivo inserindo-o na posição 0 de `sys.path`, garantindo compatibilidade total tanto com execução via `streamlit run app/app.py` quanto via `python make.py data-app`."
        }
    }

    agent_dict = responses.get(agent_id, {})
    query_lower = query.lower()

    for key, text in agent_dict.items():
        if key != "default" and key in query_lower:
            return text

    return agent_dict.get("default", f"Como **{agent.display_name}** ({agent.arcade_title}), estou pronto para executar minhas diretrizes operacionais no case Dadosfera. Especialidade: {agent.mission}")
