# Skills para agentes de código

Skills em markdown para orquestração de agentes: uma sessão principal planeja, delega a agentes mais baratos e verifica o resultado.
Sem código, sem dependências e sem runtime próprio: a mesma pasta roda em bot, CLI e GUI.

## As skills

| Skill | O que resolve |
|---|---|
| [`orquestrar-agentes`](orquestrar-agentes/) | Divide um trabalho grande em ondas: fatos, fundação, pacotes paralelos, verificação independente, correção e fecho com PR. A sessão principal planeja e decide; agentes mais baratos executam. |
| [`daily-hub`](daily-hub/) | Uma thread por dia como hub: mantém a fila, delega filhas efêmeras por task, recebe cartões de ≤10 linhas e esconde o filho da tela. Você revisa produto (PR/CI), nunca processo. |

## Roda em qualquer lugar

A skill é só markdown. O agente lê o `SKILL.md`; o que muda é onde a pasta está.

| Ambiente | Como carregar |
|---|---|
| **CLI** — Claude Code | `cp -r <skill> ~/.claude/skills/` para todos os projetos, ou `.claude/skills/` para um projeto. O frontmatter `name`/`description` faz o carregamento. |
| **GUI** — T3 Code | Use a pasta como skill do workspace/projeto e aponte o `AGENTS.md` (ou o prompt da thread) para o `SKILL.md`. A skill não depende do T3; a thread só hospeda o agente. |
| **Bot** — OpenBot, Telegram, Discord etc. | Registre a pasta como skill local do agente. Ele carrega o `SKILL.md` e usa os templates; não há API nem serviço para subir. |
| **Outro** — OpenCode, Codex, Cursor etc. | Aponte as regras/`AGENTS.md` para o `SKILL.md`; a skill é markdown puro. |

O que não muda: os briefs, os templates, os critérios e o jeito de verificar. O que muda é o transporte do agente.

## Como usar

1. Copie a pasta da skill para o diretório de skills do seu agente (ou referencie no `AGENTS.md`).
2. Peça o trabalho; a sessão principal lê o `SKILL.md` e conduz.
3. Ela escreve o contexto e os briefs, lança os executores e lê os relatórios.
4. A verificação independente e o fecho com PR continuam iguais em qualquer ambiente.

## O que tem dentro

Cada pasta na raiz é uma skill:

- `SKILL.md`: o comportamento que o agente carrega.
- `README.md`: o que a skill faz, por que existe e como usar.
- `templates/`: textos prontos para copiar e preencher.
- `AGENTS.md` ou `scripts/`: quando a skill precisa de uma regra de workspace ou de uma ferramenta local.

## Contribuindo

Issues e pull requests são bem-vindos, de qualquer pessoa. O merge é do mantenedor (`@wdcarvalho`).
Para mudanças grandes, abra uma issue antes para combinar o recorte.

## Licença

Sem licença definida até aqui. Se for reutilizar, abra uma issue para conversar.
