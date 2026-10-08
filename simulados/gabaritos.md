# Gabaritos Comentados — Simulados OTCA

> Corrija cada questão e, para as que errou, releia a seção indicada entre colchetes. Meta: **≥ 85%**.
>
> Cálculo da nota: (acertos / total) × 100. Em múltipla seleção, conte como acerto só se marcou **todas** as corretas e **nenhuma** errada.

---

## Simulado 1

| # | Resposta | Comentário | Revisar |
|---|---|---|---|
| 1 | **B** | Observabilidade investiga perguntas novas a partir da telemetria. | [S1 D1] |
| 2 | **A** | Sinais = traces, metrics, logs, profiles. **B é a pegadinha**: baggage é propagação de contexto, não sinal. | [S1 D2] |
| 3 | **C** | Receber requisição remota = `SERVER`. | [S1 D2] |
| 4 | **B** | Sobe e desce = `UpDownCounter`. | [S1 D2] |
| 5 | **B** | `service.name` descreve a entidade = Resource. | [S1 D3] |
| 6 | **B** | Zero-code adiciona telemetria sem mudar o código. | [S1 D4] |
| 7 | **B** | Sem SDK, a API é no-op (não quebra, não exporta). | [S2 D1] |
| 8 | **B** | BatchSpanProcessor é o padrão de produção. | [S2 D2] |
| 9 | **C** | ParentBased mantém o trace consistente. | [S2 D3] |
| 10 | **C** | W3C TraceContext usa `traceparent`. | [S2 D5] |
| 11 | **B** | View renomeia, filtra atributos e muda aggregation. | [S2 D4] |
| 12 | **B** | Reader pull/Prometheus expõe `/metrics`. | [S2 D4] |
| 13 | **B** | `inject` escreve o contexto no carrier (headers). | [S2 D5] |
| 14 | **C** | TraceFlags contém o sampled bit. | [S2 D5] |
| 15 | **B** | Head-based decide no SDK de origem, no início. | [S2 D3] |
| 16 | **B** | `OTEL_SERVICE_NAME`. | [S2 D6] |
| 17 | **B** | Providers configurados uma vez no startup. | [S2 D1] |
| 18 | **B** | Scope = lib/instrumentador; Resource = serviço. | [S2 D1] |
| 19 | **A** | RECORD_AND_SAMPLE / RECORD_ONLY / DROP. | [S2 D3] |
| 20 | **B** | Propagador B3 (eventualmente composto). | [S2 D5] |
| 21 | **B** | Desabilita o SDK, telemetria não é gerada. | [S2 D6] |
| 22 | **B** | `-javaagent:opentelemetry-javaagent.jar`. | [S2 D6] |
| 23 | **B** | Batch agrupa e reduz overhead de rede. | [S2 D2] |
| 24 | **B** | Baggage = chave-valor propagado no contexto. | [S1 D2 / S2 D5] |
| 25 | **B** | Não referenciado em `service.pipelines`. | [S3 D1] |
| 26 | **D** | Extension fica fora do fluxo de dados. | [S3 D1] |
| 27 | **B** | spanmetrics: traces → métricas RED. | [S3 D4] |
| 28 | **B** | memory_limiter primeiro, batch por último. | [S3 D3] |
| 29 | **B** | OTTL em transform e filter. | [S3 D4] |
| 30 | **B** | tail_sampling precisa dos spans do trace juntos. | [S3 D5] |

*(S1 D2 = Semana 1, Dia 2; S2 = Semana 2; S3 = Semana 3.)*

---

## Simulado 2

| # | Resposta | Comentário | Revisar |
|---|---|---|---|
| 1 | **A, C** | Convenções padronizam nomes e permitem comparar fontes. | [S1 D3] |
| 2 | **B** | Log pontual com timestamp dentro do span = Span event. | [S1 D2] |
| 3 | **B** | Span link conecta spans de traces diferentes. | [S1 D2] |
| 4 | **B** | Histogram para distribuição de latência. | [S1 D2] |
| 5 | **B** | Alta cardinalidade multiplica séries e custo. | [S1 D5] |
| 6 | **A, B** | API/SDK separados: libs usam só API; app controla SDK. | [S2 D1] |
| 7 | **B** | Propagadores incompatíveis quebram o trace. | [S4 D1] |
| 8 | **B** | `ParentBased(root=TraceIdRatioBased(0.1))`. | [S2 D3] |
| 9 | **C** | Observable Gauge é assíncrono (callback). | [S1 D2 / S2 D4] |
| 10 | **B** | `extract` lê headers e recria o SpanContext remoto. | [S2 D5] |
| 11 | **A, B, C** | SpanContext: TraceId, SpanId, TraceFlags, TraceState (não service.name). | [S2 D5] |
| 12 | **B** | Simple exporta cada span na hora; caro em produção. | [S2 D2] |
| 13 | **B** | Define o protocolo OTLP (HTTP protobuf). | [S2 D6] |
| 14 | **B** | O Sampler decide registrar/exportar. | [S2 D3] |
| 15 | **B** | Logs recebem TraceId/SpanId para correlação. | [S2 D5] |
| 16 | **B** | Prometheus espera `cumulative`. | [S2 D4] |
| 17 | **A** | CompositePropagator combina formatos. | [S2 D5] |
| 18 | **B** | Agent (instrumentação) ≠ Collector em modo agent. | [S2 D6 / S3 D5] |
| 19 | **A, B, C** | Env vars, programática e declarativa (file-based). | [S2 D6] |
| 20 | **B** | `tipo/nome` = instâncias nomeadas do mesmo tipo. | [S3 D2] |
| 21 | **B** | memory_limiter protege contra OOM. | [S3 D3] |
| 22 | **A, B, D** | Connector liga pipelines, muda sinal e roteia; não substitui backend. | [S3 D4] |
| 23 | **B** | `delete_key(attributes, "senha")`. | [S3 D4] |
| 24 | **B** | Gateway: agregação, sampling, routing, egress, segurança. | [S3 D5] |
| 25 | **B** | Rotear por traceID com loadbalancing exporter. | [S3 D5] |
| 26 | **B** | Contrib = Core + componentes da comunidade. | [S3 D1] |
| 27 | **A** | `debug` exporter com verbosity detailed. | [S4 D1] |
| 28 | **A, B, C** | retry_on_failure, sending_queue, file_storage. | [S4 D2] |
| 29 | **B** | Schema URL versiona convenções e habilita transformações. | [S4 D3] |
| 30 | **B** | `otelcol_exporter_send_failed_spans`. | [S4 D1/D2] |

