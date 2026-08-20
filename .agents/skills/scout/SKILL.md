---
name: scout
description: Explora, mapeia e analisa a estrutura do repositorio antes de propor ou aplicar alteracoes. Use sempre que iniciar uma nova feature, investigar bugs complexos ou precisar entender fluxos de codigo existentes.
---

# Scout Skill (Mapeamento & Reconhecimento)

## Objetivo
Mapear, entidades, relacionamentos, contratos, fluxos de dados, padrões de comportamento dos dados, entidades e padrões existentes no projeto antes de modificar ou gerar arquivos de código.

## Diretrizes de Execução

Quando esta skill estiver ativa, **NÃO crie ou edite arquivos de código imediatamente**. Siga rigorosamente este fluxo:

### 1. Descoberta e Contexto
- Localize e leia os manifestos principais de Entidadades e modelos, majoriatiamente no diretório '/data'
- Mapeie arquivos de configuração e relacionaodos relevantes, '_config.py' dentro de generators, que dita as especificações de geração de dados mock

### 2. Análise de Padrões e Convenções
- Identifique o padrão arquitetural predominante (Clean Architecture, CQRS, MVC, Ports & Adapters, etc.).
- Verifique como são tratadas exceções, injeção de dependências e logs estruturados.
- Mapeie os contratos de interface/tipos centrais relacionados à tarefa atual.

### 3. Síntese do Reconhecimento
Antes de avançar para a fase de implementação, documente brevemente na resposta:
- **Arquivos-chave identificados:** Lista dos arquivos que serão afetados ou usados como base.
- **Padrões a seguir:** Resumo dos padrões de nomenclatura, estilo e tratamento de erros observados.
- **Riscos / Pontos de Atenção:** Efeitos colaterais potenciais em outros módulos ou schemas.
- **Plano de Ação Proposto:** Sequência de passos recomendada para implementação.

---

## Regras Fundamentais
- **Somente Leitura:** Execute buscas (`grep`, `find`, `cat` ou ferramentas de busca de símbolos) sem alterar arquivos.
- **Sem Suposições:** Se a arquitetura ou convenção não estiver clara, liste as opções encontradas no código real em vez de adivinhar.
