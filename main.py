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
logger = logging.getLogger("main")

# Plantillas
templates_dir = Path(__file__).resolve().parent / "templates"
env = Environment(loader=FileSystemLoader(templates_dir))

# Correo
GMAIL_USER = "dev@leadgrowthco.com"
GMAIL_PASS = "rablsocexhfirukg"

EXCLUDED_KEYS = {
    "tags", "fbcid", "leads prueba", "fecha de creación", "fuente del lead", "contact_type",
    "job title", "any additional comments or suggestions", "estimated number of users",
    "preferred contact method", "please select the services you’re interested in",
    "which crm features are you most interested in", "options", "tipo vehículo", "signature 1h3t",
    "timestamp masivos", "make", "timestamp respuesta", "model", "year", "primer mensaje registrado",
    "whatsapp automation active", "envio primer mensaje", "do you have your social security number",
    "whatsapp active on/off", "mortgage/ rent payment", "número de veces contactado",
    "hora de primer mensaje", "location", "user", "workflow", "triggerdata", "contact",
    "attributionsource", "customdata"
}

def normalizar_clave(key: str) -> str:
    return key.strip().lower().replace(":", "").replace("¿", "").replace("?", "")

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
    data = await request.json()
    logger.info("📩 POST recibido")

    try:
        form_data = {
            k: v for k, v in data.items()
            if normalizar_clave(k) not in {normalizar_clave(e) for e in EXCLUDED_KEYS}
        }

        logger.info(f"🔍 Campos incluidos en PDF: {form_data.keys()}")

        pdf_path = generar_pdf(form_data)

        enviar_email(
            destinatario="luis1233210e@gmail.com",
            asunto="Nuevo lead recibido",
            cuerpo="Adjunto el PDF con la información del lead.",
            archivo_pdf=pdf_path
        )

        os.remove(pdf_path)
        logger.info(f"✅ PDF generado y enviado: {pdf_path}")
        return JSONResponse(content={"message": "PDF generado y correo enviado."})

    except Exception as e:
        logger.exception("❌ Error procesando el webhook")
        return JSONResponse(status_code=500, content={"error": str(e)})
