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
GMAIL_PASS = "rablsocexhfirukg"  

# Claves que no deben ir al PDF ni imprimirse
EXCLUDED_KEYS = {
    "location", "user", "workflow", "triggerData", 
    "contact", "attributionSource", "customData"
}

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

    with open(archivo_pdf, "rb") as f:
        msg.add_attachment(f.read(), maintype="application", subtype="pdf", filename=archivo_pdf.name)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(GMAIL_USER, GMAIL_PASS)
        smtp.send_message(msg)

@app.post("/webhook")
async def recibir_datos(request: Request):
    raw_data = await request.json()
    logger.info(f"📩 POST recibido completo: {raw_data}")

    try:
        # Filtrar solo datos del formulario (excluir campos innecesarios)
        filtered_data = {k: v for k, v in raw_data.items() if k not in EXCLUDED_KEYS}
        logger.info(f"✅ Datos filtrados del formulario: {filtered_data}")

        # Generar PDF
        pdf_path = generar_pdf(filtered_data)

        # Enviar correo
        enviar_email(
            destinatario="luis1233210e@gmail.com",
            asunto="Nuevo lead recibido",
            cuerpo="Adjunto el PDF con la información del lead.",
            archivo_pdf=pdf_path
        )

        os.remove(pdf_path)
        logger.info(f"🗑️ PDF eliminado: {pdf_path}")
        return JSONResponse(content={"message": "PDF generado y correo enviado."})

    except Exception as e:
        logger.exception("❌ Error procesando el webhook")
        return JSONResponse(status_code=500, content={"error": str(e)})
