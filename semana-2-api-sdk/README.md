# Semana 2 — The OpenTelemetry API and SDK (46%)

> **Este é o domínio mais importante da prova — quase metade das questões.** Dedique a semana inteira. O foco é entender a separação **API vs SDK**, o data model, os três sinais no nível de SDK, as **pipelines de processamento**, **propagação de contexto** e **configuração**.

### Competências cobradas
- Data Model
- Composability and Extension
- Configuration
- Signals (Tracing, Metric, Log)
- SDK Pipelines
- Context Propagation
- Agents

### Mapa mental da semana

Se a prova te perguntasse: "o que faz cada peça do SDK do OpenTelemetry?", a resposta curta é esta:

```text
Application code
      │
      ├── API: describe intent ("quero um span", "quero uma métrica")
      │
      └── SDK: decide como collect / sample / export / batch / propagate
               │
               ├── Sampler → decide se o trace entra ou não
               ├── SpanProcessor → observa onStart/onEnd
               ├── Exporter → envia para OTLP/Console/Backend
               ├── MetricReader → coleta dados de métricas
               └── Propagator → serializa contexto entre processos
```

> **Regra de ouro:** a API é o “contrato”. O SDK é a “máquina que resolve a entrega”.

### 3 regras de ouro para memorizar

1. **API sem SDK = no-op**. O código não quebra, mas também não emite telemetria.
2. **TraceContext é o padrão**. Se o header `traceparent` não passa, o sistema perde a continuidade do trace.
3. **Padrão de produção é Batch**. `batch` é mais eficiente do que `simple` em ambientes reais.

### Mini flashcards de revisão

- **Q:** O que o `TracerProvider` faz?  
  **A:** Cria tracers e define o pipeline de spans, resource e processamento do trace.

- **Q:** Qual a diferença entre `inject` e `extract`?  
  **A:** `inject` escreve o contexto no carrier; `extract` lê de volta no outro processo.

- **Q:** Por que `ParentBased` é tão importante?  
  **A:** Porque ele evita traces quebrados e mantém consistência de amostragem.

- **Q:** Qual reader geralmente entra no Prometheus?  
  **A:** O `Pull` / Prometheus reader, que expõe `/metrics` para scrape.

### Armadilha da prova mais comum

- **“Baggage não é sinal.”**
- **“ParentBased root default é AlwaysOn.”**
- **“BatchSpanProcessor não é só otimização; ele também reduz overhead de export.”**
- **“View pode mudar a cardinalidade e a agregação sem mexer no código da app.”**

### Cronograma da semana
| Dia | Tema | Lab |
|---|---|---|
| 1 | API vs SDK; composability; data model | Lab 2.1 |
| 2 | Tracing: TracerProvider → pipeline → exporter | Lab 2.2 |
| 3 | Sampling (head-based) e Span Processors | Lab 2.3 |
| 4 | Metrics: MeterProvider, views, readers, exporters | Lab 2.4 |
| 5 | Logs: LoggerProvider; Context Propagation | Lab 2.5 |
| 6 | Configuration + Agents + Revisão + Quiz | Quiz |

---

## Dia 1 — API vs SDK (a distinção mais cobrada)

**API** e **SDK** são separados **de propósito**:

| | API | SDK |
|---|---|---|
| O que é | Interface/contrato | Implementação concreta |
| Quem usa | Código da aplicação **e bibliotecas** | A aplicação (no startup) |
| Se não configurado | Vira **no-op** (não quebra) | — |
| Decide | *o que* medir | *como* processar/exportar/amostrar |

Ponto-chave: uma **biblioteca** instrumentada depende **só da API**. Se a aplicação final não instalar/configurar o SDK, a API é **no-op** (não gera telemetria, mas também não quebra nada). Isso permite instrumentar bibliotecas sem forçar overhead a quem não quer telemetria.

### Providers (ponto de entrada de cada sinal)
- **TracerProvider** → cria `Tracer`s → criam `Span`s
- **MeterProvider** → cria `Meter`s → criam instrumentos (Counter, etc.)
- **LoggerProvider** → cria `Logger`s → emitem `LogRecord`s

A aplicação configura os Providers (SDK) **uma vez no startup**. Depois, código e bibliotecas pegam tracers/meters/loggers globais.

