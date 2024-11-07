import requests
import json
import pandas as pd
#from polygonos import extraer_multipolygons
from functions.polygonos import extraer_multipolygons
#from map_atributes import report_images, colors
from functions.map_atributes import report_images, colors

puntos_csv = 'data/reportes_agua.csv'
polygonos_csv = 'data/polygonos_ciudad.csv'

def cargar_csv_poligonos_a_orion(archivo_csv, url_orion):

    polygonos = pd.read_csv(archivo_csv)

    for i in range(len(polygonos)):
        coordinates = [extraer_multipolygons(polygonos['geo_shape'][i])]

        entity = {
            "id": "poligono"+str(i),
            "type": "Feature",
            "Feature": {
                "type": "Feature",
                "value": {
                    "name": polygonos['alcaldia'][i],
                    "color": colors[polygonos['intensidad'][i]],
                    "coordinates": coordinates
                }
            }
        }
    
        entity = json.dumps(entity)
        entity = json.loads(entity)
        requests.post(url_orion, json=entity)

def cargar_csv_puntos_a_orion(archivo_csv, url_orion):
    reader = pd.read_csv(archivo_csv)
    for i in range(len(reader)):
        entity = {
            "id": "reporte_agua"+str(i),
            "type": "Reporte_agua",
            "Reporte": {
                "type": "Reporte_agua",
                "value": {
                    "tipo_reporte" : reader['reporte'][i],
                    "lat" : float(reader['latitud'][i]),
                    "lon" : float(reader['longitud'][i]),
                    "img" : report_images[reader["reporte"][i]]
                }
            },
        }
        entity = json.dumps(entity)
        entity = json.loads(entity)
        requests.post(url_orion, json=entity)

def cargar_csv_velocidades_a_orion(url_orion):
    data = pd.read_csv('data/coordenadas_trafico.csv')
    velocidades_df = pd.read_csv('data/velocidades.csv')
    data_merged = pd.merge(data, velocidades_df, how='left', left_on='Vialidad', right_on='Street Name')
    data_merged = data_merged.fillna(0)

    data_merged["Current Speed (km/h)"] = data_merged["Current Speed (km/h)"] / 20
    
    for i in range(len(data_merged)):
        entity = {
            "id": "velocidad_"+str(i),
            "type": "Velocidad_condesa",
            "Velocidad": {
                "type": "Velocidad_condesa",
                "value": {
                    "velocidad" : data_merged["Current Speed (km/h)"][i],
                    "lat_inicial" : data_merged['x1'][i],
                    "lon_inicial" : data_merged['y1'][i],
                    "lat_final" : data_merged['x2'][i],
                    "lon_final" : data_merged['y2'][i],
                    "dia" : data_merged['dia'][i],
                    "hora" : data_merged['hora'][i]
                }
            },
        }
        entity = json.dumps(entity)
        entity = json.loads(entity)
        requests.post(url_orion, json=entity)

def get_entities_by_type(url, entity_type, limit=50):
    offset = 0
    all_entities = []
    while True:
        response = requests.get(f"{url}?type={entity_type}&limit={limit}&offset={offset}")
        entities = response.json()
        if not entities:
            break
        all_entities.extend(entities)
        offset += limit
    return all_entities

def delete_all_entities(url, entity_type):
    entities = get_entities_by_type(url, entity_type)
    for entity in entities:
        requests.delete(f"{url}/{entity['id']}")
    
#elete_all_entities('http://localhost:1026/v2/entities', 'Reporte')
#cargar_csv_poligonos_a_orion(polygonos_csv, 'http://localhost:1026/v2/entities')
#cargar_csv_velocidades_a_orion('http://localhost:1026/v2/entities')
#cargar_csv_puntos_a_orion(puntos_csv, 'http://localhost:1026/v2/entities')
#print(get_entities_by_type('http://localhost:1026/v2/entities', 'Velocidad_condesa')[-1])