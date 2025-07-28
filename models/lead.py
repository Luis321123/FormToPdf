from typing import Dict, Set

class LeadDataProcessor:
    EXCLUDED_KEYS: Set[str] = {
        "tags", "fbcid", "leads prueba", "fecha de creación", "fuente del lead", "contact_type",
        "job title", "any additional comments or suggestions", "estimated number of users",
        "preferred contact method", "please select the services you're interested in",
        "which crm features are you most interested in", "options", "tipo vehículo",
        "signature 1h3t", "timestamp masivos", "make", "timestamp respuesta", "model", "year",
        "primer mensaje registrado", "whatsapp automation active", "envio primer mensaje",
        "whatsapp active on/off", "número de veces contactado", "hora de primer mensaje",
        "mortgage/ rent payment", "do you have your social security number", "fecha de agendamiento",
        "inicial", "sede", "hora respuesta del vendedor", "fecha de venta cerrada",
        "última vez contactado", "documentación",
        "tienes al menos $1,500 para el down payment",
        "tienes cuenta de banco y social"
    }

    EXCLUDED_NESTED_KEYS: Set[str] = {
        "location", "user", "workflow", "triggerData", "contact", "attributionSource", "customData"
    }

    TRANSLATIONS: Dict[str, str] = {
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