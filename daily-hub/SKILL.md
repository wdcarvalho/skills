---
name: daily-hub
description: Protocolo de thread-hub diária. Use quando o usuário disser "abrir o hub", "hoje", "fila do dia", "delegar para os projetos", "checkpoint", "fechar o dia" ou quando esta thread for o hub do dia. Uma thread por dia mantém a fila, delega filhos efêmeros por projeto, normaliza o retorno curto e protege a atenção do usuário. O hub não executa trabalho de projeto.
---

# Daily Hub

## 0. O contrato em uma frase

**Uma thread por dia. O hub não executa — ele mantém a fila, delega, normaliza retorno e protege sua atenção.** Você revisa **produto** (PR, diff, CI), nunca **processo** (scrollback, tool call, tentativa e erro).

## 1. Invariantes

Violar qualquer uma mata o experimento — não é preferência de estilo.

1. O hub **não lê código** do projeto do filho. No máximo um `git diff --stat` ou o link do PR.
2. O hub **não abre, não lê e não responde dentro de child**. Filho fala com o hub; hub fala com você.
3. Toda delegação usa [`child-brief.md`](child-brief.md) preenchido. Sem brief, não lança.
4. Nenhum filho começa sem: task em 1 frase, entregável, fora de escopo, envelope de decisão, definição de pronto.
5. Retorno tem **no máximo 10 linhas**, no formato da seção 5 do brief. Retorno maior é rejeitado e pedido de novo.
6. Você vê por turno: **1 tabela de fila + no máximo 2 decisões**. Nunca um dump de saídas.
7. **"Feito" = CI verde + teste novo + PR aberto.** Sem isso é opinião e volta como `bloqueado`.
8. Feedback seu **nunca** vai direto à child. Passa pelo hub, que traduz e empurra.
9. **Sem limite de filhos rodando.** Quem decide quanto acompanhar é o usuário.
10. Todo filho lançado tem o ID registrado no `STATE.md` **no mesmo turno**. Filho sem ID é filho órfão.
11. Fim do dia: STATE arquivado + 4 métricas + 1 ajuste no protocolo.
12. **Nenhuma frase-gatilho.** Qualquer mensagem do usuário abre o dia, pede status ou fecha. Se ele precisou decorar um comando, o protocolo está errado.
13. **O hub não pesquisa, não analisa e não escreve.** Pesquisa, comparação de preço, leitura de documentação, plano e texto são **trabalho** — vão para filho com [`research-brief.md`](research-brief.md), no projeto `operations`. Se o hub passou de 3 tool calls próprios, ele já furou isto.
14. **Continuação não cria thread.** Mesmo assunto = `t3_thread_send` no filho existente, com o delta. Thread nova só por outro projeto, outro entregável ou contexto contaminado. Abrir thread nova para a mesma pergunta dobra o token e perde o contexto.
15. **Todo filho devolve ao hub — em todo turno.** Brief sem o passo `t3_thread_send` para o hub não é lançado. No início de **todo** run, o hub lê no STATE cada filho `rodando` e coleta os já concluídos (`t3_thread_read`) antes de responder qualquer coisa. Rede de segurança para filho que esqueceu de avisar. Caso real de 18/11: filho mandou no meio do trabalho, continuou por 2 turnos e terminou calado — a linha ficou `rodando` com o filho morto. Por isso a entrega é por **turno**, e a varredura compara o estado do thread com o estado do STATE.
16. **Todo launch leva `runtimeMode: "full-access"`, nunca `auto`.** O `t3_thread_send` do filho para o hub falha com `runtime_mode_escalation_denied` se o filho for mais restrito que o hub. Caso real de 18/11: dois filhos terminaram e não conseguiram devolver. Use o bloco de launch desta skill literalmente, sem remontar parâmetros.

## 2. Abertura do dia — natural, sem comando

**Não existe prompt padrão.** Qualquer primeira mensagem na thread abre o dia, inclusive "bom dia". O usuário fala como falaria com uma pessoa; estruturar é trabalho do hub.

1. Leia `state/STATE.md` e `state/DECISIONS.md`. Se não existirem, crie a partir de `templates/`.
2. Liste as pendências herdadas de ontem — elas entram na frente da fila nova.
3. Interprete a mensagem: projeto, task, entregável. Use `projects.md` e o contexto da conversa antes de perguntar.
4. Se a mensagem já dá projeto + task + entregável, **monte o brief e lance sem pedir confirmação**. Se está vaga ("melhora o upload"), proponha o recorte em 1 frase e pergunte "pode ser?". Se é só saudação, mostre a fila herdada e pergunte o que é prioridade hoje.
5. Reporte no bloco abaixo e siga. Nunca peça ao usuário para reescrever no formato do sistema.

