from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import pandas as pd
import random

load_dotenv()
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

data = pd.read_csv('data/coordenadas_trafico.csv')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global data
        
    coords = []
    velocidades = []
    for i in range(len(data)):
        coords.append([{"lat": data['x1'][i], "lng": data['y1'][i]}, {"lat": data['x2'][i], "lng": data['y2'][i]}])
        # generar aleatoriamente velocidades entre 0 y 2 float
        velocidades.append(random.uniform(0, 2))

    return render_template('index.html', MAPS_API_KEY=MAPS_API_KEY, coords=coords, velocidades=velocidades)

if __name__ == '__main__':  
    app.run(debug=True)