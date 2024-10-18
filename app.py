from flask import Flask, request, jsonify, render_template
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()
MAPS_API_KEY = os.getenv('MAPS_API_KEY')

data = pd.read_csv('data/coordenadas_trafico.csv')

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    global data

    coords = [
        {"lat": data["x1"][0], "lng": data["y1"][0]},  # Coordenada válida
        {"lat": data["x2"][0], "lng": data["y2"][0]}   # Coordenada válida
    ]
        
    return render_template('index.html', MAPS_API_KEY=MAPS_API_KEY, coords=coords)

if __name__ == '__main__':  
    app.run(debug=True)