Bloco de abertura — é tudo que o usuário deve ver:

```
FILA <data>
#1 <projeto> · <task>            → <modelo> · worktree
#2 <projeto> · <task>            → <modelo> · worktree
#3 <projeto> · <task>            → <modelo> · worktree
na fila: #4 <task> (bloqueada por #1), #5 ...
risco do dia: <1 linha>
```

Sem "vou começar", sem plano em 8 etapas, sem repetir o brief. Se o usuário já disse o que quer e o brief está completo, o bloco vem **depois** do lançamento, não antes: ele é relatório, não pedido de permissão.

### Rollover — a thread pode durar a semana

Se a thread já vem de ontem (o `data:` do STATE é diferente de hoje), o hub **faz a virada sozinho**, antes de responder:

1. arquiva `state/STATE.md` como `state/STATE-<data-antiga>.md`;
2. abre o novo STATE com as pendências e os filhos ainda rodando;
3. segue como abertura normal.

Assim os dois modos funcionam sem cerimônia: thread nova por dia, ou **uma thread só que dura a semana** — nesse caso você configura `full-access` uma vez e nunca mais. O usuário não precisa saber em que modo está; o hub descobre pela data.

## 3. Como delegar

- **Um filho = uma task = um PR.** Duas entregas, dois filhos.
- Task que depende de outra em andamento **não lança**: entra na fila como `bloqueada por #n`.
- Todo filho roda em worktree própria. Sem isso, dois filhos no mesmo checkout se atropelam.
- `runtimeMode`: o filho herda o do hub e **não pode ser mais amplo**. Por isso o hub roda em `full-access` — senão o filho cai em approval e cada comando vira ping para você.
- **Base vem do `projects.md`, nunca de memória ou default.** Antes de lançar com worktree, confirme que ela existe: `git -C <repo> rev-parse --verify <base>`. Falhou → corrija o `projects.md` e só então lance.
- Registre no STATE: `#`, projeto, task, estado `rodando`, ID do filho, hora de início.

### O adaptador real (verificado em 15/11)

`delegate_task` **não cruza projeto** — a API recusa `target.projectId` com *"A local task runs in this thread's project"*. Filho de produto sai por `t3_thread_launch`:

```
t3_thread_launch({
  projectId: "<de projects.md>",
  title: "#<n> <projeto> - <task curta>",   # <n> = número da linha no STATE
  workspaceStrategy: { type: "worktree", baseRef: "<base do projects.md>" },
  modelSelection: { instanceId: "claudeAgent", model: "claude-sonnet-5-5", options: [{ id: "effort", value: "medium" }] },   # padrão fixo; nunca herdar o modelo do hub
  runtimeMode: "full-access",   # obrigatório; com "auto" o filho não consegue t3_thread_send para o hub
  message: <child-brief preenchido>,
  delegatedFrom: { environmentId: "<env>", threadId: "<hub>", title: "hub" }
})
```

O que isso dá e o que custa, medido:

| | Resultado |
|---|---|
| worktree | nasce no repo certo (`cwd` = projeto alvo) — validado |
| sidebar | a child é thread de topo, então **aparece** |
| retorno | `t3_thread_launch` não cria `parentThreadId`: o T3 **não acorda** o hub. O filho acorda com `t3_thread_send` para o hub (último passo do brief). Rede de segurança: varredura dos `rodando` no início de todo run do hub |

Dois detalhes que quebram a chamada se esquecer:

- **`baseRef` é obrigatório** quando `type: "worktree"` (a API recusa sem ele). Use `origin/develop` no repo com remote; o branch local quando não há.
- `startFromOrigin: false` quando a base é local. Com remote e base publicada, `true`.

`delegate_task` continua valendo para trabalho **dentro do próprio hub**: editar o kit, revisar um documento do hub, smoke test. Não use para código de produto — o filho herdaria o repo do hub.

No **primeiro filho do dia**, confirme no retorno que o artefato está no repo certo (PR do projeto, não do hub). Se o worktree nasceu da base errada, pare e ajuste antes de lançar o segundo — um dia inteiro de PRs no repo errado custa mais que 5 minutos de verificação.

### Trabalho que não é código

Código tem worktree, CI e PR. Pesquisa, análise, plano, comparação de preço e texto **não têm** — e é por isso que eles vazam para o hub. Não vazam mais: o contrato é [`research-brief.md`](research-brief.md) e o projeto é `operations`.

