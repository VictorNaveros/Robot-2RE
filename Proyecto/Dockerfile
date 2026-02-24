FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Instalar solo lo necesario
RUN apt-get update && apt-get install -y \
    default-libmysqlclient-dev \
    build-essential \
    pkg-config \
    libgl1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# 🚀 Mejor forma de instalar dependencias
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["gunicorn", "Proyecto.wsgi:application", "--bind", "0.0.0.0:8000"]