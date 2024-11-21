from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from functions.fiware import cargar_csv_puntos_a_orion, get_entities_by_type
import os
#from tensorflow.keras.models import load_model
#from tensorflow.keras.preprocessing import image
import numpy as np

load_dotenv()
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

velocidades = get_entities_by_type('http://localhost:1026/v2/entities', 'Velocidad_condesa')
puntos = get_entities_by_type('http://localhost:1026/v2/entities', 'Reporte_agua')
FeatureCollection = get_entities_by_type('http://localhost:1026/v2/entities', 'Feature')

def obtener_velocidades(dia, hora):
    velocidades = get_entities_by_type('http://localhost:1026/v2/entities', 'Velocidad_condesa')
    velocidades = [velocidad for velocidad in velocidades if velocidad['Velocidad']['value']['dia'] == dia and velocidad['Velocidad']['value']['hora'] == hora]
    return velocidades

dias = set()
horas = set()

for velocidad in velocidades:
    dias.add(velocidad['Velocidad']['value']['dia'])
    horas.add(velocidad['Velocidad']['value']['hora'])

dias = list(dias)
horas = list(horas)

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camaras', methods=['GET', 'POST'])
def camaras():
    return render_template('camaras.html')

@app.route('/upload_ml', methods=['GET', 'POST'])
def upload_ml():
    if request.method == 'POST':
        result = {"error": "No se ha seleccionado un archivo"}
        
        return jsonify(result)
    
    return render_template('upload_ml.html')

@app.route('/mapa', methods=['GET', 'POST'])
def mapa():    
    fecha = '2024-09-12'
    hora = 21

    if request.method == 'POST':
        fecha = request.form.get('date')
        hora = int(request.form.get('hour'))
    
    velocidades_aux = obtener_velocidades(fecha, hora)
    
    return render_template('mapa.html', MAPS_API_KEY=MAPS_API_KEY, velocidades=velocidades_aux, dias=dias, horas=horas, fecha=fecha, hora=hora, FeatureCollection=FeatureCollection, markersData=puntos)

@app.route('/dashboard/<tipo>')
def dashboard(tipo):
    if tipo == "general":
        return render_template('graficas/analisis_general.html')
    elif tipo == "reportes":
        return render_template('graficas/analisis_reportes.html')
    elif tipo == "poligonos":
        return render_template('graficas/analisis_poligonos.html')
    else:
        return render_template('404.html'), 404

if __name__ == '__main__':  
    MAPS_API_KEY = "AIzaSyD-DFSJFKDSJFKSD-FIDSJF23E3IJFS"
    import os
    app.run(port=5000, debug=True)