"""Serviço funcional de geração declarativa de copies persuasivas e apresentações GenAI (Dispatch Pattern)."""

import json
from types import MappingProxyType
from typing import Callable, Final, Mapping, Tuple
from app.types.models import (
    AbandonmentReason,
    ChannelType,
    GeneratedCopy,
    RFMSegment,
    ShowcasePresentation,
    VoiceTone,
)

PERSUASION_TRIGGERS: Final[Mapping[AbandonmentReason, str]] = MappingProxyType({
    "Frete Abusivo": "Eliminação de Fricção Logística (Frete Grátis / Despacho Imediato)",
    "Preço Elevado": "Ancoragem de Valor & Condição Exclusiva (Cupom Pontual / Parcelamento)",
    "Dúvida Técnica": "Autoridade & Suporte Especializado (Consultoria / Garantia Estendida)",
    "Checkout Complexo": "Facilidade de Pagamento (1-Click Checkout / PIX Imediato)",
    "Indecisão": "Escassez de Estoque & Prova Social (Últimas Unidades Reservadas)",
})

# Type alias para o gerador de template funcional: (title, price, segment, reason, discount) -> (subject, body, cta)
CopyGeneratorFn = Callable[[str, float, RFMSegment, AbandonmentReason, float], Tuple[str, str, str]]

