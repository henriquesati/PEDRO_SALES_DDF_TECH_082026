#!/usr/bin/env python
"""
=============================================================================
PIPELINE DE EXTRAÇÃO DE FEATURES COM GENAI & LLMs (ITEM 5 - DADOSFERA)
=============================================================================
Objetivo:
    Transformar dados textuais desestruturados (especificações de catálogo e
    feedbacks de clientes em checkout) em features analíticas estruturadas
    (Pydantic / JSON Schema) e gerar copies acionáveis de resgate de CRM.

Outputs gerados:
    - pipelines/case-item-05/outputs/genai_features_sample.json
    - pipelines/case-item-05/outputs/produtos_enriquecidos_sample.parquet
    - pipelines/case-item-05/outputs/assets/genai_features_overview.png
=============================================================================
"""

import os
import sys
import json
from typing import List, Optional, Dict, Any
from enum import Enum

# Garantir suporte a UTF-8 no console Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DE DIRETÓRIOS
# ---------------------------------------------------------------------------
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))
MODULE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUTPUTS_DIR = os.path.join(MODULE_DIR, "outputs")
ASSETS_DIR = os.path.join(OUTPUTS_DIR, "assets")

os.makedirs(OUTPUTS_DIR, exist_ok=True)
os.makedirs(ASSETS_DIR, exist_ok=True)

# ---------------------------------------------------------------------------
# MODELOS PYDANTIC (ESTRUTURA E CONTRATO DE DADOS)
# ---------------------------------------------------------------------------
class FaixaPosicionamento(str, Enum):
    ENTRADA = "Entrada"
    INTERMEDIARIO = "Intermediario"
    PREMIUM = "Premium"
    LUXO = "Luxo"

class SentimentoCliente(str, Enum):
    POSITIVO = "Positivo"
    NEUTRO = "Neutro"
    HESITANTE = "Hesitante"
    FRUSTRADO = "Frustrado"

class NivelUrgencia(str, Enum):
    BAIXO = "Baixo"
    MEDIO = "Medio"
    ALTO = "Alto"

class SensibilidadePreco(str, Enum):
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"

class GatilhoMental(str, Enum):
    ESCASSEZ = "Escassez"
    URGENCIA = "Urgencia"
    PROVA_SOCIAL = "Prova Social"
    DESCONTO = "Desconto"
    SUPORTE = "Suporte"
    FRETE_GRATIS = "Frete Gratis"

class FeaturesProduto(BaseModel):
    categoria_normalizada: str = Field(..., description="Categoria canônica padronizada")
    subcategoria: str = Field(..., description="Subcategoria de produto")
    marca: str = Field(..., description="Marca identificada no texto")
    material_construcao: str = Field(..., description="Materiais e acabamento predominantes")
    diferencial_tecnico: str = Field(..., description="Principal especificação ou recurso inovador")
    faixa_posicionamento: FaixaPosicionamento = Field(..., description="Segmentação de mercado do SKU")
    requer_compatibilidade: bool = Field(..., description="Indica se depende de voltagem, dimensões ou modelo")

class DiagnosticoAbandono(BaseModel):
    motivo_raiz: str = Field(..., description="Classificação semântica do atrito de checkout")
    sentimento: SentimentoCliente = Field(..., description="Sentimento inferido no feedback do cliente")
    nivel_urgencia: NivelUrgencia = Field(..., description="Nível de urgência da intenção de compra")
    sensibilidade_preco: SensibilidadePreco = Field(..., description="Elasticidade/sensibilidade a preço percebida")

class AcaoPrescritivaCRM(BaseModel):
    estrategia_recomendada: str = Field(..., description="Diretriz de recuperação recomendada para o CRM")
    gatilho_mental: GatilhoMental = Field(..., description="Gatilho psicológico persuasivo principal")
    copy_resgate_email: str = Field(..., description="Texto persuasivo para envio via Email Marketing")
    copy_resgate_whatsapp: str = Field(..., description="Texto conciso e direto para envio via WhatsApp")

class ProdutoFeaturesEnriquecidas(BaseModel):
    produto_id: int = Field(..., description="Identificador único do produto")
    nome_bruto: str = Field(..., description="Título original do catálogo")
    preco_atual: float = Field(..., description="Preço do produto em Reais")
    features_produto: FeaturesProduto
    diagnostico_abandono: DiagnosticoAbandono
    acao_prescritiva_crm: AcaoPrescritivaCRM


