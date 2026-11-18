# Rotina do dia

Tempos são alvo, não cerimônia. Se a abertura passar de 5 minutos, o hub está fazendo trabalho que não é dele.

---

## Manhã — 5 min

**Você fala:** "bom dia" — ou já vai direto: "hoje quero terminar o upload do document-hub". Qualquer coisa serve; não há comando.

Se você reusar a thread de ontem, não precisa fazer nada: o hub vê que o `data:` do STATE é de outro dia, arquiva e abre o dia novo sozinho.

**O hub faz:**

1. `cp templates/STATE.md state/STATE.md` (se não existir STATE de hoje) e preenche a data.
2. Lê o STATE de ontem (`state/STATE-<data>.md`) e `state/DECISIONS.md` (últimas 10 linhas).
3. Consulta `projects.md` para repo, base e comando de teste de cada projeto.
4. Propõe a fila  e **espera seu "vai"**.
5. Preenche um `child-brief.md` por filho, lança em paralelo, registra os IDs.
6. Responde com o bloco de abertura de 6 linhas.

**Você aprova a fila em uma palavra** — ou nem isso, se a mensagem já trazia projeto, task e entregável: nesse caso o hub lança direto e reporta. Ajuste de prioridade é aqui, não no meio do dia.

Se um filho de ontem ainda está rodando, ele entra como `rodando` herdado — o hub de hoje adota o ID. Não relança.

---

## Meio do dia — 2 min (12:30 e 17:00)

O relógio é um agendamento do T3 criado **na thread do dia** (12:30 e 17:00, seg-sex). Nos dois horários o hub coleta os filhos, atualiza o STATE, faz `settle` e responde só o que mudou.

O hub só aparece se houver o que dizer. Formato:

```
12:30 · 1 retorno
#2 connector: feito · PR #412 · premissa: chunk 5MB
aguardando você: sobe limite para 50MB? default 20MB até 15h
```

Sem retorno e sem bloqueio → **nada**. Silêncio é o comportamento correto.

Se você quiser status, pergunte do jeito que quiser ("como tá?", "e o #2?") — o hub responde com a tabela do STATE, não com prosa.

## Thread nova do hub — quando e como

Abra thread nova quando a atual estiver **gorda** (contexto > ~1.000 itens, handoffs de provider frequentes) — não por assunto novo nem porque virou o dia.

O custo é zero (estado mora em `state/`), com uma exceção: **os checkpoints agendados ficam presos à thread antiga.** Ao abrir a nova, peça ao hub: "recrie os checkpoints 12:30 e 17:00 nesta thread" — e remova os antigos. Sem isso o relógio coleta na thread morta e você volta a ser o cronômetro dele.

---

## Feedback — a qualquer momento

Você escreve em linguagem de produto. O hub:

1. identifica o filho certo pelo `#`;
2. traduz para instrução de execução;
3. envia ao filho (ou relança, se não houver canal);
4. confirma em 1 linha.

Se o feedback muda o **entregável**, não é feedback: é task nova, com brief novo, e a antiga é cancelada.

---

## Fechamento — 10 min (17:30)

**Você fala:** "fecha aí", "por hoje é isso", "acabou" — qualquer variação.

**O hub faz:**

1. Tabela final: feito / revisar / bloqueado / morto.
2. Calcula as 4 métricas de [`metrics.md`](metrics.md) e preenche no STATE.
3. Arquiva `state/STATE.md` → `state/STATE-<AAAA-MM-DD>.md`.
4. Cria o STATE de amanhã com as pendências e os filhos ainda rodando (com ID).
5. Escreve 5 linhas de balanço, incluindo **1 ajuste no protocolo**.
6. Pergunta, no máximo: "abro o dia amanhã com a mesma fila?"

**Não faz:** fechar PR, fazer merge, cancelar filho bom para "zerar".

---

## Semana — 10 min (sexta)

Releia as 5 fichas de métrica. Aplique o critério de morte de [`metrics.md`](metrics.md): continua, ajusta ou mata. Essa decisão é sua, não do hub — e ela precisa acontecer na sexta, não "quando der".

Se continua: promova o protocolo a repo próprio (se ainda não for) e congele a v0. Mudança de protocolo só na segunda, uma por semana. Protocolo que muda todo dia não é protocolo, é humor.
