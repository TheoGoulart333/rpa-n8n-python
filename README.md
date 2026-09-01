# RPA local com n8n e Python

Projeto pronto para rodar sem conta no n8n e sem Docker. O n8n fica instalado localmente, recebe um pedido por webhook, gera o relatorio e devolve o texto ao Python. O Python cria um arquivo de e-mail e, quando o Gmail estiver configurado, envia a mensagem automaticamente.

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