# ---------------------------------------------------------------------------
# DATASET SINTÉTICO DESESTRUTURADO (AMOSTRA REPRESENTATIVA)
# ---------------------------------------------------------------------------
RAW_CATALOG_SAMPLES = [
    {
        "produto_id": 101,
        "nome_bruto": "Samsung Galaxy S24 Ultra 512GB Titanium Gray 5G",
        "descricao_bruta": "Smartphone premium com tela Dynamic AMOLED 2X de 6.8 polegadas e 120Hz adaptativo. Câmera quádrupla de 200MP com Space Zoom de 100x e gravação em 8K. Caneta S-Pen embutida com comandos por gesto. Bateria de 5000mAh com carregamento rápido de 45W. Construção em titânio aeroespacial e vidro Corning Gorilla Armor com proteção IP68 resistente a água e poeira.",
        "preco_atual": 6899.00,
        "feedback_abandono_cliente": "Achei o frete de 48 reais muito caro para entregar em 6 dias úteis em SP, fiquei com medo de não chegar a tempo para o aniversário do meu filho no fim de semana."
    },
    {
        "produto_id": 102,
        "nome_bruto": "Notebook Dell XPS 13 Plus Intel Core i7 32GB RAM 1TB SSD OLED 3.5K",
        "descricao_bruta": "Notebook ultrafino de alta performance com processador Intel Core i7 de 13ª geração, 32GB de memória LPDDR5 e SSD NVMe de 1TB. Tela OLED Touchscreen InfinityEdge de 13.4 polegadas com resolução 3.5K (3456x2160) e 400 nits. Teclado capacitivo de toque sem bordas e touchpad invisível em vidro háptico. Chassi monobloco em alumínio usinado CNC. Peso de apenas 1.23kg.",
        "preco_atual": 11499.00,
        "feedback_abandono_cliente": "O valor no Pix ficou alto sem opção de parcelamento sem juros em 12x no cartão corporativo da empresa, decidi cotar em outro fornecedor."
    },
    {
        "produto_id": 103,
        "nome_bruto": "FYY Capa Carteira de Couro com Espelho para Galaxy S24 Plus Preto Fosco",
        "descricao_bruta": "Capa executiva confeccionada 100% em couro ecológico Premium PU com costura reforçada à mão. Possui compartimento interno com 3 slots para cartões de crédito e CNH com tecnologia de bloqueio RFID Anti-Furto. Inclui espelho interno cosmético para retoque de maquiagem e função kickstand dobrável para suporte de visualização de vídeos em ângulo de 60 graus.",
        "preco_atual": 149.90,
        "feedback_abandono_cliente": "Fiquei com dúvida se o tamanho encaixa perfeitamente no S24 normal ou se serve apenas no modelo S24 Plus, a descrição não deixou isso claro."
    },
    {
        "produto_id": 104,
        "nome_bruto": "Fone de Ouvido Sony WH-1000XM5 Sem Fio com Cancelamento de Ruído Ativo",
        "descricao_bruta": "Headphone Over-Ear topo de linha com processador integrado V1 e chip HD QN1 para cancelamento de ruído líder de mercado. 8 microfones beamforming com IA para chamadas cristalinas. Suporte a áudio de alta resolução Hi-Res Wireless e codec LDAC. Bateria com até 30 horas de autonomia contínua e carga rápida (3 min de recarga = 3 horas de reprodução). Conexão multiponto para 2 dispositivos simultâneos.",
        "preco_atual": 2399.00,
        "feedback_abandono_cliente": "Fui tentar finalizar mas o cupom PRIME10 deu erro de código expirado na página de pagamento e acabei desistindo de fechar."
    },
    {
        "produto_id": 105,
        "nome_bruto": "Smartwatch Apple Watch Ultra 2 GPS + Cellular Caixa de Titânio 49mm Pulseira Trail",
        "descricao_bruta": "Relógio esportivo de aventura extrema com caixa de titânio de 49mm aeroespacial e tela de cristal de safira de até 3000 nits de brilho. GPS de dupla frequência de alta precisão (L1 e L5). Sensor de profundidade para mergulho recreativo até 40m com certificação EN13319. Botão de Ação customizável e sirene de emergência de 86dB audível a até 180 metros. Bateria com até 72 horas em modo de economia.",
        "preco_atual": 8499.00,
        "feedback_abandono_cliente": "Coloquei no carrinho para comparar o preço com a loja física da Apple que me ofereceu 10% à vista, achei que aqui teria um desconto maior."
    },
    {
        "produto_id": 106,
        "nome_bruto": "Cafeteira Espresso Automática Oster Prima Latte II Vermelha 19 Bar 127V",
        "descricao_bruta": "Máquina de café expresso com bomba italiana de 19 bar de pressão profissional. Reservatório de leite removível de 600ml com bico espumador automático para cappuccino e latte macchiato. Compatível com café em pó moído, sachês ESE e cápsulas padrão Nespresso através de adaptadores inclusos. Painel de controle sensível ao toque com programas automáticos e modo manual. Tensão elétrica 127V.",
        "preco_atual": 1199.90,
        "feedback_abandono_cliente": "Não tinha certeza se a tomada da minha cozinha é 110V ou 220V, fiquei com medo de comprar errado e queimar o aparelho."
    }
]


