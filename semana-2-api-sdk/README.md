# Semana 1 — Fundamentals of Observability (18%)

> Objetivo da semana: entender **o que** é observabilidade, **quais** são os sinais de telemetria, **como** eles são padronizados (semantic conventions) e **como** a aplicação é instrumentada. Base conceitual para todo o resto.

### Competências cobradas
- Telemetry Data
- Semantic Conventions
- Instrumentation
- Analysis and Outcomes

### Cronograma da semana
| Dia | Tema | Lab |
|---|---|---|
| 1 | Observabilidade vs Monitoramento; por que OpenTelemetry | — |
| 2 | Os sinais: traces, metrics, logs, profiles (+ baggage como contexto) | Lab 1.1 |
| 3 | Semantic Conventions e Resource | Lab 1.2 |
| 4 | Instrumentação: manual, biblioteca, zero-code/auto | Lab 1.3 |
| 5 | Analysis & Outcomes: do dado à decisão | Lab 1.4 |
| 6 | Revisão + Quiz da Semana 1 | Quiz |

---

## Dia 1 — O que é observabilidade

**Monitoramento** responde a perguntas que você já sabia fazer ("a CPU passou de 80%?"). **Observabilidade** é a capacidade de entender o estado interno de um sistema a partir dos seus dados de saída (telemetria), permitindo responder perguntas que você **não** antecipou ("por que *esse* usuário específico teve 3s de latência às 14h07?").

**OpenTelemetry (OTel)** é um projeto da CNCF que fornece um **padrão aberto e vendor-neutral** para gerar, coletar e exportar telemetria. Resolve o problema do *vendor lock-in*: você instrumenta uma vez e exporta para qualquer backend (Jaeger, Prometheus, Grafana, Datadog, etc.).

Componentes do projeto OTel:
- **Especificação** (specification) — define o comportamento de API, SDK e data model.
- **APIs** — interface que o código da aplicação usa para gerar telemetria.
- **SDKs** — implementação concreta da API (amostragem, processamento, exportação).
- **Collector** — binário standalone que recebe, processa e exporta telemetria.
- **OTLP** — OpenTelemetry Protocol, o protocolo de transporte da telemetria.
- **Semantic Conventions** — nomes padronizados de atributos.
- **Instrumentation libraries** — bibliotecas prontas para frameworks populares.

Pilares vs sinais: o termo clássico "3 pilares" (logs, metrics, traces) é incompleto no OTel. Os **sinais (signals)** de telemetria são: **traces, metrics, logs** e **profiles** (sinal mais recente). O diferencial do OTel é **correlacionar** os sinais (ex.: pular de uma métrica anômala para o trace exato).

> ⚠️ **Pegadinha de prova:** o **baggage NÃO é um sinal**. Baggage é um mecanismo de **propagação de contexto** (cross-cutting concern), estudado junto com propagação na Semana 2. Se uma questão listar "baggage" como sinal de telemetria, está errada. Sinais = traces, metrics, logs, profiles.

---

## Dia 2 — Os sinais de telemetria

### Traces (rastros)
Representam o caminho de uma requisição através de um sistema distribuído.

- **Trace**: a árvore completa de uma operação. Identificado por um **TraceId** (16 bytes).
- **Span**: uma unidade de trabalho dentro do trace (ex.: uma chamada HTTP, uma query). Identificado por **SpanId** (8 bytes).
- Um span tem: nome, timestamps (início/fim), **SpanKind**, status, atributos, eventos, links e referência ao span pai.

**SpanKind** (muito cobrado):
| Kind | Uso |
|---|---|
| `SERVER` | recebe uma requisição remota |
| `CLIENT` | faz uma requisição remota |
| `PRODUCER` | envia mensagem para fila/async |
| `CONSUMER` | processa mensagem de fila/async |
| `INTERNAL` | operação interna, sem cruzar processo |

**Span Status**: `Unset` (padrão), `Ok`, `Error`.

**Span Events**: um "log estruturado" dentro de um span, com timestamp. **Span Links**: conectam spans de traces diferentes (ex.: batch processing).

