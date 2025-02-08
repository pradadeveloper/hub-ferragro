from flask import Flask, render_template, request, send_file
from modules.pdf_generator import generar_pdf
from modules.pdf_generator_ferragro import generar_pdf_ferragro
from modules.calculos_solar import calcular_proyecto
from modules.calculadora_ia import extraer_texto_factura, analizar_factura_con_openai
import json
import os
from datetime import datetime

app = Flask(__name__)

# 🗕 LOGICA DEL NUMERO DE COTIZACIÓN
def cargar_cotizacion():
    if os.path.exists("cotizacion.json"):
        with open("cotizacion.json", "r") as file:
            return json.load(file).get("cotizacion", 0)
    return 0

def guardar_cotizacion(numero):
    with open("cotizacion.json", "w") as file:
        json.dump({"cotizacion": numero}, file)

cotizacion_contador = cargar_cotizacion()

# --------------------- RUTAS ------------------------------

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/calculadora_solar')
def calculadora_solar():
    return render_template('calculadora_solar.html')

@app.route('/calculadora_ia')
def calculadora_solar_ia():
    return render_template('calculadora_ia.html')

@app.route('/calculadora_equipos')
def calculadora_equipos():
    return render_template('calculadora_equipos.html')

@app.route('/calculadora_equipos_ferragro')
def calculadora_equipos_ferragro():
    return render_template('calculadora_equipos_ferragro.html')

@app.route('/generar_pdf', methods=['POST'])
def generar_pdf_route():
    global cotizacion_contador
    cotizacion_contador += 1
    guardar_cotizacion(cotizacion_contador)

    try:
        cliente = request.form['cliente']
        proyecto = request.form['proyecto']
        celular = request.form['celular']
        correo_asesor = request.form['correo_asesor']
        correo = request.form['correo']
        ubicacion = request.form['ubicacion']
        potencia = float(request.form['potencia'])
        costo = float(request.form['costo'])
        area = float(request.form['area'])

        fecha_cotizacion = datetime.now().strftime("%d/%m/%Y")

        datos_proyecto = calcular_proyecto(ubicacion, potencia, costo)

        pdf_path = generar_pdf(
            cotizacion_contador, fecha_cotizacion, cliente, proyecto, celular,
            correo, correo_asesor, ubicacion, potencia, costo, area, datos_proyecto
        )

        return send_file(pdf_path, as_attachment=True)
    except KeyError as e:
        return f"Error: Falta el campo {str(e)} en el formulario", 400
    except ValueError:
        return "Error: Verifica que los campos numéricos sean correctos.", 400

@app.route('/generar_pdf_ferragro', methods=['POST'])
def generar_pdf_ferragro_route():
    global cotizacion_contador
    cotizacion_contador += 1
    guardar_cotizacion(cotizacion_contador)

    try:
        cliente = request.form['cliente']
        proyecto = request.form['proyecto']
        celular = request.form['celular']
        correo_asesor = request.form['correo_asesor']
        correo = request.form['correo']
        ubicacion = request.form['ubicacion']
        potencia = float(request.form['potencia'])
        costo = float(request.form['costo'])
        area = float(request.form['area'])

        fecha_cotizacion = datetime.now().strftime("%d/%m/%Y")

        datos_proyecto = calcular_proyecto(ubicacion, potencia, costo)

        pdf_path = generar_pdf_ferragro(
            cotizacion_contador, fecha_cotizacion, cliente, proyecto, celular,
            correo, correo_asesor, ubicacion, potencia, costo, area, datos_proyecto
        )

        return send_file(pdf_path, as_attachment=True)
    except KeyError as e:
        return f"Error: Falta el campo {str(e)} en el formulario", 400
    except ValueError:
        return "Error: Verifica que los campos numéricos sean correctos.", 400

@app.route('/procesar_factura', methods=['POST'])
def procesar_factura():
    if 'factura_frontal' not in request.files or 'factura_atras' not in request.files:
        return "No se adjuntaron ambas facturas.", 400

    factura_frontal = request.files['factura_frontal']
    factura_atras = request.files['factura_atras']

    if factura_frontal.filename == '' or factura_atras.filename == '':
        return "Uno o ambos archivos están vacíos.", 400

    upload_folder = 'uploads'
    os.makedirs(upload_folder, exist_ok=True)

    filepath_frontal = os.path.join(upload_folder, factura_frontal.filename)
    filepath_atras = os.path.join(upload_folder, factura_atras.filename)

    factura_frontal.save(filepath_frontal)
    factura_atras.save(filepath_atras)

    # Extraer texto de las facturas
    texto_frontal = extraer_texto_factura(filepath_frontal)
    texto_atras = extraer_texto_factura(filepath_atras)

    texto_completo = texto_frontal + "\n" + texto_atras

    # Imprimir el texto extraído para depuración
    print("Texto extraído de la factura:")
    print(texto_completo)

    # Procesar el texto con OpenAI
    datos_extraidos_texto = analizar_factura_con_openai(texto_completo)

    # Imprimir la respuesta de OpenAI para depuración
    print("Respuesta de OpenAI:")
    print(datos_extraidos_texto)

    # Convertir el texto en diccionario
    datos_extraidos = {}
    for linea in datos_extraidos_texto.split('\n'):
        if ':' in linea:
            clave, valor = linea.split(':', 1)
            datos_extraidos[clave.strip()] = valor.strip()

    print("Datos extraídos procesados:")
    print(datos_extraidos)

    # Obtener los valores extraídos
    zona_proyecto = datos_extraidos.get('Zona del Proyecto', 'No disponible')
    consumo_promedio_kwh = datos_extraidos.get('Consumo promedio mensual de energía', '0')
    costo_kwh = datos_extraidos.get('Costo del kWh', '0')

    # Verificar si los datos se extrajeron correctamente
    if not zona_proyecto or not consumo_promedio_kwh or not costo_kwh:
        return "No se pudieron extraer todos los datos necesarios de la factura.", 400

    # Limpiar y convertir los valores numéricos
    consumo_promedio_kwh = float(consumo_promedio_kwh.replace('kWh/mes', '').replace(',', '').strip())
    costo_kwh = float(costo_kwh.replace('COP', '').replace('$', '').replace(',', '').strip())

    # Limpiar la zona antes del cálculo
    zona_proyecto_limpia = zona_proyecto.split('-')[-1].strip()

    # Calcular el proyecto
    datos_proyecto = calcular_proyecto(zona_proyecto_limpia, consumo_promedio_kwh, costo_kwh)

    return render_template('resultado_factura.html', datos={
    "Zona del Proyecto": zona_proyecto,
    "Consumo promedio mensual de energía": f"{consumo_promedio_kwh} kWh/mes",
    "Costo del kWh": f"${costo_kwh} COP",
    "Resultados Generales": datos_proyecto["Resultados Generales"]
    }, cliente=request.form)

@app.route('/diligenciamiento_contratos')
def diligenciamiento_contratos():
    return render_template('diligenciamiento_contratos.html')

@app.route('/instalaciones_terceros')
def instalaciones_terceros():
    return render_template('instalaciones_terceros.html')

@app.route('/sagrilaft')
def sagrilaft():
    return render_template('sagrilaft.html')

# --------------------- EJECUCIÓN DEL SERVIDOR ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
