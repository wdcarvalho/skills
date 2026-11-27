# Reviewer brief: <tema>

Trabalhe no commit <sha>, que não recebe mais commits.
Leia nesta ordem: <contexto>, <decisão escrita>, <este brief>.
Só leia e reporte: não altere código, teste, configuração nem documento.

## Theme

<tema: segurança e dados pessoais, ou qualidade e consistência>
Regras do tema que precisam de prova:
- <regra 1>
- <regra 2>

## What to hunt for

- A regra aplicada num caminho e esquecida no outro, quando vários agentes escreveram em paralelo.
- A mesma coisa feita duas vezes, em pontos diferentes.
- <risco específico do tema, com o arquivo e a função onde olhar>
- <superfície de entrada que chega sem validação>

## Required proof

Cada achado precisa de prova: teste curto ou caminho exato com arquivo e linha.
Sem prova, não reporte.
Monte a tabela regra, onde o código cumpre, cumpre em todos os caminhos.
Marque cada caminho como coberto, descoberto ou não aplicável.

## Limits

- Não escreva dado pessoal nem segredo no relatório.
- Nunca imprima token.
- Se a decisão escrita contradisser o código, não invente: registre a divergência.
- Não faça merge.

## Delivery

Relatório completo em <caminho do relatório>, com as seções "Pendências" e "Achados".
Resposta final com no máximo 10 linhas e, na última, a contagem de achados por severidade.