def _build_wpp_urgency(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"💬 [Dadosfera Concierge] Atendimento VIP para seu {title[:25]}..."
    discount_msg = f"Liberamos *{disc:.0f}% OFF imediato* para você concluir seu pedido agora!" if disc > 0 else "Garantimos o despacho prioritário no mesmo dia!"
    body = (
        f"Olá! Notamos que o item *{title}* está reservado no seu carrinho. "
        f"Devido à alta demanda desta semana, sua reserva expira em *poucas horas*. "
        f"{discount_msg}"
    )
    cta = "👉 Clique aqui para resgatar sua reserva prioritária: [Link Seguro]"
    return subject, body, cta

def _build_wpp_support(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"💬 [Dadosfera Concierge] Atendimento VIP para seu {title[:25]}..."
    body = (
        f"Olá! Sou do time de atendimento ao cliente da Dadosfera. "
        f"Vimos que você selecionou o *{title}* (R$ {price:,.2f}). "
        f"Ficou alguma dúvida sobre compatibilidade, voltagem (127V/220V) ou opções de parcelamento no PIX/Cartão?"
    )
    cta = "👉 Responder agora para falar com consultor técnico ou finalizar pedido: [Link de Ajuda]"
    return subject, body, cta

def _build_wpp_social(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"💬 [Dadosfera Concierge] Atendimento VIP para seu {title[:25]}..."
    body = (
        f"Olá! O *{title}* que você separou é um dos itens mais bem avaliados (4.9 estrelas) do catálogo. "
        f"Mais de 1.200 clientes confirmaram excelente durabilidade e entrega pontual."
    )
    cta = "👉 Veja as avaliações reais e conclua sua compra: [Link Oficial]"
    return subject, body, cta

def _build_email_urgency(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"⏳ Última Chamada: Sua reserva do {title[:30]} expira hoje"
    promo_msg = f"Código promocional de {disc:.0f}% aplicado: **RESGATEVIP**\n\n" if disc > 0 else ""
    body = (
        f"Prezado(a) cliente,\n\n"
        f"Identificamos que você iniciou o checkout do **{title}**.\n"
        f"Para garantir que você não perca esta unidade em estoque, mantivemos suas condições reservadas por tempo limitado.\n\n"
        f"{promo_msg}"
        f"Valor do pedido: R$ {price:,.2f} | Envio com rastreamento em tempo real."
    )
    cta = "Finalizar Pedido com Prioridade"
    return subject, body, cta

def _build_email_support(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"🤝 Suporte Especializado: Dúvidas sobre o {title[:30]}?"
    body = (
        f"Prezado(a) cliente do segmento **{segment}**,\n\n"
        f"Notamos uma pausa no checkout do seu **{title}**.\n"
        f"Nossos especialistas técnicos estão à disposição para esclarecer qualquer dúvida sobre especificações, frete e garantia de fábrica.\n\n"
        f"Valor original: R$ {price:,.2f} | Opções flexíveis em até 12x sem juros."
    )
    cta = "Acessar Suporte Técnico ou Finalizar Compra"
    return subject, body, cta

def _build_email_social(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    subject = f"⭐ O que dizem sobre o {title[:30]}: 98% de aprovação"
    body = (
        f"Prezado(a) cliente,\n\n"
        f"O item **{title}** é a escolha número 1 em sua categoria.\n"
        f"Confira os depoimentos de quem já comprou e comprove a qualidade dos materiais e facilidade de uso."
    )
    cta = "Ver Avaliações e Concluir Pedido"
    return subject, body, cta

def _build_sms_urgency(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    return "📱 Notificação de Checkout", f"Reserva de {title[:20]} expira em breve! Conclua agora com seguranca.", "Link: ddf.ai/r/cart"

def _build_sms_support(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    return "📱 Notificação de Suporte", f"Precisa de ajuda com seu {title[:20]}? Fale com nosso concierge no chat.", "Link: ddf.ai/r/cart"

def _build_sms_social(title: str, price: float, segment: RFMSegment, reason: AbandonmentReason, disc: float) -> Tuple[str, str, str]:
    return "📱 Notificação de Catálogo", f"O {title[:20]} tem 4.9 estrelas! Garanta o seu antes que esgote.", "Link: ddf.ai/r/cart"

# Tabela de Despacho Declarativa Imutável
COPY_DISPATCH_TABLE: Final[Mapping[Tuple[ChannelType, VoiceTone], CopyGeneratorFn]] = MappingProxyType({
    ("WhatsApp", "Urgência"): _build_wpp_urgency,
    ("WhatsApp", "Suporte"): _build_wpp_support,
    ("WhatsApp", "Prova Social"): _build_wpp_social,
    ("Email", "Urgência"): _build_email_urgency,
    ("Email", "Suporte"): _build_email_support,
    ("Email", "Prova Social"): _build_email_social,
    ("SMS", "Urgência"): _build_sms_urgency,
    ("SMS", "Suporte"): _build_sms_support,
    ("SMS", "Prova Social"): _build_sms_social,
    ("Push", "Urgência"): _build_sms_urgency,
    ("Push", "Suporte"): _build_sms_support,
    ("Push", "Prova Social"): _build_sms_social,
})

def generate_prescriptive_copy(
    product_title: str,
    price: float,
    segment: RFMSegment,
    reason: AbandonmentReason,
    channel: ChannelType,
    tone: VoiceTone = "Suporte",
    discount_pct: float = 0.0,
) -> GeneratedCopy:
    """Gera uma cópia de resgate altamente personalizada usando tabela declarativa de despacho."""
    trigger = PERSUASION_TRIGGERS.get(reason, "Oportunidade Exclusiva")
    generator = COPY_DISPATCH_TABLE.get((channel, tone), _build_wpp_support)
    
    subject, body, cta = generator(product_title, price, segment, reason, discount_pct)

    json_payload = json.dumps({
        "customer_segment": segment,
        "product_id_anchor": product_title[:30],
        "friction_reason": reason,
        "voice_tone": tone,
        "channel": channel,
        "discount_offered_pct": discount_pct,
        "persuasion_trigger": trigger,
        "generated_timestamp": "2026-08-25T22:30:00Z",
        "pydantic_schema_version": "v1.2",
    }, indent=2, ensure_ascii=False)

    return GeneratedCopy(
        channel=channel,
        segment=segment,
        reason=reason,
        tone=tone,
        subject_or_headline=subject,
        body_text=body,
        call_to_action=cta,
        persuasion_trigger=trigger,
        json_schema_payload=json_payload,
    )

def generate_showcase_presentation(
    product_title: str,
    category: str,
    price: float,
    material: str,
    technical_differential: str,
    target_audience: str = "Consumidores Exigentes & B2B",
) -> ShowcasePresentation:
    """Gera o contrato estruturado da apresentação visual do produto (Item Bônus GenAI)."""
    return ShowcasePresentation(
        title=f"Apresentação Executiva: {product_title}",
        value_proposition=f"O melhor equilíbrio entre {technical_differential} e acabamento em {material}.",
        key_pillars=(
            f"1. **Engenharia & Materiais:** Confeccionado em {material} de alta durabilidade.\n"
            f"2. **Diferencial Competitivo:** {technical_differential}.\n"
            f"3. **Público-Alvo:** Projetado sob medida para {target_audience}.\n"
            f"4. **Investimento & ROI:** R$ {price:,.2f} com excelente valor residual."
        ),
        visual_prompt_reference=(
            f"High-end commercial studio product photography of {product_title}, "
            f"materials visible ({material}), clean minimalist background with corporate lighting (#1E3A8A accents), "
            f"photorealistic 8k, award-winning e-commerce showcase."
        ),
        sales_pitch_hook=f"Descubra como o {product_title} eleva a sua performance diária com {technical_differential}."
    )
