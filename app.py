from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import pandas as pd
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

# reportes: ['Fuga', 'Drenaje Obstruido', 'Falta de agua','Falta de tapa en valvula', 'Brote en aguas negras','Mala calidad', 'Mal uso', 'Hundimiento', 'Coladera sin tapa','Rejilla de piso']

report_images = {
    'Fuga': '/static/imgs/fuga.png',
    'Drenaje Obstruido': '/static/imgs/drenaje_obstruido.png',
    'Falta de agua': '/static/imgs/falta_agua.png',
    'Falta de tapa en valvula': '/static/imgs/falta_tapa_valvula.png',
    'Brote en aguas negras': '/static/imgs/brote_aguas_negras.png',
    'Mala calidad': '/static/imgs/mala_calidad.png',
    'Mal uso': '/static/imgs/mal_uso.png',
    'Hundimiento': '/static/imgs/hundimiento.png',
    'Coladera sin tapa': '/static/imgs/coladera_sin_tapa.jpg',
    'Rejilla de piso': '/static/imgs/rejilla_piso.png'
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
puntos = pd.read_csv('data/reportes_agua.csv')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global data
    global velocidades_df
    global puntos

    markersData = {}
    # formato "marker2": { lat: 34.0522, lng: -118.2437, title: "Marker 2", imagen: "https://cdn.pixabay.com/photo/2015/10/01/17/17/car-967387_1280.png" },
    for i in range(len(puntos)):
        img = report_images[puntos['reporte'][i]]

        markersData["marker" + str(i)] = {
            "lat": puntos['latitud'][i],
            "lng": puntos['longitud'][i],
            "title": puntos['id_reporte'][i],
            "imagen": img
        }
    
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

    return render_template('index.html', MAPS_API_KEY=MAPS_API_KEY, coords=coords, velocidades=velocidades, dias=dias, horas=horas, fecha=fecha, hora=hora, FeatureCollection=FeatureCollection, markersData=markersData)

if __name__ == '__main__':  
    app.run(debug=True)