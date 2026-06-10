FROM python:3.12-slim

WORKDIR /app

# Dependencias del proyecto
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia el código de la aplicación
COPY . .

ENV PYTHONUNBUFFERED=1

# Ejecuta el programa principal
CMD ["python", "main.py"]
