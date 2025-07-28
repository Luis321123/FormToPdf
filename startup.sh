export PYTHONPATH=/app

apt-get update && apt-get install -y \
    libpango-1.0-0 \
    libcairo2 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libpq-dev \
    build-essential \
    python3-dev \
    libxml2 \
    libxslt1.1 \
    libjpeg-dev \
    libpng-dev \
    libpangocairo-1.0-0 \
    fonts-liberation \
    fonts-dejavu \
    fonts-freefont-ttf



echo " Iniciando FastAPI..."
uvicorn main:app --host 0.0.0.0 --port 8000
