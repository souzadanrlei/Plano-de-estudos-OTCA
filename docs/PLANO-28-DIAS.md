# Plano Consolidado — 28 Dias (checklist)

Marque cada dia ao concluir. Cada dia = teoria + lab + quiz do dia (~1h30–2h30). Dias de folga opcionais nos fins de semana; ajuste as datas.

> Preencha a data de início: **____/____/______**

---

## Semana 1 — Fundamentos (18%)
- [ ] **Dia 1** — Observabilidade vs monitoramento; por que OTel. *(Semana 1, Dia 1)*
- [ ] **Dia 2** — Sinais (traces/metrics/logs/profiles) + Lab 1.1. ⚠️ baggage não é sinal
- [ ] **Dia 3** — Semantic Conventions e Resource + Lab 1.2
- [ ] **Dia 4** — Instrumentação (manual/library/zero-code) + Lab 1.3
- [ ] **Dia 5** — Analysis & Outcomes (RED/USE/SLO) + Lab 1.4
- [ ] **Dia 6** — Revisão + Quiz Semana 1
- [ ] **Dia 7** — Folga / repasse flashcards de Fundamentos

## Semana 2 — API & SDK (46%) ⭐ domínio mais pesado
- [ ] **Dia 8** — API vs SDK, no-op, data model + Lab 2.1
- [ ] **Dia 9** — Tracing SDK: pipeline, SpanProcessors + Lab 2.2
- [ ] **Dia 10** — Sampling (head-based), default = parentbased_always_on + Lab 2.3
- [ ] **Dia 11** — Metrics SDK: views, readers + Lab 2.4
- [ ] **Dia 12** — Logs SDK + Context Propagation + Lab 2.5
- [ ] **Dia 13** — Configuration + Agents (OpAMP/eBPF/Operator) + Quiz Semana 2
- [ ] **Dia 14** — Folga / repasse flashcards de API & SDK (foco redobrado)

## Semana 3 — Collector (26%)
- [ ] **Dia 15** — Anatomia + `service` + distribuições/OCB + Lab 3.1
- [ ] **Dia 16** — Configuration (ler/escrever config.yaml) + Lab 3.2
- [ ] **Dia 17** — Processors essenciais + Lab 3.3
- [ ] **Dia 18** — Connectors + OTTL + Lab 3.4
- [ ] **Dia 19** — Deployment (agent/gateway) + Scaling + Segurança (TLS/auth) + Lab 3.5
- [ ] **Dia 20** — Revisão + Quiz Semana 3
- [ ] **Dia 21** — Folga / repasse flashcards de Collector

## Semana 4 — Pipelines (10%) + Revisão + Simulados
- [ ] **Dia 22** — Debugging + propagação quebrada + Lab 4.1
- [ ] **Dia 23** — Error handling (queue/retry/storage) + Lab 4.2
- [ ] **Dia 24** — Schema Management + Lab 4.3
- [ ] **Dia 25** — Revisão geral (cheatsheets + apêndice técnico) + flashcards completos
- [ ] **Dia 26** — **Simulado 1** cronometrado + correção + caderno de erros
- [ ] **Dia 27** — **Simulado 2** cronometrado + correção + revisar erros
- [ ] **Dia 28** — **Simulado 3 (pegadinhas)** + repasse final + checklist véspera

---

## Marcos de verificação
- [ ] Fim da Semana 1: explico sinais, SpanKind, instrumentos de métrica
- [ ] Fim da Semana 2: explico API vs SDK, sampling default, propagação, SpanContext
- [ ] Fim da Semana 3: monto um pipeline do Collector de cabeça
- [ ] Fim da Semana 4: ≥ 85% nos 3 simulados → **agendar exame**

## Mapa de confiança (auto-diagnóstico)

Avalie cada competência de 1 (inseguro) a 5 (domino e explico). Refaça ao fim de cada semana. Só agende o exame quando **tudo ≥ 4**. Dê prioridade de revisão ao que tiver nota menor — e lembre que o domínio 2 vale 46%.

| Competência | Domínio | Peso | S1 | S2 | S3 | S4 |
|---|---|---|---|---|---|---|
| Sinais / telemetry data | D1 | 18% | | | | |
| Semantic conventions / Resource | D1 | 18% | | | | |
| Instrumentação (manual/lib/zero-code) | D1 | 18% | | | | |
| API vs SDK / no-op | D2 | 46% | | | | |
| Tracing SDK / span processors | D2 | 46% | | | | |
| Sampling (head, default, parentbased) | D2 | 46% | | | | |
| Metrics SDK (views/readers/temporality) | D2 | 46% | | | | |
| Context propagation / propagadores | D2 | 46% | | | | |
| Configuration / agents | D2 | 46% | | | | |
| Agents (OpAMP, eBPF, Operator) | D2 | 46% | | | | |
| Collector: componentes / service | D3 | 26% | | | | |
| Processors / ordem | D3 | 26% | | | | |
| Connectors / OTTL | D3 | 26% | | | | |
| Deployment / scaling / segurança | D3 | 26% | | | | |
| Distribuições / OCB / extensão | D3 | 26% | | | | |
| Debugging pipelines | D4 | 10% | | | | |
| Error handling / resiliência | D4 | 10% | | | | |
| Schema management | D4 | 10% | | | | |

> Preencha a coluna da semana atual (S1–S4) a cada revisão. A tendência deve ser crescente.

## Links rápidos
- Teoria: [S1](semana-1-fundamentos/README.md) · [S2](semana-2-api-sdk/README.md) · [S3](semana-3-collector/README.md) · [S4](semana-4-pipelines-revisao/README.md)
- Prática: [Ambiente](00-ambiente/README.md)
- Treino: [Simulado 1](simulados/simulado-1.md) · [Simulado 2](simulados/simulado-2.md) · [Simulado 3](simulados/simulado-3.md) · [Gabaritos](simulados/gabaritos.md)
- Revisão: [Flashcards](recursos/flashcards.md) · [Cheatsheets](recursos/README.md) · [Apêndice técnico](recursos/apendice-tecnico.md)
