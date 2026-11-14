# Round context: <nome curto da rodada>

Este arquivo vale para todos os agentes da rodada e é a única fonte das regras comuns.

## Goal

<o resultado que o usuário pediu, em uma frase>

## Decision already made

<o comportamento final escolhido, sem alternativa em aberto>

## Contract between agents

<rotas, campos, formatos e códigos de erro acordados, quando dois agentes dependem um do outro>

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
- Responda com no máximo <8 a 12> linhas, sem código e sem saída de comando, e grave o detalhe em <caminho do relatório>.
- Leia antes de agir: <ordem dos arquivos>.
