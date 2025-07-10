# Usamos la imagen oficial de Playwright con Ubuntu y navegadores preinstalados
FROM mcr.microsoft.com/playwright:focal

# Directorio de trabajo dentro del contenedor
WORKDIR /app

# Copiamos el archivo de dependencias y el código
COPY requirements.txt .
COPY . .

# Instalamos las dependencias Python
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# (Opcional) Si necesitás instalar algo extra de sistema, podés hacerlo aquí con apt-get

# Puerto expuesto
EXPOSE 8000

# Comando para iniciar la app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
