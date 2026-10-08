# Semana 4 — Maintaining & Debugging Pipelines (10%) + Revisão Final

> Objetivo: fechar o último domínio (menor peso, mas tema que amarra tudo), fazer **revisão geral** dos 4 domínios e treinar com os **simulados cronometrados**.

### Competências cobradas (domínio 4)
- Context Propagation
- Debugging Pipelines
- Error Handling
- Schema Management

### Cronograma da semana
| Dia | Tema | Atividade |
|---|---|---|
| 1 | Debugging de pipelines e context propagation quebrada | Lab 4.1 |
| 2 | Error handling: retry, queue, backpressure, storage | Lab 4.2 |
| 3 | Schema Management e semantic conventions versionadas | Lab 4.3 |
| 4 | Revisão geral dos 4 domínios (cheatsheet) | Revisão |
| 5 | **Simulado 1** cronometrado + correção + caderno de erros | Simulado |
| 6 | **Simulado 2** + correção + revisar erros | Simulado |
| 7 | **Simulado 3** (pegadinhas) + repasse final | Simulado |

---

## Dia 1 — Debugging de pipelines

Quando telemetria "não chega", debugue **em camadas**:
```
App/SDK → (rede) → Collector receiver → processors → exporter → backend
```
Pergunte em cada ponto: *o dado chegou aqui?*

**Ferramentas de debug do Collector:**
- **`debug` exporter** (`verbosity: detailed`): imprime a telemetria no stdout. Primeira parada.
- **Métricas internas** (`:8888/metrics`): compare `otelcol_receiver_accepted_*` vs `otelcol_receiver_refused_*` vs `otelcol_exporter_sent_*` vs `otelcol_exporter_send_failed_*`.
- **zPages** (`:55679`): `tracez` (spans recentes), `servicez` (pipelines).
- **health_check** (`:13133`): o Collector está vivo?
- **pprof**: profiling de CPU/memória quando o Collector consome demais.
- **telemetria do próprio Collector** (`service.telemetry`): logs e métricas internas.

> 📎 Nomes exatos das métricas internas e um mapa **sintoma → onde olhar** estão nas seções 7 e 8 de [recursos/apendice-tecnico.md](../recursos/apendice-tecnico.md).

### Context propagation quebrada (o bug clássico distribuído)
Sintoma: traces "cortados" — serviço B abre um trace **novo** em vez de continuar o de A. Causas comuns:
- **Propagadores incompatíveis**: A usa W3C `tracecontext`, B espera `b3`. Headers não batem → extract falha → novo root span.
- Proxy/gateway que **remove** headers (`traceparent`, `b3`, `baggage`).
- Instrumentation library ausente num dos lados (não injeta/extrai).
- `OTEL_PROPAGATORS` divergente entre serviços.

Correção: alinhar `OTEL_PROPAGATORS` nos dois lados (ou usar composite), garantir que os headers passam pela infra.

### Lab 4.1 — Quebrar e consertar a propagação
1. Com os dois serviços A→B do Lab 2.5, configure `OTEL_PROPAGATORS=b3` em A e `tracecontext` em B.
2. Gere tráfego e confirme no Jaeger que os traces estão **quebrados** (A e B em traces separados).
3. Alinhe ambos para `tracecontext,baggage` e confirme a reunificação.
4. Use o `debug` exporter no Collector para inspecionar os TraceIds de cada lado.

**Entregável:** descreva como você diagnosticou a quebra usando os TraceIds.

---

## Dia 2 — Error Handling

O Collector precisa lidar com **backend indisponível**, picos de carga e falhas de rede sem perder tudo nem cair.

Mecanismos (cobrados):
- **memory_limiter**: evita OOM aplicando backpressure (recusa entrada quando a memória aperta).
- **sending_queue** (nos exporters): fila que desacopla ingestão da exportação.
  ```yaml
  exporters:
    otlp:
      endpoint: backend:4317
      sending_queue:
        enabled: true
        queue_size: 1000
      retry_on_failure:
        enabled: true
        initial_interval: 5s
        max_elapsed_time: 300s
  ```
- **retry_on_failure**: retenta com backoff exponencial quando o export falha.
- **file_storage extension** + `sending_queue` persistente: a fila sobrevive a **restart** do Collector (não perde dados em memória).
- **Backpressure** encadeada: exporter cheio → fila cheia → memory_limiter recusa → receiver sinaliza ao SDK → SDK pode retentar/dropar.

Trade-off central: **perder dados** (dropar) vs **consumir recursos** (bufferizar/persistir). O OTCA cobra que você entenda esse equilíbrio.

### Lab 4.2 — Resiliência a backend fora do ar
1. Configure `retry_on_failure` e `sending_queue` no exporter de traces.
2. Pare o Jaeger (`docker compose stop jaeger`) e gere tráfego.
3. Observe nas métricas (`:8888`) o `otelcol_exporter_send_failed_spans` subindo e a fila enchendo.
4. Suba o Jaeger de novo e veja o retry entregar o backlog.

**Entregável:** explique a diferença entre uma fila em memória e uma persistida com `file_storage`.

---

## Dia 3 — Schema Management

As **Semantic Conventions evoluem** (ex.: `http.method` virou `http.request.method`). Para não quebrar dashboards/alertas quando a convenção muda:

- **Schema URL**: cada telemetria pode carregar uma URL que identifica a **versão** das convenções que ela segue (ex.: `https://opentelemetry.io/schemas/1.x.y`).
- **Schema files / Telemetry Schema**: descrevem **transformações** entre versões (ex.: renomear atributo da v1.20 para v1.21).
- **schemaprocessor** (Collector): aplica essas transformações para **normalizar** telemetria de produtores em versões diferentes para uma versão alvo comum.

