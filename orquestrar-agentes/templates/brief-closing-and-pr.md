# Closing and PR brief: <nome da entrega>

Você é o único agente do fecho e responde por tudo que vai no PR.
Leia nesta ordem: <contexto>, <todos os briefs e relatórios da rodada>, <este brief>.

## Before opening the PR

- Traga a branch e confira que ela está atualizada com a base <base>.
- Rode a verificação completa: <comandos, na ordem>.
- Confira cada afirmação dos documentos de decisão no código, porque o código é a verdade.
- Corrija divergência de documento no próprio documento.
- Feche as pendências pequenas listadas em <caminho das pendências>.
- Monte os documentos finais a partir dos arquivos de decisão separados, sem perder item.

## The PR

- Título no padrão do repositório: <padrão>.
- Descrição com o que mudou de comportamento, o que depende do usuário e o que ficou em aberto.
- Diga no texto o que não foi validado em ambiente real.
- Linked a issue <referência> quando o repositório exigir.
- Nenhum dado pessoal, segredo ou token no título, no corpo ou nos anexos.

## Limits

- Não faça merge.
- Não use force push.
- Não amplie escopo: pendência grande vira item em aberto, não correção de última hora.
- Não escreva dado pessoal nem segredo em log, resposta ou relatório.
- Nunca imprima token.
- Se algo contradisser o código, não invente: faça o que for seguro e registre a pendência.

## Delivery

Relatório completo em <caminho do relatório>, com as seções "Pendências" e "Achados".
Resposta final com no máximo <8 a 12> linhas.
Última linha: URL do PR, head <sha>, checks e reviews <estado>.
