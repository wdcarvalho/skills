# Métricas e critério de morte

O experimento não é "me senti mais em flow". É uma troca mensurável: **menos intervenção sua, mesmo throughput**. Quatro números, coletados no fechamento, sem planilha.

## Os 4 números

### 1. Intervenções por dia (`I`)

Quantas vezes você **escreveu dentro de uma child** ou respondeu no meio de uma task (não conta aprovar a fila nem o fechamento).

- **Alvo:** ≤ 2/dia.
- **Onde medir:** contagem manual no fim do dia; o hub anota no STATE quando você pede algo no meio.
- **Se alto:** o envelope está aberto ou o modo de permissão está errado. Não é falta de disciplina sua.

### 2. WIP máximo (`W`)

Maior número de filhos rodando ao mesmo tempo no dia.

- **Alvo:** 3. Acima de 3, seu custo de troca de contexto come o ganho.
- **Se alto:** a fila furou. O hub segura; se ele não segurou, é bug do hub.

### 3. Lead time (`L`)

Horas entre "lançou o filho" e "PR aberto com CI verde". Mediana do dia.

- **Alvo inicial:** nenhum. Meça a primeira semana e compare com sua média histórica de thread-por-task.
- **Se pior que o baseline:** o ganho é conforto, não velocidade — e você precisa saber disso antes de defender o método.

### 4. "Feito" de primeira (`Q`)

% dos retornos `feito` que você **mergeou sem pedir mudança**.

- **Alvo:** ≥ 70%.
- **Se baixo:** o brief está vago ou a definição de pronto não está sendo checada. É o número que mais rápido melhora com calibração de envelope.

### 5. Flow (`F`) — subjetivo, 1 a 5

No fim do dia: "eu consegui pensar em uma coisa por vez?".

- **Alvo:** ≥ 4.
- Esse é o número que o experimento existe para mover. Se `I` e `W` estão bons e `F` não subiu, o problema não era a topologia de threads.

## Ficha do dia

```
data:       2026-11-__
I:          _        (alvo ≤2)
W:          _        (alvo 3)
L:          _ h      (baseline: __ h)
Q:          _/_ = _% (alvo ≥70%)
F:          _/5      (alvo ≥4)
ajuste de protocolo: <1 linha>
```

## Critério de morte — 5 dias úteis

Mata o método se **qualquer** condição abaixo for verdadeira ao fim da semana:

1. `I` média > 4/dia — você está abrindo child o tempo todo, o protocolo não pegou.
2. `F` média < 3 — não te deixou em flow, que era o ponto.
3. `Q` < 50% — os filhos entregam errado e você revisa tudo; o custo subiu.
4. `L` > 1,5× seu baseline — ficou mais lento **e** mais confuso.
5. **Você abriu child "só para ver" em 2 dias ou mais.** Essa é a mais honesta: significa que a prova de "feito" não te convence, e sem confiança o método é só uma aba a mais.

Se matar: o prejuízo é uma tarde de markdown. Se sobreviver aos 5 dias: promova a repo, congele a v0, e só mude uma coisa por semana.

## O que não medir

- número de mensagens no hub (incentiva conversa, não entrega);
- tokens gastos (o ganho é atenção, não custo — e o custo já cai ao trocar modelo caro por modelo que roteia);
- "quantas threads abertas" (o objetivo é 1, não é KPI).
