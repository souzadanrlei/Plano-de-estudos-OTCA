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
        <a href="semana-1-fundamentos/" class="md-button md-button--primary">Começar a estudar · Dia 1</a>
        <a href="PLANO-28-DIAS.md" class="md-button">Ver cronograma completo</a>
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

## Trilha completa de estudo

Se a dúvida é “por onde começar?”, siga esta ordem do primeiro ao último passo:

<div class="feature-grid">
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">1️⃣</div>
    <h3><a href="semana-1-fundamentos/">Semana 1 — Fundamentos</a></h3>
    <p>Entenda observabilidade, sinais, contexto, spans e os princípios que sustentam o resto da trilha.</p>
  </div>
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">2️⃣</div>
    <h3><a href="semana-2-api-sdk/">Semana 2 — API & SDK</a></h3>
    <p>Veja como a API, SDK, samplers, propagadores e métricas funcionam na prática.</p>
  </div>
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">3️⃣</div>
    <h3><a href="semana-3-collector/">Semana 3 — Collector</a></h3>
    <p>Aprenda pipelines, processors, exporters, deploy e arquitetura para coleta e transformação de dados.</p>
  </div>
  <div class="feature-card" data-animate="fade-up">
    <div class="feature-icon">4️⃣</div>
    <h3><a href="semana-4-pipelines-revisao/">Semana 4 — Revisão e pipelines</a></h3>
    <p>Feche a trilha com revisão, troubleshooting, comparações de arquitetura e simulados.</p>
  </div>
</div>

> ✅ Caminho recomendado: comece em [Semana 1](semana-1-fundamentos/README.md), siga em ordem e finalize com [Simulados](simulados/simulado-1.md).

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

Antes de qualquer conteúdo mais avançado, melhor subir a stack de laboratório:

```bash
docker compose -f 00-ambiente/docker-compose.yaml up -d
```

Depois, siga a ordem abaixo:

1. [Semana 1 — Fundamentos](semana-1-fundamentos/README.md)
2. [Semana 2 — API & SDK](semana-2-api-sdk/README.md)
3. [Semana 3 — Collector](semana-3-collector/README.md)
4. [Semana 4 — Revisão e pipelines](semana-4-pipelines-revisao/README.md)
5. [Simulados](simulados/simulado-1.md)

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

Se quiser um começo objetivo, clique em [Semana 1 — Fundamentos](semana-1-fundamentos/README.md). Se quiser ver a jornada completa primeiro, abra [PLANO-28-DIAS.md](PLANO-28-DIAS.md).

---

## Fontes e referências

- [Linux Foundation OTCA](https://training.linuxfoundation.org/certification/opentelemetry-certified-associate-otca/)
- [CNCF — OTCA](https://www.cncf.io/training/certification/otca/)
- [OpenTelemetry documentation](https://opentelemetry.io/docs/)
