# STATE — <AAAA-MM-DD>

data: <AAAA-MM-DD>

> Fonte de verdade do dia. O hub atualiza a cada retorno de filho. Sem limite de rodando.

## Fila

| # | Projeto | Task (1 frase) | Estado | Filho (ID) | Início | Fim | Artefato |
|---|---|---|---|---|---|---|---|
| 1 | <proj> | <task> | fila | — | — | — | — |
| 2 | <proj> | <task> | rodando | <id> | 09:12 | — | — |
| 3 | <proj> | <task> | revisar | <id> | 09:12 | 10:40 | PR #412 |

Estados: `fila` · `rodando` · `revisar` · `bloqueado` · `feito` · `morto`

## Aguardando você

> Máximo 2. Cada linha com default e prazo. Se não houver, escreva "nada".

- [ ] <projeto> — <pergunta sim/não> · default: <...> · até <hora>

## Premissas do dia

> Decisões que os filhos tomaram sozinhos. Revise no fim do dia, não no meio.

- <proj> · <premissa> · reversível: sim/não

## Pendências para amanhã

- <proj> · <o que falta> · bloqueada por <#n | nada>

## Métricas (preencher no fechamento)

- intervenções: <n>
- WIP máximo: <n>
- lead time mediano: <h>
- "feito" de primeira: <n>/<n>
- flow (1-5): <n>
