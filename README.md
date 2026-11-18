# Skills

Skills para agentes de código, escritas em português e pensadas para rodar em Claude Code e OpenCode.

Cada pasta na raiz é uma skill: um `SKILL.md` com o comportamento e os arquivos de apoio que ela referencia.

## Conteúdo

| Skill | Para que serve |
|---|---|
| [`orquestrar-agentes`](orquestrar-agentes/) | Divide um trabalho grande em ondas: fatos, fundação, pacotes paralelos, verificação independente, correção e fecho com PR. A sessão principal planeja e decide; agentes mais baratos executam. |
| [`daily-hub`](daily-hub/) | Uma thread por dia como hub: ela mantém a fila, delega filhas efêmeras por task, recebe cartões de ≤10 linhas e esconde o filho da tela. Troca N abas por uma conversa — você revisa produto (PR/CI), nunca processo. |

## Instalação

Copie a pasta da skill para o diretório de skills do agente.

Para todos os projetos:

```bash
cp -r orquestrar-agentes ~/.claude/skills/
```

Só para um projeto:

```bash
mkdir -p .claude/skills
cp -r orquestrar-agentes .claude/skills/
```

O `SKILL.md` traz o frontmatter (`name` e `description`) que o agente usa para decidir quando carregar a skill.

## Como uma skill é escrita

- `SKILL.md`: comportamento, regras e critérios. É o arquivo que o agente carrega.
- `README.md`: o que a skill faz, por que existe e como usar.
- `templates/`: textos prontos que a skill manda copiar e preencher, em vez de reescrever a cada uso.

## Licença

Sem licença definida até aqui. Se for reutilizar, abra uma issue para conversar.
