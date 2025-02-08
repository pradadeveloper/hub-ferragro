from fpdf import FPDF
import os

# Carpeta donde se guardarán los PDFs generados
PDF_FOLDER = 'generated_pdfs'
os.makedirs(PDF_FOLDER, exist_ok=True)

def format_value(value, unit=""):
    """ Formatea valores numéricos eliminando los decimales si son enteros. """
    if isinstance(value, (int, float)):  
        if value == int(value):
            return f"{int(value)} {unit}".strip()  # Convierte a entero sin decimales
        else:
            return f"{value:,.2f} {unit}".replace(",", ".")  # Formato con decimales si es necesario
    return str(value)  # Si no es número, devolverlo como texto

def add_red_title(pdf, title):
    """ Agrega un título con fondo rojo y letra blanca en toda la fila. """
    pdf.set_fill_color(34, 139, 34) # Verde
    pdf.set_text_color(255, 255, 255)  # Blanco
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, title, ln=True, align='C', fill=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # Restablece el color de texto a negro

def agregar_forma_pago_y_mantenimiento(pdf):
    """ Agrega la sección de Forma de Pago y Mantenimiento Anual en el PDF. """
    
    # ✅ Sección FORMA DE PAGO
    add_red_title(pdf, "Forma de Pago")

    pdf.set_font('Arial', '', 12)

    # Tabla centrada
    table_width = 130
    col_width_1 = table_width * 0.7
    col_width_2 = table_width * 0.3
    x_start = (pdf.w - table_width) / 2
    pdf.set_x(x_start)

    # Encabezados
    pdf.cell(col_width_1, 10, "Concepto", border=1, align='C')
    pdf.cell(col_width_2, 10, "Porcentaje", border=1, align='C')
    pdf.ln()

    forma_pago = [
        ("Anticipo", "50%"),
        ("Entrega de materiales", "40%"),
        ("Retie", "10%")
    ]

    for concepto, porcentaje in forma_pago:
        pdf.set_x(x_start)  
        pdf.cell(col_width_1, 10, concepto, border=1, align='C')
        pdf.cell(col_width_2, 10, porcentaje, border=1, align='C')
        pdf.ln()

    pdf.ln(10)  

    # ✅ Sección MANTENIMIENTO ANUAL
    add_red_title(pdf, "Mantenimiento Anual")

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, "Monto: $315.900", ln=True, align='C', border=1)
    pdf.ln(5)
    pdf.cell(0, 10, "Condición: Indexado IPC", ln=True, align='C', border=1)
    pdf.ln(10)  