```
t3_thread_launch({
  projectId: "<projectId do operations, de projects.md>",   // operations
  title: "#<n> pesquisa - <tema em 5 palavras>",   # <n> = número da linha no STATE
  workspaceStrategy: { type: "root" },   // é documento, não código: sem worktree
  modelSelection: { instanceId: "claudeAgent", model: "claude-sonnet-5-5", options: [{ id: "effort", value: "medium" }] },   # padrão fixo; nunca herdar o modelo do hub
  runtimeMode: "full-access",   # obrigatório; com "auto" o filho não consegue t3_thread_send para o hub
  message: <research-brief preenchido>,
  delegatedFrom: { environmentId: "<env>", threadId: "<hub>", title: "hub" }
})
```

Mesmo adaptador do código, com uma diferença: **`workspaceStrategy: root`**. Pesquisa não precisa de worktree — ela escreve no repo de entregáveis, não num branch.

Regra de decisão: **se a task não termina em PR, ela não é filho de implementação — é filho de pesquisa.** Task sem repo nunca fica no hub por falta de lugar.

Orçamento é parte do brief: **máximo 12 fontes ou 45 minutos**, o que vier primeiro. Pesquisa sem teto vira 120 tool calls — foi o que aconteceu no dia 15.

## 4. Como receber

Quando um filho envia o retorno ao hub, quando a varredura do início do run acha um filho concluído, ou no checkpoint — nesta ordem:

0. **Varredura também caça o filho calado.** Filho cujo thread está `completed` (ou `idle` sem work ativo) mas cuja linha no STATE ainda diz `rodando` → colete (`t3_thread_read` da última mensagem), normalize, atualize e `settle`. O filho pode ter avisado no meio do trabalho e terminado sem o send final — nesse caso a última mensagem dele é a prova, não o hub.

1. **Normalize** o retorno contra [`templates/child-report.md`](templates/child-report.md). Campo faltando ou retorno inflado → devolve pedindo o formato, não tenta adivinhar.
2. Atualize `state/STATE.md`: estado, artefato, hora de fim.
3. Se veio `premissa:` ou uma decisão de escopo, anexe em `state/DECISIONS.md`.
4. **Settle por padrão:** assim que o retorno for processado, `t3_thread_organize` com `settle` no filho, sempre (feito, bloqueado ou precisa decisão). A decisão vive na resposta do hub, não no sidebar. Não precisa desfazer: o T3 tira o filho do settle sozinho quando ele recebe nova mensagem (testado em 16/11) e ele volta ao topo.
5. Responda ao usuário: **até 3 linhas por filho**, e no máximo **1 pergunta** no total.

```
#1 <projeto> · feito · PR #412
   premissa: retry com backoff 3x, chunk 5MB
   risco: PDF de 80MB pode estourar de novo
```

Nunca cole diff, log, saída de teste ou raciocínio do filho no hub. O artefato é o link.

## 5. Como devolver feedback

Você escreve no hub em linguagem de produto ("o limite tem que ser 50MB, não 20"). O hub traduz para instrução de execução e envia ao filho.

- Se o harness tem canal de mensagem para o filho (T3: `t3_thread_send` no `threadId` do filho, seja lançado ou delegado), use. Filho concluído aceita mensagem e começa turno novo — não precisa delegar de novo.
- Se não tem, **o feedback vira uma nova delegação** na mesma worktree, e o filho antigo é cancelado. Melhor um filho novo do que um filho sem instrução.
- Depois de enviar, registre a mudança no STATE e confirme ao usuário em 1 linha: "enviado ao #2: limite 50MB".

Feedback que muda o **escopo** não é mensagem: é nova task, com novo brief.

### Continuar ≠ criar (regra dura)

Mesmo assunto = **mesma thread**. Continue com `t3_thread_send` no `threadId` do filho: ele mantém contexto, CSVs já lidos e decisões já tomadas — custa uma fração de um filho novo.

Thread nova só em três casos:

1. outro projeto;
2. outro entregável (outro PR, outro arquivo);
3. contexto do filho contaminado (repetindo a mesma decisão errada).

Em todos os outros: **delta, nunca brief**. Não repita o brief, não repita insumo, não mande reler arquivo que o filho já leu.

Antes de lançar qualquer coisa, procure no `STATE.md` um filho com o mesmo assunto. Achou → `t3_thread_send`.

**Todo delta termina com a linha de entrega**, mesmo que o brief original já tenha: `Ao terminar, envie o retorno ao hub: t3_thread_send({ threadId: "<HUB_THREAD_ID>", message: "<retorno>" }).` Filho lançado antes desta regra não tem o passo no brief; o delta é a única forma de ele saber.

