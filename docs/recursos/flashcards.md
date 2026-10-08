# Flashcards OTCA — Revisão Espaçada

> Use no modo pergunta→resposta. Cubra a coluna "Verso" e tente responder antes de olhar. Marque as que errar e refaça a cada 2 dias (repetição espaçada). ~70 cards cobrindo os pontos mais cobrados e as pegadinhas.

## Fundamentos

| Frente | Verso |
|---|---|
| Sinais de telemetria do OTel | Traces, metrics, logs, profiles. (**Baggage NÃO é sinal.**) |
| Baggage é sinal? | Não — é propagação de contexto (cross-cutting concern). |
| Tamanho do TraceId | 16 bytes. |
| Tamanho do SpanId | 8 bytes. |
| SpanKind para requisição recebida | SERVER. |
| SpanKind para chamada remota feita | CLIENT. |
| SpanKind para publicar em fila | PRODUCER. |
| SpanKind para consumir de fila | CONSUMER. |
| SpanKind sem cruzar processo | INTERNAL. |
| Status possíveis de um span | Unset (padrão), Ok, Error. |
| Span event é o quê | "Log" pontual com timestamp dentro de um span. |
| Span link conecta | Spans de traces diferentes. |
| 6 instrumentos de métrica | Counter, UpDownCounter, Histogram, Gauge (síncrono), Observable Counter, Observable UpDownCounter, Observable Gauge. |
| Instrumento para fila (sobe/desce) | UpDownCounter. |
| Instrumento para latência (distribuição) | Histogram. |
| Instrumento só sobe, síncrono | Counter. |
| Diferença Gauge síncrono x Observable Gauge | Síncrono: você tem o valor no código. Observable: lido via callback na coleta. |
| Síncrono vs observable | Síncrono registra inline; observable coleta via callback no momento da leitura. |
| Resource descreve | A entidade que PRODUZ a telemetria (serviço/host/pod). |
| service.name é atributo de | Resource. |
| Semantic Conventions servem para | Padronizar nomes de atributos → correlação entre fontes. |
| 3 formas de instrumentação | Manual, instrumentation library, zero-code/automatic. |
| RED | Rate, Errors, Duration. |
| USE | Utilization, Saturation, Errors. |
| Cardinalidade | Nº de combinações distintas de valores de atributo; alta = custo. |

## API & SDK

| Frente | Verso |
|---|---|
| API sem SDK configurado | No-op: não gera/exporta, mas não quebra. |
| Por que lib depende só da API | Para não forçar telemetria/overhead ao consumidor. |
| Providers do SDK | TracerProvider, MeterProvider, LoggerProvider. |
| Quando configurar os Providers | Uma vez, no startup da aplicação. |
| SimpleSpanProcessor | Exporta cada span na hora; debug; caro em produção. |
| BatchSpanProcessor | Agrupa e exporta em lotes; padrão de produção. |
| Ordem da pipeline de trace (SDK) | Sampler → Span → SpanProcessor → Exporter. |
| Samplers padrão | AlwaysOn, AlwaysOff, TraceIdRatioBased, ParentBased. |
| Sampler DEFAULT do SDK | ParentBased(root=AlwaysOn) = parentbased_always_on = 100%. |
| ParentBased resolve | Consistência: filho segue decisão do pai → trace completo. |
| Composição p/ 10% | ParentBased(root=TraceIdRatioBased(0.1)). |
| Resultados do sampler | RECORD_AND_SAMPLE, RECORD_ONLY, DROP. |
| Head-based sampling decide | No início, no SDK do serviço de origem. |
| Tail-based sampling decide | No fim do trace, no Collector. |
| MetricReader push | PeriodicExportingMetricReader (OTLP). |
| MetricReader pull | Prometheus (expõe /metrics para scrape). |
| View (métricas) pode | Renomear, filtrar atributos, mudar aggregation, dropar instrumento. |
| Temporality para Prometheus | Cumulative. |
| inject() | Escreve o contexto num carrier (headers) na origem. |
| extract() | Lê o carrier no destino e recria o SpanContext remoto. |
| Propagador padrão do OTel | W3C TraceContext (`traceparent`, `tracestate`). |
| Header do W3C Baggage | `baggage`. |
| Headers do B3 | `b3` / `X-B3-*` (Zipkin). |
| Header do Jaeger | `uber-trace-id`. |
| Combinar propagadores | CompositePropagator. |
| SpanContext carrega | TraceId, SpanId, TraceFlags (sampled), TraceState, flag remote. |
| SpanContext é mutável? | Não — imutável e serializável. |
| InstrumentationScope | Nome/versão de QUEM instrumentou (lib/tracer). |
| OTEL_SERVICE_NAME | Define service.name. |
| OTEL_EXPORTER_OTLP_PROTOCOL | grpc ou http/protobuf. |
| OTEL_SDK_DISABLED=true | Desliga o SDK (vira no-op). |
| OTEL_PROPAGATORS | Lista de propagadores. |
| "Agent" (zero-code) em Java | `-javaagent:opentelemetry-javaagent.jar`. |
| Agent (instrum.) ≠ Collector agent | 1º injeta instrumentação na app; 2º é Collector rodando perto da app. |
| OpAMP | Protocolo de gestão remota de agentes/collectors (config, update, saúde). |
| eBPF instrumentation | Instrumentação no kernel, zero-code, sem alterar a app/linguagem. |
| OpenTelemetry Operator | K8s: injeta instrumentação E gerencia o Collector no cluster. |