def generar_pdf_ferragro(cotizacion, fecha, cliente, proyecto, celular, correo_asesor, correo, ubicacion, potencia, costo, area, resultados_proyecto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font('Arial', size=12)

    # ✅ LOGO CENTRADO SIN SOLAPAMIENTO
    logo_path = "./static/css/imagenes/logos.jpeg"

    # Ajustamos la posición en Y para que haya más espacio
    pdf.image(logo_path, x=(pdf.w - 120) / 2, y=5, w=120)  # Más grande y centrado
    pdf.ln(50)  # Agrega espacio después del logo para evitar solapamiento

    # ✅ TITULO Y FECHA
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, txt=f"Cotización #{cotizacion}", ln=True, align='C')
    pdf.cell(0, 10, txt="Cotización de Proyecto de Energía Solar", ln=True, align='C')
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, txt=f"Fecha: {fecha}", ln=True, align='C')
    pdf.ln(5)

    # ✅ IMAGEN CENTRAL
    imagen_path = "./static/css/imagenes/energia.jpg"
    pdf.image(imagen_path, x=(pdf.w - 200) / 2, w=200, h=80)
    pdf.ln(10)

    # ✅ DATOS DEL CLIENTE
    add_red_title(pdf, "Datos proporcionados por el Cliente")

    col_width = (pdf.w - 20) / 2  

    pdf.set_font('Arial', 'B', 12)
    pdf.cell(col_width, 8, txt="Campo", border=1, align='C')
    pdf.cell(col_width, 8, txt="Valor", border=1, align='C')
    pdf.ln()

    pdf.set_font('Arial', size=12)
    cliente_info = [
        ("Cliente", cliente),
        ("Correo", correo),
        ("Proyecto", proyecto),
        ("Celular", celular),
        ("Correo Asesor", correo_asesor),
        ("Ubicación", ubicacion),
        ("Potencia", f"{potencia} kWp"),
        ("Costo del kWp", f"${costo}"),
        ("Área Disponible", f"{area} m²")
    ]

    for campo, valor in cliente_info:
        pdf.cell(col_width, 8, txt=campo, border=1)
        pdf.cell(col_width, 8, txt=str(valor), border=1, align='C')
        pdf.ln()

    pdf.ln(10)

    # # ✅ TABLA DE RESULTADOS DEL PROYECTO Y EQUIPOS NECESARIOS
    for section, data in resultados_proyecto.items():
        add_red_title(pdf, section)

        pdf.set_font('Arial', 'B', 12)
        pdf.cell(col_width, 8, txt="Concepto", border=1, align='C')
        pdf.cell(col_width, 8, txt="Valor", border=1, align='C')
        pdf.ln()

        pdf.set_font('Arial', size=12)

        for key, value in data.items():
            if isinstance(value, dict):  
                pdf.set_font('Arial', 'B', 12)
                pdf.cell(0, 8, txt=key, ln=True, align='L', border=1)
                pdf.ln(2)

                pdf.set_font('Arial', size=12)
                for subkey, subvalue in value.items():
                    pdf.cell(col_width, 8, txt=subkey, border=1)
                    pdf.cell(col_width, 8, txt=format_value(subvalue), border=1, align='C')
                    pdf.ln()

                pdf.ln(5)  

            else:
                pdf.cell(col_width, 8, txt=key, border=1)
                pdf.cell(col_width, 8, txt=format_value(value), border=1, align='C')
                pdf.ln()

        pdf.ln(10)

    # ✅ FORMA DE PAGO Y MANTENIMIENTO
    agregar_forma_pago_y_mantenimiento(pdf)

    # ✅ MARCAS ALIADAS
    add_red_title(pdf, "Marcas aliadas")
    marcas_path = "./static/css/imagenes/MARCAS_ALIADAS.png"
    pdf.image(marcas_path, x=(pdf.w - 150) / 2, w=150)
    pdf.ln(10)
    
    # SALTO DE PAGINA
    pdf.add_page()

    # ✅ CONDICIONES DEL PROYECTO
    add_red_title(pdf, "Condiciones del Proyecto")
    condiciones_path = "modules/condiciones.txt"
    if os.path.exists(condiciones_path):
        with open(condiciones_path, "r", encoding="utf-8") as file:
            condiciones = file.read()
        pdf.set_font('Arial', size=8)
        pdf.multi_cell(0, 6, condiciones, border=1, align='J')

    pdf_path = os.path.join(PDF_FOLDER, f'cotizacion_{cotizacion}.pdf')
    
    # ✅ INFORMACIÓN DE FACTURACIÓN Y MENSAJE LEGAL
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(34, 139, 34)  # Rojo
    pdf.multi_cell(0, 10, "Cualquier inquietud adicional que tengan con gusto será atendida. Con la solicitud de esta cotización, autorizas el uso de tus datos personales. Para más información, ingresa a www.ferragro.com", align='L')

    pdf.ln(5)

    # ✅ INFORMACIÓN DE FACTURACIÓN
    pdf.set_text_color(0, 0, 0)  # Negro
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "FACTURADO POR:", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "FERRAGRO S.A.S.", ln=True, align='C')
    pdf.cell(0, 8, "NIT: 800.060.880-3", ln=True, align='C')
    pdf.cell(0, 8, "Somos Autorretenedores", ln=True, align='C')

    pdf.ln(10)  # 🔹 Asegura espacio antes del logo

    # ✅ LOGO EMPRESA (Centrado y más grande)
    logo_empresa = "./static/css/imagenes/logos.jpeg"
    logo_width = 100  # Aumenta el tamaño del logo
    x_position = (pdf.w - logo_width) / 2  # Calcula la posición centrada

    pdf.image(logo_empresa, x=x_position, y=pdf.get_y(), w=logo_width)  # Centrado y más grande

    pdf.ln(25)  # 🔹 Agrega más espacio después del logo para evitar solapamiento

        
    # SALTO DE PAGINA
    pdf.add_page()
    
    # ✅ BENEFICIOS DEL PROYECTO
    add_red_title(pdf, "Beneficios del Proyecto")
    pdf.set_font('Arial', '', 11)
    pdf.multi_cell(0, 8, 
    """1. Ahorro Inmediato en tu Factura de Energía:
        - Tu sistema solar reduciría hasta un 80% en la factura de electricidad desde el primer mes.
        - Hoy pagas aproximadamente 500,000 COP al mes, podrías ahorrar hasta $400,000 COP/mes.
        - En 25 años, el ahorro acumulado supera los $120 millones COP.

    2. Energía Gratis y Protección Contra Aumentos de Tarifas:
        - Los paneles solares generan electricidad gratuita por más de 25 años.
        - Las tarifas de energía suben cada año. Con tu sistema solar, congelas tu costo de electricidad.
        - Además, puedes almacenar energía en baterías y evitar cortes eléctricos.

    3. Inversión Inteligente con Retorno Garantizado:
        - Recuperas tu inversión en 3 a 6 años gracias al ahorro en electricidad.
        - Vida útil del sistema: 25-30 años, lo que equivale a más de 20 años de energía gratuita.
        - Valorización de tu propiedad: Las casas con paneles solares aumentan su valor hasta un 10%.

    4. Impacto Ambiental Positivo:
        - Reducirás tu huella de carbono en hasta 7.5 toneladas de CO2 al año.
        - Esto equivale a evitar el uso de un auto de combustión por 30,000 km al año.
        - Contribuirás a un planeta más limpio y sostenible, sin sacrificar tu comodidad.

    5. Accede a Incentivos y Beneficios Tributarios:
        - La Ley 1715 en Colombia otorga beneficios como:
        - Deducción de impuestos hasta el 50% de la inversión.
        - Exención de IVA y aranceles en equipos solares.
        - Financiamiento con tasas preferenciales y créditos verdes.

    Invierte en Energía Solar y Empieza a Ahorrar desde Hoy:
        - Te ofrecemos un sistema solar completo con instalación profesional y garantía.
        - Contáctanos ahora y solicita tu cotización personalizada.""", 
    border=1, align='J')

    pdf.ln(10)
    
    pdf.output(pdf_path)
    return pdf_path

    # pdf.set_font('Arial', 'I', 12)
    # pdf.multi_cell(0, 10, "Nota:Los equipos listados están sujetos a disponibilidad. La cantidad y tipo de paneles, inversores y demás componentes son opcionales y pueden ajustarse según las necesidades del proyecto. Por ejemplo, la instalación podría incluir 6 paneles de 400W, 5 paneles de 585W o 4 paneles de 605W, dependiendo de la configuración más conveniente para el cliente. Para determinar con precisión la cantidad de baterías necesarias, es fundamental conocer su disposición en el sistema, ya sea en paralelo o en serie, así como el tipo de instalación: ON-GRID, OFF-GRID o sistema mixto. \n Debido a la importancia de estos factores, recomendamos recibir una asesoría de nuestro equipo técnico para garantizar una configuración óptima. Si el sistema no requiere independencia de la red, el uso de baterías no es necesario, por lo que esta sección puede omitirse.", align='L')

