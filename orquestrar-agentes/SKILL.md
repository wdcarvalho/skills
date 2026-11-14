---
name: orquestrar-agentes
description: Use quando o usuário pedir para orquestrar, coordenar ou delegar um trabalho grande a subagentes mais baratos, ou disser que o agente principal só planeja e não executa.
---

# Orchestrate Agents

## Main session behavior

Diagnostique, decida, especifique, leia relatórios e relance.
Não edite código, não rode suíte, não faça commit, push nem PR.
Escreva uma linha por turno enquanto o trabalho roda.
Entregue um único resumo curto no fim e encerre, sem tabela e sem progresso no meio.
Aponte o caminho do modelo em `templates/` em vez de copiar o texto dele.

## 1. Roles

Decida e escreva o brief, e deixe implementar, testar, revisar, corrigir e fechar para o executor.
Use modelo barato com esforço alto para implementar, testar, revisar e corrigir.
Use esforço baixo para tarefa mecânica, como editar texto de PR e commit simples.
Use um executor mais caro só quando apenas ele alcança uma ferramenta necessária, como um conector.
Leia do pedido quais modelos usar e não troque por conta própria.
Nunca repasse ao executor um problema sem a decisão já tomada.

## 2. Context economy

Nunca receba código nem saída de comando.
Exija resposta final de 8 a 12 linhas e o detalhe num arquivo de relatório.
Abra o relatório só para decidir, e só as seções de pendências e de achados, por `grep` do título.
Mantenha toda instrução longa em arquivo e o prompt do agente curto.
Envie ao agente o que ler, em que ordem, um resumo de três linhas e as regras inquebráveis.
Escreva uma vez o que vale para todos os agentes no arquivo de contexto comum.
Leia código só antes de escrever um brief, no trecho que define a regra, com número de linha.
Delegue diagnóstico amplo a um agente de levantamento de fatos.

## 3. Writing the brief

Assuma que o executor não raciocina bem sobre o que não está escrito.
Traga o problema com a evidência medida, o arquivo e a função.
Escreva a regra de cada item como comportamento final testável, com nomes de campo, valores padrão e códigos de erro.
Nunca escreva "melhore X".
Liste o critério de aceite por item, incluindo o caso hostil e o caso que não pode mudar.
Diga o que não fazer: arquivos reservados a outro agente, escopo proibido, o que não refatorar.
Dê os comandos de verificação na ordem.
Defina os entregáveis e o formato da resposta final, com teto de linhas e última linha fixa quando houver PR.
Inclua a saída de emergência: se o brief contradisser o código, faça o que for seguro e registre a pendência.
Escreva no contexto comum o contrato entre dois agentes que dependem um do outro, com rotas, campos e erros.

## 4. Waves

1. Levante fatos com agentes só de leitura: fluxo real, fins sem entrega, dependências e o que os testes não cobrem.
2. Entregue cada fato com arquivo e linha e sem proposta de solução, e decida em cima disso.
3. Feche a fundação antes de tudo: o que é transversal e os demais pacotes vão usar.
4. Lance os pacotes em paralelo com arquivos ou funções disjuntos, declarados no topo do brief.
5. Rode a verificação independente e depois as correções.
6. Deixe o fecho, com pendências pequenas, conferência completa e PR, para um agente só.
7. Lance em paralelo só o que não disputa arquivo.
8. Ponha em sequência o que disputa, ou mande o segundo fazer o item por último, depois de trazer a branch.

## 5. Verification by someone who did not write it

Nunca dê por pronto sem verificação independente, porque toda rodada real achou defeito, inclusive em código já mergeado.
Mande o testador testar por fora contra a decisão escrita, sem ver o trabalho de quem implementou.
Proíba o testador de alterar o produto e peça um patch só de testes e a tabela cenário, regra, passa ou falha.
Aceite teste vermelho por defeito do produto como resultado esperado.
Separe revisores por tema: segurança e dados pessoais, e qualidade e consistência.
Exija de cada achado a prova: teste curto ou caminho exato com arquivo e linha.
Peça ao revisor a tabela regra, onde o código cumpre, cumpre em todos os caminhos.
Mande o revisor procurar a regra aplicada num caminho e esquecida no outro, e a mesma coisa feita duas vezes.
Fixe testador e revisor num commit, não na ponta da branch que ainda recebe commits.

## 6. Corrections

Decida a regra de cada correção e não repasse o achado cru.
Separe as correções por tema para não haver dois agentes no mesmo trecho.
Mande o corretor aplicar o patch de testes de quem verificou como prova.
Inverta o teste que passa afirmando o comportamento errado antes de corrigir.
Proíba enfraquecer teste e mande listar o cenário que mudou por regra nova.
Corrija a regra no brief seguinte e diga isso ao corretor quando o defeito veio de um brief seu.

## 7. Work that is not lost

Peça um commit por item com push logo depois, para o agente que travar não perder o que fez.
Relance o agente travado ou interrompido com "continue de onde parou", apontando o que já está publicado e com um pedaço menor.
Mande dar push sem force quando houver agentes em paralelo na mesma branch.
Mande trazer a branch e manter as duas mudanças quando o push for rejeitado.
Mantenha contexto, briefs, relatórios e patches numa pasta de trabalho fora do repositório.
Grave o estado da rodada na memória persistente a cada onda: o que foi lançado, o que falta e onde estão os arquivos.
Confira o estado real de branches, PRs e checks antes de decidir depois de qualquer interrupção.

## 8. Fixed rules in every brief

Repita estas regras no arquivo de contexto e aponte esse arquivo em todo brief.
Trabalhe só no próprio worktree e nunca toque no checkout principal do usuário.
Não suba ambiente compartilhado: teste com dublês em memória.
Comece pelo teste que falha.
Não escreva dado pessoal nem segredo em log, resposta, documento ou relatório.
Nunca imprima token.
Escreva a mensagem de commit no padrão do repositório e sem co-autor.
Não faça merge.

## 9. Documentation and decisions

Mande cada pacote escrever a própria decisão: contexto, regras numeradas como ficaram no código, consequências e motivo.
Peça também a tabela do que pode ser ajustado: padrão, como mudar e quando rever.
Mande as decisões saírem em arquivos separados para não conflitar entre agentes paralelos.
Mande um agente de documentação montar os documentos no fim e conferir cada afirmação no código.
Trate o código como a verdade.

## 10. Each turn

Ao aviso de um agente, leia a resposta curta.
Leia só a seção de pendências ou de achados do relatório quando houver.
Decida, lance o próximo e termine o turno com uma linha.
Não faça polling nem espere, porque a conclusão do agente acorda a sessão.
Não refaça o que delegou e não confira à mão o que um agente de conferência confere.
No fim, resuma o que entrou com links, o que mudou de comportamento, o que depende do usuário e o que ficou em aberto.
Diga sem enfeite o que não foi validado em ambiente real.

## Templates

Use `templates/context.md` para o arquivo único de contexto da rodada.
Use `templates/agent-task.md` para o prompt curto enviado a cada agente, junto do brief da função.
Use `templates/brief-implementation.md` para a fundação e para os pacotes das ondas paralelas.
Use `templates/brief-tester.md` para a verificação funcional independente.
Use `templates/brief-reviewer.md` para a revisão por tema.
Use `templates/brief-correction.md` para as correções.
Use `templates/brief-closing-and-pr.md` para o agente de fecho.
