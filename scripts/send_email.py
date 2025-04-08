import os
import smtplib
from email.message import EmailMessage

def main():
    sender = os.environ.get("EMAIL_USER")
    password = os.environ.get("EMAIL_PASSWORD")
    receiver = os.environ.get("DEST_EMAIL")

    if not all([sender, password, receiver]):
        raise EnvironmentError("Faltando variáveis de ambiente: EMAIL_USER, EMAIL_PASSWORD ou DEST_EMAIL.")

    msg = EmailMessage()
    msg.set_content("Tudo certo! O pipeline foi executado com sucesso no GitHub Actions.")
    msg["Subject"] = "Pipeline executado com sucesso!"
    msg["From"] = sender
    msg["To"] = receiver

    # Para servidores SMTP que usam SSL, como o Gmail
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, password)
        smtp.send_message(msg)

if __name__ == "__main__":
    main()
