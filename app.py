from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import pandas as pd
import json
from polygonos import extraer_multipolygons

load_dotenv()
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

colors = {
    'Muy Alto' : 'rgba(255, 0, 0, 0.3)',
    'Alto' : 'rgba(255, 255, 0, 0.3)',
    'Medio' : 'rgba(0, 255, 0, 0.3)',
    'Bajo' : 'rgba(0, 0, 255, 0.3)',
    'Muy Bajo' : 'rgba(0, 0, 0, 0.3)'
}

FeatureCollection = {
    "type": "FeatureCollection",
    "features": []
}

polygonos = pd.read_csv('data/polygonos_ciudad.csv')
for i in range(len(polygonos)):
    coordinates = [extraer_multipolygons(polygonos['geo_shape'][i])]
    FeatureCollection["features"].append({
        "type": "Feature",
        "properties": {
            "name": polygonos['alcaldia'][i],
            "color": colors[polygonos['intensidad'][i]]
        },
        "geometry": {
            "type": "Polygon",
            "coordinates": coordinates
        }
    })

data = pd.read_csv('data/coordenadas_trafico.csv')
velocidades_df = pd.read_csv('data/velocidades.csv')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global data
    global velocidades_df

    dias = velocidades_df['dia'].unique()
    horas = velocidades_df['hora'].unique()

    velocidades_copy = velocidades_df.copy()
    fecha = '2024-09-12'
    hora = 21

    if request.method == 'POST':
        fecha = request.form.get('date')
        hora = int(request.form.get('hour'))
    

    velocidades_copy = velocidades_copy[velocidades_copy['dia'] == fecha]
    velocidades_copy = velocidades_copy[velocidades_copy['hora'] == hora]

    data_merged = pd.merge(data, velocidades_copy, how='left', left_on='Vialidad', right_on='Street Name')
    data_merged = data_merged.fillna(0)

    data_merged["Current Speed (km/h)"] = data_merged["Current Speed (km/h)"] / 20

    coords = []
    velocidades = []
    for i in range(len(data_merged)):
        coords.append([{"lat": data_merged['x1'][i], "lng": data_merged['y1'][i]}, {"lat": data_merged['x2'][i], "lng": data_merged['y2'][i]}])
        velocidades.append(data_merged["Current Speed (km/h)"][i])

    return render_template('index.html', MAPS_API_KEY=MAPS_API_KEY, coords=coords, velocidades=velocidades, dias=dias, horas=horas, fecha=fecha, hora=hora, FeatureCollection=FeatureCollection)

if __name__ == '__main__':  
    app.run(debug=True)