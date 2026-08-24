"""Serviço puro de geração declarativa de copies persuasivas e apresentações GenAI."""

from typing import Final, Mapping
from types import MappingProxyType
from app.types.models import (
    AbandonmentReason,
    ChannelType,
    GeneratedCopy,
    RFMSegment,
    ShowcasePresentation,
)

PERSUASION_TRIGGERS: Final[Mapping[AbandonmentReason, str]] = MappingProxyType({
    "Frete Abusivo": "Eliminação de Fricção Logística (Frete Grátis / Despacho Imediato)",
    "Preço Elevado": "Ancoragem de Valor & Condição Exclusiva (Cupom Pontual / Parcelamento)",
    "Dúvida Técnica": "Autoridade & Suporte Especializado (Consultoria / Garantia Estendida)",
    "Checkout Complexo": "Facilidade de Pagamento (1-Click Checkout / PIX Imediato)",
    "Indecisão": "Escassez de Estoque & Prova Social (Últimas Unidades Reservadas)",
})

def generate_prescriptive_copy(
    product_title: str,
    price: float,
    segment: RFMSegment,
    reason: AbandonmentReason,
    channel: ChannelType,
    discount_pct: float = 10.0,
) -> GeneratedCopy:
    """Gera uma cópia de resgate altamente personalizada e contextualizada (Função Pura)."""
    trigger = PERSUASION_TRIGGERS.get(reason, "Oportunidade Exclusiva")
    
    if channel == "WhatsApp":
        subject = f"💬 [Dadosfera Resgate] Oportunidade para seu {product_title[:25]}..."
        if reason == "Frete Abusivo":
            body = (
                f"Olá! Vimos que você separou o *{product_title}* e queremos garantir sua melhor experiência. "
                f"Liberamos *FRETE GRÁTIS EXPRESSO* exclusivamente para você finalizar agora!"
            )
            cta = "👉 Clique aqui para resgatar com Frete Grátis: [Link Seguro]"
        elif reason == "Preço Elevado":
            body = (
                f"Olá! Como você é um cliente especial do segmento *{segment}*, "
                f"conseguimos autorização para aplicar *{discount_pct:.0f}% OFF* no *{product_title}*."
            )
            cta = f"👉 Ativar cupom de {discount_pct:.0f}%: [Link com Desconto Aplicado]"
        else:
            body = (
                f"Olá! Seu *{product_title}* ainda está reservado no seu carrinho. "
                f"Ficou alguma dúvida sobre as especificações ou forma de pagamento?"
            )
            cta = "👉 Falar agora com um consultor ou finalizar compra: [Link Direto]"
            
    elif channel == "Email":
        if reason == "Frete Abusivo":
            subject = f"🚚 Frete Grátis Liberado para seu {product_title}!"
            body = (
                f"Prezado(a) cliente,\n\n"
                f"Identificamos que você deixou o item **{product_title}** no seu carrinho de compras.\n"
                f"Sabemos que o custo logístico faz a diferença, por isso removemos a taxa de entrega para o seu endereço.\n\n"
                f"Valor original: R$ {price:,.2f} | Envio: R$ 0,00."
            )
            cta = "Finalizar Pedido com Frete Grátis"
        elif reason == "Preço Elevado":
            subject = f"🎁 Condição VIP: {discount_pct:.0f}% de desconto no seu carrinho"
            body = (
                f"Prezado(a) cliente,\n\n"
                f"Para clientes prioritários do grupo **{segment}**, preparamos uma condição única.\n"
                f"Conclua a compra do seu **{product_title}** hoje e garanta {discount_pct:.0f}% de desconto imediato."
            )
            cta = f"Resgatar com {discount_pct:.0f}% de Desconto"
        else:
            subject = f"⏳ Seu {product_title} está reservado por tempo limitado"
            body = (
                f"Prezado(a) cliente,\n\n"
                f"O item **{product_title}** permanece reservado no seu carrinho.\n"
                f"Nosso time de suporte está à disposição para sanar qualquer dúvida técnica."
            )
            cta = "Ir para o Checkout Seguro"
            
    else:  # SMS / Push
        subject = "📱 Alerta de Carrinho"
        if reason == "Frete Abusivo":
            body = f"Frete Zero liberado para seu {product_title[:20]}! Acesse e garanta entrega expressa."
        elif reason == "Preço Elevado":
            body = f"Cupom {discount_pct:.0f}% OFF ativado para {product_title[:20]}! Válido por 2h."
        else:
            body = f"Seu {product_title[:20]} ainda esta reservado. Finalize agora!"
        cta = "Link: ddf.ai/r/cart"

    return GeneratedCopy(
        channel=channel,
        segment=segment,
        reason=reason,
        subject_or_headline=subject,
        body_text=body,
        call_to_action=cta,
        persuasion_trigger=trigger,
    )

def generate_showcase_presentation(
    product_title: str,
    category: str,
    price: float,
    material: str,
    technical_differential: str,
    target_audience: str = "Consumidores Exigentes & B2B",
) -> ShowcasePresentation:
    """Gera o contrato estruturado da apresentação visual do produto (Item Bônus)."""
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
