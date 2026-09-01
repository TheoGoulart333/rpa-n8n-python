import json
import os
import smtplib
import sys
from datetime import datetime
from email.message import EmailMessage
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


BASE_DIR = Path(__file__).resolve().parent


def carregar_env() -> None:
    arquivo = BASE_DIR / ".env"
    if not arquivo.exists():
        return
    for linha in arquivo.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        os.environ.setdefault(chave.strip(), valor.strip())


def chamar_n8n() -> dict:
    payload = {
        "cliente": os.getenv("CLIENTE", "Theo Goulart"),
        "email_destino": os.getenv("EMAIL_DESTINO", "seu-email@gmail.com"),
        "mensagem": os.getenv(
            "MENSAGEM",
            "Gostaria de receber o relatorio atualizado de investimentos.",
        ),
    }
    dados = json.dumps(payload).encode("utf-8")
    requisicao = Request(
        os.getenv("N8N_WEBHOOK_URL", "http://localhost:5678/webhook/rpa-relatorio"),
        data=dados,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urlopen(requisicao, timeout=30) as resposta:
        return json.loads(resposta.read().decode("utf-8"))


def criar_email(resultado: dict) -> EmailMessage:
    mensagem = EmailMessage()
    mensagem["To"] = resultado["email_destino"]
    mensagem["From"] = os.getenv("SMTP_USUARIO", "automacao@localhost")
    mensagem["Subject"] = resultado["assunto"]
    mensagem.set_content(resultado["corpo"])
    return mensagem


def salvar_email(mensagem: EmailMessage) -> Path:
    pasta = BASE_DIR / "outbox"
    pasta.mkdir(exist_ok=True)
    nome = datetime.now().strftime("email-%Y%m%d-%H%M%S.eml")
    destino = pasta / nome
    destino.write_bytes(mensagem.as_bytes())
    return destino


def enviar_email(mensagem: EmailMessage) -> bool:
    usuario = os.getenv("SMTP_USUARIO", "")
    senha = os.getenv("SMTP_SENHA_APP", "")
    if not usuario or not senha:
        return False
    host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    porta = int(os.getenv("SMTP_PORT", "587"))
    with smtplib.SMTP(host, porta, timeout=30) as servidor:
        servidor.starttls()
        servidor.login(usuario, senha)
        servidor.send_message(mensagem)
    return True


def main() -> int:
    carregar_env()
    try:
        resultado = chamar_n8n()
        mensagem = criar_email(resultado)
        arquivo = salvar_email(mensagem)
        enviado = enviar_email(mensagem)
    except (HTTPError, URLError, TimeoutError, KeyError, ValueError) as erro:
        print(f"Falha na automacao: {erro}", file=sys.stderr)
        return 1

    print("E-mail enviado com sucesso." if enviado else "E-mail gerado; envio SMTP nao configurado.")
    print(f"Arquivo: {arquivo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