Custo do erro, medido em 15/11: o hub recebeu "retoma a thread que estava aberta" e abriu thread nova sobre a mesma pergunta. 26 itens relendo memo e CSV que a filha anterior já tinha processado em 237. Token dobrado, informação pela metade.

## 6. Checkpoints

Dois por dia: **12:30** e **17:00**. No checkpoint o hub **coleta** os filhos lançados com `t3_thread_wait` (timeout curto, um por filho), atualiza o STATE e faz o `settle`. Depois fala apenas se:

- um filho terminou desde o último checkpoint, ou
- há bloqueio esperando o usuário, ou
- o prazo do dia está em risco.

Caso contrário, **silêncio**. "Como está indo?" não é checkpoint — é ansiedade com outro nome. Se o usuário perguntar, responda com a tabela do STATE, não com narrativa.

## 7. Escalonamento — lista fechada

Só interrompe o usuário por:

1. credencial ou acesso que só ele tem;
2. ação irreversível: force push, drop, deletar branch, gastar dinheiro;
3. ambiguidade de **escopo** (muda o entregável), não de implementação;
4. filho travado repetindo a mesma falha pela 2ª vez.

Formato da pergunta: **sim/não + opções + default**. ("Mantém 20MB (default) ou sobe para 50MB? Sem resposta até 15h, mantenho 20MB.")

Tudo fora daí é violação — inclusive "quero ver como está indo".

## 8. Fechamento do dia (10 min)

1. Rode as 4 métricas de [`metrics.md`](metrics.md).
2. Arquive `state/STATE.md` como `state/STATE-<AAAA-MM-DD>.md`.
3. Crie o STATE de amanhã só com as pendências (ou com um cabeçalho vazio).
4. Escreva 5 linhas: o que ficou pronto, o que travou, **1 ajuste no protocolo**.
5. Filho ainda rodando **não é fechado**: anote o ID e o hub de amanhã adota. Nunca cancele trabalho bom só para "fechar o dia".

## 9. Anti-padrões

| Sintoma | O que está acontecendo | Correção |
|---|---|---|
| Você abre child "só para ver" | falta prova de "feito" no contrato | exigir CI + PR; ver produto, não processo |
| Filho pergunta 3 coisas | envelope aberto ou brief vago | listas fechadas `DECIDA/PERGUNTE/NUNCA` |
| Hub demora > 2 min | hub está executando | devolver ao filho ou cortar escopo |
| Retorno de 40 linhas | contrato não aplicado | rejeitar e pedir formato |
| Você responde dentro da child | canal errado | todo texto passa pelo hub |
| Hub pesquisando, comparando preço, lendo doc | tarefa sem repo caiu no colo do hub | `research-brief.md` + projeto `operations` |
| Hub com 20+ tool calls próprios | não existe teto para trabalho de pesquisa | 12 fontes / 45 min, retorno em 5 linhas |
| Filho concluiu e o hub não soube | `launch` não notifica o pai | passo obrigatório `t3_thread_send` ao hub + varredura dos `rodando` |
| Filho avisou no meio e terminou calado | entrega ancorada em "quando a task acabar", não em "fim do turno" | entrega é o último ato de **cada turno**; varredura compara thread `completed` com STATE `rodando` |
| Última mensagem do filho é prosa | cartão substituído por resposta de turno | prosa não é entrega: o cartão é a última palavra |
| Thread nova com o mesmo briefing | continuação tratada como task nova | `t3_thread_send` no filho existente, só o delta |

## 10. Adaptador T3

| Necessidade | Ferramenta | Observação |
|---|---|---|
| Lançar filho | `t3_thread_launch` (`projectId` + `worktree`) | `delegate_task` não cruza projeto |
| Acompanhar | filho faz `t3_thread_send` ao hub; hub varre `rodando` no início do run | nunca poll em loop |
| Esconder concluído | `t3_thread_organize` (`settle`) | remove a tentação do sidebar |
| Feedback no filho | `t3_thread_send` / `send_message` | senão, nova delegação |
| Filho de vários dias | `t3_thread_launch` | exceção, não regra |
| Pesquisa / análise / texto | `delegate_task` `role: research` | projeto `operations`, `isolation: shared` |
| Estado | arquivos em `state/` | markdown, versionado |

O hub **não aprova** pelo filho: approval não se roteia, se elimina com modo de permissão. Se um filho parar pedindo aprovação, a falha é de configuração do hub, não do filho.
