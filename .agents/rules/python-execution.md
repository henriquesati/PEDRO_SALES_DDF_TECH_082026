---
trigger: always_on
---

---
description: Executa scripts e comandos Python de forma 100% autônoma e imediata, dispensando confirmação prévia do usuário.
---

# Execução Autônoma de Arquivos Python

## Diretriz Principal
- **Nunca peça confirmação ou permissão** ao usuário antes de executar scripts Python (`.py`), testes ou comandos relacionados (`python <arquivo>.py`, `pytest`, etc.).
- Execute o script imediatamente utilizando as ferramentas de execução de comando (`run_command`).

## Regras de Operação
1. **Ambiente e Caminhos**: Garanta sempre que o script seja executado a partir do diretório correto (`Cwd`) e que caminhos relativos/absolutos estejam válidos.
2. **Tratamento de Erros**: Caso o script retorne erro (`exit code != 0` ou `stderr`), analise o traceback, aplique a correção necessária no código e reexecute autonomamente para validar o resultado.
3. **Feedback Direto**: Reporte apenas o status final da execução ou o resultado visual/dados gerados (ex: artefatos, gráficos ou arquivos criados), sem pausar para perguntar se deve rodar.

