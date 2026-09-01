# GitHub Repo Health Dashboard

Um projeto de automação em Python que consulta a API do GitHub, mede a saúde de um repositório e publica um dashboard estático em `docs/index.html`. O projeto também mantém a automação RPA local com n8n e Python como exemplo de integração.

## O que ele entrega

- coleta estrelas, forks, issues, pull requests, linguagens e execuções do GitHub Actions;
- calcula uma pontuação de saúde de 0 a 100 e sugere melhorias;
- gera uma página responsiva pronta para GitHub Pages;
- atualiza o painel diariamente e sob demanda com GitHub Actions;
- mantém o fluxo original de webhook n8n + Python em `workflows/`.

## Ver agora

Para criar uma prévia local sem token:

```bash
python3 github_dashboard.py --demo
open docs/index.html
```

Para consultar um repositório real, defina `GITHUB_REPOSITORY` e, se necessário, `GITHUB_TOKEN` no ambiente. O token é usado somente para autenticar as consultas e nunca deve ser salvo no repositório.

## Automação diária

O workflow `.github/workflows/dashboard.yml` roda uma vez por dia e também pode ser iniciado manualmente na aba **Actions**. Ele usa o token automático do GitHub, gera o HTML e grava a atualização no próprio repositório.

Para exibir a página, ative GitHub Pages nas configurações do repositório, escolhendo a pasta `docs` da branch `main`.

## Iniciar pela primeira vez

No Terminal, dentro desta pasta:

```bash
npm install
cp .env.example .env
npm run importar
npm run ativar
npm run n8n
```

Abra `http://localhost:5678`, crie apenas o usuario local solicitado pelo n8n, abra o fluxo **RPA - Relatorio por Webhook** e clique em **Active**.

Em outro Terminal, execute:

```bash
python3 disparar.py
```

O e-mail gerado aparece em `outbox/`. Ele pode ser aberto normalmente no aplicativo de e-mail.

## Envio real pelo Gmail

Edite `.env` e preencha:

```text
EMAIL_DESTINO=destinatario@gmail.com
SMTP_USUARIO=seu-email@gmail.com
SMTP_SENHA_APP=sua-senha-de-app-do-google
```

Use uma senha de app do Google, nunca a senha normal da conta. Depois, execute `python3 disparar.py` novamente.

## Fluxo

```text
Python -> Webhook n8n -> Validacao -> Geracao do relatorio -> Resposta -> E-mail
```

O projeto usa somente a biblioteca padrao do Python. A primeira instalacao do n8n exige internet e pode levar alguns minutos.

## Próximo passo para o GitHub Developer Program

Este repositório já contém uma integração funcional com a API do GitHub. Para a candidatura, falta completar no perfil um e-mail público de suporte e publicar uma página de documentação ou demonstração. O programa não é automático nem garantido: o GitHub analisa a aplicação enviada.

## Contribuindo

Contribuicoes sao bem-vindas. Veja [CONTRIBUTING.md](CONTRIBUTING.md) para rodar o projeto, abrir issues e enviar Pull Requests.

Boas primeiras tarefas ficam marcadas com `good first issue`. Melhorias de documentacao, testes e pequenos ajustes de interface sao excelentes pontos de entrada para novos contribuidores.
