# daily-hub

**Uma thread por dia. O hub não executa — mantém a fila, delega e esconde o filho.**

Protocolo em markdown, sem código. Funciona em qualquer agente de código com delegação e worktree (T3 Code, Claude Code, OpenCode).

---

## O problema

O fluxo padrão é *thread por task*: N abas no sidebar, N labels, e você alternando contexto para acompanhar cada uma. O custo não é o trabalho — é a **atenção de gerente** paga em cada troca.

## A ideia em 4 linhas

1. Uma thread por dia é o **hub**: ela não lê código, não pesquisa, não escreve. Só mantém fila, delega, normaliza retorno.
2. Cada task vira uma **thread filha** no repo real, em worktree própria, com modelo próprio.
3. O filho devolve um **cartão de ≤10 linhas** (projeto, estado, PR, premissa, risco) e o hub o esconde da tela (`settle`).
4. Você revisa **produto** (PR, diff, CI) — nunca processo (scrollback, tool call).

Você fala com **uma** thread. O resto trabalha sozinho.

## Instalação (~5 min)

```bash
cp -r daily-hub ~/.claude/skills/        # ou para o diretório de skills do seu agente
```

1. Crie um **projeto "hub"** apontando para a pasta copiada (é o escritório, não um produto).
2. Abra a **thread do dia** nesse projeto, em *full access* (`approval-required` transforma cada comando em ping para você; approval não se roteia — se elimina).
3. Copie `templates/projects.example.md` → `projects.md` e preencha repo, base e comando de teste. **Não versione o seu** (tem IDs e caminhos da sua máquina).
4. Fale normal: "bom dia" ou a task. Não existe frase-gatilho.

## Sugestões que a skill não faz por você

- **Pine a thread do hub** no topo do T3 Code. O hub esconde as filhas do sidebar, mas a thread do dia é sua âncora — deixe-a sempre visível.
- **Thread nova só quando gorda** (contexto > ~1.000 itens). Estado mora em `state/`, então trocar não custa nada — mas os **checkpoints agendados ficam presos à thread antiga**: peça ao hub para recriá-los, senão o relógio coleta no lugar errado.
- **"Feito" tem prova:** CI verde + teste novo + PR aberto. Sem isso, o filho não terminou — não aceite narrativa no lugar.
- **Trabalho sem repo** (pesquisa, análise, plano, texto) vira filho no projeto `operations`, com teto de 12 fontes/45 min. Pesquisa é trabalho, não conversa.
- **PR sempre com `pr-format` + `copilot-pr-loop`** (se existirem no harness), nunca a pipeline completa com e2e.

## O que tem aqui

| Arquivo | Papel |
|---|---|
| `SKILL.md` | comportamento do hub: 15 invariants, adaptador do harness, anti-padrões |
| `AGENTS.md` | faz o hub se comportar sozinho no workspace (carregado automaticamente) |
| `child-brief.md` | contrato do filho de código: envelope de decisão, pronto, entrega |
| `research-brief.md` | o mesmo para trabalho que não termina em PR |
| `daily.md` | rotina: manhã / checkpoints / feedback / fechamento / semana |
| `metrics.md` | 4 números + critério de morte |
| `templates/` | STATE, DECISIONS, cartão de retorno, projects.example.md |

## A troca, honestamente

| Você ganha | Você perde |
|---|---|
| uma fila, um lugar, um estado | a chance de pegar o filho indo errado no meio |
| retorno curto e comparável | a leitura do raciocínio do agente |
| silêncio entre checkpoints | a sensação de "estou acompanhando" |

A compensação é o **envelope de decisão** (decida/pergunte/nunca) + `DECISIONS.md` append-only: você audita premissas no artefato, no fim do dia.

## Critério de morte

5 dias úteis. Rode as 4 métricas de [`metrics.md`](metrics.md): intervenções/dia, WIP máximo, lead time, "feito" de primeira. Mata se você abrir filha "só para ver" em 2 dias ou mais.

Se sobreviver: congele e mude **uma coisa por semana**.
