"""
Gerador da visualização: Painel Visual do Data App Streamlit & Simulação de ROI com GenAI.
Paradigma funcional e declarativo com tipagem estrita (Type Annotations).
"""

from typing import Final
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

BASE_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
PITCH_DIR: Final[str] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PITCH_DIR not in sys.path:
    sys.path.insert(0, PITCH_DIR)

from config.chart_theme import apply_dadosfera_theme, save_chart_artifact, DADOSFERA_PALETTE

OUTPUT_IMAGE_PATH: Final[str] = os.path.join(
    os.path.dirname(__file__), "chart_08_simulador_roi_data_app.png"
)

def plot_data_app_simulation() -> plt.Figure:
    """Gera visualização da curva de simulação de ROI interativa e módulos de GenAI."""
    apply_dadosfera_theme()
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12.0, 6.5))
    
    # Gráfico 1: Curva de Sensibilidade de ROI por Investimento e Taxa de Recuperação
    taxas_recup = np.linspace(5, 20, 100)  # 5% a 20%
    roi_email = taxas_recup * 4.2          # Multiplicador canal email
    roi_whats = taxas_recup * 2.8          # Multiplicador whatsapp
    roi_sms = taxas_recup * 2.1            # Multiplicador SMS
    
    ax1.plot(taxas_recup, roi_email, color=DADOSFERA_PALETTE.accent_green, linewidth=2.8, label="Canal Email (Baixo Custo / Alto Volume)")
    ax1.plot(taxas_recup, roi_whats, color=DADOSFERA_PALETTE.accent_cyan, linewidth=2.5, label="Canal WhatsApp (Alto Engajamento / VIP)")
    ax1.plot(taxas_recup, roi_sms, color=DADOSFERA_PALETTE.accent_yellow, linewidth=2.2, linestyle="--", label="Canal SMS (Reforço 48h)")
    
    ax1.axvline(10.1, color=DADOSFERA_PALETTE.accent_coral, linestyle=":", label="Taxa Atual do Case (~10.1%)")
    ax1.scatter([10.1], [10.1 * 4.2], color=DADOSFERA_PALETTE.accent_coral, s=90, zorder=5)
    ax1.text(10.5, 43, "Target Atual: 45x ROI", color=DADOSFERA_PALETTE.accent_coral, fontsize=10, fontweight="bold")
    
    ax1.set_xlabel("Taxa de Recuperação Simulada (%)", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax1.set_ylabel("Múltiplo de ROI Esperado", fontsize=11, fontweight="bold", color=DADOSFERA_PALETTE.text_light)
    ax1.set_title("Simulador de Sensibilidade de ROI\n(Painel Interativo Streamlit)", fontsize=13, fontweight="bold", pad=12)
    ax1.legend(loc="upper left", fontsize=9, framealpha=0.9)
    ax1.grid(True, linestyle="--", alpha=0.3)
    
    # Gráfico 2: Painel de GenAI & Personalização de Copy
    ax2.axis("off")
    
    card_text = (
        "MOTOR DE GENAI INTEGRADO (LLMs & Copywriting)\n"
        "-----------------------------------------------------\n\n"
        "[+] Personalizacao Dinamica por Causa-Raiz:\n\n"
        "  * Frete Alto (>15%):\n"
        "    'Ola [Nome], notamos que o frete pesou. Use FRETEOFF!'\n\n"
        "  * Erro no Checkout (Pagamento):\n"
        "    'Tivemos instabilidade no PIX. Seu carrinho esta reservado!'\n\n"
        "  * Indecisao / Premium:\n"
        "    'Mais de 140 clientes compraram este item. Veja reviews!'\n\n"
        "-----------------------------------------------------\n"
        "[*] Beneficios da Camada GenAI Dadosfera:\n"
        "  [OK] Aumento de +18% no CTR (Click-through Rate)\n"
        "  [OK] Vitrine Dinamica de Produtos Resgatados\n"
        "  [OK] Integracao Nativa no Modulo Consumir / Streamlit"
    )
    
    bbox_props = dict(boxstyle="round,pad=1.0", facecolor=DADOSFERA_PALETTE.secondary_dark, edgecolor=DADOSFERA_PALETTE.accent_purple, linewidth=2)
    ax2.text(0.05, 0.5, card_text, transform=ax2.transAxes, fontsize=10.5, color=DADOSFERA_PALETTE.text_light, va="center", bbox=bbox_props, family="monospace")
    ax2.set_title("Inteligência Generativa Aplicada ao Resgate\n(Case Bônus & Personalização Semântica)", fontsize=13, fontweight="bold", pad=12)
    
    plt.suptitle("Data App & GenAI: O Futuro da Recuperação no Marketplace", fontsize=15, fontweight="bold", y=0.98)
    plt.tight_layout()
    
    return fig

def main() -> None:
    fig = plot_data_app_simulation()
    saved_path = save_chart_artifact(fig, OUTPUT_IMAGE_PATH)
    print(f"[SUCCESS] Gráfico gerado em: {saved_path}")

if __name__ == "__main__":
    main()
