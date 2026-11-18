# Child Brief

Preenchido pelo hub, um por filho. Máx. 40 linhas. Substituir `<...>`.

---

## 0. Config de lançamento

```
runtimeMode: full-access   # OBRIGATÓRIO e igual ao do hub; com auto o filho não consegue t3_thread_send ao hub
isolation:   worktree      # obrigatório para implementação
base:        origin/develop
modelo:      claude-sonnet-5-5 · effort medium   # padrão; só muda se o usuário pedir
```

> Motivo: `approval-required` transforma cada comando em ping. O hub **não** pode aprovar por você. Approval não se roteia — se elimina.

---

## 1. Contexto

- **Projeto:** `<nome>`
- **Repo / worktree:** `<path>`
- **Task:** `<uma frase imperativa>`
- **Entregável:** `<PR | branch | relatório | correção>`
- **Fora de escopo:** `<o que não é para tocar>`

---

## 2. Envelope de decisão

### DECIDA SOZINHO — reversível, dentro do escopo

- nomes de variáveis, arquivos, funções
- ordem de implementação, refactor interno
- biblioteca já presente no repo
- estrutura de teste, fixtures, mocks
- mensagens de erro e log
- detalhes de formatação e estilo

### PERGUNTE — pare e retorne `bloqueado`, **uma** pergunta só

- muda contrato público de API
- exige credencial ou acesso que você não tem
- escolha entre dois comportamentos de produto
- conflita com decisão já registrada em `DECISIONS.md`

### NUNCA — violação = tarefa falhou

- merge, push em `main`/`develop`, force push
- alterar arquivo fora do repo/worktree
- deletar branch, drop de dados, migração destrutiva
- instalar dependência global
- comando que gasta dinheiro
- reabrir task já fechada por outro filho

---

## 3. Regra de não-bloqueio

Ambiguidade de **implementação** → escolha a opção mais simples e reversível, registre em `DECISIONS.md`, marque `premissa:` no retorno. Não pare.

Só bloqueia o que está na lista **PERGUNTE**. Uma pergunta, não três.

---

## 4. Definição de pronto

- [ ] testes novos cobrindo o comportamento
- [ ] lint + typecheck verdes
- [ ] CI verde
- [ ] PR aberto (não mergeado) ou artefato no lugar
- [ ] `DECISIONS.md` atualizado, se houve decisão
- [ ] retorno no formato da seção 5

> "Feito" sem CI verde é opinião.

---

## 5. Retorno — máx. 10 linhas

```
projeto:
task:
estado: feito | bloqueado | precisa decisão
artefato: PR #<n> | branch <nome> | nenhum
premissa: <decisão que você tomou sozinho>
decisão pendente: <1 frase, sim/não — só se bloqueado>
risco:
```

---

## 6. Entrega ao hub — último ato de cada turno

**Todo turno termina com o `t3_thread_send` para o hub.** Não só quando a task acabar:

- task concluída, bloqueada ou precisa decisão → cartão da seção 5
- vai continuar em outro turno (hub ou usuário mandou algo depois) → cartão com `estado: rodando` e uma linha do que falta

```
t3_thread_send({ threadId: "<HUB_THREAD_ID>", message: "<cartão da seção 5>" })
```

**Prosa não é entrega.** Se você escreveu texto longo como resposta, o que vai ao hub é o cartão — o hub não lê prosa.

Turno que termina sem send deixa o trabalho invisível: o hub não acorda, não settle, e a linha do STATE fica `rodando` para sempre. Não é o último passo "da tarefa" — é o último passo **de cada turno**.

---

## 7. Não faça

- não peça confirmação para o que está em **DECIDA SOZINHO**
- não faça mais de uma pergunta
- não reporte progresso intermediário
- não toque em outro projeto que não o seu
- não abra PR em `main`

---

## 8. Ao abrir PR

- Use a skill **`pr-format`** para título e descrição (padrão Ademicon).
- Depois de abrir, use **`copilot-pr-loop`**: lê a review do Copilot e zera medium/high. Máximo 3 rodadas.
- **Não** use `pr-pipeline` nem `quality-gate`: são caros e rodam e2e.
- Se a skill não existir no seu harness, siga sem ela e registre no retorno:
  `premissa: pr-format/copilot-pr-loop indisponíveis neste harness`.

---

## Exemplo preenchido

```
## 1. Contexto
- Projeto: connector-document-hub
- Repo / worktree: /w/proj-a
- Task: corrigir timeout no upload de PDF > 20MB
- Entregável: PR
- Fora de escopo: fila de reprocessamento, antifraude

## 2. Envelope
DECIDA: onde fica o retry, tamanho do chunk, nome do módulo
PERGUNTE: se o limite de 20MB muda para o cliente
NUNCA: merge, push em develop, migração
```

Retorno esperado:

```
projeto: connector-document-hub
task: timeout upload PDF > 20MB
estado: feito
artefato: PR #412
premissa: retry com backoff em 3 tentativas, chunk 5MB
decisão pendente: —
risco: cliente com PDF de 80MB pode estourar timeout de novo
```
