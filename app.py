from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
from functions.fiware import cargar_csv_puntos_a_orion, get_entities_by_type
from werkzeug.utils import secure_filename
import os
import numpy as np
import tensorflow as tf
import tensorflow.keras.models as tfkm
from PIL import Image

load_dotenv()
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

print("loading models: ")
model_bin_96 = tfkm.load_model('models/CNN.h5')
print("Binary model loaded.")
model_cat_84 = tfkm.load_model('models/CNN.h5')
print("Categorical model loaded.")

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
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/camaras', methods=['GET', 'POST'])
def camaras():
    return render_template('camaras.html')

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
    

@app.route('/upload_ml', methods=['GET', 'POST'])
def upload_ml():
    prediction = None
    if request.method == 'POST':
        # Verificar si se subió un archivo
        if 'file' not in request.files:
            return 'No se ha seleccionado ningún archivo', 400
        
        file = request.files['file']
        
        # Verificar si el nombre del archivo está vacío
        if file.filename == '':
            return 'No se ha seleccionado ningún archivo', 400
        
        if file:
            # Guardar archivo de forma segura
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            try:
                # Usar PIL para cargar y redimensionar
                image = Image.open(filepath)
                image = image.resize((120,90))
                image_np = np.array(image)
                image_np = np.expand_dims(image_np, 0)
                #result = randint(0,1) #mocking a result
            
                
                # Hacer predicción
                prediccion = model_cat_84.predict(image_np)
                
                # Convertir predicción a texto legible 
                prediction = prediccion[0][0]
                
                # Opcional: eliminar archivo después de procesar
                os.remove(filepath)
            
            except Exception as e:
                return f"Error procesando imagen: {str(e)}", 500
    
    return render_template('upload_ml.html', prediction=prediction)

if __name__ == '__main__':  
    app.run(port=5000, debug=True)