### Metrics (métricas)
Medições numéricas agregadas ao longo do tempo. A especificação define **6 instrumentos** (muito cobrado) — 3 síncronos clássicos + Gauge síncrono + 3 observable (assíncronos):

| Instrumento | Tipo | Monotônico? | Exemplo |
|---|---|---|---|
| **Counter** | síncrono | sim (só sobe) | total de requisições |
| **UpDownCounter** | síncrono | não | itens numa fila |
| **Histogram** | síncrono | — | distribuição de latência |
| **Gauge** (síncrono) | síncrono | não | valor medido na hora (ex.: temperatura lida) |
| **Observable Counter** | assíncrono (callback) | sim | CPU time acumulado |
| **Observable UpDownCounter** | assíncrono (callback) | não | conexões ativas via callback |
| **Observable Gauge** | assíncrono (callback) | não | uso de memória atual |

> ⚠️ **Pegadinha:** existe **Gauge síncrono** E **Observable Gauge** — são instrumentos distintos. Use síncrono quando você já tem o valor no código; observable quando precisa ler o valor sob demanda (via callback) no momento da coleta.

Conceitos: **síncrono** (registrado inline no código quando o evento ocorre) vs **assíncrono/observable** (coletado via callback no momento da coleta). **Temporalidade (temporality)**: `cumulative` (acumula desde o início) vs `delta` (só o intervalo). **Aggregation**: como pontos são combinados (sum, last value, histogram).

### Logs
Registros de eventos com timestamp. No OTel, o **LogRecord** tem campos como: Timestamp, SeverityText/SeverityNumber, Body, Attributes, e **TraceId/SpanId** (correlação com traces). O OTel foca em **integrar** logs existentes, não substituir seu logging framework — ele dá o *bridge* para padronizar e correlacionar.

### Baggage
Pares chave-valor que **viajam junto com o contexto** através dos serviços (propagados). Útil para passar informação de negócio (ex.: `user.tier=premium`) adiante. **Atenção**: baggage NÃO é adicionado automaticamente aos spans como atributo (por segurança/custo); você faz isso explicitamente se quiser.

### Profiles
Sinal mais recente do OTel — **continuous profiling**: medições de onde o programa gasta recursos (CPU, memória, alocações) ao longo do tempo, no nível de função/stack trace. Complementa os outros sinais respondendo "**por que** está lento/caro, em qual linha de código". Para a prova: saiba que **profiles é o 4º sinal** (o mais novo), que serve para profiling contínuo de performance, e que se integra ao ecossistema OTel (OTLP, Collector têm suporte emergente). Não é cobrada profundidade de implementação.

### Lab 1.1 — Identificar sinais na prática
1. Suba o ambiente ([00-ambiente](../00-ambiente/README.md)).
2. Rode a app `demo-app` e gere tráfego nas rotas `/` e `/erro`.
3. No Jaeger, abra um trace e identifique: TraceId, SpanId, SpanKind (`SERVER`), o span de erro com Status=Error.
4. No Prometheus, procure métricas começando com `http_` ou as internas do collector (`otelcol_`).
5. No stdout do collector (`docker compose logs otel-collector`), observe os logs exportados pelo `debug`.

**Entregável:** anote qual sinal respondeu a quais perguntas (latência? taxa de erro? causa raiz?).

---

## Dia 3 — Semantic Conventions e Resource

**Semantic Conventions** são nomes padronizados de atributos para que telemetria de fontes diferentes seja comparável. Sem elas, um time chama `http.method` e outro `httpMethod` — e nada correlaciona.

As convenções cobrem várias **áreas (domains)**: HTTP, Database, Messaging, RPC, Network, Cloud, Kubernetes, FaaS, e **GenAI** (mais recente). Exemplos de atributos padronizados:
- HTTP: `http.request.method`, `http.response.status_code`, `url.path`
- DB: `db.system`, `db.statement`
- Rede: `server.address`, `server.port`, `network.protocol.name`
- Messaging: `messaging.system`, `messaging.operation`

