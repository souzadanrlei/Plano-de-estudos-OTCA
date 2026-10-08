# Plano de Estudos OTCA

Guia prático para você passar na certificação OpenTelemetry Certified Associate (OTCA) com foco em aprendizado progressivo, exercícios e labs reais.

## Visão geral

Este repositório foi organizado para funcionar como um plano de estudo completo em 4 semanas, com teoria, prática, simulações e revisão ativa.

- Objetivo: preparar você para a certificação OTCA
- Perfil: estudo auto-dirigido, com foco em observabilidade e OpenTelemetry
- Modelo: teoria + laboratórios + revisão + simulados

## O que você vai encontrar

- [PLANO-28-DIAS.md](PLANO-28-DIAS.md): cronograma diário e checklist de estudo
- [00-ambiente/README.md](00-ambiente/README.md): ambiente de labs com Docker, Prometheus, Jaeger e Grafana
- [semana-1-fundamentos/README.md](semana-1-fundamentos/README.md): fundamentos de observabilidade
- [semana-2-api-sdk/README.md](semana-2-api-sdk/README.md): API e SDK do OpenTelemetry
- [semana-3-collector/README.md](semana-3-collector/README.md): Collector e pipelines
- [semana-4-pipelines-revisao/README.md](semana-4-pipelines-revisao/README.md): debugging e revisão final
- [Simulado 1](simulados/simulado-1.md), [Simulado 2](simulados/simulado-2.md), [Simulado 3](simulados/simulado-3.md): simulados e gabaritos
- [recursos/README.md](recursos/README.md): flashcards, glossário e apêndice técnico

---

## Como começar

### 1) Prepare o ambiente

```bash
docker compose -f 00-ambiente/docker-compose.yaml up -d
```

### 2) Siga o planejamento

Reserve um tempo por dia e siga o checklist em [PLANO-28-DIAS.md](PLANO-28-DIAS.md).

### 3) Faça os labs

Use a pasta [00-ambiente/README.md](00-ambiente/README.md) para validar conceitos com traces, métricas e visualização.

### 4) Revise com repetição espaçada

Use [recursos/flashcards.md](recursos/flashcards.md) e os simulados para fixar os pontos de maior risco.

---

## Cronograma recomendado

| Semana | Foco | Peso |
|---|---|---|
| 1 | Fundamentos de observabilidade | 18% |
| 2 | API e SDK | 46% |
| 3 | Collector | 26% |
| 4 | Pipelines, debugging e revisão | 10% |

### Ritmo sugerido diário

- 20 a 30 minutos de leitura
- 40 a 60 minutos de laboratório
- 15 a 20 minutos de revisão
- 10 minutos de anotações

---

## Pré-requisitos

- Docker + Docker Compose
- Python 3.9+
- `curl`
- Editor de texto ou IDE

---

## Critérios para se sentir pronto

- [ ] Entender a diferença entre trace, span e span context
- [ ] Explicar como os sinais de telemetria se relacionam
- [ ] Ler e interpretar uma configuração do Collector
- [ ] Reconhecer as diferenças entre propagadores e instrumentação
- [ ] Acertar pelo menos 85% dos simulados

---

## Dica de estudo

A maior parte da prova não é sobre memorizar comandos; é sobre entender o fluxo de dados e a arquitetura. Foque em raciocínio, contexto e diagnóstico.

Comece por aqui: [Semana 1 — Fundamentos](semana-1-fundamentos/README.md)

---

## Fontes e referências

- [Linux Foundation OTCA](https://training.linuxfoundation.org/certification/opentelemetry-certified-associate-otca/)
- [CNCF — OTCA](https://www.cncf.io/training/certification/otca/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
