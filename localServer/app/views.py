from flask import jsonify
from app.database import *

def index():
    mensaje = crear_tablas()
    if mensaje != "TODO ANDO BIEN":
        return jsonify({'mensaje': f'{mensaje}'})
    mensaje = cargar_datos_tabla_tipo_usuario()
    return jsonify({'mensaje': f'{mensaje}'})
