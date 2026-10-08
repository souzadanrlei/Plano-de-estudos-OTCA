# Ambiente de Labs OTCA

Esta seção reúne os recursos necessários para você executar o ambiente de demonstração do OpenTelemetry e validar o comportamento dos sinais de telemetry em cenário real.

## Visão geral

O ambiente inclui:

- `docker-compose.yaml` — orquestra os serviços do laboratório
- `collector-config.yaml` — configuração do OpenTelemetry Collector
- `prometheus.yaml` — coleta e armazenamento de métricas
- `datasources.yaml` — provisionamento dos data sources do Grafana
- `app.py` — aplicação Flask com rastreio manual e falha proposital

## Início rápido

### Opção 1: a partir da pasta do ambiente

```bash
cd 00-ambiente
docker compose up -d
```

### Opção 2: a partir da raiz do projeto

```bash
docker compose -f 00-ambiente/docker-compose.yaml up -d
```

## Endpoints úteis

- Jaeger UI: http://localhost:16686
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Collector health check: http://localhost:13133

## Executando a aplicação de exemplo

```powershell
cd 00-ambiente
pip install flask opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

$env:OTEL_SERVICE_NAME = "demo-app"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
opentelemetry-instrument flask run --port 8080
```

Depois, gere tráfego para testar o pipeline:

```powershell
for ($i=0; $i -lt 50; $i++) { curl http://localhost:8080/; curl http://localhost:8080/erro }
```

> O endpoint `/erro` gera uma falha proposital para evidenciar spans com erro e rastros de exceção.

## Dicas práticas

- Se o Grafana não carregar os data sources, verifique se os arquivos em `00-ambiente/grafana/provisioning/datasources/` existem.
- Se o Collector não iniciar, confirme que a porta 4318 está livre e que o arquivo `collector-config.yaml` está correto.
- Para acompanhar a propagação de contexto, visualize os traces no Jaeger em paralelo com o Prometheus e o Grafana.

## Próximo passo

Depois de subir o ambiente, siga para a [Semana 1 — Fundamentos](../semana-1-fundamentos/README.md) e comece a explorar os conceitos da observabilidade em prática.
