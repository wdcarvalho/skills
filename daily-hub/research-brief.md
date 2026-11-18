# Research Brief

Para trabalho que **não termina em PR**: pesquisa, comparação, análise, plano, texto, automação pessoal.

Vai para o projeto `operations`. Máx. 25 linhas.

---

## 0. Config de lançamento

```
target:  { projectId: "<projectId do operations, de projects.md>" }
role:    research
isolation: shared      # não é código; não precisa de worktree
mode:    async
```

---

## 1. Pergunta

- **Pergunta:** `<uma frase — o que precisa estar decidido no fim>`
- **Entregável:** `<arquivo em operations/research/ | operations/entregaveis/>`
- **Para quê:** `<a decisão que este documento habilita>`
- **Fora de escopo:** `<o que não investigar>`

Se a pergunta não cabe em uma frase, ela são duas pesquisas.

---

## 2. Envelope de decisão

### DECIDA SOZINHO

- quais fontes consultar, em que ordem
- profundidade de cada fonte
- formato e tamanho do documento
- o que descartar por ser irrelevante ou desatualizado

### PERGUNTE — pare e retorne `bloqueado`, uma pergunta só

- a pergunta mudou de escopo no meio
- exige acesso pago, login ou dado que você não tem
- duas fontes confiáveis se contradizem em algo que muda a decisão

### NUNCA

- publicar, postar, comprar, assinar, criar conta
- executar a recomendação (só recomendar)
- usar fonte sem data ou sem autor quando o dado for numérico
- entregar “depende” sem default

---

## 3. Orçamento — parte do contrato

- **máximo 12 fontes** ou **45 minutos**, o que vier primeiro.
- Se não decidir com 12 fontes, o problema é a pergunta, não a pesquisa: pare e devolva `bloqueado`.
- Proibido abrir a mesma fonte duas vezes. Se precisou, registre o trecho na primeira.

---

## 4. Definição de pronto

- [ ] documento no lugar, com data e fontes
- [ ] cada número tem fonte e ano
- [ ] termina com **1 recomendação** e o custo dela
- [ ] retorno no formato da seção 5

---

## 5. Retorno — máx. 5 linhas

```
pergunta:
achado: <a resposta em 1 frase>
fonte: <2 principais, com ano>
decisão que habilita: <o que você pode fazer agora>
custo/risco: <dinheiro, tempo, dependência>
```

---

## 5b. Entrega ao hub — último ato de cada turno

**Todo turno termina com o `t3_thread_send` para o hub.** Não só quando a pesquisa acabar:

- pesquisa concluída, bloqueada ou precisa decisão → retorno da seção 5
- vai continuar em outro turno → retorno com `estado: rodando` e uma linha do que falta

```
t3_thread_send({ threadId: "<HUB_THREAD_ID>", message: "<retorno da seção 5>" })
```

**Prosa não é entrega.** Turno que termina sem send deixa o trabalho invisível: o hub não acorda, não settle, e a linha do STATE fica `rodando` para sempre. É o último passo **de cada turno**, não "da tarefa".

## 6. Não faça

- não narre a pesquisa no hub
- não entregue 3 opções sem escolher default
- não cole transcrição de página
- não ultrapasse o orçamento "porque estava quase"