### Composability and Extension
O SDK é feito de peças plugáveis que você **compõe**:
- **Samplers** (quais traces manter)
- **SpanProcessors** (o que fazer com spans que começam/terminam)
- **Exporters** (para onde enviar)
- **MetricReaders** + **Views** + **Aggregations**
- **Propagators** (como contexto cruza processos)
- **Resource** (atributos da entidade)

Você pode escrever componentes **customizados** (ex.: um exporter próprio) porque tudo é definido por interfaces.

### Data Model
Cada sinal tem um data model definido pela spec e representado no OTLP:
- **Trace**: Resource → ScopeSpans (InstrumentationScope) → Spans.
- **Metric**: Resource → ScopeMetrics → Metrics (com data points e temporality/aggregation).
- **Log**: Resource → ScopeLogs → LogRecords.
- **InstrumentationScope**: nome/versão do instrumentador (ex.: a lib que criou o tracer). Diferente do Resource (que é o serviço).

### Lab 2.1 — API no-op
1. Num script Python, use **só a API** sem configurar SDK:
   ```python
   from opentelemetry import trace
   tracer = trace.get_tracer("teste")
   with tracer.start_as_current_span("sem-sdk") as span:
       print("span válido?", span.get_span_context().is_valid)
   ```
2. Rode. Note que **não quebra** e nada é exportado (TraceId zerado / inválido = no-op).
3. Agora rode via `opentelemetry-instrument` (SDK configurado) e veja a diferença.

**Entregável:** explique o que muda quando o SDK está presente.

---

## Dia 2 — Tracing SDK e a pipeline

Fluxo de um span no SDK:
```
Tracer.start_span()
     │
     ▼
  Sampler  ── decide: RecordAndSample / RecordOnly / Drop
     │
     ▼
  Span (ativo)  ──► SpanProcessor.onStart()
     │ (aplicação adiciona attrs/events)
     ▼
  span.end()  ──► SpanProcessor.onEnd()
                      │
                      ▼
                  Exporter ──► OTLP / backend
```

**Resource** é anexado pelo TracerProvider a todos os spans.

### SpanProcessors (muito cobrado)
| Processor | Comportamento | Uso |
|---|---|---|
| **SimpleSpanProcessor** | exporta **cada span imediatamente** ao terminar | debug/dev; ineficiente em prod |
| **BatchSpanProcessor** | agrupa spans e exporta em lotes | **padrão de produção** |

BatchSpanProcessor tem parâmetros: `maxQueueSize`, `scheduledDelay`, `maxExportBatchSize`, `exportTimeout`.

### Exporters do SDK
- **OTLP** (gRPC ou HTTP) — padrão, envia para Collector/backend.
- **Console/Logging** — stdout, para debug.
- Exporters específicos de backend (via SDK ou, idealmente, deixe o Collector fazer isso).

### Lab 2.2 — Montar a pipeline manualmente (Python)
```python
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor, ConsoleSpanExporter
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter

resource = Resource.create({"service.name": "lab-manual"})
provider = TracerProvider(resource=resource)
provider.add_span_processor(BatchSpanProcessor(ConsoleSpanExporter()))
provider.add_span_processor(
    BatchSpanProcessor(OTLPSpanExporter(endpoint="http://localhost:4318/v1/traces"))
)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("lab")
with tracer.start_as_current_span("op-raiz") as parent:
    parent.set_attribute("etapa", "inicio")
    with tracer.start_as_current_span("op-filha"):
        pass
provider.shutdown()  # flush
```
Rode e confirme: spans no **console** E no **Jaeger** (dois processors, dois destinos).

**Entregável:** troque `BatchSpanProcessor` por `SimpleSpanProcessor` e descreva a diferença de comportamento.

---

## Dia 3 — Sampling (head-based) e decisões

**Head-based sampling** (no SDK): a decisão de amostrar é tomada **no início do trace**, no serviço de origem, e propagada via trace flags. (Tail sampling, decidido no fim e no Collector, é tema da Semana 3.)

Samplers padrão (muito cobrado):
| Sampler | Comportamento |
|---|---|
| `AlwaysOn` | amostra tudo |
| `AlwaysOff` | não amostra nada |
| `TraceIdRatioBased` | amostra uma fração (ex.: 10%) baseada no TraceId |
| `ParentBased` | respeita a decisão do **span pai**; usa um sampler "root" quando não há pai |

