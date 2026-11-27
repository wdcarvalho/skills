# Orchestrate Agents (orquestrar-agentes)

## What it does

A skill ensina a sessão principal, que usa um modelo caro, a planejar, especificar e verificar o trabalho.
Subagentes baratos executam a implementação, os testes, as revisões e as correções.
A sessão principal não executa código, não roda suíte, não faz commit, push nem PR.

## Why

O modelo caro custa mais e gasta contexto rápido quando recebe código e saída de comando.
Trabalho grande se perde quando um agente trava no meio, por isso ele é dividido em commits pequenos com push.
Um executor barato bem instruído entrega bem quando a decisão já vem escrita no brief.
Verificação independente achou defeito em toda rodada real, inclusive em código já mergeado.

## What is inside

| File | What it is for |
|---|---|
| `SKILL.md` | Regras de comportamento da sessão principal, papéis, ondas e regras de cada turno. |
| `templates/context.md` | Contexto único da rodada, com decisão, contratos, fatos e regras fixas. |
| `templates/agent-task.md` | Prompt curto enviado a cada agente, apontando para o contexto e o brief. |
| `templates/brief-implementation.md` | Brief de implementação, usado na fundação e nos pacotes paralelos. |
| `templates/brief-tester.md` | Brief de teste independente, feito por fora contra a decisão escrita. |
| `templates/brief-reviewer.md` | Brief de revisão por tema, com prova obrigatória para cada achado. |
| `templates/brief-correction.md` | Brief de correção, com a regra decidida para cada achado. |
| `templates/brief-closing-and-pr.md` | Brief do agente de fecho, que confere o código, documenta e abre o PR. |

## How to use

1. O usuário pede a orquestração e diz quais modelos usar.
2. Copie `templates/context.md` para a pasta de trabalho fora do repositório e preencha.
3. Para cada agente, escreva um brief a partir do modelo certo e envie `templates/agent-task.md` como prompt curto, apontando para o brief e para o contexto.
   Lance cada agente em worktree próprio, com o modelo explícito e registrando o ID dele, como na seção 11 do `SKILL.md`.
4. Lance as ondas na ordem da seção "Waves" do `SKILL.md`.
5. Rode a verificação independente antes de dar a entrega por pronta.
6. Lance as correções, separadas por tema.
7. Faça o fecho com o PR.
8. Entregue o resumo final.

## Example of a turn

Durante o trabalho: "Onda 2 concluída, fundação em commit e dois pacotes lançados em paralelo sem disputa de arquivo."
No fim: "Entregue em três itens, com uma pendência de ambiente real que depende de você."

## Limits

A skill não substitui a revisão humana.
Ela depende de modelos baratos capazes de seguir um brief bem escrito.
Ela não valida em ambiente real por si, e esse passo continua com quem entrega.
