#!/usr/bin/env python
"""Script utilitário para inicialização local do Data App Streamlit (Item 9 & Bônus)."""

import os
import subprocess
import sys

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

def check_dependencies() -> bool:
    """Verifica se os pacotes essenciais estão instalados."""
    required = [
        ("streamlit", "streamlit"),
        ("plotly", "plotly"),
        ("pandas", "pandas"),
        ("pyarrow", "pyarrow"),
        ("sklearn", "scikit-learn"),
        ("matplotlib", "matplotlib"),
    ]
    missing_packages = []
    for module_name, pip_name in required:
        try:
            __import__(module_name)
        except ImportError:
            missing_packages.append(pip_name)
            
    if missing_packages:
        print(f"⚠️ Dependências ausentes: {', '.join(missing_packages)}")
        print("Instalando dependências via pip...")
        res = subprocess.run([sys.executable, "-m", "pip", "install", *missing_packages])
        return res.returncode == 0
    return True

def main():
    print("=" * 70)
    print("🛒 INICIALIZADOR DO DATA APP STREAMLIT - DADOSFERA (ITEM 9 & BÔNUS)")
    print("=" * 70)
    
    if not check_dependencies():
        print("[ERRO] Falha ao verificar dependências.", file=sys.stderr)
        sys.exit(1)
        
    app_path = os.path.join(BASE_DIR, "app", "app.py")
    if not os.path.exists(app_path):
        print(f"[ERRO] Arquivo principal não encontrado: {app_path}", file=sys.stderr)
        sys.exit(1)
        
    print(f"\n🚀 Iniciando Streamlit a partir de: {app_path}\n")
    cmd = [sys.executable, "-m", "streamlit", "run", app_path]
    try:
        subprocess.run(cmd, cwd=BASE_DIR)
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada pelo usuário.")

if __name__ == "__main__":
    main()
