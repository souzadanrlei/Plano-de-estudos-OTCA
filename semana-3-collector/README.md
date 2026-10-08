# Semana 3 — The OpenTelemetry Collector (26%)

> Objetivo: dominar a **anatomia do Collector**, ler e escrever `config.yaml`, entender **deployment** (agent vs gateway), **scaling**, **pipelines** e **transformação de dados** (OTTL). Segundo domínio mais pesado.

> 💡 Você já tem um mapa arquitetural detalhado em `../../ok.txt`. Use-o como material de aprofundamento. Esta semana foca no que **cai na prova**.

### Competências cobradas
- Configuration
- Deployment
- Scaling
- Pipelines
- Transforming Data

### Cronograma da semana
| Dia | Tema | Lab |
|---|---|---|
| 1 | Anatomia: 5 componentes + service + distribuições/OCB | Lab 3.1 |
| 2 | Configuration: ler/escrever config.yaml | Lab 3.2 |
| 3 | Processors essenciais (batch, memory_limiter, etc.) | Lab 3.3 |
| 4 | Connectors + Transforming Data (OTTL) | Lab 3.4 |
| 5 | Deployment (agent/gateway) + Scaling + Segurança | Lab 3.5 |
| 6 | Revisão + Quiz | Quiz |

---

## Dia 1 — Anatomia do Collector

O Collector é um binário que **recebe → processa → exporta** telemetria, de forma vendor-neutral.

### Distribuições (distributions)
Uma distribuição = um binário do Collector com um conjunto específico de componentes.
| Distribuição | Conteúdo |
|---|---|
| **Core** | componentes estáveis essenciais (OTLP, batch, memory_limiter...) — conservadora e pequena |
| **Contrib** | Core + centenas de componentes da comunidade (todos os receivers/processors/exporters) |
| **k8s** | enxuta, focada em cenários Kubernetes |
| **Custom (via OCB)** | só os componentes que você precisa |

Use `otel/opentelemetry-collector-contrib` nos labs (tem tudo).

### OpenTelemetry Collector Builder (OCB)
O **OCB** (`ocb` / `builder`) gera um **binário customizado** do Collector a partir de um **manifesto** (YAML) que lista exatamente os receivers/processors/exporters/connectors/extensions desejados. Benefícios cobrados:
- **Menor footprint** (binário menor) e **menor superfície de ataque** (só o necessário).
- Permite incluir **componentes próprios/privados** não presentes no Contrib.
- É assim que distros vendor (ex.: Jaeger v2, distros de observabilidade) são montadas.

> Para a prova: saiba **o que é o OCB e por que usar** (customizar/enxugar a distribuição), não a sintaxe do manifesto.

### Os 5 tipos de componente
| Componente | Papel | No fluxo de dados? |
|---|---|---|
| **Receiver** | entrada (push ou scrape) | sim |
| **Processor** | transforma/filtra/agrupa | sim |
| **Exporter** | saída para backends | sim |
| **Connector** | liga a saída de um pipeline à entrada de outro (é exporter + receiver) | sim |
| **Extension** | capacidades fora do fluxo (health, auth, pprof, zpages, storage) | **não** |

### A regra de ouro: `service`
Declarar um componente **não o ativa**. Ele só funciona se for referenciado em `service.pipelines`. É o erro conceitual mais cobrado.

```yaml
service:
  extensions: [health_check]
  pipelines:
    traces:
      receivers: [otlp]
      processors: [memory_limiter, batch]
      exporters: [otlp]
  telemetry:   # observabilidade do PRÓPRIO collector
    logs: {level: info}
    metrics: {level: detailed}
```

### Lab 3.1 — Explorar o Collector rodando
1. Com o ambiente de pé, abra `http://localhost:55679/debug/servicez` (zPages) e veja as pipelines ativas.
2. `docker compose logs otel-collector` — ache a linha que lista pipelines/components na inicialização.
3. Acesse `http://localhost:8888/metrics` e veja as métricas internas (`otelcol_receiver_accepted_spans`, `otelcol_exporter_sent_spans`, etc.).

**Entregável:** liste os receivers, processors e exporters ativos no seu collector.