**O padrão (default) do SDK é `ParentBased(root=AlwaysOn)`** — ou seja, `parentbased_always_on`, que amostra **100%** dos traces. O `ParentBased` respeita a decisão do pai e, quando não há pai (root span), usa o sampler `root` configurado. É o padrão recomendado porque mantém o trace **consistente** entre serviços: se o pai foi amostrado, o filho também é.

> ⚠️ **Pegadinha:** dizer que "ParentBased" é o padrão, sozinho, é incompleto — ParentBased **exige** um sampler root. O padrão da spec é ParentBased **com root AlwaysOn**. Para amostrar 10%, você compõe `ParentBased(root=TraceIdRatioBased(0.1))` (via env: `OTEL_TRACES_SAMPLER=parentbased_traceidratio` + `OTEL_TRACES_SAMPLER_ARG=0.1`).

Resultado da decisão do sampler:
- `RECORD_AND_SAMPLE` — grava e exporta (sampled flag = 1)
- `RECORD_ONLY` — grava localmente mas não exporta
- `DROP` — não grava

### Lab 2.3 — Sampling
1. Configure via env var (zero-code):
   ```powershell
   $env:OTEL_TRACES_SAMPLER = "parentbased_traceidratio"
   $env:OTEL_TRACES_SAMPLER_ARG = "0.25"   # 25%
   ```
2. Gere ~40 requisições e conte quantos traces aparecem no Jaeger (~25%).
3. Troque para `always_on` e repita; compare.

**Entregável:** explique por que ParentBased evita "traces quebrados" (spans faltando no meio).

---

## Dia 4 — Metrics SDK

Fluxo:
```
Instrumento (Counter/Histogram/...) 
      │ measurement
      ▼
     View  ── (opcional) renomeia, filtra attrs, muda aggregation
      ▼
  MetricReader  ── periódico (push) ou on-demand (pull)
      ▼
  MetricExporter ──► OTLP / Prometheus
```

**MeterProvider** (SDK) é configurado com Resource + Readers + Views.

### MetricReader (cobrado)
- **PeriodicExportingMetricReader**: coleta e exporta a cada intervalo (push, ex.: para OTLP).
- **Pull/Prometheus**: expõe um endpoint `/metrics` para o Prometheus fazer scrape.

### Views (cobrado)
Uma **View** customiza um instrumento sem mudar o código:
- renomear a métrica
- selecionar/dropar atributos (controle de **cardinalidade**!)
- trocar a aggregation (ex.: definir buckets de histogram)
- dropar o instrumento inteiro

### Aggregation e Temporality
- **Aggregation**: Sum, LastValue, ExplicitBucketHistogram, etc.
- **Temporality**: `cumulative` (padrão para Prometheus) vs `delta` (comum para alguns backends).

### Lab 2.4 — Métricas custom
```python
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.http.metric_exporter import OTLPMetricExporter

reader = PeriodicExportingMetricReader(
    OTLPMetricExporter(endpoint="http://localhost:4318/v1/metrics"),
    export_interval_millis=5000,
)
metrics.set_meter_provider(MeterProvider(metric_readers=[reader]))

meter = metrics.get_meter("lab")
pedidos = meter.create_counter("pedidos_total", unit="1", description="pedidos processados")
latencia = meter.create_histogram("pedido_duracao_ms", unit="ms")

import time, random
for _ in range(100):
    pedidos.add(1, {"tipo": random.choice(["web", "api"])})
    latencia.record(random.uniform(5, 300), {"tipo": "web"})
    time.sleep(0.2)
```
No Prometheus (`:9090`) procure `pedidos_total` e `pedido_duracao_ms_bucket`.

**Entregável:** descreva como uma View poderia reduzir a cardinalidade removendo o atributo `tipo`.

---

## Dia 5 — Logs SDK e Context Propagation

### Logs no SDK
- **LoggerProvider** + **LogRecordProcessor** (Simple/Batch) + **LogExporter** (espelha o modelo de traces).
- A estratégia principal é o **log appender/bridge**: conectar o logging nativo da linguagem ao OTel, anexando automaticamente **TraceId/SpanId** aos logs emitidos dentro de um span → correlação log↔trace.

