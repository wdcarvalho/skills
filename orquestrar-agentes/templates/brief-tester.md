# Independent tester brief: <nome do pacote>

Trabalhe no commit <sha>, que não recebe mais commits.
Leia nesta ordem: <contexto>, <decisão escrita>, <este brief>.
Não leia o trabalho de quem implementou e não pergunte a ele o que fazer.
Teste pelo lado de fora, contra a decisão escrita, não contra o código.

## What to test

- <regra 1: entrada, saída esperada e código de erro>
- <regra 2: entrada, saída esperada e código de erro>
- Caso hostil: <entrada e condição de contorno>.
- Caso que não pode mudar: <comportamento existente>.

## Limits

- Não altere o produto, nem código, nem configuração.
- Entregue apenas um patch de testes em <caminho do patch>.
- Não escreva dado pessoal nem segredo em teste, log ou relatório.
- Nunca imprima token.
- Se a decisão escrita contradisser o código, não invente: registre a divergência e teste o que a decisão manda.
- Não faça merge.

## Delivery

Tabela com cenário, regra, passa ou falha, para cada caso.
Liste o teste vermelho por defeito do produto como resultado esperado, não como erro seu.
Relatório completo em <caminho do relatório>, com as seções "Pendências" e "Achados".
Resposta final com no máximo <8 a 12> linhas e, na última, o caminho do patch e a contagem de falhas.
