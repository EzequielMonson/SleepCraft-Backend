from flask import Flask, session
from flask_cors import CORS
from app.views import *

app = Flask(__name__)
app.secret_key = '4b89ac97746a5998ab553a96294d571513d09f505ac50ad4'
CORS(app, supports_credentials=True)

# Definir las rutas
app.route('/traer_datos', methods=['GET'])(traer_datos)
app.route('/login', methods=['POST'])(loguear_usuario)
app.route('/codigo', methods=['GET'])(buscar_codigo_admin)
app.route('/registrar', methods=['POST'])(registrar_usuario)
app.route('/logout', methods=['GET'])(logout)
app.route('/guardarCorreo', methods=['GET'])(traer_correo)
app.route('/traer_id', methods=['GET'])(traer_id_usuario)
app.route('/crear_tablas', methods=['GET'])(crear_tablas)
# Rutas para manejar pedidos
app.route('/pedidos', methods=['POST'])(hacer_pedido)
app.route('/mostrar_pedidos', methods=['GET'])(mostrar_pedidos)
app.route('/actualizar_estado_pedido', methods=['POST'])(actualizar_estado_pedido)
app.route('/mostrar_pedidos_cliente', methods=['POST'])(mostrar_pedidos_cliente)

if __name__ == '__main__':
    app.run(debug=True)
