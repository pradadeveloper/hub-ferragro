FROM python:3.11-slim

# Instalar Tesseract y sus dependencias
RUN apt-get update && \
    apt-get install -y tesseract-ocr tesseract-ocr-spa libleptonica-dev pkg-config poppler-utils && \
    apt-get clean

# Configurar el directorio de trabajo
WORKDIR /app

# Copiar los archivos del proyecto
COPY . .

# Instalar las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Exponer el puerto para Render
EXPOSE 10000

# Comando para iniciar la aplicación
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:10000"]
