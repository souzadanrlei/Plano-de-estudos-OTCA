# Apêndice Técnico — Detalhes finos que podem cair

Pontos específicos que a prova às vezes explora e que vale memorizar. Complementa as cheatsheets do [README de recursos](README.md).

---

## 1. OTLP (OpenTelemetry Protocol)

OTLP é o protocolo nativo de transporte da telemetria. Dois transportes:

| Transporte | Porta padrão | Endpoint |
|---|---|---|
| **gRPC** | 4317 | — (um único canal) |
| **HTTP/protobuf** | 4318 | `/v1/traces`, `/v1/metrics`, `/v1/logs` |

Detalhes cobrados:
- OTLP transporta **os três sinais** (traces, metrics, logs) e está **stable** para todos.
- No **gRPC** o endpoint é só host:porta (`http://host:4317`). No **HTTP** você acrescenta o path do sinal (`http://host:4318/v1/traces`).
- `OTEL_EXPORTER_OTLP_ENDPOINT` define a base; variantes por sinal: `OTEL_EXPORTER_OTLP_TRACES_ENDPOINT`, etc.
- `OTEL_EXPORTER_OTLP_PROTOCOL`: `grpc` | `http/protobuf` | `http/json`.
- Encoding: Protocol Buffers (protobuf). Compressão opcional (gzip).

> ⚠️ Pegadinha: se usar HTTP e esquecer o path `/v1/traces`, o export falha. Com gRPC não há path.

---

## 2. Anatomia do header `traceparent` (W3C Trace Context)

```
traceparent: 00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01
             │  │                                │                │
          version          trace-id (16B)      parent-id (8B)   trace-flags
             00     32 hex chars = 16 bytes    16 hex = 8 bytes   01 = sampled
```

- **version**: `00` (atual).
- **trace-id**: 16 bytes (32 hex). Não pode ser todo zero.
- **parent-id** (span-id): 8 bytes (16 hex). Não pode ser todo zero.
- **trace-flags**: 1 byte; bit `01` = **sampled**.
- `tracestate`: campo adicional, vendor-specific, lista de key=value.

---

## 3. Contextos OTTL (por sinal)

OTTL opera em "contexts" diferentes conforme o sinal e o nível:

| Statement block | Contextos comuns |
|---|---|
| `trace_statements` | `resource`, `scope`, `span`, `spanevent` |
| `metric_statements` | `resource`, `scope`, `metric`, `datapoint` |
| `log_statements` | `resource`, `scope`, `log` |

O contexto define **o que** você acessa (`attributes`, `name`, `status`, etc.). Ex.: no contexto `span` você acessa `attributes["http.route"]`, `name`, `status.code`.

Funções úteis além das básicas: `set`, `delete_key`, `delete_matching_keys`, `keep_keys`, `replace_pattern`, `replace_all_patterns`, `limit`, `truncate_all`, `Concat`, `Int`, `Substring`.

---

## 4. Estabilidade de componentes (conceito)

Componentes do Collector têm níveis de maturidade: **Development → Alpha → Beta → Stable → Deprecated/Unmaintained**. Isso aparece na documentação por componente e por sinal (ex.: um exporter pode ser stable para traces e beta para logs). Para a prova: saiba que a estabilidade é **por componente e por sinal**, e que OTLP receiver/exporter são stable nos três sinais.

---

## 5. Resource Detection e precedência de atributos

- `resourcedetection` descobre atributos do ambiente (host, cloud, k8s, container).
- Precedência típica: valores explícitos (código/`OTEL_RESOURCE_ATTRIBUTES`) tendem a prevalecer sobre detecção automática, conforme configuração do processor (`override`).
- `OTEL_SERVICE_NAME` tem precedência sobre `service.name` definido em `OTEL_RESOURCE_ATTRIBUTES`.

---

## 6. Diferença: Span Event vs Span Link vs Log

| Conceito | O que é | Quando usar |
|---|---|---|
| **Span Event** | anotação com timestamp DENTRO de um span | marcar um momento (ex.: "cache miss") |
| **Span Link** | referência a um span de OUTRO trace | relacionar traces (ex.: batch, fan-in) |
| **Log (LogRecord)** | registro de evento independente | logging geral, correlacionado via TraceId/SpanId |

---

## 7. Métricas internas do Collector (nomes exatos)

Para debugar pipelines (`:8888/metrics`):

| Métrica | Significado |
|---|---|
| `otelcol_receiver_accepted_spans` | spans aceitos pelo receiver |
| `otelcol_receiver_refused_spans` | spans recusados (ex.: memory_limiter) |
| `otelcol_exporter_sent_spans` | spans enviados com sucesso |
| `otelcol_exporter_send_failed_spans` | spans que falharam ao enviar |
| `otelcol_exporter_queue_size` | tamanho atual da fila do exporter |
| `otelcol_processor_batch_batch_send_size` | tamanho dos lotes do batch |

> Equivalentes existem para `_metric_points` e `_log_records`.

---

## 8. Mapeamento rápido: sintoma → onde olhar

| Sintoma | Primeiro suspeito |
|---|---|
| Nada chega ao backend | debug exporter + `otelcol_exporter_sent_*` |
| Collector reiniciando / OOM | memory_limiter + pprof |
| Traces quebrados entre serviços | propagadores (`OTEL_PROPAGATORS`) alinhados? |
| Métrica some após 1 restart | fila em memória sem file_storage |
| Spans recusados | `otelcol_receiver_refused_*` (backpressure/limite) |
| Métrica com explosão de séries | cardinalidade — use View/filter para dropar atributos |

---

## 9. Extensão, distribuições e gestão de agentes

- **OCB (OpenTelemetry Collector Builder)**: gera binário customizado do Collector a partir de um manifesto YAML. Motivos: binário menor, menos superfície de ataque, incluir componentes próprios. É como distros (ex.: Jaeger v2) são montadas.
- **Distribuições**: Core (essencial), Contrib (tudo), k8s (enxuta p/ Kubernetes), custom (OCB), vendor.
- **OpAMP** (Open Agent Management Protocol): gestão **remota** de uma frota de agentes/collectors — config, atualização, saúde, versão.
- **eBPF**: instrumentação zero-code no **kernel**, sem alterar a aplicação.
- **OpenTelemetry Operator** (K8s): auto-injeção de instrumentação + gestão do Collector.

## 10. Segurança no Collector

- **TLS**: criptografa a conexão; servidor apresenta certificado. **mTLS**: cliente **e** servidor apresentam certificado (autenticação mútua).
- **Auth extensions**: `basicauth`, `bearertokenauth`, `oauth2clientauth`, `headerssetter`, auth de cloud. Referenciadas por receiver (servidor) ou exporter (cliente).
- **PII/Redaction**: processor `redaction` e OTTL `delete_key`/`replace_pattern` para remover dados sensíveis antes do egress.
- Credenciais via `${env:...}`; nunca commitar segredos.

## 11. Confusões clássicas (não erre!)

- **Baggage** não é sinal nem vira atributo automaticamente.
- Sampler **default** = `parentbased_always_on` (100%), não "ParentBased" sozinho.
- Existe **Gauge síncrono** além do **Observable Gauge**.
- **Extension** NÃO está no fluxo de dados (receiver/processor/exporter/connector estão).
- Declarar componente ≠ ativar: precisa estar no `service.pipelines`.
- **memory_limiter primeiro, batch por último** no pipeline.
- **Head sampling** = SDK/início; **tail sampling** = Collector/fim.
- Agent (instrumentação zero-code) ≠ Collector em modo agent.
- HTTP OTLP exige path `/v1/<sinal>`; gRPC não.