## Collector

| Frente | Verso |
|---|---|
| 5 componentes do Collector | Receiver, Processor, Exporter, Connector, Extension. |
| Qual fica fora do fluxo de dados | Extension. |
| Componente ativo só se | Referenciado em `service.pipelines`. |
| Ordem recomendada de processors | memory_limiter → enriquecimento → transform/filter/sampling → batch. |
| memory_limiter faz | Protege contra OOM; recusa entrada / backpressure. |
| batch faz | Agrupa dados; reduz overhead de rede. |
| Connector é | Exporter de um pipeline + receiver de outro. |
| spanmetrics | Gera métricas (RED) a partir de traces. |
| servicegraph | Métricas de grafo de serviços a partir de traces. |
| routing | Roteia dados para pipelines por condição. |
| OTTL aparece em | transform e filter (entre outros). |
| OTTL: remover chave | `delete_key(attributes, "x")`. |
| OTTL: manter só algumas chaves | `keep_keys(attributes, ["a","b"])`. |
| OTTL: set condicional | `set(attributes["k"], v) where <cond>`. |
| Deployment agent | Junto da app/host; coleta local. |
| Deployment gateway | Central; agregação, sampling, routing, egress, segurança. |
| Gateway escala | Horizontalmente (réplicas atrás de LB). |
| tail_sampling + scaling | Precisa dos spans do trace juntos → loadbalancing por traceID. |
| Core vs Contrib | Contrib = Core + componentes da comunidade. |
| Instâncias nomeadas | `tipo/nome` (ex.: otlp/jaeger). |
| OCB (Collector Builder) | Gera binário customizado do Collector a partir de manifesto (só os componentes necessários). |
| Por que usar OCB | Menor binário, menor superfície de ataque, incluir componentes próprios. |
| Distribuições do Collector | Core, Contrib, k8s, custom (OCB), distros vendor. |
| TLS vs mTLS no Collector | TLS: servidor autentica; mTLS: ambos os lados com certificado. |
| Auth no Collector | Via extensions: basicauth, bearertokenauth, oauth2clientauth. |

## Pipelines / Debug

| Frente | Verso |
|---|---|
| 1ª ferramenta p/ ver telemetria chegando | debug exporter (verbosity: detailed). |
| Métricas internas do Collector | `:8888/metrics` (otelcol_*). |
| Métrica de falha de envio | otelcol_exporter_send_failed_spans. |
| zPages | `:55679` (tracez, servicez). |
| health_check | `:13133`. |
| pprof | Profiling CPU/memória do Collector. |
| Causa de trace quebrado | Propagadores incompatíveis / headers removidos. |
| sending_queue | Desacopla ingestão da exportação. |
| retry_on_failure | Reenvia com backoff ao falhar. |
| Fila que sobrevive a restart | file_storage extension + queue persistente. |
| Schema URL | Versiona a versão das semantic conventions seguida. |
| schemaprocessor | Normaliza telemetria entre versões de convenções. |