**Estável vs experimental:** cada convenção tem um status de maturidade. Convenções **stable** não mudam de forma incompatível; **experimental** ainda podem mudar. Por isso o versionamento (schema URL) importa — veja Schema Management abaixo e na Semana 4.

**Resource**: conjunto de atributos que descrevem **a entidade que produz** a telemetria (o "quem/onde"), não a operação. Exemplos:
- `service.name` (**o mais importante** — obrigatório na prática)
- `service.version`, `service.namespace`
- `deployment.environment.name`
- `host.name`, `k8s.pod.name`, `cloud.provider`, `cloud.region`

Diferença chave para a prova:
- **Resource attributes** = descrevem a origem (serviço/host/pod). Fixos durante o processo.
- **Span/metric attributes** = descrevem a operação específica (método HTTP, status).

**Schema URL / Schema Management**: as convenções evoluem; o schema URL versiona qual versão das convenções a telemetria segue, permitindo transformação entre versões (tema aprofundado na Semana 4).

### Lab 1.2 — Resource e atributos
1. Rode a app definindo recursos:
   ```powershell
   $env:OTEL_SERVICE_NAME = "demo-app"
   $env:OTEL_RESOURCE_ATTRIBUTES = "service.version=1.0.0,deployment.environment.name=lab,service.namespace=otca"
   opentelemetry-instrument flask run --port 8080
   ```
2. Gere tráfego e, no Jaeger, abra um span → aba **Process/Resource**. Confirme `service.version` e `deployment.environment.name`.
3. Observe nos atributos do span os nomes seguindo semantic conventions (`http.*`, `url.*`).

**Entregável:** liste 5 resource attributes e 5 span attributes que você viu, classificando cada um.

---

## Dia 4 — Instrumentação

Três formas (muito cobrado qual é qual):

1. **Manual (code-based)**: você usa a **API** no seu código para criar spans, métricas e logs. Máximo controle, mais trabalho.
2. **Instrumentation libraries**: bibliotecas prontas que instrumentam frameworks (Flask, Express, gRPC...). Você adiciona a dependência; ela gera spans automaticamente para aquele framework.
3. **Zero-code / Automatic**: injeta instrumentação **sem alterar o código-fonte** — via agente (ex.: Java agent `-javaagent`), ou wrappers como `opentelemetry-instrument` em Python, ou o **OpenTelemetry Operator** com auto-injection em Kubernetes.

Zero-code é o caminho mais rápido para começar; manual é necessário para telemetria específica de negócio.

### Exemplo de instrumentação manual (Python)
```python
from opentelemetry import trace
tracer = trace.get_tracer("meu.modulo")

with tracer.start_as_current_span("processar-pedido") as span:
    span.set_attribute("pedido.id", 123)
    span.add_event("validacao-ok")
    # ... trabalho ...
```

### Lab 1.3 — Comparar zero-code x manual
1. **Zero-code**: rode `opentelemetry-instrument flask run` (como já fez). Veja os spans HTTP gerados sozinhos.
2. **Manual**: adicione um span custom dentro da rota `/`:
   ```python
   from opentelemetry import trace
   tracer = trace.get_tracer("demo")

   @app.route("/")
   def hello():
       with tracer.start_as_current_span("regra-de-negocio") as span:
           span.set_attribute("cliente.tier", "premium")
           time.sleep(random.uniform(0.01, 0.3))
       return "ok\n"
   ```
3. Gere tráfego e no Jaeger veja o span `regra-de-negocio` **aninhado** dentro do span HTTP automático.

**Entregável:** explique por que o span manual aparece como filho do span automático (dica: context/current span).

---

## Dia 5 — Analysis and Outcomes

A telemetria só vale se gera **resultado**. Fluxo mental:
```
Instrumentar → Coletar → Correlacionar → Analisar → Agir (alertar, otimizar, corrigir)
```

