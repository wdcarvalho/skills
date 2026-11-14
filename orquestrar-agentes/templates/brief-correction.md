# Correction brief: <tema>

Corrija sobre o commit <sha>, trazendo a branch antes de começar.
Leia nesta ordem: <contexto>, <lista de achados com a regra decidida>, <este brief>.
Arquivos seus: <lista>.
Não toque em arquivo de outro corretor que trabalha no mesmo tema ao lado.

## Findings and decided rule

- Achado <n>: <prova, arquivo e linha>.
  Regra: <comportamento final exigido>.
  Aceite: <teste que prova a correção>.
- Achado <n>: <prova, arquivo e linha>.
  Regra: <comportamento final exigido>.
  Aceite: <teste que prova a correção>.

## Order of work

1. Aplique o patch de testes de quem verificou em <caminho do patch> e rode.
2. Inverta o teste que passa afirmando o comportamento errado, antes de corrigir o produto.
3. Corrija o produto até o teste ficar verde.
4. Rode a verificação completa: <comandos, na ordem>.

## Limits

- Não enfraqueça teste: proibido remover asserção, afrouxar expectativa ou marcar como pulado.
- Ajuste o cenário que mudou por regra nova e liste esse ajuste na resposta.
- Não refatore fora do escopo do achado.
- Não escreva dado pessoal nem segredo em log, resposta ou relatório.
- Nunca imprima token.
- Faça um commit por item e dê push sem force.
- Não faça merge.

## Delivery

Relatório completo em <caminho do relatório>, com as seções "Pendências" e "Achados".
Resposta final com no máximo <8 a 12> linhas e, na última, branch <nome>, commit <sha>, push <ok ou rejeitado>.