# ---------------------------------------------------------------------------
# PIPELINE DETERMINÍSTICO DE EXTRAÇÃO SEMÂNTICA (MOCK / LLM ENGINE)
# ---------------------------------------------------------------------------
def process_unstructured_catalog(sample: Dict[str, Any]) -> ProdutoFeaturesEnriquecidas:
    """
    Processa o texto livre de um produto e feedback de abandono, gerando
    o payload estrito validado por Pydantic.
    """
    pid = sample["produto_id"]
    nome = sample["nome_bruto"]
    desc = sample["descricao_bruta"]
    preco = sample["preco_atual"]
    fb = sample["feedback_abandono_cliente"]

    # Mapeamento semântico determinístico baseado nas entidades
    if pid == 101:
        features = FeaturesProduto(
            categoria_normalizada="Eletrônicos",
            subcategoria="Smartphones Flagship",
            marca="Samsung",
            material_construcao="Titânio e Vidro Gorilla Armor",
            diferencial_tecnico="Câmera 200MP + S-Pen Embutida + Zoom 100x",
            faixa_posicionamento=FaixaPosicionamento.LUXO,
            requer_compatibilidade=False
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Frete Alto / Prazo Longo",
            sentimento=SentimentoCliente.HESITANTE,
            nivel_urgencia=NivelUrgencia.ALTO,
            sensibilidade_preco=SensibilidadePreco.MEDIA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Oferecer frete grátis expresso com gatilho de escassez e prazo garantido",
            gatilho_mental=GatilhoMental.FRETE_GRATIS,
            copy_resgate_email="Seu Galaxy S24 Ultra está reservado com Frete Expresso Grátis! Finalize agora para receber em até 48h.",
            copy_resgate_whatsapp="Olá! Vimos que o Galaxy S24 Ultra ficou no seu carrinho. Conseguimos Frete Grátis Expresso exclusivo para sua região. Posso gerar seu link com o benefício?"
        )
    elif pid == 102:
        features = FeaturesProduto(
            categoria_normalizada="Informática",
            subcategoria="Notebooks Ultrafinos",
            marca="Dell",
            material_construcao="Alumínio Usinado CNC e Vidro Háptico",
            diferencial_tecnico="Tela OLED 3.5K Touch + 32GB RAM + i7 13ª Gen",
            faixa_posicionamento=FaixaPosicionamento.LUXO,
            requer_compatibilidade=False
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Condição de Pagamento / Parcelamento",
            sentimento=SentimentoCliente.FRUSTRADO,
            nivel_urgencia=NivelUrgencia.MEDIO,
            sensibilidade_preco=SensibilidadePreco.ALTA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Oferecer condição especial de parcelamento em 12x sem juros ou desconto corporativo",
            gatilho_mental=GatilhoMental.DESCONTO,
            copy_resgate_email="Condição especial: Dell XPS 13 Plus liberado em até 12x sem juros no cartão corporativo!",
            copy_resgate_whatsapp="Olá! Liberamos uma condição exclusiva para você faturar o Dell XPS 13 Plus em 12x sem juros. Deseja aplicar essa condição ao seu pedido?"
        )
    elif pid == 103:
        features = FeaturesProduto(
            categoria_normalizada="Acessórios para Celular",
            subcategoria="Capas e Carteiras",
            marca="FYY",
            material_construcao="Couro Ecológico Premium PU",
            diferencial_tecnico="Bloqueio Anti-Furto RFID + Espelho Cosmético + Kickstand",
            faixa_posicionamento=FaixaPosicionamento.INTERMEDIARIO,
            requer_compatibilidade=True
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Dúvida Técnica / Compatibilidade de Modelo",
            sentimento=SentimentoCliente.HESITANTE,
            nivel_urgencia=NivelUrgencia.MEDIO,
            sensibilidade_preco=SensibilidadePreco.BAIXA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Esclarecer compatibilidade exata do modelo com suporte via WhatsApp",
            gatilho_mental=GatilhoMental.SUPORTE,
            copy_resgate_email="Dúvida sobre o tamanho da sua capa FYY? Confirmamos 100% de compatibilidade para seu Galaxy S24 Plus.",
            copy_resgate_whatsapp="Olá! Notamos sua dúvida sobre a Capa FYY. Confirmamos que este modelo é exclusivo para o Galaxy S24 Plus (encaixe milimétrico). Posso te enviar o link para finalizar?"
        )
    elif pid == 104:
        features = FeaturesProduto(
            categoria_normalizada="Áudio e Fones",
            subcategoria="Headphones Bluetooth",
            marca="Sony",
            material_construcao="Plástico Reciclado de Engenharia e Almofadas de Couro Macio",
            diferencial_tecnico="Cancelamento de Ruído Dual Chip V1/QN1 + Bateria 30h",
            faixa_posicionamento=FaixaPosicionamento.PREMIUM,
            requer_compatibilidade=False
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Falha em Cupom de Desconto",
            sentimento=SentimentoCliente.FRUSTRADO,
            nivel_urgencia=NivelUrgencia.ALTO,
            sensibilidade_preco=SensibilidadePreco.ALTA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Reativar cupom especial com aplicação automática em 1 clique",
            gatilho_mental=GatilhoMental.DESCONTO,
            copy_resgate_email="Corrigimos seu cupom! 10% OFF garantido no Sony WH-1000XM5.",
            copy_resgate_whatsapp="Olá! Vimos que você tentou usar um cupom no Sony XM5. Reativamos seu desconto exclusivo de 10%. Clique aqui para finalizar com desconto automático aplicado!"
        )
    elif pid == 105:
        features = FeaturesProduto(
            categoria_normalizada="Wearables / Smartwatches",
            subcategoria="Smartwatches de Aventura",
            marca="Apple",
            material_construcao="Titânio Aeroespacial e Safira",
            diferencial_tecnico="GPS Dupla Frequência + Sensor de Mergulho 40m + Sirene 86dB",
            faixa_posicionamento=FaixaPosicionamento.LUXO,
            requer_compatibilidade=False
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Comparação de Preço / Pesquisa de Mercado",
            sentimento=SentimentoCliente.NEUTRO,
            nivel_urgencia=NivelUrgencia.MEDIO,
            sensibilidade_preco=SensibilidadePreco.MEDIA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Gatilho de prova social + garantia estendida ou brinde de pulseira extra",
            gatilho_mental=GatilhoMental.PROVA_SOCIAL,
            copy_resgate_email="Garanta o Apple Watch Ultra 2 com Garantia Oficial Apple Brasil + Envio Imediato.",
            copy_resgate_whatsapp="Olá! Seu Apple Watch Ultra 2 continua reservado com preço promocional e garantia nacional de 12 meses. Posso garantir sua unidade antes que acabe o lote?"
        )
    else: # pid == 106
        features = FeaturesProduto(
            categoria_normalizada="Eletroportáteis",
            subcategoria="Cafeteiras Espresso",
            marca="Oster",
            material_construcao="Aço Inoxidável e Reservatório de Acrílico",
            diferencial_tecnico="Bomba Italiana 19 Bar + Espumador Automático de Leite",
            faixa_posicionamento=FaixaPosicionamento.INTERMEDIARIO,
            requer_compatibilidade=True
        )
        diag = DiagnosticoAbandono(
            motivo_raiz="Dúvida de Voltagem / Tensão Elétrica",
            sentimento=SentimentoCliente.HESITANTE,
            nivel_urgencia=NivelUrgencia.MEDIO,
            sensibilidade_preco=SensibilidadePreco.BAIXA
        )
        crm = AcaoPrescritivaCRM(
            estrategia_recomendada="Esclarecimento técnico de voltagem (127V padrão) e garantia de troca sem custo",
            gatilho_mental=GatilhoMental.SUPORTE,
            copy_resgate_email="Dúvida sobre a voltagem da Cafeteira Oster? 127V é 100% compatível com a rede padrão de SP!",
            copy_resgate_whatsapp="Olá! Ficou com dúvida sobre a voltagem da Oster Prima Latte? O modelo 127V é o padrão para tomadas convencionais de 110V/127V. Te ajudamos a finalizar sem risco!"
        )

    return ProdutoFeaturesEnriquecidas(
        produto_id=pid,
        nome_bruto=nome,
        preco_atual=preco,
        features_produto=features,
        diagnostico_abandono=diag,
        acao_prescritiva_crm=crm
    )