Por que importa: num ambiente real você tem apps instrumentadas em épocas diferentes; schema management mantém a telemetria **consistente e comparável** ao longo do tempo.

### Lab 4.3 — Conceitual + inspeção
1. No Jaeger, abra um span e localize o campo de **schema URL** (quando presente nos atributos do scope/resource).
2. Leia um trecho da página de Schemas da documentação oficial e anote: o que o schema URL versiona e como uma transformação de rename funciona.
3. (Opcional) Experimente o `schemaprocessor` na config apontando para um schema alvo.

**Entregável:** explique, com um exemplo de rename de atributo, por que schema URL evita quebrar dashboards.

---

## Dia 4 — Revisão geral (cheatsheet dos 4 domínios)

### D1 — Fundamentos (18%)
- **Sinais: traces, metrics, logs, profiles.** Baggage NÃO é sinal (é propagação de contexto).
- Span: Kind (SERVER/CLIENT/PRODUCER/CONSUMER/INTERNAL), Status, attrs, events, links.
- 6 instrumentos: Counter, UpDownCounter, Histogram, Gauge (síncrono) + Observable Counter/UpDownCounter/Gauge.
- Resource (quem) vs attributes (o quê). Semantic Conventions padronizam nomes.
- Instrumentação: manual / library / zero-code.

### D2 — API & SDK (46%) ⭐
- API = contrato (no-op sem SDK); SDK = implementação.
- Pipeline trace: Sampler → Span → SpanProcessor (Simple/Batch) → Exporter.
- Samplers: AlwaysOn/Off, TraceIdRatioBased, ParentBased. Padrão = ParentBased(root=AlwaysOn) = 100%.
- Métricas: Instrumento → View → MetricReader (periodic/pull) → Exporter.
- Propagação: inject/extract; W3C TraceContext (`traceparent`) é padrão; B3/Jaeger p/ interop.
- SpanContext imutável: TraceId, SpanId, TraceFlags, TraceState.
- Config: env vars padronizadas; agent = zero-code (javaagent, operator).

### D3 — Collector (26%)
- 5 componentes: receiver, processor, exporter, connector, extension.
- Nada ativa sem `service.pipelines`. Ordem: memory_limiter → ... → batch.
- Connector muda sinal (spanmetrics: trace→metric). OTTL em transform/filter.
- Deployment: agent vs gateway; gateway escala horizontalmente.
- tail_sampling exige spans do trace juntos → loadbalancing por traceID.

### D4 — Pipelines (10%)
- Debug: debug exporter, `:8888` métricas internas, zpages, health_check, pprof.
- Propagação quebrada = propagadores divergentes / headers removidos.
- Error handling: memory_limiter, sending_queue, retry_on_failure, file_storage.
- Schema management: schema URL versiona convenções; schemaprocessor transforma.

> Cheatsheets completas e glossário em [../recursos/README.md](../recursos/README.md).

---

## Dia 5, 6 e 7 — Simulados

Faça cada simulado **cronometrado**, sem consultar material (como no exame real):

- [Simulado 1](../simulados/simulado-1.md) — 30 questões, 45 min
- [Simulado 2](../simulados/simulado-2.md) — 30 questões (múltipla seleção), 45 min
- [Simulado 3](../simulados/simulado-3.md) — 30 questões (pegadinhas + avançado), 45 min
- [Gabaritos comentados](../simulados/gabaritos.md)

> Dica: o exame real é 90 min / ~60 questões. Depois de ir bem nos três, refaça o Simulado 1 + 2 em sequência num bloco único de 90 min para treinar o ritmo real.

**Rotina pós-simulado:**
1. Corrija pelo gabarito. Calcule sua % (meta ≥ 85%).
2. Toda questão errada → caderno de erros com o **porquê** e o conceito/domínio.
3. Volte à seção da semana correspondente ao erro e releia.
4. Refaça as questões erradas 2 dias depois.

### Quiz — Semana 4

1. Quais ferramentas o Collector oferece para debugar uma pipeline?
2. Qual a causa mais comum de traces "quebrados" entre serviços?
3. Para que serve `retry_on_failure` + `sending_queue` num exporter?
4. Como fazer uma fila sobreviver ao restart do Collector?
5. O que é o schema URL e qual problema ele resolve?
6. Qual métrica interna indica que o exporter está falhando ao enviar?
7. Explique a cadeia de backpressure quando o backend fica indisponível.

<details>
<summary><b>Gabarito Semana 4</b></summary>

1. `debug` exporter, métricas internas (`:8888`), zPages (`:55679`), `health_check` (`:13133`), `pprof`, e `service.telemetry`.
2. Propagadores incompatíveis entre serviços (ou headers de contexto removidos pela infra), fazendo o extract falhar e criar um novo root span.
3. Resiliência: a queue desacopla ingestão de exportação e o retry reenvia com backoff quando o backend falha, evitando perda imediata de dados.
4. Usar a `file_storage` extension com `sending_queue` persistente (fila em disco).
5. Uma URL que versiona qual versão das semantic conventions a telemetria segue; permite transformar/normalizar telemetria entre versões sem quebrar consumidores (dashboards/alertas).
6. `otelcol_exporter_send_failed_spans` (e equivalentes `_metric_points` / `_log_records`).
7. Exporter/queue enchem → memory_limiter recusa entrada → receiver sinaliza ao produtor → SDK aplica retry/drop conforme configurado.

</details>

🎓 Terminou os 4 domínios. Agora é simulado, caderno de erros e revisão até bater a meta. Boa prova!