### Context Propagation (MUITO cobrado)
**Context** é um container imutável que carrega valores (como o span ativo e o baggage) **dentro do processo**. **Propagators** serializam/desserializam esse contexto **entre processos** (via headers HTTP, por exemplo).

Fluxo distribuído:
```
Serviço A (span ativo)
   │ inject() → escreve headers (ex.: traceparent)
   ▼ HTTP request com headers
Serviço B
   │ extract() → lê headers → recria o SpanContext remoto
   ▼
   novo span filho continua o MESMO trace
```

**Propagadores (formatos) — saber diferenciar:**
| Propagador | Formato / headers |
|---|---|
| **W3C TraceContext** | `traceparent`, `tracestate` — **padrão do OTel** |
| **W3C Baggage** | header `baggage` |
| **B3** | headers `b3` (ou `X-B3-*`) — comum em Zipkin |
| **Jaeger** | header `uber-trace-id` |

O padrão do OTel é **TraceContext + Baggage**. Você pode compor múltiplos propagadores (ex.: para interoperar com um sistema B3 legado) via **CompositePropagator**.

**SpanContext** (o que é propagado): TraceId, SpanId, **TraceFlags** (inclui o sampled bit), **TraceState**, e flag `remote`. É **imutável** e serializável — diferente do Span (que é o objeto mutável local).

### Lab 2.5 — Propagação entre dois serviços
1. Suba dois Flask (`A` na 8080 chamando `B` na 8081), ambos com `opentelemetry-instrument`.
2. Faça `A` chamar `B` via `requests` (a instrumentation lib injeta `traceparent` automaticamente).
3. No Jaeger, confirme **um único trace** com spans de A **e** B.
4. Force `OTEL_PROPAGATORS=b3` nos dois e repita; depois teste `tracecontext,baggage`.

**Entregável:** mostre o header `traceparent` capturado e explique seus campos (version-traceid-spanid-flags).

> 📎 Aprofunde em [recursos/apendice-tecnico.md](../recursos/apendice-tecnico.md): seção 1 (OTLP, portas 4317/4318 e paths `/v1/*`) e seção 2 (anatomia byte a byte do `traceparent`).

---

## Dia 6 — Configuration, Agents, Revisão + Quiz

### Configuration (cobrado)
Duas formas principais:
1. **Variáveis de ambiente** (padronizadas pela spec): portáteis entre linguagens.
   | Env var | Função |
   |---|---|
   | `OTEL_SERVICE_NAME` | define `service.name` |
   | `OTEL_RESOURCE_ATTRIBUTES` | resource attrs extras |
   | `OTEL_EXPORTER_OTLP_ENDPOINT` | destino OTLP |
   | `OTEL_EXPORTER_OTLP_PROTOCOL` | `grpc` / `http/protobuf` |
   | `OTEL_TRACES_SAMPLER` / `..._ARG` | sampler e parâmetro |
   | `OTEL_PROPAGATORS` | lista de propagadores |
   | `OTEL_TRACES_EXPORTER` / `OTEL_METRICS_EXPORTER` / `OTEL_LOGS_EXPORTER` | exporters |
   | `OTEL_SDK_DISABLED` | desliga o SDK |
2. **Programática** (no código, no startup) — mais controle.
3. **Declarative Configuration** (file-based, YAML) — formato emergente para configurar o SDK via arquivo, análogo ao do Collector.

### Agents
"Agent" aqui = o processo/mecanismo que faz instrumentação **zero-code**:
- **Java agent** (`-javaagent:opentelemetry-javaagent.jar`): injeta bytecode em runtime, sem recompilar.
- **Python** `opentelemetry-instrument`, **Node** `--require @opentelemetry/auto-instrumentations-node/register`.
- **OpenTelemetry Operator** (Kubernetes): injeta o agent/SDK automaticamente nos pods via annotations.

Diferencie **agent (zero-code, lado da aplicação)** do **Collector agent** (um deployment do Collector perto da app — tema da Semana 3). Não confunda.

