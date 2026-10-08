# Simulado 2 — OTCA (estilo exame)

> **Instruções:** 30 questões, mais difíceis/cenários. Cronometre **45 minutos**. Sem consulta. Correção em [gabaritos.md](gabaritos.md).
>
> Questões marcadas **[Múltipla seleção]** têm mais de uma resposta correta (como no exame real).

---

### Fundamentos

**1.** [Múltipla seleção] Quais afirmações sobre Semantic Conventions são corretas?
- A) Padronizam nomes de atributos entre fontes diferentes
- B) São opcionais e não afetam correlação
- C) Permitem comparar telemetria de serviços distintos
- D) Só se aplicam a logs

**2.** Um Span registra um "log pontual com timestamp" durante sua execução. Isso é um:
- A) Span link
- B) Span event
- C) Resource
- D) Baggage

**3.** Para conectar um span de processamento assíncrono a um span de outro trace, usa-se:
- A) Span event
- B) Span link
- C) Baggage
- D) Resource attribute

**4.** Qual instrumento é mais adequado para medir distribuição de latência de requisições?
- A) Counter
- B) Histogram
- C) UpDownCounter
- D) Observable Gauge

**5.** Alta cardinalidade em métricas é problemática porque:
- A) Melhora a performance
- B) Multiplica séries temporais, aumentando custo/armazenamento
- C) Reduz a precisão dos traces
- D) Desabilita o sampling

---

### API & SDK

**6.** [Múltipla seleção] Por que a API e o SDK são separados no OTel?
- A) Para que bibliotecas dependam só da API (no-op sem SDK)
- B) Para que a aplicação final controle processamento/exportação
- C) Para obrigar o uso de um backend específico
- D) Para impedir instrumentação manual

**7.** Um serviço A chama B. No Jaeger aparecem dois traces separados em vez de um. Causa provável?
- A) Sampling a 100%
- B) Propagadores incompatíveis entre A e B
- C) Resource igual nos dois
- D) BatchSpanProcessor

**8.** Qual composição de sampler é recomendada para amostrar 10% dos traces mantendo consistência?
- A) `AlwaysOff`
- B) `ParentBased(root=TraceIdRatioBased(0.1))`
- C) `AlwaysOn`
- D) `TraceIdRatioBased(1.0)`

**9.** Qual destes é um instrumento assíncrono (observable)?
- A) Counter
- B) Histogram
- C) Observable Gauge
- D) UpDownCounter

**10.** O que `extract` faz num serviço que recebe uma requisição?
- A) Escreve headers de saída
- B) Lê headers de entrada e reconstrói o SpanContext remoto
- C) Cria um exporter
- D) Define o Resource

**11.** [Múltipla seleção] O que o SpanContext carrega?
- A) TraceId
- B) SpanId
- C) TraceFlags
- D) O nome do serviço (service.name)

**12.** Qual afirmação sobre o SimpleSpanProcessor é correta?
- A) Agrupa spans em lotes
- B) Exporta cada span imediatamente ao término — útil em debug, caro em produção
- C) Nunca exporta
- D) É o padrão de produção

**13.** `OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf` configura:
- A) O sampler
- B) O protocolo de transporte OTLP (HTTP em vez de gRPC)
- C) O propagador
- D) O Resource

**14.** Qual componente do SDK decide se um trace será registrado/exportado?
- A) Exporter
- B) Sampler
- C) Propagator
- D) Reader

**15.** Para correlacionar logs com traces, o SDK de logs tipicamente:
- A) Ignora o contexto
- B) Anexa TraceId/SpanId ao LogRecord quando emitido dentro de um span
- C) Converte logs em métricas
- D) Usa B3 obrigatoriamente

**16.** A temporalidade padrão esperada por backends tipo Prometheus é:
- A) delta
- B) cumulative
- C) rate
- D) gauge-only

**17.** Qual é a função de um CompositePropagator?
- A) Combinar vários formatos de propagação (ex.: tracecontext + baggage + b3)
- B) Combinar vários exporters
- C) Combinar spans em um trace
- D) Combinar métricas em histogramas

**18.** Diferença entre "agent" (instrumentação zero-code) e "Collector em modo agent"?
- A) São a mesma coisa
- B) O primeiro injeta instrumentação na app; o segundo é um Collector rodando perto da app
- C) Ambos rodam só no backend
- D) O Collector agent não processa telemetria

**19.** [Múltipla seleção] Formas válidas de configurar o SDK incluem:
- A) Variáveis de ambiente
- B) Configuração programática no código
- C) Configuração declarativa por arquivo (file-based)
- D) Editando o backend

---

### Collector

**20.** No Collector, `otlp/jaeger` e `otlp/backend` na mesma config representam:
- A) Erro de sintaxe
- B) Duas instâncias nomeadas do mesmo tipo de componente
- C) Dois pipelines
- D) Dois propagadores

**21.** Qual processor protege o Collector contra OOM aplicando backpressure?
- A) batch
- B) memory_limiter
- C) attributes
- D) filter

**22.** [Múltipla seleção] O que um connector pode fazer?
- A) Ligar a saída de um pipeline à entrada de outro
- B) Mudar o tipo de sinal (ex.: trace → metric)
- C) Substituir o backend
- D) Rotear dados entre pipelines (ex.: routing)

**23.** Qual statement OTTL remove uma chave de atributo sensível?
- A) `set(attributes["x"], 1)`
- B) `delete_key(attributes, "senha")`
- C) `keep_keys(attributes, ["senha"])`
- D) `limit(attributes, 10)`

**24.** No padrão agent → gateway, o gateway tipicamente faz:
- A) Apenas repassar sem processar
- B) Agregação, sampling, routing, egress centralizado e segurança
- C) Instrumentar a aplicação
- D) Substituir o SDK

**25.** Para escalar tail_sampling com múltiplas réplicas, você precisa:
- A) Mais memória apenas
- B) Rotear por traceID (loadbalancing exporter) para juntar spans do mesmo trace
- C) Desabilitar o batch
- D) Usar SimpleSpanProcessor

**26.** A distribuição Contrib do Collector:
- A) Tem menos componentes que a Core
- B) Inclui a Core + componentes da comunidade
- C) Não suporta OTLP
- D) É só para Kubernetes

---

### Manutenção e Debug de Pipelines

**27.** Qual é a primeira ferramenta para ver se a telemetria chega ao Collector?
- A) O `debug` exporter com verbosity detailed
- B) Reiniciar o backend
- C) Trocar o sampler
- D) Remover o batch

**28.** [Múltipla seleção] Mecanismos de error handling/resiliência no Collector:
- A) `retry_on_failure`
- B) `sending_queue`
- C) `file_storage` extension (fila persistente)
- D) Desabilitar o receiver

**29.** O schema URL serve para:
- A) Definir o endpoint do exporter
- B) Versionar qual versão das semantic conventions a telemetria segue, permitindo transformações
- C) Autenticar no backend
- D) Escolher o sampler

**30.** Qual métrica interna confirma falha de envio pelo exporter?
- A) `otelcol_receiver_accepted_spans`
- B) `otelcol_exporter_send_failed_spans`
- C) `otelcol_processor_batch_batch_size`
- D) `otelcol_exporter_queue_size`

---

Fim do Simulado 2. Confira em [gabaritos.md](gabaritos.md).
