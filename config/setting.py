import os
from pathlib import Path
from typing import Set, Dict

class Settings:
    # Gmail configuration
    GMAIL_USER: str = "dev@leadgrowthco.com"
    GMAIL_PASS: str = "rablsocexhfirukg"  # En producción usar variables de entorno
    
    # Email settings
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 465
    
    # Templates
    TEMPLATES_DIR: Path = Path(__file__).resolve().parent.parent / "templates"
    
    # Recipient email
    RECIPIENT_EMAIL: str = "luis1233210e@gmail.com"
    
    # Email content
    EMAIL_SUBJECT: str = "Nuevo lead recibido"
    EMAIL_BODY: str = "Adjunto el PDF con la información del lead."

settings = Settings()