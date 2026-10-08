# Simulado 3 — OTCA (pegadinhas e cenários)

> **Nível difícil.** 30 questões focadas nas confusões mais comuns, distinções sutis e tópicos avançados (OCB, OpAMP, eBPF, segurança, profiles). Cronometre **45 minutos**. Gabarito em [gabaritos.md](gabaritos.md#simulado-3).

---

**1.** Qual destes NÃO é um sinal de telemetria do OpenTelemetry?
- A) Traces
- B) Metrics
- C) Baggage
- D) Logs

**2.** O sampler **padrão** de um SDK OpenTelemetry, se nada for configurado, é:
- A) AlwaysOff
- B) TraceIdRatioBased(0.1)
- C) ParentBased com root AlwaysOn (amostra 100%)
- D) Tail sampling

**3.** Sobre Gauge, qual afirmação é correta?
- A) Só existe Observable Gauge (assíncrono)
- B) Existe Gauge síncrono E Observable Gauge, são instrumentos distintos
- C) Gauge é sempre monotônico
- D) Gauge é um tipo de Counter

**4.** Uma biblioteca instrumentada com a API é usada numa app que não configura o SDK. O comportamento é:
- A) Erro em tempo de execução
- B) No-op: nada é exportado, sem quebrar
- C) Telemetria vai para o console por padrão
- D) O SDK é baixado automaticamente

**5.** Baggage, quando propagado, é automaticamente adicionado como atributo nos spans?
- A) Sim, sempre
- B) Não — por custo/segurança, você deve copiá-lo explicitamente
- C) Só em traces de erro
- D) Só se o sampler permitir

**6.** `service.name` é:
- A) Um atributo de span
- B) Um resource attribute
- C) Um span event
- D) Um propagador

**7.** No Collector, declarei um processor em `processors:` mas ele não surte efeito. Por quê?
- A) Precisa de licença
- B) Não foi referenciado em `service.pipelines`
- C) Processors nunca têm efeito sozinhos por design de segurança
- D) Falta reiniciar o host

**8.** [Múltipla seleção] Quais afirmações sobre tail_sampling estão corretas?
- A) É decidido no fim do trace
- B) Normalmente roda no Collector
- C) Escala trivialmente com qualquer número de réplicas sem cuidado extra
- D) Exige que todos os spans de um trace cheguem ao mesmo Collector

**9.** O header do propagador **padrão** do OpenTelemetry é:
- A) `uber-trace-id`
- B) `b3`
- C) `traceparent`
- D) `x-trace`

**10.** Qual componente do Collector é simultaneamente exporter de um pipeline e receiver de outro?
- A) Extension
- B) Processor
- C) Connector
- D) Receiver

**11.** Head-based e tail-based sampling diferem em:
- A) Linguagem de programação
- B) Onde/quando a decisão é tomada (início no SDK vs fim no Collector)
- C) Formato do TraceId
- D) Protocolo de transporte

**12.** SpanContext é imutável e carrega:
- A) TraceId, SpanId, TraceFlags, TraceState
- B) Apenas o nome do span
- C) service.name e service.version
- D) A lista de exporters

**13.** A diferença entre "agent" de instrumentação zero-code e "Collector em modo agent":
- A) São exatamente a mesma coisa
- B) O primeiro injeta instrumentação na aplicação; o segundo é um Collector próximo da app
- C) Ambos rodam só no backend
- D) O Collector agent não processa dados

**14.** Qual processor deve vir **primeiro** no pipeline, e qual **por último** (antes do exporter)?
- A) batch primeiro, memory_limiter último
- B) memory_limiter primeiro, batch último
- C) filter primeiro, attributes último
- D) a ordem é irrelevante

**15.** Para expor métricas que o Prometheus faz scrape, o SDK usa:
- A) PeriodicExportingMetricReader via OTLP
- B) Um MetricReader do tipo pull (Prometheus) que serve `/metrics`
- C) BatchSpanProcessor
- D) debug exporter

**16.** [Múltipla seleção] O que uma View pode fazer com uma métrica?
- A) Renomear a métrica
- B) Dropar atributos para reduzir cardinalidade
- C) Mudar a aggregation (ex.: buckets)
- D) Propagar contexto entre serviços

**17.** `OTEL_SDK_DISABLED=true` faz:
- A) Desabilita só o exporter
- B) Faz os providers virarem no-op (telemetria não gerada)
- C) Remove o Resource
- D) Desabilita o Collector

**18.** Um trace aparece "quebrado" (B inicia novo trace em vez de continuar o de A). Causa mais provável?
- A) Sampler a 100%
- B) Propagadores incompatíveis ou headers de contexto removidos
- C) BatchSpanProcessor em B
- D) Resource diferente

**19.** Qual métrica interna do Collector indica falha de envio pelo exporter?
- A) `otelcol_receiver_accepted_spans`
- B) `otelcol_exporter_send_failed_spans`
- C) `otelcol_process_uptime`
- D) `otelcol_processor_batch_timeout`

**20.** Para uma fila de exportação sobreviver ao restart do Collector:
- A) Aumentar `queue_size`
- B) Usar `file_storage` extension com queue persistente
- C) Trocar para SimpleSpanProcessor
- D) Desabilitar retry

**21.** O InstrumentationScope descreve:
- A) O serviço que produz telemetria
- B) O nome/versão da biblioteca/instrumentador que criou a telemetria
- C) O endpoint OTLP
- D) O sampler em uso

**22.** [Múltipla seleção] Formas válidas de configurar o SDK:
- A) Variáveis de ambiente OTEL_*
- B) Configuração programática no startup
- C) Configuração declarativa por arquivo
- D) Alterando o firmware do host

**23.** Qual connector deriva métricas RED a partir de traces?
- A) routing
- B) spanmetrics
- C) forward
- D) failover

**24.** Schema URL serve para:
- A) Autenticar no backend
- B) Versionar qual versão das semantic conventions a telemetria segue
- C) Definir o sampler
- D) Escolher gRPC ou HTTP

**25.** Qual afirmação sobre temporality é correta?
- A) Prometheus usa delta por padrão
- B) Prometheus usa cumulative; delta é comum em outros backends
- C) Temporality só se aplica a traces
- D) Cumulative e delta são samplers

**26.** Para que serve o OpenTelemetry Collector Builder (OCB)?
- A) Fazer scrape de métricas
- B) Gerar um binário customizado do Collector só com os componentes necessários
- C) Propagar contexto entre serviços
- D) Substituir o SDK

**27.** O que é o OpAMP?
- A) Um exporter de métricas
- B) Um protocolo para gerenciar agentes/collectors remotamente (config, update, saúde)
- C) Um tipo de sampler
- D) Um formato de propagação

**28.** Instrumentação baseada em eBPF se caracteriza por:
- A) Exigir reescrever a aplicação
- B) Capturar telemetria no nível do kernel, sem alterar a aplicação
- C) Só funcionar com Java
- D) Substituir o Collector

**29.** mTLS entre um agent e um gateway do Collector significa:
- A) Só o gateway apresenta certificado
- B) Ambos os lados se autenticam com certificado
- C) Não há criptografia
- D) Autenticação por senha em texto puro

**30.** [Múltipla seleção] Qual o 4º sinal (mais recente) do OTel e para que serve?
- A) Profiles
- B) Continuous profiling (onde o código gasta CPU/memória)
- C) Baggage
- D) Serve para propagar contexto

---

Fim do Simulado 3. Confira em [gabaritos.md](gabaritos.md#simulado-3).