---

## Dia 2 — Configuration

Estrutura canônica do `config.yaml`:
```yaml
receivers:    # definições (não ativam nada sozinhas)
processors:
exporters:
connectors:
extensions:
service:      # o que de fato liga tudo
  extensions: [...]
  pipelines:
    traces:   { receivers, processors, exporters }
    metrics:  { ... }
    logs:     { ... }
  telemetry: { ... }
```

Pontos cobrados:
- Nomes com `tipo/nome` para **múltiplas instâncias**: `otlp/jaeger`, `otlp/backend2`.
- Ordem dos **processors importa**: eles rodam na sequência listada. `memory_limiter` **primeiro**, `batch` **por último** (antes do exporter) é a convenção.
- Um mesmo receiver/exporter pode ser usado em **vários pipelines**.
- Variáveis de ambiente: `${env:MINHA_VAR}`.

### Lab 3.2 — Editar a config
1. No `collector-config.yaml`, adicione um segundo exporter de debug só para logs e um pipeline de logs separado.
2. Adicione o processor `attributes` para inserir um atributo fixo:
   ```yaml
   processors:
     attributes/env:
       actions:
         - key: deployment.environment.name
           value: lab
           action: insert
   ```
3. Referencie `attributes/env` no pipeline de traces. `docker compose restart otel-collector`.
4. Gere tráfego e confirme no Jaeger o novo atributo nos spans.

**Entregável:** mostre o diff da sua config e explique por que `attributes/env` só teve efeito após entrar no `service`.

---

## Dia 3 — Processors essenciais

| Processor | O que faz | Cobrado? |
|---|---|---|
| **memory_limiter** | protege o Collector de OOM, aplica backpressure | ⭐ muito |
| **batch** | agrupa dados para eficiência de rede | ⭐ muito |
| **attributes** | insert/update/delete/hash de atributos | ⭐ |
| **resource** | manipula resource attributes | ⭐ |
| **filter** | descarta telemetria por condição | ⭐ |
| **transform** | OTTL — transformações ricas | ⭐ (dia 4) |
| **k8sattributes** | enriquece com metadata do Kubernetes | ⭐ |
| **resourcedetection** | detecta ambiente (cloud/host) | |
| **tail_sampling** | amostragem baseada no trace completo | ⭐ |
| **redaction** | remove/mascara dados sensíveis (PII) | |

**Ordem recomendada** num pipeline: `memory_limiter` → (enriquecimento: `k8sattributes`, `resource`, `attributes`) → (transform/filter/sampling) → `batch` → exporter.

**tail_sampling** (diferença-chave vs head-based do SDK): o Collector **espera o trace terminar** e decide com base no trace inteiro (ex.: manter se tem erro, ou latência > 2s). Precisa de todos os spans do trace no mesmo Collector → impacta o design de scaling (dia 5).

### Lab 3.3 — memory_limiter, filter e batch
1. Adicione `filter` para dropar spans de health check:
   ```yaml
   processors:
     filter/health:
       error_mode: ignore
       traces:
         span:
           - 'attributes["http.route"] == "/health"'
   ```
2. Ajuste o `batch` (`send_batch_size`, `timeout`) e observe no `:8888/metrics` o efeito em `otelcol_exporter_sent_spans`.
3. Reduza o `limit_mib` do memory_limiter e observe logs de recusa sob carga.

**Entregável:** explique o que o memory_limiter faz quando atinge o limite (dica: recusa dados e sinaliza backpressure).

---

## Dia 4 — Connectors e Transforming Data (OTTL)

### Connectors
Um **connector** é exporter de um pipeline **e** receiver de outro — liga pipelines e pode **mudar o tipo de sinal**.
| Connector | Faz |
|---|---|
| **spanmetrics** | gera **métricas** (RED) a partir de **traces** |
| **servicegraph** | gera métricas de grafo de serviços a partir de traces |
| **count** | conta spans/logs/métricas e emite como métrica |
| **routing** | roteia dados para pipelines diferentes por condição |
| **forward** | encaminha entre pipelines |
| **failover** | fallback entre exporters/pipelines |

