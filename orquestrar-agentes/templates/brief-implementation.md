# Implementation brief: <nome do pacote>

Leia nesta ordem: <contexto>, <este brief>, <arquivos de regra>.
Resumo em três linhas: <o que muda>, <onde muda>, <para quê>.

## Owner of this package

Arquivos e funções seus: <lista>.
Não edite nada fora desta lista, porque outro agente é dono do resto.

## Item <n>: <nome do item>

Problema: <fato medido, arquivo e linha>.
Regra: <comportamento final em frases testáveis, com nomes de campo, valores padrão e códigos de erro>.
Aceite: <casos de teste, incluindo o caso hostil e o caso que não pode mudar>.
Não pode mudar: <comportamento existente que deve continuar igual>.
Verificação: <comandos, na ordem>.

## Item <n>: <nome do item>

Problema: <fato medido, arquivo e linha>.
Regra: <comportamento final em frases testáveis, com nomes de campo, valores padrão e códigos de erro>.
Aceite: <casos de teste, incluindo o caso hostil e o caso que não pode mudar>.
Não pode mudar: <comportamento existente que deve continuar igual>.
Verificação: <comandos, na ordem>.

## Decision of this package

Escreva a decisão em <caminho do arquivo de decisão>, com contexto, regras numeradas como ficaram no código, consequências e motivo.
Acrescente a tabela do que pode ser ajustado: padrão, como mudar, quando rever.
Não edite documentos que outro agente também edita.

## What not to do

- <arquivo reservado a outro agente>
- <escopo proibido>
- <refatoração vetada>
- Não faça merge.
- Não altere arquivos de orquestração.
- Se este brief contradisser o código, não invente: faça o que for seguro e registre a pendência.

## Final answer

No máximo 10 linhas, sem código e sem saída de comando.
Relatório completo em <caminho do relatório>, com as seções "Pendências" e "Achados".
Última linha: branch <nome>, commit <sha>, push <ok ou rejeitado>.
