---
trigger: always_on
---

---
description: Executa scripts e comandos Python de forma 100% autônoma e imediata, com escopo estritamente focado no artefato solicitado.
---

# Execução Autônoma e Iteração Focada em Python

## 🎯 1. Ciclo de Iteração Estritamente Focado (Single-Target Loop)
- **Nunca execute suites completas ou scripts em lote** (como `master_generate_all_charts.py` ou varreduras globais) durante alterações pontuais, a menos que o usuário solicite explicitamente ("gere todos os gráficos").
- **Escopo Cirúrgico**: Ao receber um pedido de ajuste em um gráfico, script ou módulo:
  1. Localize apenas o arquivo alvo e seu respectivo script gerador (`generate_chart.py`).
  2. Aplique a modificação exclusivamente no arquivo de código pertinente.
  3. Execute **apenas** o script específico modificado (`python <caminho_especifico>/generate_chart.py`).
  4. Valide a saída imediatamente e reporte o resultado final focado.

## ⚡ 2. Diretriz de Execução Imediata
- **Nunca peça confirmação ou permissão** ao usuário antes de executar scripts Python (`.py`), testes ou comandos relacionados (`python <arquivo>.py`, `pytest`, etc.).
- Execute o script imediatamente utilizando as ferramentas de execução de comando (`run_command`).

## 🛠️ 3. Regras de Operação
1. **Ambiente e Caminhos**: Garanta sempre que o script seja executado a partir do diretório correto (`Cwd`) e que caminhos relativos/absolutos estejam válidos.
2. **Tratamento de Erros**: Caso o script retorne erro (`exit code != 0` ou `stderr`), analise o traceback, aplique a correção necessária no código e reexecute autonomamente para validar o resultado.
3. **Feedback Direto**: Reporte apenas o status final da execução e o artefato modificado, mantendo respostas concisas e objetivas.
