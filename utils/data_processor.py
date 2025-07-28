from typing import Dict
from models.lead import LeadDataProcessor

def normalize_key(key: str) -> str:
    """Normaliza una clave para comparación."""
    return key.strip().lower().replace(":", "").replace("¿", "").replace("?", "")

def clean_lead_data(data: dict) -> Dict[str, any]:
    """Limpia y procesa los datos del lead."""
    processor = LeadDataProcessor()
    clean_data = {}

    for k, v in data.items():
        # Omitir diccionarios anidados
        if isinstance(v, dict):
            continue

        # Normalizar clave para comparación
        normalized = normalize_key(k)

        # Excluir claves no deseadas
        if normalized in map(normalize_key, processor.EXCLUDED_KEYS):
            continue

        # Traducir clave si existe traducción
        translated_key = processor.TRANSLATIONS.get(k.strip(), k.strip())
        clean_data[translated_key] = v

    return clean_data