Exemplo mental: `traces → spanmetrics → metrics → Prometheus` (deriva latência/erros sem instrumentar métricas na app).

### OTTL — OpenTelemetry Transformation Language
Linguagem usada pelos processors `transform` e `filter` (e outros) para manipular telemetria por **statements** e **conditions**.

Funções/estrutura (reconhecer na prova):
```yaml
transform:
  trace_statements:
    - context: span
      statements:
        - set(attributes["env"], "prod") where attributes["env"] == nil
        - replace_pattern(attributes["url.path"], "/user/[0-9]+", "/user/{id}")
        - delete_key(attributes, "senha")
        - keep_keys(attributes, ["http.method", "http.route"])
```
Operações comuns: `set`, `delete_key`, `keep_keys`, `replace_pattern`, `limit`, `truncate_all`, condições com `where`.

> 📎 Os **contextos OTTL** por sinal (`span`, `spanevent`, `metric`, `datapoint`, `log`, `resource`, `scope`) estão na seção 3 de [recursos/apendice-tecnico.md](../recursos/apendice-tecnico.md). Saber em qual contexto um statement roda é cobrado.

### Lab 3.4 — spanmetrics + OTTL
1. Adicione o connector `spanmetrics`:
   ```yaml
   connectors:
     spanmetrics:
   service:
     pipelines:
       traces:
         receivers: [otlp]
         processors: [memory_limiter, batch]
         exporters: [otlp/jaeger, spanmetrics]
       metrics:
         receivers: [otlp, spanmetrics]
         processors: [batch]
         exporters: [prometheus]
   ```
2. Gere tráfego e no Prometheus procure as métricas derivadas dos traces — tipicamente `calls_total` (contador de chamadas) e o histograma de duração exposto como `duration_milliseconds_bucket` / `_count` / `_sum`.
3. Adicione um `transform` que normaliza um atributo com `replace_pattern` e confirme no Jaeger.

**Entregável:** explique como o spanmetrics "muda o sinal" de trace para métrica e por que é útil.

---

## Dia 5 — Deployment e Scaling

### Padrões de deployment
| Padrão | Onde roda | Função |
|---|---|---|
| **Agent** | junto da app (sidecar, DaemonSet, no host) | coleta local, host metrics, logs, baixa latência |
| **Gateway** | serviço central (deployment com várias réplicas) | agregação, sampling, routing, egress único, segurança |
| **Sem Collector** | SDK exporta direto ao backend | simples, mas acopla app ao backend |

Arquitetura comum: `App → Agent (local) → Gateway (central) → Backends`.

### Scaling (cobrado)
- O **gateway escala horizontalmente** (mais réplicas atrás de um load balancer).
- **Cuidado com tail_sampling e spanmetrics**: precisam de **todos os spans de um trace no mesmo collector**. Com múltiplas réplicas, use um **load balancing exporter** por `traceID` numa camada de collectors antes dos que fazem tail sampling.
  ```
  Agents → Collector (loadbalancing exporter, roteia por traceID) → Collectors (tail_sampling) → Backend
  ```
- Dimensione com `memory_limiter`, réplicas e recursos (CPU/mem). Monitore as métricas internas (`:8888`) para ajustar.

### Segurança no Collector (cobrado em Deployment)
- **TLS / mTLS**: receivers e exporters OTLP suportam `tls:` (certificado, chave, CA). mTLS = ambos os lados se autenticam com certificado. Em dev usa-se `tls: {insecure: true}`.
- **Autenticação via extensions**: `basicauth`, `bearertokenauth`, `oauth2clientauth`, `headerssetter`, auth de cloud (AWS/Azure). O auth é referenciado pelo receiver (lado servidor) ou exporter (lado cliente).
- **Redaction / PII**: processor `redaction` e OTTL (`delete_key`) para remover dados sensíveis antes de exportar.
- Boas práticas: não logar segredos, usar `${env:...}` para credenciais, limitar quem fala com o gateway.

