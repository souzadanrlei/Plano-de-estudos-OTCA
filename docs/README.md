# Plano de Estudos OTCA

<div class="hero" data-animate="fade-up">
  <div class="hero-grid">
    <div>
      <span class="kicker">Certificação OTCA</span>
      <h2>Estude com método, prática e revisão contínua.</h2>
      <p>
        Este material foi organizado para transformar a teoria em rotina produtiva: você acompanha a jornada em 4 semanas,
        valida conceitos com labs reais e reforça os pontos mais exigidos na prova.
      </p>
      <div class="hero-actions">
        <a href="PLANO-28-DIAS.md" class="md-button md-button--primary">Ver cronograma</a>
        <a href="00-ambiente/README.md" class="md-button">Preparar ambiente</a>
      </div>
      <div class="badge-row">
        <span class="badge">4 semanas</span>
        <span class="badge">Hands-on</span>
        <span class="badge">Simulados</span>
      </div>
    </div>
    <div class="progress-panel" data-animate="fade-up">
      <strong>Fluxo recomendado</strong>
      <div class="progress-steps">
        <div class="progress-step" data-step="1">Teoria e conceitos</div>
        <div class="progress-step" data-step="2">Labs práticos</div>
        <div class="progress-step" data-step="3">Revisão ativa</div>
        <div class="progress-step" data-step="4">Simulados</div>
      </div>
    </div>
  </div>
</div>

## Visão geral

Este repositório foi organizado para funcionar como um plano de estudo completo em 4 semanas, combinando teoria, prática, testes e revisão contínua.

- Objetivo: preparar você para a certificação OTCA
- Perfil: estudo guiado e prático
- Modelo: teoria + laboratórios + revisão + simulados

<div class="feature-grid">
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">📘</div>
    <h3>Estrutura clara</h3>
    <p>Você acompanha uma jornada organizada por semana e por objetivo de estudo.</p>
  </div>
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">🧪</div>
    <h3>Laboratórios reais</h3>
    <p>O ambiente com Docker, Prometheus, Jaeger e Grafana ajuda a validar o comportamento real da telemetria.</p>
  </div>
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">✅</div>
    <h3>Revisão ativa</h3>
    <p>Flashcards e simulados ajudam a reforçar o que importa para a prova.</p>
  </div>
</div>

## O que você vai encontrar

- [Simulado 1](simulados/simulado-1.md), [Simulado 2](simulados/simulado-2.md), [Simulado 3](simulados/simulado-3.md)
- [Plano 28 dias](PLANO-28-DIAS.md)
- [Recursos e flashcards](recursos/README.md)
- [Ambiente de labs](00-ambiente/README.md)

---

## Como começar

### 1) Prepare o ambiente

```bash
docker compose -f 00-ambiente/docker-compose.yaml up -d
```

### 2) Siga o planejamento

Reserve um tempo por dia e siga o checklist em [PLANO-28-DIAS.md](PLANO-28-DIAS.md).

### 3) Faça os labs

Use a documentação da pasta [00-ambiente/README.md](00-ambiente/README.md) para validar conceitos com traces, métricas e visualização.

### 4) Revise com repetição espaçada

Use [recursos/flashcards.md](recursos/flashcards.md) e os simulados para reforçar os pontos de maior risco.

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
