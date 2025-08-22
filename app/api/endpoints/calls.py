from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
import json
from datetime import datetime 
import logging

from app.core.database import get_session
from app.models.CallCrm import CallCrmDriverUs

router = APIRouter()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@router.post("/webhook/lead")
async def receive_webhook(request: Request, db: Session = Depends(get_session)):
    try:
        payload = await request.json()
        logger.info("📥 Webhook recibido:")
        logger.info(json.dumps(payload, indent=2, ensure_ascii=False))

        call_data = payload.get('data', {})
        custom_data = payload.get('customData', {})  # 👈 extraemos customData

        # Registrar customData si está presente
        if custom_data:
            logger.info("📞 Registrando llamada desde customData")

            call = CallCrmDriverUs(
                user_from=custom_data.get("user_from"),
                stamp_time=custom_data.get("stamp_time"),
                status_call=custom_data.get("status_call"),
                duration=custom_data.get("duration"),
                contact_id=custom_data.get("contact_id"),
                direction=custom_data.get("direction")
            )
            db.add(call)
            db.commit()
            db.refresh(call)
            db.close()

            logger.info(f"✅ Llamada registrada con UUID: {call.uuid}")
        else:
            logger.warning("⚠️ No se encontró 'customData' en el webhook")

        # Análisis adicional (grabación, duración, etc.)
        if call_data.get('answered_at'):
            logger.info("✅ Llamada ATENDIDA")

            duration = call_data.get('duration', 0)
            answered_at = call_data.get('answered_at', 0)
            ended_at = call_data.get('ended_at', 0)

            talk_time = ended_at - answered_at if all([answered_at, ended_at]) else 0

            if talk_time < 5:
                logger.warning(f"⚠️ Grabación corta o vacía. Duración: {talk_time}s")

            if not call_data.get('recording'):
                logger.error("❌ No se encontró URL de grabación")

        elif call_data.get('missed_call_reason'):
            logger.warning(f"⛔ Llamada NO atendida: {call_data['missed_call_reason']}")
        else:
            logger.warning("⚠️ Estado de llamada desconocido")

        return {"status": "ok", "message": "llamada recibida"}

    except Exception as e:
        logger.exception("❌ Error al procesar el webhook")
        return {"status": "error", "message": str(e)}