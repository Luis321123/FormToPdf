export PYTHONPATH=/app

apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libpq-dev \
    python3-dev \
    build-essential


echo " Iniciando FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000