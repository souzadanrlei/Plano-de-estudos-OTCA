# Ambiente de Labs OTCA

Esta pasta reúne os arquivos necessários para montar o ambiente de demonstração usado durante o estudo da certificação OTCA.

## Conteúdo

- `docker-compose.yaml` — sobe o Collector, Jaeger, Prometheus e Grafana
- `collector-config.yaml` — configuração do OpenTelemetry Collector
- `prometheus.yaml` — scrape para métricas do Collector e da app
- `datasources.yaml` — provisionamento de datasources para Grafana
- `app.py` — aplicação Flask com rastreio manual e falhas propositalmente geradas

## Subir o ambiente

A partir da raiz do repositório:

```bash
cd 00-ambiente
docker compose up -d
```

Ou, se você estiver na raiz do projeto:

```bash
docker compose -f 00-ambiente/docker-compose.yaml up -d
```

## Verificações rápidas

- Jaeger UI: http://localhost:16686
- Prometheus: http://localhost:9090
- Grafana: http://localhost:3000
- Collector health: http://localhost:13133

## Aplicação de exemplo

A aplicação Flask pode ser executada localmente ou via `opentelemetry-instrument` apontando para o Collector:

```powershell
cd 00-ambiente
pip install flask opentelemetry-distro opentelemetry-exporter-otlp
opentelemetry-bootstrap -a install

$env:OTEL_SERVICE_NAME = "demo-app"
$env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
$env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
opentelemetry-instrument flask run --port 8080
```

Depois, gere tráfego:

```powershell
for ($i=0; $i -lt 50; $i++) { curl http://localhost:8080/; curl http://localhost:8080/erro }
```

> O endpoint `/erro` gera uma falha proposital para demonstrar spans com erro e rastros de exceção.
