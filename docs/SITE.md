# Publicar como site (GitHub Pages via MkDocs)

Este plano de estudos pode ser publicado como um site navegável (com busca e tema escuro) usando **MkDocs Material**. O conteúdo é o mesmo Markdown — nada é duplicado.

---

## 1. Pré-visualizar localmente

Requer Python 3.9+. O `mkdocs.yml` fica na **raiz do repositório**, então rode os comandos de lá.

```powershell
# a partir da raiz do repositório
python -m pip install -r requirements.txt
python -m mkdocs serve
```

Abra http://127.0.0.1:8000 — o site recarrega automaticamente ao editar os `.md`.

Para gerar o site estático localmente:

```powershell
python -m mkdocs build
# saída em _site/
```

---

## 2. Publicar no GitHub Pages (automático)

Já existe um workflow em `.github/workflows/deploy-docs.yml` (na raiz do repositório) que faz build e deploy a cada push.

### Passo a passo
1. **Suba o projeto para um repositório GitHub** (se ainda não estiver):
   ```powershell
   git init
   git add .
   git commit -m "Plano de estudos OTCA + site MkDocs"
   git branch -M main
   git remote add origin https://github.com/SEU-USUARIO/SEU-REPO.git
   git push -u origin main
   ```
2. No GitHub, vá em **Settings → Pages** e em **Build and deployment → Source** selecione **GitHub Actions**.
3. Edite o `mkdocs.yml` e ajuste a linha `site_url` para o seu endereço:
   ```yaml
   site_url: https://SEU-USUARIO.github.io/SEU-REPO/
   ```
4. Faça push. O workflow roda sozinho e publica. O endereço aparece em **Settings → Pages** e no resumo da Action.

> O workflow dispara em pushes na branch `main`/`master` que alterem arquivos Markdown, `mkdocs.yml` ou o workflow de deploy. Você também pode rodar manualmente em **Actions → Deploy OTCA site → Run workflow**.

---

## 3. Publicar manualmente (alternativa sem Actions)

```powershell
# a partir da raiz do repositório (opentelemetry/)
mkdocs gh-deploy --force
```

Isso faz build e empurra para a branch `gh-pages`. Nesse caso, em **Settings → Pages** escolha **Deploy from a branch → gh-pages**.

---

## 4. Estrutura relevante

```
Plano-de-estudos-OTCA/            <- raiz do repositório
├── mkdocs.yml                   <- configuração do site
├── requirements.txt             <- dependências do build
├── README.md                    <- home do site
├── PLANO-28-DIAS.md             <- cronograma diário
├── SITE.md                      <- este guia
├── .github/workflows/deploy-docs.yml
├── 00-ambiente/
├── semana-1-fundamentos/
├── semana-2-api-sdk/
├── semana-3-collector/
├── semana-4-pipelines-revisao/
├── simulados/
├── recursos/
└── ...
```

> A estrutura do repositório foi ajustada para manter a raiz como o conteúdo do site, com `docs_dir: .` e caminhos consistentes para os diretórios de material e laboratórios.
---

## 5. Observações
- Os blocos `<details>` dos gabaritos funcionam no site (extensão `pymdownx.details`).
- A busca está habilitada em português.
- O tema tem alternância claro/escuro no topo.
- Os arquivos de lab (`docker-compose.yaml`, `app.py`, etc.) não viram páginas, mas continuam no repositório para download/clone.
