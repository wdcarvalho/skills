# projects.example.md

> Copie para `projects.md` na raiz da skill e preencha. **Não versione o seu** — tem
> IDs de projeto e caminhos da sua máquina. Uma linha por projeto que o hub pode acionar.

```markdown
## <nome-do-projeto>
projectId:  <id do projeto no T3>   # obrigatório: faz o filho nascer no repo certo
repo:       /caminho/absoluto
base:       origin/develop          # branch de onde o worktree nasce
teste:      npm test && npm run lint && npm run typecheck
pr:         develop                 # branch alvo do PR
modelo:     forte                   # forte | rápido (ou fixe em SKILL.md)
fora de escopo padrão: migrations, infra, deploy

## operations
projectId:  <id>
repo:       /caminho/do/operations  # casa do trabalho sem repo: pesquisa, análise, texto
base:       main
teste:      nenhum — pronto = arquivo no lugar + retorno de 5 linhas
pr:         nenhum
modelo:     forte
fora de escopo padrão: publicar, comprar, gastar dinheiro, mexer em conta do usuário
```

Regras:

- `projectId` é o que faz o filho nascer no repo certo. Sem ele, o filho herda o projeto do hub.
- `base` é sempre a branch de onde o worktree nasce. Nunca `main` se o fluxo do repo usa `develop`.
- `teste` é o comando que o filho roda **antes** de dizer `feito`. Sem prova, o contrato não fecha.
- Projeto que não está aqui não é acionado. Adicione na hora, não no meio da task.
