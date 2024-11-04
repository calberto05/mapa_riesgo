import requests
import json
import pandas as pd
from functions.map_atributes import report_images

archivo_csv = 'data/reportes_agua.csv'

def cargar_csv_puntos_a_orion(archivo_csv, url_orion):
    reader = pd.read_csv(archivo_csv)
    for i in range(len(reader)):
        entity = {
            "type": "Store",
            "id": "reporte"+reader['id_reporte'][i],
            "Reporte": {
                "type": "Reporte",
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

def delete_all_entities(url):
    entities = get_all_entities(url)
    for entity in entities:
        requests.delete(f"{url}/{entity['id']}")

def get_all_entities(url, limit=50):
    offset = 0
    all_entities = []
    while True:
        response = requests.get(f"{url}?limit={limit}&offset={offset}")
        entities = response.json()
        if not entities:
            break
        all_entities.extend(entities)
        offset += limit
    return all_entities

cargar_csv_puntos_a_orion(archivo_csv, 'http://localhost:1026/v2/entities')