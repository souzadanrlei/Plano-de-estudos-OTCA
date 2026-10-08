"""App de exemplo para os labs do plano OTCA.

Rodar com instrumentação zero-code apontando para o Collector:

    pip install flask opentelemetry-distro opentelemetry-exporter-otlp
    opentelemetry-bootstrap -a install

    # PowerShell:
    $env:OTEL_SERVICE_NAME = "demo-app"
    $env:OTEL_EXPORTER_OTLP_ENDPOINT = "http://localhost:4318"
    $env:OTEL_EXPORTER_OTLP_PROTOCOL = "http/protobuf"
    opentelemetry-instrument flask run --port 8080

Gerar tráfego:
    for ($i=0; $i -lt 50; $i++) { curl http://localhost:8080/; curl http://localhost:8080/erro }
"""
from flask import Flask
import time
import random

# Tracer manual (usado no Lab 1.3): coexiste com a instrumentação automática.
from opentelemetry import trace

app = Flask(__name__)
tracer = trace.get_tracer("demo-app.manual")


@app.route("/")
def hello():
    # Span manual aninhado dentro do span HTTP gerado automaticamente.
    with tracer.start_as_current_span("regra-de-negocio") as span:
        span.set_attribute("cliente.tier", random.choice(["free", "premium"]))
        time.sleep(random.uniform(0.01, 0.3))
    return "ok\n"


@app.route("/erro")
def erro():
    raise RuntimeError("falha proposital para gerar span de erro")


if __name__ == "__main__":
    app.run(port=8080)
