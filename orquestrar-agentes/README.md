# Orchestrate Agents (orquestrar-agentes)

## What it does

A skill ensina a sessão principal, que usa um modelo caro, a planejar, especificar e verificar o trabalho.
Subagentes baratos executam a implementação, os testes, as revisões e as correções.
A sessão principal não executa código, não roda suíte, não faz commit, push nem PR.

## Why

O modelo caro custa mais e gasta contexto rápido quando recebe código e saída de comando.
Trabalho grande se perde quando um agente trava no meio, por isso ele é dividido em commits pequenos com push.
Um executor barato bem instruído entrega bem quando a decisão já vem escrita no brief.
Verificação independente achou defeito em toda rodada real, inclusive em código já mergeado.

## What is inside

| File | What it is for |
|---|---|
| `SKILL.md` | Regras de comportamento da sessão principal, papéis, ondas e regras de cada turno. |
| `templates/context.md` | Contexto único da rodada, com decisão, contratos, fatos e regras fixas. |
| `templates/agent-task.md` | Prompt curto enviado a cada agente, apontando para o contexto e o brief. |
| `templates/brief-implementation.md` | Brief de implementação, usado na fundação e nos pacotes paralelos. |
| `templates/brief-tester.md` | Brief de teste independente, feito por fora contra a decisão escrita. |
| `templates/brief-reviewer.md` | Brief de revisão por tema, com prova obrigatória para cada achado. |
| `templates/brief-correction.md` | Brief de correção, com a regra decidida para cada achado. |
| `templates/brief-closing-and-pr.md` | Brief do agente de fecho, que confere o código, documenta e abre o PR. |
| `templates/harness-feedback.md` | Formato do bloco `HARNESS_FEEDBACK`, em que o agente reporta atrito do harness. |
| `scripts/report.py` | Registra runs e blocos de atrito num SQLite local e agrega os atritos por fingerprint. Python 3, só biblioteca padrão. |
| `scripts/test_report.py` | Testes do `report.py` com `unittest`. |

## How to use

1. O usuário pede a orquestração e diz quais modelos usar.
2. Copie `templates/context.md` para a pasta de trabalho fora do repositório e preencha.
3. Para cada agente, escreva um brief a partir do modelo certo e envie `templates/agent-task.md` como prompt curto, apontando para o brief e para o contexto.
   Lance cada agente em worktree próprio, com o modelo explícito e registrando o ID dele, como na seção 11 do `SKILL.md`.
4. Lance as ondas na ordem da seção "Waves" do `SKILL.md`.
5. Rode a verificação independente antes de dar a entrega por pronta.
6. Lance as correções, separadas por tema.
7. Faça o fecho com o PR.
8. Entregue o resumo final.

## HARNESS_FEEDBACK (autoimprovement)

A skill melhora com o atrito que os agentes encontram ao usá-la.
Ao terminar, cada agente escreve até 3 blocos de texto puro na seção "Atritos do harness" do relatório:

```
HARNESS_FEEDBACK
alvo: skill|template|ferramenta|sandbox|config|contrato-saida|outro
ref: <arquivo ou nome, opcional>
obstaculo: <obrigatório, sem dado pessoal, segredo nem trecho de log>
contorno: <opcional, vazio se travou>
severidade: travou|contornou-caro|contornou-barato
FIM_HARNESS_FEEDBACK
```

Atrito do harness é brief ambíguo, template faltando ou quebrado, ferramenta, sandbox, configuração ou contrato de saída.
Defeito de produto vai em "Achados" e dúvida de negócio em "Pendências", nunca em bloco.
O agente nunca escreve o fingerprint: o parser calcula o hash de `alvo`, `ref` e `obstaculo` normalizados, de modo que "timeout de 30s", "300s" e "45 s" caem no mesmo grupo.
O parser mascara e-mail, CPF, CNPJ, telefone, dado bancário e token antes de truncar, descarta o bloco inválido inteiro e nunca lança exceção.
O bloco é contexto, não prova, e não muda o resultado da task.

### Banco e comandos

A sessão principal registra cada retorno em `~/.orquestrar-agentes/runs.sqlite`, num diretório 700 e com o arquivo 600.

```
python3 scripts/report.py init
python3 scripts/report.py add-run < run.json
python3 scripts/report.py add-feedback --run <id> --file <relatório>
python3 scripts/report.py atritos --since 30d --top 20 [--json]
python3 scripts/report.py mark-fixed <fingerprint> --ref <PR ou commit>
python3 scripts/report.py list-runs
```

O `atritos` agrupa por fingerprint e ordena pelos que mais se repetem, com a maior severidade vista, o total, o número de runs e o último run.
O `mark-fixed` marca como corrigido o que já está no banco, e o mesmo atrito que voltar entra como aberto e faz o grupo reaparecer como `open`.
Use `--db <caminho>` para apontar outro banco.

### Sempre ativo, com flag para desligar

O harness feedback não é uma fase de duas semanas: fica ativo por padrão em toda rodada.
A revisão dos atritos é recomendada e não bloqueia a coleta.
Para desligar, defina `ORQUESTRAR_HARNESS_FEEDBACK=0` (o padrão é `1`) ou passe `--no-harness-feedback` ao `add-feedback`.
Desligado, apague a seção "Harness feedback" e a linha `atrito` do `templates/context.md`: nenhum brief exige o bloco e o parser ignora o que vier, sem erro.

### Testes

```
cd orquestrar-agentes
python3 -m unittest scripts/test_report.py
```

## Example of a turn

Durante o trabalho: "Onda 2 concluída, fundação em commit e dois pacotes lançados em paralelo sem disputa de arquivo."
No fim: "Entregue em três itens, com uma pendência de ambiente real que depende de você."

## Limits

A skill não substitui a revisão humana.
Ela depende de modelos baratos capazes de seguir um brief bem escrito.
Ela não valida em ambiente real por si, e esse passo continua com quem entrega.
O `report.py` só registra e agrega: ele não decide nem corrige nada, e o atrito que ele mostra ainda precisa de leitura humana.
