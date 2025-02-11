import pytesseract
from pdf2image import convert_from_path
from PIL import Image
import openai
import os
import shutil

# Buscar la ruta de Tesseract
tesseract_path = shutil.which('tesseract')

if tesseract_path:
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
else:
    raise EnvironmentError("Tesseract no está instalado o no se encuentra en el PATH.")

# Leer la clave desde la variable de entorno
openai.api_key = os.getenv('OPENAI_API_KEY')

if not openai.api_key:
    raise ValueError("La clave de API de OpenAI no está configurada en la variable de entorno 'OPENAI_API_KEY'.")

# Ruta para almacenar archivos temporales
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def extraer_texto_factura(filepath):
    """
    Extrae texto de una factura que puede ser una imagen o un archivo PDF.
    """
    try:
        if filepath.lower().endswith(('.png', '.jpg', '.jpeg')):
            texto = pytesseract.image_to_string(Image.open(filepath), lang='spa')
        elif filepath.lower().endswith('.pdf'):
            pages = convert_from_path(filepath)
            texto = ''
            for page in pages:
                texto += pytesseract.image_to_string(page, lang='spa')
        else:
            raise ValueError("Formato de archivo no compatible. Usa PNG, JPG o PDF.")
    except Exception as e:
        texto = f"Error al procesar la factura: {str(e)}"
    
    return texto

def analizar_factura_con_openai(texto_factura):
    """
    Analiza el texto extraído de la factura utilizando la API de OpenAI para obtener
    información relevante como zona, consumo promedio y costo del kWh.
    """
    prompt = f"""
    A continuación tienes el texto de una factura de servicios públicos. Extrae la siguiente información si está disponible:

    1. Ciudad y Departamento: Ejemplo: Medellín, Antioquia.
    2. Región correspondiente según la ciudad (elige una de las siguientes):
        - Costa Caribe
        - Región Andina
        - Región Pacífica
        - Llanos Orientales
        - Amazonía
        - Desierto de la Guajira
    3. Consumo promedio mensual de energía en kWh.
    4. Costo del kWh en pesos colombianos (COP).

    Texto de la factura:
    \"\"\"{texto_factura}\"\"\"

    Responde en el siguiente formato:
    Zona del Proyecto: <zona>
    Consumo promedio mensual de energía: <valor> kWh/mes
    Costo del kWh: $<valor> COP
    """

    try:
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un asistente que extrae datos de facturas de servicios públicos."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        resultado = respuesta.choices[0]['message']['content'].strip()
    except Exception as e:
        resultado = f"Error al analizar la factura con OpenAI: {str(e)}"
    
    return resultado
