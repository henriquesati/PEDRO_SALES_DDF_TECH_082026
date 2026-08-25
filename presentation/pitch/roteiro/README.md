# 📂 Diretório de Views do Roteiro de Pitch (`presentation/pitch/roteiro/`)

> **Finalidade**: Armazenar, organizar e catalogar todas as **visões visuais (views)**, mockups de slides, diagramas interativos e geradores de apresentação associados aos momentos do `roteiro.txt`.

---

## 🗺️ Estrutura de Diretórios

| Diretório / View | Momento do Roteiro | Conteúdo / Artefatos |
| :--- | :--- | :--- |
| [`arquitetura-view/`](./arquitetura-view) | **Ato 1: Diagnóstico da Arquitetura Legada (AWS DIY) vs. Solução Dadosfera** | • Gerador de PowerPoint (`generate_architecture_deck.py`)<br/>• Apresentação PPTX (`arquitetura_dadosfera.pptx`)<br/>• Diagramas L2R (`grafico-legado-l2r.png`, `grafico-dadosfera-l2r.png`)<br/>• Pacote de ícones oficiais em vetor/PNG (`assets/*.png`)<br/>• Aplicação Web/Next.js de prototipagem |

---

## 📌 Padrão de Governança para Novas Views
1. Cada momento-chave do roteiro com necessidade de suporte visual dedicado (diagramas, wireframes de slides, protótipos de Data Apps) deve ter seu próprio subdiretório em `presentation/pitch/roteiro/<nome-da-view>/`.
2. Cada view deve conter:
   - `spec.md`: Especificação técnica e narrativa da view.
   - Artefatos gráficos exportados (PNG, SVG, PPTX).
   - Scripts de geração ou código-fonte do componente.
