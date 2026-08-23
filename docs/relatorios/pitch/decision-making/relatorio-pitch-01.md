# Relatório: Incorporação do Arquivo Raw Analysis no Pitch

> **Documento**: `relatorio-pitch-01.md`  
> **Arquivo-Fonte**: [`user-case-raw-analyses.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/agents_prompts_refs/case-internship-files/user-case-raw-analyses.md)  
> **Destino da Incorporação**: [`pitch_spec.md`](file:///c:/Users/pedro/OneDrive/Desktop/wheels/presentation/pitch/pitch_spec.md) e Módulo 07

---

## 📌 O que foi extraído do arquivo do usuário e incorporado

### 1. Plataforma como Meio vs Carrinho como Fim (PoC)
- **Do arquivo**: A Dadosfera é o meio (Sistema Operacional de Dados unificado para governança, descoberta e agregação para toda a empresa) e a Recuperação de Carrinho é a Prova de Conceito prática para comprovar ROI rápido.
- **Incorporado em**: Blocos 1 e 2 do `pitch_spec.md`.

### 2. Gargalos Técnicos da Arquitetura Legada AWS
- **Do arquivo**:
  - **Kinesis Stream**: Sharding manual e custo imprevisível.
  - **Firehose**: Latência de buffering que atrasa ações em tempo real.
  - **S3 Bucket**: Falta de schema enforcement rígido.
  - **Redis ElastiCache**: Complexidade standalone vs cluster, upgrades com 5–15 min de parada e risco de perda de **R$ 50k a 100k por minuto** em picos (Black Friday).
  - **Headcount**: Necessidade contínua de 1 Platform Engineer + 2 Data Engineers apenas para criar conexões manuais.
  - **Governança**: IAM complexo que trava o compartilhamento seguro com marketing (LGPD).
- **Incorporado em**: Bloco 1, Bloco 2, Perguntas & Objeções do `pitch_spec.md` e no Módulo 07 (`spec.md` e `generate_chart.py`).

### 3. Preservação de Margem de Lucro & Segmentação
- **Do arquivo**: Cruzar o valor do carrinho com o histórico RFM para não queimar margem (WhatsApp humanizado para clientes Premium em vez de cupom; cupons reservados para clientes Novos com barreira de frete).
- **Incorporado em**: Bloco 3 (Regra 4) do `pitch_spec.md`.

---

## 🎯 Resumo das Mudanças Aplicadas no Projeto

1. **`agents_prompts_refs/case-internship-files/user-case-raw-analyses.md`**: Arquivo de esboço renomeado e preservado com cabeçalho explicativo.
2. **`presentation/pitch/pitch_spec.md`**: Roteiro e backbone ajustados com os argumentos e dores técnicas exatas da raw analysis.
3. **`presentation/pitch/07_arquitetura_dadosfera_vs_aws/`**: Spec e gráfico comparativo atualizados com os componentes da stack AWS vs Dadosfera.
