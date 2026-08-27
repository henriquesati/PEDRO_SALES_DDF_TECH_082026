"""View da Landing Page Inicial: Split-Screen 100% Nativo Edge-to-Edge (Borda a Borda 100vh x 100vw).

- Links Âncoras 100% Nativos com redirecionamento instantâneo via Query Params (?nav=management / ?nav=business).
- Efeito Hover 3D de "desprender e inchar pra frente" puro e ultra-fluido em CSS.
- Título "Dadosfera Solutions" centralizado no topo sobre a linha divisória.
"""

import textwrap
import streamlit as st

HTML_HUB_SPLIT = textwrap.dedent("""
<div class="hub-floating-brand">
<span class="dadosfera-brand-shine">Dadosfera</span>
<span class="solutions-brand-text">&nbsp;Solutions</span>
</div>

<div class="split-screen-container">
<a href="?nav=management" target="_self" class="split-portal-left">
<div class="portal-inner-container">
<span class="portal-badge-left">ORQUESTRAÇÃO MULTI-AGENTE</span>
<div class="portal-title-left">🥋 Central de Agentes & Gestão</div>
<div class="portal-desc-left">Console de Engenharia Multi-Agente com 10 Agentes especialistas, 10 Skills modulares, documentação técnica de specs e blueprints analíticos executáveis.</div>
<div class="portal-metrics-row">
<div class="portal-metric-card-left">
<div class="metric-num-cyan">10</div>
<div class="metric-label-left">Agentes</div>
</div>
<div class="portal-metric-card-left">
<div class="metric-num-green">10</div>
<div class="metric-label-left">Skills</div>
</div>
<div class="portal-metric-card-left">
<div class="metric-num-amber">10</div>
<div class="metric-label-left">Dossiês</div>
</div>
</div>
<div class="portal-features-box-left">
<div><span class="hl-cyan">🥋 10 Agentes Especialistas:</span> Data Strategy, Data Quality, DW, BI e GenAI</div>
<div><span class="hl-cyan">⚡ 10 Skills Modulares:</span> Diretrizes e regras de negócio padronizadas</div>
<div><span class="hl-cyan">📁 Dossiês Fidedignos:</span> Catálogo de metadados, schemas e contratos de dados</div>
<div><span class="hl-cyan">📐 Specs & Blueprints:</span> Especificações analíticas e artefatos executáveis</div>
</div>
</div>
</a>

<a href="?nav=business" target="_self" class="split-portal-right">
<div class="portal-inner-container">
<span class="portal-badge-right">DADOSFERA LAKEHOUSE &bull; BUSINESS BI</span>
<div class="portal-title-right">🏢 Módulo Executivo de Negócios</div>
<div class="portal-desc-right">Simulação financeira de ROI em tempo real, inteligência semântica de catálogo (t-SNE / PCA), copiloto prescritivo multicanal e vitrine GenAI.</div>
<div class="portal-metrics-row">
<div class="portal-metric-card-right">
<div class="metric-num-emerald">R$ 314.5k</div>
<div class="metric-label-right">Recuperação</div>
</div>
<div class="portal-metric-card-right">
<div class="metric-num-blue">45.2x</div>
<div class="metric-label-right">ROI E-mail</div>
</div>
<div class="portal-metric-card-right">
<div class="metric-num-purple">28.5%</div>
<div class="metric-label-right">Margem</div>
</div>
</div>
<div class="portal-features-box-right">
<div><span class="hl-blue">📊 Simulador Financeiro:</span> Mix prescritivo Dadosfera (85/12/2/1)</div>
<div><span class="hl-blue">🔍 Projeção Vetorial 2D:</span> Busca semântica (t-SNE / PCA) em 300 SKUs</div>
<div><span class="hl-blue">🤖 Copiloto Prescritivo:</span> Resgate CRM com JSON Schema Pydantic</div>
<div><span class="hl-blue">🎙️ Vitrine Comercial:</span> Suporte Multimodal Whisper AI & DALL-E</div>
</div>
</div>
</a>
</div>
""").strip()


def render_hub_landing() -> None:
    """Renderiza a tela plana 100% nativa com hover 3D e clique universal via links âncora."""
    st.markdown(HTML_HUB_SPLIT, unsafe_allow_html=True)
