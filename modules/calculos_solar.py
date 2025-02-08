import math

# Diccionario con la radiación solar por zona (kWh/m²/mes)
RADIACION_ANUAL_POR_ZONA = {
    "Costa Caribe": 1643,
    "Región Andina": 1460,
    "Región Pacífica": 1278,
    "Llanos Orientales": 1643,
    "Amazonía": 1278,
    "Desierto de la Guajira": 2190
}

def radiacion_anual_zona(ubicacion):
    if ubicacion in RADIACION_ANUAL_POR_ZONA:
        return RADIACION_ANUAL_POR_ZONA[ubicacion] * 12
    else:
        raise ValueError(f'Ubicación {ubicacion} no encontrada en la base de datos.')

class CalculoNumeroPaneles:
    def __init__(self, ubicacion, potencia):
        self.radiacion_anual = radiacion_anual_zona(ubicacion)
        self.potencia = potencia

        # Potencia de diferentes tipos de paneles (kWp)
        self.potencia_panel_400 = 0.400
        self.potencia_panel_585 = 0.585
        self.potencia_panel_605 = 0.605

        # Área del panel en m²
        self.area_panel = 1.13  

    def calcular_paneles(self):
        energia_400 = round(self.potencia_panel_400 * self.radiacion_anual, 2)
        energia_585 = round(self.potencia_panel_585 * self.radiacion_anual, 2)
        energia_605 = round(self.potencia_panel_605 * self.radiacion_anual, 2)
        
        consumo_anual = self.potencia * 12  

        numeroPaneles_400 = round(math.ceil(consumo_anual / energia_400))
        numeroPaneles_585 = round(math.ceil(consumo_anual / energia_585))
        numeroPaneles_605 = round(math.ceil(consumo_anual / energia_605))

        return {
            "Número de paneles de 400W": numeroPaneles_400,
            "Número de paneles de 585W": numeroPaneles_585,
            "Número de paneles de 605W": numeroPaneles_605
        }

def calcular_impacto_ambiental(consumo_anual_kwh, porcentaje_energia_solar=100):
    """
    Calcula la reducción de huella de carbono y su equivalente en kilómetros no recorridos en auto.

    Args:
        consumo_anual_kwh (float): Consumo anual de energía en kilovatios hora (kWh).
        porcentaje_energia_solar (float): Porcentaje de energía que será reemplazada por energía solar (0-100%).

    Returns:
        dict: Impacto ambiental en toneladas de CO2 y kilómetros no recorridos en auto.
    """
    CO2_POR_KWH = 0.0007  # Toneladas de CO2 por cada kWh (promedio global)
    CO2_POR_KM_AUTO = 0.00025  # Toneladas de CO2 emitidas por km en auto de combustión (promedio)

    energia_solar_generada_kwh = consumo_anual_kwh * (porcentaje_energia_solar / 100)
    reduccion_CO2_toneladas = energia_solar_generada_kwh * CO2_POR_KWH
    km_equivalentes_auto = reduccion_CO2_toneladas / CO2_POR_KM_AUTO

    return {
        "reduccion_CO2_toneladas": round(reduccion_CO2_toneladas, 2),
        "km_equivalentes_auto": int(km_equivalentes_auto)
    }

def calcular_proyecto(ubicacion, potencia, costo):
    paneles = CalculoNumeroPaneles(ubicacion, potencia).calcular_paneles()

    consumoAnual = potencia * 12
    ahorroAnual = f'${int(consumoAnual * costo):,}'.replace(",", ".")
    costokWp = 375320
    costoProyecto = f'${int(costokWp * paneles["Número de paneles de 400W"]):,}'.replace(",", ".")
    disminucionRenta = f'${int(costokWp * paneles["Número de paneles de 400W"] / 2):,}'.replace(",", ".")

    area_minima_Requerida = f'{round(math.ceil(paneles["Número de paneles de 400W"] * 1.13))} m²'

    numeroInversores_3500 = round(math.ceil((paneles['Número de paneles de 400W'] * 400) / 3500))
    numeroInversores_6000 = round(math.ceil((paneles['Número de paneles de 585W'] * 585) / 6000))
    numeroInversores_12000 = round(math.ceil((paneles['Número de paneles de 605W'] * 600) / 12000))

    voltaje_baterias_gel = 12
    capacidad_bateria_gel = math.ceil(((consumoAnual/365) / voltaje_baterias_gel) / 0.5)
    cantidad_bateriasg_100 = round(math.ceil(capacidad_bateria_gel/100))
    cantidad_bateriasg_150 = round(math.ceil(capacidad_bateria_gel/150))
    cantidad_bateriasg_200 = round(math.ceil(capacidad_bateria_gel/200))
    cantidad_bateriasg_250 = round(math.ceil(capacidad_bateria_gel/250))

    voltaje_baterias_litio = 24
    capacidad_bateria_litio = round(math.ceil((((consumoAnual/365)/voltaje_baterias_litio)*0.9)*12))
    cantidad_bateriasl_60 = round(math.ceil(capacidad_bateria_litio/60))
    cantidad_bateriasl_100 = round(math.ceil(capacidad_bateria_litio/100))
    cantidad_bateriasl_120 = round(math.ceil(capacidad_bateria_litio/120))
    cantidad_bateriasl_150 = round(math.ceil(capacidad_bateria_litio/150))
    cantidad_bateriasl_200 = round(math.ceil(capacidad_bateria_litio/200))

    longitud_riel = 4.7
    rieles_47m_400W = round(math.ceil((paneles['Número de paneles de 400W'] * 1.15) / longitud_riel) * 2)

    midcland_400W = round(math.ceil(paneles['Número de paneles de 400W'] * 2) - 2)
    endcland_400W = round(math.ceil(paneles['Número de paneles de 400W'] / 2))

    impacto_ambiental = calcular_impacto_ambiental(consumoAnual)

    return {
        "Resultados Generales": {
            "Costo Proyecto": costoProyecto,
            "Ahorro Anual": ahorroAnual,
            "Disminución de Renta": disminucionRenta,
            "Área mínima requerida para páneles": area_minima_Requerida,
            "Impacto Ambiental": impacto_ambiental
        },
        "Equipos Necesarios:": {
            "Paneles": paneles,
            "Inversores": {
                "Número de Inversores 3.500W": numeroInversores_3500,
                "Número de Inversores 6.000W": numeroInversores_6000,
                "Número de Inversores 12.000W": numeroInversores_12000,
            },
            "Baterias gel": {
                "Número de Baterías Gel 100Ah": cantidad_bateriasg_100,
                "Número de Baterías Gel 150Ah": cantidad_bateriasg_150,
                "Número de Baterías Gel 200Ah": cantidad_bateriasg_200,
                "Número de Baterías Gel 250Ah": cantidad_bateriasg_250,
            },
            "Baterias Litio": {
                "Número de Baterías litio 60Ah": cantidad_bateriasl_60,
                "Número de Baterías litio 100Ah": cantidad_bateriasl_100,
                "Número de Baterías litio 120Ah": cantidad_bateriasl_120,
                "Número de Baterías litio 150Ah": cantidad_bateriasl_150,
                "Número de Baterías litio 2000Ah": cantidad_bateriasl_200,
            },
            "Estructura": {
                "Número de Rieles 4.7m 400W": rieles_47m_400W,
                "Número de Midcland 400W": midcland_400W,
                "Número de Endcland 400W": endcland_400W    
            }
        }
    }


