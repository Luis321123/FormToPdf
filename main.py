from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import logging
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from pathlib import Path
import smtplib
from email.message import EmailMessage
import tempfile
import os

app = FastAPI()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Configuración de Gmail
GMAIL_USER = "dev@leadgrowthco.com"
GMAIL_PASS = "rablsocexhfirukg"

# Configuración de plantillas
templates_dir = Path(__file__).resolve().parent / "templates"
env = Environment(loader=FileSystemLoader(templates_dir))

# Campos a excluir
EXCLUDED_KEYS = {
    "tags", "fbcid", "Leads prueba", "Fecha de creación", "Fuente del lead", "contact_type",
    "Job Title::", "Any additional comments or suggestions?:", "Estimated Number of Users::",
    "Preferred Contact Method::", "Please select the services you’re interested in::",
    "Which CRM features are you most interested in?:", "Options :", "Tipo vehículo:",
    "Signature 1h3t:", "Timestamp masivos:", "Make:", "Timestamp Respuesta:", "Model:", "Year:",
    "Primer mensaje registrado:", "WhatsApp Automation Active:", "¿Envio primer mensaje?:",
    "WhatsApp Active ON/OFF:", "Número de veces contactado:", "Hora de primer mensaje:",
    "Mortgage/ Rent Payment: 2", "Do you have your social security number?: ['Yes']",
    "fecha de agendamiento", "inicial", "sede:", "hora respuesta del vendedor",
    "fechad e venta cerrada", "ultima vez contactado:", "Options:", "Documentación:",
    "Última vez contactado:", "Fecha de venta cerrada:"
}

EXCLUDED_NESTED_KEYS = {"location", "user", "workflow", "triggerData", "contact", "attributionSource", "customData"}

TRANSLATIONS = {
    "First Name": "First Name",
    "Middle name": "Middle Name",
    "Last Name": "Last Name",
    "Phone": "Phone",
    "Email": "Email",
    "Date of birth": "Date of Birth",
    "Address": "Address",
    "City": "City",
    "State": "State",
    "Zip code": "ZIP Code",
    "Do you have your social security number?": "Has SSN",
    "Mortgage/ Rent Payment": "Monthly Rent/Mortgage",
    "Residence Type": "Residence Type",
    "Time at Residence": "Time at Residence",
    "Employment status": "Employment Status",
    "Employer name": "Employer Name",
    "Employer Address": "Employer Address",
    "Employer city": "Employer City",
    "Employer State": "Employer State",
    "Employer ZIP": "Employer ZIP",
    "Business Phone": "Business Phone",
    "Occupation": "Occupation",
    "Time on Job": "Time on Job",
    "How often are you paid?": "Payment Frequency",
    "Gross income": "Gross Income",
    "Other Income": "Other Income",
    "Pay stubs 1": "Pay Stub 1",
    "Pay stubs 2": "Pay Stub 2",
    "Pay stubs 3": "Pay Stub 3",
    "Pay stubs 4": "Pay Stub 4",
    "Pay stubs 5": "Pay Stub 5",
    "Down Payment Amount:": "Down Payment Amount",
    "Trade-in Make:": "Trade-in Make",
    "Trade-in Model:": "Trade-in Model",
    "Trade-in Year:": "Trade-in Year",
    "Additional Comments:": "Additional Comments"
}


def normalize_key(key: str) -> str:
    return key.strip().lower().replace(":", "").replace("¿", "").replace("?", "")


def generar_pdf(data: dict) -> Path:
    clean_data = {
        TRANSLATIONS.get(k.strip(), k.strip()): v
        for k, v in data.items()
        if k.strip() not in EXCLUDED_KEYS and k not in EXCLUDED_NESTED_KEYS and not isinstance(v, dict)
    }

    template = env.get_template("pdf_template.html")
    html_out = template.render(data=clean_data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
        HTML(string=html_out).write_pdf(tmp_file.name)
        return Path(tmp_file.name)


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
    try:
        data = await request.json()
        logger.info("📩 POST recibido")

        pdf_path = generar_pdf(data)

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
