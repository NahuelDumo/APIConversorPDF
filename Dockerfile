# Imagen base de Python
FROM python:3.10-slim

# Variables de entorno para evitar errores con debconf
ENV DEBIAN_FRONTEND=noninteractive

# Instalamos dependencias del sistema necesarias para Playwright
RUN apt-get update && apt-get install -y \
    wget gnupg unzip curl \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libxkbcommon0 libgtk-3-0 \
    libasound2 libxcomposite1 libxdamage1 libxrandr2 libgbm1 libxshmfence1 \
    libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libdrm2 libx11-xcb1 \
    libxext6 libxfixes3 libxrender1 libxcb1 libx11-6 libglib2.0-0 \
    libfontconfig1 libfreetype6 fonts-liberation libappindicator3-1 \
    && apt-get clean

# Directorio de trabajo
WORKDIR /app

# Copiamos archivos
COPY requirements.txt .
COPY . .

# Instalamos las dependencias Python y Playwright
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN playwright install --with-deps

# Exponer puerto
EXPOSE 8000

# Comando de inicio
# Comando para iniciar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
