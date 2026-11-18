# DECISIONS

Append-only. Nunca edite uma linha antiga; se mudar de ideia, adicione uma linha nova que a substitui.

Serve para uma coisa: **auditar as premissas que você delegou sem ler conversa**. Se uma premissa daqui te incomoda, o conserto é o envelope de amanhã — não o filho de hoje.

Formato:

```
## <AAAA-MM-DD> · <projeto> · #<n>
decisão:    <o que foi decidido, 1 frase>
quem:       filho | hub | usuário
origem:     premissa | bloqueio respondido | regra do envelope
reversível: sim | não
custo de reverter: <baixo | médio | alto>
substitui:  <data · #n | —>
```

---

## Exemplo

## 2026-11-14 · connector-document-hub · #2
decisão: retry de upload com backoff exponencial em 3 tentativas, chunk de 5MB
quem: filho
origem: premissa
reversível: sim
custo de reverter: baixo
substitui: —

## 2026-11-14 · connector-document-hub · #2
decisão: limite de upload sobe de 20MB para 50MB
quem: usuário
origem: bloqueio respondido
reversível: não (contrato com cliente)
custo de reverter: alto
substitui: —
