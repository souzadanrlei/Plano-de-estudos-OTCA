# Simulado 1 — OTCA (estilo exame)

> **Instruções:** 30 questões. Cronometre **45 minutos** (metade do exame real, proporcional a 60 questões em 90 min). Não consulte material. Anote suas respostas (ex.: 1-C, 2-A...). Correção em [gabaritos.md](gabaritos.md).
>
> Distribuição por domínio: Fundamentos (6), API & SDK (14), Collector (7), Pipelines (3) — proporcional aos pesos reais.

---

### Fundamentos de Observabilidade

**1.** Qual afirmação descreve melhor a diferença entre monitoramento e observabilidade?
- A) São sinônimos
- B) Monitoramento responde perguntas conhecidas; observabilidade permite investigar perguntas não antecipadas
- C) Observabilidade só usa logs
- D) Monitoramento é mais recente que observabilidade

**2.** Quais destes são sinais (signals) de telemetria do OpenTelemetry?
- A) Traces, metrics, logs e profiles
- B) Traces, metrics, logs e baggage
- C) Dashboards, alertas e relatórios
- D) CPU, memória e disco

**3.** Uma requisição HTTP é recebida por um serviço. Qual `SpanKind` descreve o span correspondente nesse serviço?
- A) CLIENT
- B) PRODUCER
- C) SERVER
- D) INTERNAL

**4.** Você quer medir o número de conexões ativas, que sobe e desce. Qual instrumento?
- A) Counter
- B) UpDownCounter
- C) Histogram
- D) Observable Counter

**5.** O atributo `service.name` pertence a:
- A) Atributos de span
- B) Resource
- C) Span events
- D) TraceState

**6.** O que caracteriza instrumentação "zero-code"?
- A) Exige reescrever a aplicação
- B) Adiciona telemetria sem alterar o código-fonte (ex.: Java agent)
- C) Só funciona com logs
- D) Desabilita o SDK

---

### A API e o SDK do OpenTelemetry

**7.** Uma biblioteca é instrumentada com a API do OTel, mas a aplicação final não configura o SDK. O que acontece?
- A) A aplicação quebra
- B) A API opera como no-op; nada é exportado, sem erro
- C) O SDK é configurado automaticamente
- D) A telemetria vai para o console

**8.** Qual SpanProcessor é recomendado para produção?
- A) SimpleSpanProcessor
- B) BatchSpanProcessor
- C) ConsoleSpanProcessor
- D) NoopSpanProcessor

**9.** Qual sampler mantém a decisão de amostragem consistente ao longo de um trace distribuído?
- A) AlwaysOn
- B) AlwaysOff
- C) ParentBased
- D) TraceIdRatioBased isolado

**10.** O propagador padrão do OpenTelemetry usa qual header?
- A) `uber-trace-id`
- B) `b3`
- C) `traceparent`
- D) `x-datadog-trace-id`

**11.** O que uma View (métricas) pode fazer?
- A) Criar spans
- B) Renomear métrica, filtrar atributos e mudar aggregation
- C) Definir o propagador
- D) Exportar logs

**12.** Qual MetricReader é usado para expor um endpoint que o Prometheus faz scrape?
- A) PeriodicExportingMetricReader via OTLP
- B) Um reader do tipo pull/Prometheus
- C) BatchLogRecordProcessor
- D) SimpleSpanProcessor

**13.** O que o método `inject` faz na propagação de contexto?
- A) Lê headers e recria o SpanContext
- B) Escreve o contexto atual num carrier (ex.: headers HTTP)
- C) Cria um novo TracerProvider
- D) Exporta spans

**14.** Qual campo do SpanContext indica se o trace foi amostrado?
- A) TraceState
- B) TraceId
- C) TraceFlags
- D) SpanName

**15.** Head-based sampling é decidido:
- A) No fim do trace, no Collector
- B) No início do trace, no SDK do serviço de origem
- C) Apenas no backend
- D) Pelo load balancer

**16.** Qual variável de ambiente define o `service.name`?
- A) `OTEL_RESOURCE_NAME`
- B) `OTEL_SERVICE_NAME`
- C) `OTEL_SDK_NAME`
- D) `SERVICE_NAME`

**17.** Os Providers (TracerProvider, MeterProvider, LoggerProvider) são tipicamente configurados:
- A) A cada requisição
- B) Uma vez, no startup da aplicação
- C) Pelo Collector
- D) Pelo backend

**18.** O InstrumentationScope descreve:
- A) O serviço/entidade que produz telemetria
- B) O nome/versão da biblioteca/instrumentador que criou a telemetria
- C) O endpoint do exporter
- D) A fila de exportação

**19.** Qual é o resultado possível de uma decisão de sampler?
- A) RECORD_AND_SAMPLE, RECORD_ONLY, DROP
- B) KEEP, DELETE
- C) PUSH, PULL
- D) OK, ERROR, UNSET

**20.** Para interoperar com um sistema legado que usa Zipkin/B3, você:
- A) Não pode usar OTel
- B) Configura o propagador B3 (possivelmente composto com tracecontext)
- C) Desabilita o sampling
- D) Usa somente logs

**21.** `OTEL_SDK_DISABLED=true` faz o quê?
- A) Desabilita o Collector
- B) Desabilita o SDK (telemetria não é gerada)
- C) Remove o Resource
- D) Força SimpleSpanProcessor

**22.** O "agent" de instrumentação zero-code em Java é tipicamente ativado via:
- A) `import opentelemetry`
- B) `-javaagent:opentelemetry-javaagent.jar`
- C) Variável `JAVA_OTEL=1`
- D) Recompilando o JDK

**23.** BatchSpanProcessor melhora a eficiência porque:
- A) Exporta cada span imediatamente
- B) Agrupa spans e exporta em lotes, reduzindo overhead de rede
- C) Remove atributos
- D) Desabilita o sampling

**24.** Baggage é:
- A) Automaticamente adicionado como atributo em todos os spans
- B) Pares chave-valor propagados pelo contexto entre serviços
- C) Um tipo de exporter
- D) Um sampler

---

### O OpenTelemetry Collector

**25.** Declarei um exporter na config mas ele não envia nada. Causa mais provável?
- A) O Collector está com bug
- B) O exporter não foi referenciado em `service.pipelines`
- C) Falta reiniciar a máquina
- D) O exporter precisa de licença

**26.** Qual componente do Collector NÃO participa do fluxo de dados de telemetria?
- A) Receiver
- B) Processor
- C) Exporter
- D) Extension

**27.** Qual connector gera métricas (RED) a partir de traces?
- A) routing
- B) spanmetrics
- C) forward
- D) failover

**28.** A ordem recomendada de processors num pipeline é:
- A) batch primeiro, memory_limiter por último
- B) memory_limiter primeiro, batch por último
- C) a ordem não importa
- D) exporter no meio

**29.** OTTL é usada principalmente em quais processors?
- A) batch e memory_limiter
- B) transform e filter
- C) otlp e debug
- D) health_check

**30.** Por que tail_sampling complica o scaling horizontal do Collector?
- A) Consome pouca memória
- B) Precisa de todos os spans de um trace no mesmo Collector
- C) Não funciona com OTLP
- D) Exige GPU

---

Fim do Simulado 1. Confira em [gabaritos.md](gabaritos.md).
