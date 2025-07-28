import os
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from services import PDFService, EmailService
from config import settings

router = APIRouter()
logger = logging.getLogger("webhook")

@router.post("/webhook")
async def receive_webhook_data(request: Request):
    """Endpoint para recibir datos del webhook y procesar leads."""
    try:
        data = await request.json()
        logger.info("📩 POST recibido")

        # Inicializar servicios
        pdf_service = PDFService()
        email_service = EmailService()

        # Generar PDF
        pdf_path = pdf_service.generate_pdf(data)
        logger.info(f"📄 PDF generado: {pdf_path}")

        # Enviar email
        email_service.send_email_with_pdf(
            recipient=settings.RECIPIENT_EMAIL,
            subject=settings.EMAIL_SUBJECT,
            body=settings.EMAIL_BODY,
            pdf_path=pdf_path
        )
        logger.info("📧 Email enviado exitosamente")

        # Limpiar archivo temporal
        os.remove(pdf_path)
        logger.info(f"🗑️ Archivo temporal eliminado: {pdf_path}")

        return JSONResponse(content={"message": "PDF generado y correo enviado exitosamente."})

    except Exception as e:
        logger.exception("❌ Error procesando el webhook")
        return JSONResponse(
            status_code=500, 
            content={"error": f"Error interno del servidor: {str(e)}"}
        )