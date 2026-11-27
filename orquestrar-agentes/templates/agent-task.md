# Task: <função do agente>

Leia nesta ordem: <caminho do contexto>, <caminho do brief>, <arquivos de regra do repositório>.

Resumo em três linhas: <o que muda>, <onde muda>, <para quê>.

Brief completo em <caminho do brief>.
Relatório completo em <caminho do relatório>.

## Rules that must not be broken

- Trabalhe só no próprio worktree e nunca toque no checkout principal do usuário.
- Não suba ambiente compartilhado: sem container, banco ou serviço em execução, use dublês em memória.
- Comece pelo teste que falha.
- Não escreva dado pessoal nem segredo em log, resposta, documento ou relatório.
- Nunca imprima token.
- Escreva a mensagem de commit no padrão do repositório e sem co-autor.
- Não faça merge.
- Faça um commit por item e dê push logo depois.
- Não edite nada fora dos arquivos declarados no brief.
- Se o brief contradisser o código, não invente: faça o que for seguro e registre a pendência.

## Final answer

Responda com no máximo 10 linhas, sem código e sem saída de comando, no cartão de retorno do contexto.
Grave o detalhe no relatório, com as seções "Pendências" e "Achados" sempre presentes.
Última linha: <formato fixo, por exemplo: branch <nome>, commit <sha>, push ok>.