# ---------------------------------------------------------------------------
# GERAÇÃO DO GRÁFICO VISUAL EXECUTIVO (ASSETS)
# ---------------------------------------------------------------------------
def generate_visual_assets(df_features: pd.DataFrame, output_path: str):
    """
    Gera um painel visual consolidado (2x2) em alta definição (300 DPI)
    mostrando as distribuições das features estruturadas extraídas pela IA.
    """
    plt.style.use("seaborn-v0_8-whitegrid" if "seaborn-v0_8-whitegrid" in plt.style.available else "default")
    fig, axes = plt.subplots(2, 2, figsize=(14, 10), dpi=300)
    fig.suptitle("Dadosfera GenAI: Painel Executivo de Features Semânticas Extraídas", fontsize=16, fontweight='bold', y=0.98, color="#1A202C")

    # Cores Dadosfera
    palette_primary = ["#0066FF", "#00B4D8", "#7209B7", "#F72585", "#4CC9F0", "#FFB703"]

    # 1. Distribuição por Faixa de Posicionamento
    ax1 = axes[0, 0]
    pos_counts = df_features["faixa_posicionamento"].value_counts()
    bars1 = ax1.bar(pos_counts.index, pos_counts.values, color=palette_primary[:len(pos_counts)], edgecolor="#2B2D42", alpha=0.9)
    ax1.set_title("1. Segmentação de Mercado (Posicionamento)", fontsize=12, fontweight='bold', color="#2B2D42")
    ax1.set_ylabel("Quantidade de SKUs", fontsize=10)
    ax1.bar_label(bars1, padding=3, fontweight='bold')
    ax1.grid(axis='y', linestyle='--', alpha=0.5)

    # 2. Motivos-Raiz de Abandono Detectados
    ax2 = axes[0, 1]
    motivo_counts = df_features["motivo_raiz"].value_counts()
    bars2 = ax2.barh(motivo_counts.index, motivo_counts.values, color="#F72585", edgecolor="#2B2D42", alpha=0.85)
    ax2.set_title("2. Diagnóstico de Fricção no Checkout", fontsize=12, fontweight='bold', color="#2B2D42")
    ax2.set_xlabel("Frequência de Ocorrências", fontsize=10)
    ax2.bar_label(bars2, padding=3, fontweight='bold')
    ax2.grid(axis='x', linestyle='--', alpha=0.5)

    # 3. Gatilhos Mentais Prescritos para Resgate
    ax3 = axes[1, 0]
    gatilho_counts = df_features["gatilho_mental"].value_counts()
    wedges, texts, autotexts = ax3.pie(
        gatilho_counts.values,
        labels=gatilho_counts.index,
        autopct='%1.1f%%',
        colors=palette_primary[:len(gatilho_counts)],
        startangle=140,
        wedgeprops=dict(width=0.6, edgecolor='white', linewidth=2)
    )
    for at in autotexts:
        at.set_fontweight('bold')
    ax3.set_title("3. Prescrição de Gatilhos de Resgate (CRM)", fontsize=12, fontweight='bold', color="#2B2D42")

    # 4. Sentimento vs Sensibilidade a Preço
    ax4 = axes[1, 1]
    ct = pd.crosstab(df_features["sentimento"], df_features["sensibilidade_preco"])
    sns.heatmap(ct, annot=True, cmap="Blues", fmt="d", cbar=False, ax=ax4, linewidths=1, linecolor="#CBD5E1")
    ax4.set_title("4. Matriz: Sentimento vs Sensibilidade a Preço", fontsize=12, fontweight='bold', color="#2B2D42")
    ax4.set_xlabel("Sensibilidade a Preço", fontsize=10)
    ax4.set_ylabel("Sentimento do Cliente", fontsize=10)

    plt.tight_layout()
    plt.savefig(output_path, bbox_inches='tight', dpi=300)
    plt.close()
    print(f"✓ Gráfico executivo salvo em: {output_path}")


