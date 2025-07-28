from fastapi import FastAPI, Request
import logging


app = FastAPI()

# Configura los logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)

logger = logging.getLogger(__name__)

app = FastAPI()

@app.post("/webhook")
async def receive_post(request: Request):
    body = await request.json()
    logger.info(f"📩 POST recibido: {body}")
    return {"message": "Datos recibidos correctamente"}
