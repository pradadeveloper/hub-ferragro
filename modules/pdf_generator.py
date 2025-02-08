from fpdf import FPDF  # type: ignore
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
    pdf.set_fill_color(255, 0, 0)  # Rojo
    pdf.set_text_color(255, 255, 255)  # Blanco
    pdf.set_font('Arial', 'B', 14)
    pdf.cell(0, 10, title, ln=True, align='C', fill=True)
    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)  # Restablece el color de texto a negro

def agregar_forma_pago_y_mantenimiento(pdf):
    """ Agrega la sección de Forma de Pago y Mantenimiento Anual en el PDF. """
    add_red_title(pdf, "Forma de Pago")
    pdf.set_font('Arial', '', 12)

    table_width = 130
    col_width_1 = table_width * 0.7
    col_width_2 = table_width * 0.3
    x_start = (pdf.w - table_width) / 2
    pdf.set_x(x_start)

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

    add_red_title(pdf, "Mantenimiento Anual")
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 10, "Monto: $315.900", ln=True, align='C', border=1)
    pdf.ln(5)
    pdf.cell(0, 10, "Condición: Indexado IPC", ln=True, align='C', border=1)
    pdf.ln(10)

def generar_pdf(cotizacion, fecha, cliente, proyecto, celular, correo_asesor, correo, ubicacion, potencia, costo, area, resultados_proyecto):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font('Arial', size=12)

    logo_path = "./static/css/imagenes/SOLARTECH.jpeg"
    pdf.image(logo_path, x=(pdf.w - 100) / 2, y=10, w=100)
    pdf.ln(30)

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, txt=f"Cotización #{cotizacion}", ln=True, align='C')
    pdf.cell(0, 10, txt="Cotización de Proyecto de Energía Solar", ln=True, align='C')
    pdf.set_font('Arial', 'I', 12)
    pdf.cell(0, 10, txt=f"Fecha: {fecha}", ln=True, align='C')
    pdf.ln(10)

    imagen_path = "./static/css/imagenes/energia.jpg"
    pdf.image(imagen_path, x=(pdf.w - 200) / 2, w=200, h=80)
    pdf.ln(10)

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

    agregar_forma_pago_y_mantenimiento(pdf)
    add_red_title(pdf, "Marcas aliadas")
    marcas_path = "./static/css/imagenes/MARCAS_ALIADAS.png"
    pdf.image(marcas_path, x=(pdf.w - 150) / 2, w=150)
    pdf.ln(10)
    pdf.add_page()

    add_red_title(pdf, "Condiciones del Proyecto")
    condiciones_path = "modules/condiciones.txt"
    if os.path.exists(condiciones_path):
        with open(condiciones_path, "r", encoding="utf-8") as file:
            condiciones = file.read()
        pdf.set_font('Arial', size=8)
        pdf.multi_cell(0, 6, condiciones, border=1, align='J')

    pdf_path = os.path.join(PDF_FOLDER, f'cotizacion_{cotizacion}.pdf')
    pdf.set_font('Arial', 'I', 12)
    pdf.set_text_color(255, 0, 0)
    pdf.multi_cell(0, 10, "Cualquier inquietud adicional que tengan con gusto será atendida. Con la solicitud de esta cotización, autorizas el uso de tus datos personales. Para más información, ingresa a www.ferragro.com", align='L')

    pdf.ln(5)
    pdf.set_text_color(0, 0, 0)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, "FACTURADO POR:", ln=True, align='C')
    pdf.set_font('Arial', '', 12)
    pdf.cell(0, 8, "FERRAGRO S.A.S.", ln=True, align='C')
    pdf.cell(0, 8, "NIT: 800.060.880-3", ln=True, align='C')
    pdf.cell(0, 8, "Somos Autorretenedores", ln=True, align='C')

    pdf.ln(10)
    logo_empresa = "./static/css/imagenes/logos.jpeg"
    logo_width = 100
    x_position = (pdf.w - logo_width) / 2
    pdf.image(logo_empresa, x=x_position, y=pdf.get_y(), w=logo_width)
    pdf.ln(25)

    pdf.add_page()
    add_red_title(pdf, "Beneficios del Proyecto")
    pdf.set_font('Arial', '', 11)
    impacto_ambiental = resultados_proyecto['Resultados Generales'].get('Impacto Ambiental', {})
    reduccion_co2 = impacto_ambiental.get('Reducción de CO2 (toneladas)', 0)
    km_equivalentes = impacto_ambiental.get('Equivalente en km no recorridos', 0)

    texto_beneficios = f"""
    1. Ahorro Inmediato en tu Factura de Energía:
        - Tu sistema solar podría reducir hasta un 80% en la factura de electricidad desde el primer mes.
        - El ahorro anual estimado es {resultados_proyecto['Resultados Generales']['Ahorro Anual']}.

    2. Energía Gratis y Protección Contra Aumentos de Tarifas:
        - Los paneles solares generan electricidad gratuita por más de 25 años.
        - Evitarás aumentos en las tarifas eléctricas congelando tu costo actual.

    3. Inversión Inteligente con Retorno Garantizado:
        - Recuperarás tu inversión en 3 a 6 años gracias al ahorro en electricidad.
        - Vida útil del sistema: 25-30 años, asegurando más de 20 años de energía gratuita.

    4. Impacto Ambiental Positivo:
        - Reducirás tu huella de carbono en aproximadamente {reduccion_co2:.2f} toneladas de CO2 al año.
        - Esto equivale a evitar el uso de un auto de combustión por {km_equivalentes:,.0f} km al año.
        - Contribuirás a un planeta más limpio y sostenible, sin sacrificar tu comodidad.

    5. Accede a Incentivos y Beneficios Tributarios:
        - Ley 1715 en Colombia ofrece deducción de impuestos hasta el 50% de la inversión.
        - Exención de IVA y aranceles en equipos solares.
        - Financiamiento con tasas preferenciales y créditos verdes.

    Invierte en Energía Solar y Empieza a Ahorrar desde Hoy:
        - Te ofrecemos un sistema solar completo con instalación profesional y garantía.
        - Contáctanos ahora y solicita tu cotización personalizada.
    """

    pdf.multi_cell(0, 8, texto_beneficios, border=1, align='J')
    pdf.ln(10)
    pdf.output(pdf_path)
    return pdf_path