### Gestão e tipos de agentes (saiba que existem)
- **OpAMP** (Open Agent Management Protocol): protocolo para **gerenciar agentes/collectors remotamente** — enviar configuração, atualizar, monitorar saúde e versão de uma frota de agentes de forma centralizada. É a resposta do OTel para "como opero centenas de collectors/agents".
- **eBPF instrumentation**: instrumentação a nível de kernel, zero-code, que captura telemetria (ex.: spans de rede/HTTP) **sem tocar na aplicação nem na linguagem**. Útil para linguagens difíceis de instrumentar.
- **OpenTelemetry Operator** (Kubernetes): além de injetar instrumentação, também **gerencia o deployment do Collector** no cluster.

> Para a prova: associe **OpAMP = gestão remota de agentes**; **eBPF = instrumentação no kernel sem alterar a app**.

### Resumo-relâmpago
- API = contrato (no-op sem SDK); SDK = implementação.
- Providers: Tracer/Meter/Logger. Configurados 1x no startup.
- Pipeline de trace: Sampler → Span → SpanProcessor (Simple/Batch) → Exporter.
- Samplers: AlwaysOn/Off, TraceIdRatioBased, ParentBased. **Padrão = ParentBased(root=AlwaysOn) = 100%.**
- Métricas: Instrumento → View → MetricReader (periodic/pull) → Exporter.
- Context propagation: inject/extract; W3C TraceContext é padrão (traceparent).
- SpanContext (imutável) carrega TraceId/SpanId/TraceFlags/TraceState.

### Quiz — Semana 2

1. Se a aplicação não configura o SDK, o que acontece com a telemetria gerada via API?
2. Por que bibliotecas devem depender só da API, não do SDK?
3. Qual a diferença entre SimpleSpanProcessor e BatchSpanProcessor? Qual usar em produção?
4. O que o Sampler `ParentBased` resolve?
5. Descreva o resultado possível da decisão de um sampler.
6. Diferencie `inject` e `extract` na propagação de contexto.
7. Qual é o propagador padrão do OpenTelemetry e qual header ele usa?
8. O que uma View pode fazer com uma métrica?
9. Qual MetricReader você usa para expor um endpoint que o Prometheus faz scrape?
10. O que é o InstrumentationScope e como difere do Resource?
11. Cite 3 variáveis de ambiente padronizadas e o que fazem.
12. O que carrega um SpanContext e por que ele é imutável?
13. Head-based vs tail-based sampling: onde cada um decide?
14. O que é um "agent" de instrumentação zero-code? Dê um exemplo em Java.

<details>
<summary><b>Gabarito Semana 2</b></summary>

1. A API opera como **no-op**: nada é gerado/exportado, mas o código não quebra.
2. Para não forçar overhead/telemetria em quem consome a lib; a aplicação final decide se e como configurar o SDK.
3. Simple exporta cada span imediatamente (bom p/ debug, caro); Batch agrupa e exporta em lotes. **Produção = Batch.**
4. Mantém a decisão de amostragem **consistente** ao longo do trace: se o pai foi amostrado, o filho também — evita traces incompletos.
5. `RECORD_AND_SAMPLE`, `RECORD_ONLY` ou `DROP`.
6. `inject` escreve o contexto atual em um carrier (ex.: headers HTTP) no serviço de origem; `extract` lê o carrier no serviço de destino e reconstrói o SpanContext remoto.
7. **W3C TraceContext**, header `traceparent` (+ `tracestate`); baggage usa o header `baggage`.
8. Renomear, filtrar/dropar atributos (cardinalidade), mudar a aggregation (ex.: buckets) ou dropar o instrumento.
9. Um reader do tipo pull/Prometheus (expõe `/metrics`).
10. Scope = nome/versão de quem instrumentou (a lib/tracer); Resource = a entidade/serviço que produz a telemetria.
11. Ex.: `OTEL_SERVICE_NAME` (service.name), `OTEL_EXPORTER_OTLP_ENDPOINT` (destino), `OTEL_TRACES_SAMPLER` (sampler), `OTEL_PROPAGATORS` (propagadores). (quaisquer 3)
12. TraceId, SpanId, TraceFlags (sampled), TraceState e flag remote. Imutável para poder ser propagado com segurança entre contextos/processos.
13. Head-based decide no início, no SDK do serviço de origem; tail-based decide no fim, tipicamente no Collector (tail_sampling).
14. Mecanismo que injeta instrumentação sem alterar o código-fonte. Em Java: o `-javaagent:opentelemetry-javaagent.jar`.

</details>

Próxima 👉 [Semana 3 — Collector](../semana-3-collector/README.md)