### Lab 3.5 — Dois níveis de collector
1. Adicione um segundo serviço `otel-gateway` no compose, com sua própria config.
2. No `otel-collector` (agent), troque o exporter de traces para `otlp` apontando para `otel-gateway:4317`.
3. No `otel-gateway`, receba OTLP e exporte para o Jaeger.
4. Gere tráfego e confirme o fluxo `app → agent → gateway → jaeger` (use o `debug` exporter em cada nível para rastrear).

**Entregável:** desenhe o fluxo e explique por que tail_sampling ficaria no gateway, não no agent.

---

## Dia 6 — Revisão + Quiz

### Resumo-relâmpago
- 5 componentes: receiver, processor, exporter, connector, extension (extension fica fora do fluxo).
- Nada funciona até estar no `service.pipelines`.
- Ordem de processors importa: memory_limiter primeiro, batch por último.
- Connector muda/deriva sinais (spanmetrics: trace→metric).
- OTTL: transform/filter com set/delete_key/keep_keys/replace_pattern + where.
- Deployment: agent (local) vs gateway (central). Gateway escala horizontalmente.
- tail_sampling/spanmetrics exigem todos os spans do trace no mesmo collector → loadbalancing por traceID.
- Distribuições: Core/Contrib/k8s/custom. **OCB** gera binário customizado (menor, mais seguro).
- Segurança: TLS/mTLS nos OTLP; auth via extensions; redaction para PII.

### Quiz — Semana 3

1. Quais são os 5 tipos de componente do Collector? Qual fica fora do fluxo de dados?
2. Declarei um processor mas ele não faz efeito. Qual o erro mais provável?
3. Em que ordem colocar `memory_limiter` e `batch` no pipeline, e por quê?
4. O que faz um connector? Dê um exemplo que muda o tipo de sinal.
5. O que é OTTL e em quais processors aparece?
6. Diferencie deployment agent e gateway.
7. Por que tail_sampling complica o scaling horizontal, e como resolver?
8. Como usar o mesmo exporter em dois pipelines diferentes?
9. O que o `memory_limiter` faz ao atingir o limite?
10. Diferença entre as distribuições Core e Contrib?
11. Onde o Collector expõe suas próprias métricas internas e health?
12. O que o processor `k8sattributes` adiciona e por que é útil?
13. O que é o OCB e por que criar uma distribuição customizada?
14. Diferença entre TLS e mTLS no Collector?

<details>
<summary><b>Gabarito Semana 3</b></summary>

1. Receiver, processor, exporter, connector, extension. **Extension** fica fora do fluxo de dados.
2. Ele não foi referenciado no `service.pipelines` — declarar não ativa.
3. `memory_limiter` **primeiro** (proteger memória/aplicar backpressure antes de processar) e `batch` **por último** (agrupar logo antes de exportar).
4. Liga a saída de um pipeline à entrada de outro (é exporter+receiver). Ex.: `spanmetrics` transforma traces em métricas.
5. OpenTelemetry Transformation Language; aparece em `transform` e `filter` (entre outros), via statements/conditions.
6. Agent roda junto da aplicação/host (coleta local); gateway é central/compartilhado (agregação, sampling, routing, egress).
7. tail_sampling precisa de todos os spans de um trace juntos; com múltiplas réplicas, roteie por `traceID` com um loadbalancing exporter antes da camada que faz tail sampling.
8. Referencie o mesmo exporter em `exporters:` de ambos os pipelines no `service`.
9. Recusa/descarta dados de entrada e aplica backpressure para evitar OOM.
10. Core = conjunto estável/essencial; Contrib = Core + componentes da comunidade (muito mais receivers/processors/exporters).
11. Métricas internas em `:8888/metrics`; health via extension `health_check` (`:13133`); diagnóstico via `zpages`.
12. Metadata do Kubernetes (namespace, pod, node, container, labels) à telemetria, correlacionando dados ao contexto do cluster.
13. OpenTelemetry Collector Builder — gera um binário customizado só com os componentes necessários (menor footprint, menor superfície de ataque, inclui componentes próprios).
14. TLS: só o servidor apresenta certificado (conexão criptografada); mTLS: cliente e servidor se autenticam mutuamente com certificado.

</details>

Próxima 👉 [Semana 4 — Pipelines & Revisão](../semana-4-pipelines-revisao/README.md)