---

## Simulado 3

| # | Resposta | Comentário | Revisar |
|---|---|---|---|
| 1 | **C** | Baggage NÃO é sinal — é propagação de contexto. | [S1 D2] |
| 2 | **C** | Default do SDK = ParentBased(root=AlwaysOn) = 100%. | [S2 D3] |
| 3 | **B** | Existe Gauge síncrono E Observable Gauge, distintos. | [S1 D2] |
| 4 | **B** | Sem SDK a API é no-op. | [S2 D1] |
| 5 | **B** | Baggage não vira atributo automático (custo/segurança). | [S1 D2] |
| 6 | **B** | service.name é resource attribute. | [S1 D3] |
| 7 | **B** | Não referenciado em `service.pipelines`. | [S3 D1] |
| 8 | **A, B, D** | tail_sampling: fim do trace, no Collector, spans juntos. **C é falso.** | [S3 D5] |
| 9 | **C** | W3C TraceContext → `traceparent`. | [S2 D5] |
| 10 | **C** | Connector = exporter + receiver. | [S3 D4] |
| 11 | **B** | Head decide no início (SDK); tail no fim (Collector). | [S2 D3] |
| 12 | **A** | TraceId, SpanId, TraceFlags, TraceState (não service.name). | [S2 D5] |
| 13 | **B** | Agent instrumenta a app; Collector agent é um Collector local. | [S2 D6] |
| 14 | **B** | memory_limiter primeiro, batch por último. | [S3 D3] |
| 15 | **B** | Reader pull/Prometheus serve `/metrics`. | [S2 D4] |
| 16 | **A, B, C** | View renomeia, filtra attrs, muda aggregation. **D é falso.** | [S2 D4] |
| 17 | **B** | Providers viram no-op. | [S2 D6] |
| 18 | **B** | Propagadores incompatíveis / headers removidos. | [S4 D1] |
| 19 | **B** | `otelcol_exporter_send_failed_spans`. | [S4 D1/D2] |
| 20 | **B** | file_storage + queue persistente. | [S4 D2] |
| 21 | **B** | Scope = lib/instrumentador. | [S2 D1] |
| 22 | **A, B, C** | Env vars, programática, declarativa. **D é falso.** | [S2 D6] |
| 23 | **B** | spanmetrics: traces → métricas RED. | [S3 D4] |
| 24 | **B** | Schema URL versiona semantic conventions. | [S4 D3] |
| 25 | **B** | Prometheus = cumulative; delta em outros. | [S2 D4] |
| 26 | **B** | OCB gera binário customizado só com os componentes necessários. | [S3 D1] |
| 27 | **B** | OpAMP = gestão remota de agentes/collectors. | [S2 D6] |
| 28 | **B** | eBPF captura no kernel, sem alterar a app. | [S2 D6] |
| 29 | **B** | mTLS = ambos os lados com certificado. | [S3 D5] |
| 30 | **A, B** | Profiles é o 4º sinal (continuous profiling). C/D descrevem baggage. | [S1 D2] |

---

## Tabela de interpretação da nota

| % de acerto | Leitura |
|---|---|
| ≥ 90% | Pronto para o exame. |
| 85–89% | Muito bom; feche lacunas pontuais do caderno de erros. |
| 75–84% | Passaria no limite; revise os domínios fracos antes de agendar. |
| < 75% | Mais uma rodada de estudo nos domínios com mais erros (foque API/SDK). |

### Caderno de erros (template)
```
Questão: Simulado _ #__
Minha resposta: __   | Correta: __
Domínio/conceito: ______________________
Por que errei: _________________________
Onde revisar: __________________________
Refazer em (data): _____________________
```
