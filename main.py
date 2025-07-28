from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import smtplib
from email.message import EmailMessage
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuración del entorno Jinja2
templates_dir = Path(__file__).resolve().parent / "templates"
env = Environment(loader=FileSystemLoader(templates_dir))

# Configuración de correo
GMAIL_USER = "dev@leadgrowthco.com"
GMAIL_PASS = "tgnbe fkty nvqv uhmo"  

def generar_pdf(data: dict, filename="lead.pdf") -> Path:
    template = env.get_template("pdf_template.html")
    html_out = template.render(data=data)
    pdf_path = Path(filename)
    HTML(string=html_out).write_pdf(pdf_path)
    return pdf_path

def enviar_email(destinatario: str, asunto: str, cuerpo: str, archivo_pdf: Path):
    msg = EmailMessage()
    msg["Subject"] = asunto
    msg["From"] = GMAIL_USER
    msg["To"] = destinatario
    msg.set_content(cuerpo)

    # Adjuntar PDF
    with open(archivo_pdf, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=archivo_pdf.name)

    # Enviar correo
    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)

@app.post("/webhook")
async def recibir_datos(request: Request):
    data = await request.json()
    logger.info(f"📩 POST recibido: {data}")

    try:
        # Generar PDF
        pdf_path = generar_pdf(data)

        # Enviar correo (aquí puedes usar un campo de `data` como email de destino)
        enviar_email(
            destinatario="luis1233210e@gmail.com",
            asunto="Nuevo lead recibido",
            cuerpo="Adjunto el PDF con la información del lead.",
            archivo_pdf=pdf_path
        )

        # Elimina el PDF si deseas
        os.remove(pdf_path)

        return JSONResponse(content={"message": "PDF generado y correo enviado."})
    except Exception as e:
        logger.exception("Error procesando el webhook")
        return JSONResponse(status_code=500, content={"error": str(e)})