Conceitos de outcome:
- **SLI / SLO / SLA**: indicador, objetivo e acordo de nível de serviço.
- **RED** (para serviços): **R**ate, **E**rrors, **D**uration.
- **USE** (para recursos): **U**tilization, **S**aturation, **E**rrors.
- **Correlação de sinais**: de uma métrica de erro → ao trace → ao log específico. Esse é o grande valor do OTel.
- **Cardinalidade**: atributos de alta cardinalidade (ex.: `user.id`) explodem o custo de métricas. Decisão de design importante.

### Lab 1.4 — Da anomalia à causa raiz
1. Gere bastante tráfego incluindo `/erro`.
2. No Prometheus, encontre uma métrica de contagem de requests e filtre por status de erro (se exposta pela auto-instrumentação).
3. No Jaeger, filtre traces por `error=true` e abra um deles. Leia o Status e os eventos do span.
4. (Opcional) No Grafana, adicione Prometheus e Jaeger como data sources e navegue de um painel de métrica para o trace.

**Entregável:** descreva em 3 passos como você iria de "taxa de erro subiu" até "a causa foi X".

---

## Dia 6 — Revisão + Quiz

### Resumo-relâmpago
- Observabilidade = entender o interno pelo externo; OTel = padrão aberto, vendor-neutral.
- **Sinais: traces, metrics, logs, profiles.** Baggage NÃO é sinal (é propagação de contexto).
- Span tem Kind, Status, atributos, eventos, links.
- 6 instrumentos de métrica: Counter, UpDownCounter, Histogram, Gauge (síncrono), Observable Counter, Observable UpDownCounter, Observable Gauge.
- Resource = quem produz; attributes de span = o que aconteceu.
- Semantic Conventions padronizam nomes.
- Instrumentação: manual, library, zero-code.

### Quiz — Semana 1 (responda sem olhar; gabarito ao final)

1. Qual a diferença entre monitoramento e observabilidade?
2. Quais são os sinais de telemetria do OpenTelemetry? O baggage é um deles?
3. Que identificadores tem um trace e um span, e qual o tamanho de cada?
4. Para uma requisição HTTP recebida pelo servidor, qual é o `SpanKind`?
5. Qual instrumento usar para "número de itens numa fila" (pode subir e descer)?
6. Qual a diferença entre um instrumento síncrono e um observable?
7. O que são Semantic Conventions e por que importam?
8. `service.name` é um atributo de span ou de resource?
9. Cite as três formas de instrumentação e dê um exemplo de zero-code.
10. O baggage é adicionado automaticamente como atributo nos spans? Por quê?
11. O que é cardinalidade e por que é um problema em métricas?
12. Explique o acrônimo RED.

<details>
<summary><b>Gabarito Semana 1</b></summary>

1. Monitoramento responde perguntas pré-definidas (dashboards/alertas conhecidos); observabilidade permite investigar perguntas novas a partir da telemetria.
2. Os sinais são **traces, metrics, logs e profiles**. **Baggage NÃO é sinal** — é um mecanismo de propagação de contexto.
3. Trace → TraceId (16 bytes); Span → SpanId (8 bytes).
4. `SERVER`.
5. `UpDownCounter`.
6. Síncrono é registrado inline no código quando o evento ocorre; observable é coletado via callback no momento da leitura (bom para valores de estado, como memória).
7. Nomes padronizados de atributos para que telemetrias de fontes distintas sejam comparáveis/correlacionáveis.
8. De **resource** (descreve a entidade que produz a telemetria).
9. Manual (API no código), instrumentation library (dependência por framework), zero-code/automatic (ex.: `opentelemetry-instrument`, Java agent, Operator com auto-injection).
10. Não. Por custo e segurança — você deve copiar explicitamente do baggage para atributos se desejar.
11. Número de combinações distintas de valores de atributos. Alta cardinalidade (ex.: `user.id` em métrica) explode armazenamento e custo.
12. Rate (taxa de requisições), Errors (taxa de erros), Duration (latência).

</details>

Próxima 👉 [Semana 2 — API & SDK](../semana-2-api-sdk/README.md)
