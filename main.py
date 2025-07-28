from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from weasyprint import HTML
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
import logging
import tempfile

app = FastAPI()
logger = logging.getLogger("main")

# Lista de claves exactas y patrones a excluir
EXCLUDED_KEYS = {
    "tags", "fbcid", "Fecha de creación", "Fuente del lead", "contact_type", "Job Title::",
    "Any additional comments or suggestions?:", "Estimated Number of Users::", "Preferred Contact Method::",
    "Please select the services you’re interested in::", "Which CRM features are you most interested in?:",
    "Options :", "Tipo vehículo:", "Signature 1h3t:", "Timestamp masivos:", "Make:", "Timestamp Respuesta:",
    "Model:", "Year:", "Primer mensaje registrado:", "WhatsApp Automation Active:", "¿Envio primer mensaje?:",
    "Do you have your social security number?:", "WhatsApp Active ON/OFF:", "Mortgage/ Rent Payment: 2",
    "Número de veces contactado:", "Hora de primer mensaje:", "fecha de agendamiento", "inicial", "sede",
    "hora respuesta del vendedor", "fecha de venta cerrada", "última vez contactado", "Fecha de venta cerrada:",
    "Options:", "Documentación:", "Última vez contactado:"
}

EXCLUDED_NESTED_KEYS = {"location", "user", "workflow", "triggerData", "contact", "attributionSource", "customData"}

# Diccionario para traducir campos
FIELD_TRANSLATIONS = {
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
    "Residence Type:": "Residence Type",
    "Time at Residence:": "Time at Residence",
    "Employment status": "Employment Status",
    "Employer name:": "Employer Name",
    "Employer Address:": "Employer Address",
    "Employer city:": "Employer City",
    "Employer State:": "Employer State",
    "Employer ZIP:": "Employer ZIP",
    "Business Phone:": "Business Phone",
    "Occupation:": "Occupation",
    "Time on Job:": "Time on Job",
    "How often are you paid?": "Payment Frequency",
    "Gross income:": "Gross Income",
    "Other Income:": "Other Income",
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

@app.post("/webhook")
async def receive_data(request: Request):
    data = await request.json()
    logger.info("📩 POST recibido")

    # Filtrar campos planos válidos
    filtered_data = {
        FIELD_TRANSLATIONS.get(k.strip(), k): v
        for k, v in data.items()
        if k.strip() not in EXCLUDED_KEYS and k not in EXCLUDED_NESTED_KEYS and not isinstance(v, dict)
    }

    # Crear PDF
    env = Environment(loader=FileSystemLoader("templates"))
    template = env.get_template("pdf_template.html")
    html_content = template.render(data=filtered_data)

    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as f:
        HTML(string=html_content).write_pdf(f.name)
        logger.info(f"✅ PDF generado en {f.name}")

    return JSONResponse({"message": "Datos procesados y PDF generado"})
