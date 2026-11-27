# Harness feedback

Use este bloco para reportar atrito do harness: o que na própria orquestração atrapalhou o seu trabalho.
O bloco é contexto para melhorar a skill, não prova, e não muda o resultado da sua task.

## When to write a block

Escreva um bloco quando o atrito vier do harness:

- brief ou contexto ambíguo, contraditório ou sem o dado que a tarefa pedia;
- template faltando, quebrado ou com instrução que não se aplica;
- ferramenta, sandbox ou configuração que travou ou obrigou a um contorno;
- contrato de saída (cartão, última linha, teto de linhas) impossível de cumprir como está escrito.

Não escreva bloco para:

- defeito do produto: ele vai em "Achados" do relatório;
- dúvida de negócio ou de regra: ela vai em "Pendências" ou na pergunta única do envelope de decisão.

## Format

Texto puro, uma chave por linha, no máximo 3 blocos.
Os blocos ficam no fim do relatório, na seção "Atritos do harness".
Na resposta final, escreva só a linha `atrito: <n> blocos no relatório` ou `atrito: nenhum`.

```
HARNESS_FEEDBACK
alvo: skill|template|ferramenta|sandbox|config|contrato-saida|outro
ref: <arquivo ou nome, opcional>
obstaculo: <obrigatório, sem dado pessoal, segredo nem trecho de log>
contorno: <opcional, vazio se travou>
severidade: travou|contornou-caro|contornou-barato
FIM_HARNESS_FEEDBACK
```

## Fields

| Chave | Regra |
|---|---|
| `alvo` | Uma das opções: `skill`, `template`, `ferramenta`, `sandbox`, `config`, `contrato-saida`, `outro`. |
| `ref` | Arquivo ou nome do que causou o atrito. Opcional, até 120 caracteres. |
| `obstaculo` | O que atrapalhou, em uma frase. Obrigatório, até 300 caracteres. |
| `contorno` | O que você fez para seguir. Opcional, vazio se travou. Até 300 caracteres. |
| `severidade` | `travou` se não conseguiu seguir, `contornou-caro` se o contorno custou tempo ou risco, `contornou-barato` se foi trivial. |

## Rules

- Nunca escreva `fingerprint`: o parser calcula.
- Nunca escreva dado pessoal, segredo, token nem trecho de log em nenhuma chave.
- Descreva o obstáculo de forma que o mesmo atrito, em outra rodada, produza o mesmo texto: sem número de linha, tempo medido nem caminho de worktree.
- Bloco com `alvo` ou `severidade` fora da lista, ou sem `obstaculo`, é descartado inteiro.
- A skill pode passar a ignorar o bloco: com `ORQUESTRAR_HARNESS_FEEDBACK=0` o contexto não pede o bloco e o parser não registra nada.

## Example

```
HARNESS_FEEDBACK
alvo: template
ref: templates/brief-closing-and-pr.md
obstaculo: o brief pede a URL do PR na última linha, mas não diz qual formato usar quando o PR já existe
contorno: atualizei o PR existente e usei o mesmo formato da última linha
severidade: contornou-barato
FIM_HARNESS_FEEDBACK
```
