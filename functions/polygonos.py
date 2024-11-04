import re

def extraer_multipolygons(multipolygons):
    multipolygon_filas = multipolygons.strip()
    multipolygon_filas = multipolygons.split("(")[1]
    multipolygon_filas = multipolygons.split(")")[0]
    multipolygon_filas = multipolygons.split(", ")

    pattern = re.compile(r'[a-zA-Z\(\)]')
    multipolygon_filas = [pattern.sub('', coord) for coord in multipolygon_filas]
    
    formatted_coords = []

    for coord in multipolygon_filas:
        lng, lat = map(float, coord.split())  # Separar longitud y latitud
        formatted_coords.append([lng, lat])   # Añadir al nuevo formato [longitud, latitud]

    # qutar elementos vacios
    return formatted_coords

