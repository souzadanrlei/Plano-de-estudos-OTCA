# Plano de Estudos OTCA — OpenTelemetry Certified Associate (4 semanas)

Guia completo de 4 semanas para preparar e passar na certificação **OpenTelemetry Certified Associate (OTCA)**, da Linux Foundation / CNCF.

---

## 1. Sobre o exame

| Item | Detalhe |
|---|---|
| Nome | OpenTelemetry Certified Associate (OTCA) |
| Autoridade | Linux Foundation / CNCF |
| Formato | Online, proctored (supervisionado remotamente) |
| Duração | 90 minutos |
| Questões | ~60, múltipla escolha e múltipla seleção |
| Nota de aprovação | ~75% |
| Validade | ~3 anos |
| Nível | Associate (fundamentos — não exige programação pesada) |

> O exame é **vendor-neutral** e **conceitual**. Não é um exame hands-on (sem terminal como no CKA/CKAD), mas as questões cobram entendimento prático de configuração, data model, sinais, pipelines e propagação de contexto. Os labs deste plano existem para **fixar os conceitos**, não porque o exame exige digitação.

Fontes: [Linux Foundation OTCA](https://training.linuxfoundation.org/certification/opentelemetry-certified-associate-otca/), [CNCF OTCA](https://www.cncf.io/training/certification/otca/), [opentelemetry.io blog](https://opentelemetry.io/blog/2025/otca-for-newcomers-and-advanced-users/). Detalhes de formato (duração/questões/nota) conforme guias públicos de preparação; confirme os números atuais no checkout oficial, pois podem mudar. *Conteúdo resumido/parafraseado para conformidade com licenciamento.*

---

## 2. Domínios e pesos

| # | Domínio | Peso | Semana |
|---|---|---|---|
| 1 | Fundamentals of Observability | **18%** | Semana 1 |
| 2 | The OpenTelemetry API and SDK | **46%** | Semana 2 |
| 3 | The OpenTelemetry Collector | **26%** | Semana 3 |
| 4 | Maintaining and Debugging Observability Pipelines | **10%** | Semana 4 |

> O domínio 2 (API e SDK) vale quase metade da prova. Dedique a Semana 2 inteira a ele e revise com carinho.

### Competências por domínio

**1. Fundamentals of Observability (18%)**
- Telemetry Data — sinais: traces, metrics, logs, profiles (baggage é propagação de contexto, não sinal)
- Semantic Conventions
- Instrumentation (manual, automática, zero-code)
- Analysis and Outcomes

**2. The OpenTelemetry API and SDK (46%)**
- Data Model
- Composability and Extension
- Configuration
- Signals (Tracing, Metric, Log)
- SDK Pipelines
- Context Propagation
- Agents

**3. The OpenTelemetry Collector (26%)**
- Configuration
- Deployment
- Scaling
- Pipelines
- Transforming Data

**4. Maintaining and Debugging Observability Pipelines (10%)**
- Context Propagation
- Debugging Pipelines
- Error Handling
- Schema Management

---

## 3. Estrutura do material

```
otca-study-plan/
├── README.md                      <- você está aqui
├── PLANO-28-DIAS.md               <- checklist diário consolidado
├── 00-ambiente/
│   ├── README.md                  <- setup docker-compose dos labs
│   ├── docker-compose.yaml        <- pronto para `docker compose up -d`
│   ├── collector-config.yaml
│   ├── prometheus.yaml
│   ├── app.py                     <- app de exemplo instrumentada
│   └── grafana/provisioning/      <- data sources Prometheus + Jaeger automáticos
├── semana-1-fundamentos/README.md
├── semana-2-api-sdk/README.md
├── semana-3-collector/README.md
├── semana-4-pipelines-revisao/README.md
├── simulados/
│   ├── simulado-1.md              <- 30 questões
│   ├── simulado-2.md              <- 30 questões (múltipla seleção)
│   ├── simulado-3.md              <- 30 questões (pegadinhas + tópicos avançados)
│   └── gabaritos.md               <- gabaritos comentados dos 3
└── recursos/
    ├── README.md                  <- cheatsheets, glossário, links
    ├── flashcards.md              <- ~70 cards de revisão espaçada
    └── apendice-tecnico.md        <- detalhes finos (OTLP, traceparent, OTTL, métricas internas)
```

---

## 4. Cronograma de 4 semanas

Planejamento sugerido: **~1h30 a 2h30 por dia**, 5–6 dias por semana. Ajuste conforme sua rotina.

| Semana | Foco | Carga | Peso na prova |
|---|---|---|---|
| 1 | Fundamentos de observabilidade | ~10h | 18% |
| 2 | API & SDK (o coração da prova) | ~14h | 46% |
| 3 | Collector | ~12h | 26% |
| 4 | Pipelines, debugging, revisão e simulados | ~10h | 10% + revisão geral |

### Ritmo diário sugerido (template)
- **20–30 min** — leitura da teoria do dia
- **40–60 min** — laboratório prático
- **15–20 min** — quiz / flashcards do dia
- **10 min** — anotar dúvidas num "caderno de erros"

---

## 5. Como usar este material

1. Siga o [PLANO-28-DIAS.md](PLANO-28-DIAS.md) — é o checklist diário que amarra tudo.
2. Comece pelo [setup de ambiente](00-ambiente/README.md): `docker compose up -d` (os arquivos já estão prontos).
3. Siga as semanas na ordem. Cada semana tem: **teoria → labs → quiz**.
4. Use os [flashcards](recursos/flashcards.md) para revisão espaçada (refaça os errados a cada 2 dias).
5. Mantenha um **caderno de erros**: toda questão que errar, anote o porquê (template nos gabaritos).
6. Faça os [simulados](simulados/simulado-1.md) na Semana 4, cronometrados. O simulado 3 foca nas pegadinhas.
7. Revise o [glossário e cheatsheets](recursos/README.md) nos últimos dias.

### Critério de "pronto para o exame"
- [ ] Acertar **≥ 85%** nos três simulados (margem acima dos 75% reais)
- [ ] Explicar com suas palavras: trace vs span vs span context
- [ ] Montar de cabeça um pipeline do Collector (receiver → processor → exporter)
- [ ] Diferenciar os propagadores (W3C TraceContext, Baggage, B3, Jaeger) e os 3 tipos de instrumentação
- [ ] Saber ler um `config.yaml` do Collector e dizer o que cada bloco faz
- [ ] Acertar as pegadinhas: baggage ≠ sinal; sampler default = parentbased_always_on; Gauge síncrono ≠ Observable Gauge

---

## 6. Pré-requisitos de software (para os labs)

- Docker + Docker Compose
- Uma linguagem à sua escolha para instrumentação manual (Python é a mais rápida de demonstrar; exemplos em Python inclusos)
- `curl` e um editor de texto

Veja detalhes em [00-ambiente/README.md](00-ambiente/README.md).

---

Bons estudos. Comece por aqui 👉 [Semana 1 — Fundamentos](semana-1-fundamentos/README.md)
