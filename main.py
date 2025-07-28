import logging
from fastapi import FastAPI
from routers import webhook_router

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("main")

# Silenciar logs verbosos
logging.getLogger("weasyprint").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Crear aplicación FastAPI
app = FastAPI(
    title="Lead Processing API",
    description="API para procesar leads y generar PDFs",
    version="1.0.0"
)

# Incluir routers
app.include_router(webhook_router)

@app.get("/")
async def root():
    return {"message": "Lead Processing API is running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)