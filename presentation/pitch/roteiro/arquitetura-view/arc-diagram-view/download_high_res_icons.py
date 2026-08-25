#!/usr/bin/env python3
"""
download_high_res_icons.py
Baixa os ícones oficiais de alta resolução do repositório oficial da AWS (awslabs/aws-icons-for-plantuml)
e substitui no diretório presentation/pitch/roteiro/arquitetura-view/assets/icons/.
O que não for encontrado na web é mantido intacto.
"""

import urllib.request
from pathlib import Path
from PIL import Image
import io

ICONS_DIR = Path(__file__).resolve().parent / "assets" / "icons"
ICONS_DIR.mkdir(parents=True, exist_ok=True)

AWS_PLANTUML_BASE = "https://raw.githubusercontent.com/awslabs/aws-icons-for-plantuml/master/dist"

ICON_URLS = {
    # AWS Oficiais PNG Transparentes (awslabs)
    "kinesis.png": f"{AWS_PLANTUML_BASE}/Analytics/Kinesis.png",
    "firehose.png": f"{AWS_PLANTUML_BASE}/Analytics/KinesisDataFirehose.png",
    "glue.png": f"{AWS_PLANTUML_BASE}/Analytics/Glue.png",
    "lake-formation.png": f"{AWS_PLANTUML_BASE}/Analytics/LakeFormation.png",
    "redshift.png": f"{AWS_PLANTUML_BASE}/Analytics/Redshift.png",
    "lambda.png": f"{AWS_PLANTUML_BASE}/Compute/Lambda.png",
    "dynamodb.png": f"{AWS_PLANTUML_BASE}/Database/DynamoDB.png",
    "redis.png": f"{AWS_PLANTUML_BASE}/Database/ElastiCache.png",
    "s3.png": f"{AWS_PLANTUML_BASE}/Storage/SimpleStorageServiceS3.png",
    "sqs.png": f"{AWS_PLANTUML_BASE}/ApplicationIntegration/SQS.png",
    "eventbridge.png": f"{AWS_PLANTUML_BASE}/ApplicationIntegration/EventBridge.png",
    "secrets-manager.png": f"{AWS_PLANTUML_BASE}/SecurityIdentityAndCompliance/SecretsManager.png",
    
    # Streamlit Oficial
    "streamlit.png": "https://streamlit.io/images/brand/streamlit-mark-color.png",
}

def download_and_save_icon(name: str, url: str):
    target_path = ICONS_DIR / name
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            data = response.read()
            img = Image.open(io.BytesIO(data)).convert("RGBA")
            img.save(target_path, "PNG")
            print(f"[OK] Atualizado de alta resolucao da web: {name} ({img.size[0]}x{img.size[1]})")
            return True
    except Exception as e:
        print(f"[WARN] Nao foi possivel baixar {name} de {url} ({e}). Mantendo versao local existente.")
        return False

def main():
    print("=" * 80)
    print(" BAIXANDO ICONES OFICIAIS DE ALTA RESOLUCAO DA AWS E ECOSSISTEMA")
    print("=" * 80)
    
    success = 0
    total = len(ICON_URLS)
    
    for filename, url in ICON_URLS.items():
        if download_and_save_icon(filename, url):
            success += 1
            
    print("\n" + "=" * 80)
    print(f" Concluido: {success}/{total} icones oficiais baixados e atualizados em assets/icons/!")
    print("=" * 80)

if __name__ == "__main__":
    main()