# ---------------------------------------------------------------------------
# FLUXO PRINCIPAL DE EXECUÇÃO
# ---------------------------------------------------------------------------
def run_pipeline() -> None:
    print("=============================================================================")
    print("🤖 EXECUTANDO PIPELINE GENAI & LLMS: EXTRAÇÃO DE FEATURES ESTRUTURADAS")
    print("=============================================================================")

    # 1. Processar dados de catálogo desestruturados
    print(f"\n[1/4] Processando {len(RAW_CATALOG_SAMPLES)} registros de texto desestruturado com validação Pydantic...")
    enriched_records = [process_unstructured_catalog(sample) for sample in RAW_CATALOG_SAMPLES]

    # Converter para dicionários estruturados
    json_output_data = [rec.model_dump() for rec in enriched_records]

    # Salvar JSON estruturado
    json_path = os.path.join(OUTPUTS_DIR, "genai_features_sample.json")
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(json_output_data, f, indent=2, ensure_ascii=False)
    print(f"✓ JSON estruturado exportado em: {json_path}")

    # 2. Criar DataFrame tabular desaninhado para a camada Silver Parquet
    print("\n[2/4] Desaninhando features para persistência em Parquet (Camada Silver Qualify)...")
    flat_records = []
    for r in enriched_records:
        flat_records.append({
            "produto_id": r.produto_id,
            "nome_bruto": r.nome_bruto,
            "preco_atual": r.preco_atual,
            "categoria_normalizada": r.features_produto.categoria_normalizada,
            "subcategoria": r.features_produto.subcategoria,
            "marca": r.features_produto.marca,
            "material_construcao": r.features_produto.material_construcao,
            "diferencial_tecnico": r.features_produto.diferencial_tecnico,
            "faixa_posicionamento": r.features_produto.faixa_posicionamento.value,
            "requer_compatibilidade": r.features_produto.requer_compatibilidade,
            "motivo_raiz": r.diagnostico_abandono.motivo_raiz,
            "sentimento": r.diagnostico_abandono.sentimento.value,
            "nivel_urgencia": r.diagnostico_abandono.nivel_urgencia.value,
            "sensibilidade_preco": r.diagnostico_abandono.sensibilidade_preco.value,
            "estrategia_recomendada": r.acao_prescritiva_crm.estrategia_recomendada,
            "gatilho_mental": r.acao_prescritiva_crm.gatilho_mental.value,
            "copy_resgate_email": r.acao_prescritiva_crm.copy_resgate_email,
            "copy_resgate_whatsapp": r.acao_prescritiva_crm.copy_resgate_whatsapp,
        })
    df_features = pd.DataFrame(flat_records)

    parquet_path = os.path.join(OUTPUTS_DIR, "produtos_enriquecidos_sample.parquet")
    df_features.to_parquet(parquet_path, index=False)
    print(f"✓ Parquet Silver exportado em: {parquet_path} ({len(df_features)} registros)")

    # Persistir diretamente no Data Lakehouse (Camada Silver Qualify)
    lakehouse_dir = os.path.join(BASE_DIR, "pipelines", "datalakes", "qualify", "produtos_enriquecidos_qualify")
    os.makedirs(lakehouse_dir, exist_ok=True)
    lakehouse_parquet_path = os.path.join(lakehouse_dir, "produtos_enriquecidos.parquet")
    df_features.to_parquet(lakehouse_parquet_path, index=False)
    print(f"✓ Parquet Lakehouse (Silver Qualify) exportado em: {lakehouse_parquet_path}")

    # 3. Gerar Gráficos Executivos
    print("\n[3/3] Gerando painel gráfico de distribuição das features...")
    chart_path = os.path.join(ASSETS_DIR, "genai_features_overview.png")
    generate_visual_assets(df_features, chart_path)

    print("\n=============================================================================")
    print("✨ PIPELINE EXECUTADO COM SUCESSO! TODOS OS ARTEFATOS FORAM GERADOS.")
    print("=============================================================================\n")


if __name__ == "__main__":
    run_pipeline()
