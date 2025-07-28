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
    "location", "user", "workflow", "triggerData", "contact", "attributionSource", "customData",
    "tags", "fbcid", "Leads prueba", "Fecha de creación", "Fuente del lead", "contact_type",
    "Job Title::", "Any additional comments or suggestions?:", "Estimated Number of Users::",
    "Preferred Contact Method::", "Please select the services you’re interested in::",
    "Which CRM features are you most interested in?:", "Options :", "Tipo vehículo:",
    "Signature 1h3t:", "Timestamp masivos:", "Make:", "Timestamp Respuesta:", "Model:",
    "Year:", "Primer mensaje registrado:", "WhatsApp Automation Active:", "¿Envio primer mensaje?:",
    "Do you have your social security number?:", "WhatsApp Active ON/OFF:",
    "Mortgage/ Rent Payment:", "Número de veces contactado:", "Hora de primer mensaje:"
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
    data = await request.json()
    logger.info(f"📩 POST recibido")

    try:
        # Filtrar los datos del formulario
        form_data = {k: v for k, v in data.items() if k not in EXCLUDED_KEYS}

        # Generar PDF con los datos filtrados
        pdf_path = generar_pdf(form_data)

        # Enviar correo
        enviar_email(
            destinatario="luis1233210e@gmail.com",
            asunto="Nuevo lead recibido",
            cuerpo="Adjunto el PDF con la información del lead.",
            archivo_pdf=pdf_path
        )

        os.remove(pdf_path)
        logger.info(f"PDF generado y enviado correctamente: {pdf_path}")
        return JSONResponse(content={"message": "PDF generado y correo enviado."})

    except Exception as e:
        logger.exception("Error procesando el webhook")
        return JSONResponse(status_code=500, content={"error": str(e)})
