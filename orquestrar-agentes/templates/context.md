# Round context: <nome curto da rodada>

Este arquivo vale para todos os agentes da rodada e é a única fonte das regras comuns.

## Goal

<o resultado que o usuário pediu, em uma frase>

## Decision already made

<o comportamento final escolhido, sem alternativa em aberto>

## Contract between agents

<rotas, campos, formatos e códigos de erro acordados, quando dois agentes dependem um do outro>

## Decision envelope

- Decida sozinho, sem perguntar: <nomes, ordem de implementação, refatoração interna, estrutura de teste, mensagens de log>.
- Pare e faça uma única pergunta: <contrato público, acesso que o agente não tem, escolha entre dois comportamentos de produto>.
- Nunca faça: <merge, force push, apagar branch, mexer fora do worktree, gastar dinheiro>.
- Ambiguidade de implementação não bloqueia: escolha o caminho mais simples e reversível e registre a premissa no cartão.

## Facts found

- <fato medido, arquivo e linha>
- <fato medido, arquivo e linha>

## Fixed rules

- Trabalhe só no próprio worktree e nunca toque no checkout principal do usuário.
- Não suba ambiente compartilhado: sem container, banco ou serviço em execução, use dublês em memória.
- Comece pelo teste que falha.
- Não escreva dado pessoal nem segredo em log, resposta, documento ou relatório.
- Nunca imprima token.
- Escreva a mensagem de commit no padrão do repositório e sem co-autor.
- Não faça merge.
- Faça um commit por item e dê push logo depois.
- Se este contexto ou o brief contradisser o código, não invente: faça o que for seguro e registre a pendência.
- Responda com no máximo 10 linhas, sem código e sem saída de comando, e grave o detalhe em <caminho do relatório>.
- Leia antes de agir: <ordem dos arquivos>.

## Return card

A resposta final traz estas linhas e termina na linha fixa de entrega do brief.

```
estado: feito | bloqueado | precisa decisão
premissa: <decisão tomada sozinho, ou nenhuma>
risco: <o que pode falhar, ou nenhum>
```

Feito exige a verificação do brief verde e o artefato publicado.
Sem isso, o estado é bloqueado.
