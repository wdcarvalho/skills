# Cartão de retorno

O contrato completo está na seção 5 de [`../child-brief.md`](../child-brief.md). Este cartão é só para o hub **normalizar** o que chegou.

## Formato aceito

```
projeto:
task:
estado: feito | bloqueado | precisa decisão
artefato: PR #<n> | branch <nome> | nenhum
premissa: <decisão tomada sozinho>
decisão pendente: <1 frase, sim/não — só se bloqueado>
risco:
```

## Normalização

| Veio | Hub faz |
|---|---|
| `feito` + PR + CI verde | STATE `revisar`; 1 linha para o usuário; settle |
| `feito` sem CI ou sem teste | devolve: "não é feito, falta X"; STATE `rodando` |
| `bloqueado` com 1 pergunta de escopo | STATE `bloqueado`; pergunta ao usuário com default |
| `bloqueado` com pergunta de implementação | devolve: "decida pelo mais reversível e registre premissa" |
| `precisa decisão` com 3 perguntas | rejeita: "uma pergunta só, a que muda o entregável" |
| retorno > 10 linhas | rejeita: "corte para o formato" |
| silêncio / timeout | STATE `rodando`; no checkpoint, checar uma vez; 2ª falha = escalar |
| `premissa:` vazia mas houve escolha | aceita o trabalho, exige a linha; registra em DECISIONS |

## Regra de ouro

O hub nunca "interpreta" um retorno ambíguo para parecer produtivo. Retorno ambíguo volta. Cada retorno aceito é uma linha no STATE, não um parágrafo.
