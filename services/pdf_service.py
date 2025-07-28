import tempfile
from pathlib import Path
from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
from config import settings
from utils.data_processor import clean_lead_data

class PDFService:
    def __init__(self):
        self.env = Environment(loader=FileSystemLoader(settings.TEMPLATES_DIR))
    
    def generate_pdf(self, data: dict) -> Path:
        """Genera un PDF a partir de los datos del lead."""
        clean_data = clean_lead_data(data)
        
        template = self.env.get_template("pdf_template.html")
        html_content = template.render(data=clean_data)
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp_file:
            HTML(string=html_content).write_pdf(tmp_file.name)
            return Path(tmp_file.name)