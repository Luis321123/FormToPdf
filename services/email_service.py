import smtplib
from pathlib import Path
from email.message import EmailMessage
from config import settings

class EmailService:
    def __init__(self):
        self.smtp_server = settings.SMTP_SERVER
        self.smtp_port = settings.SMTP_PORT
        self.gmail_user = settings.GMAIL_USER
        self.gmail_pass = settings.GMAIL_PASS
    
    def send_email_with_pdf(self, recipient: str, subject: str, body: str, pdf_path: Path):
        """Envía un email con un PDF adjunto."""
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = self.gmail_user
        msg["To"] = recipient
        msg.set_content(body)

        # Adjuntar PDF
        with open(pdf_path, "rb") as f:
            msg.add_attachment(
                f.read(), 
                maintype="application", 
                subtype="pdf", 
                filename=pdf_path.name
            )

        # Enviar email
        with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port) as smtp:
            smtp.login(self.gmail_user, self.gmail_pass)
            smtp.send_message(msg)