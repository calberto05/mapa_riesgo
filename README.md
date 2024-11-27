# Inicializar servidor fiware
## Entrar al directorio de fiware
cd fiware

## Iniciar contenedor docker
docker compose up

# Requerimientos
## Crear entorno virtual desde otra terminal
python -m venv venv

## Inicializar entorno virtual
source venv/bin/activate

## Instalar requerimientos
pip install -r requirements.txt

# Correr
python app.py