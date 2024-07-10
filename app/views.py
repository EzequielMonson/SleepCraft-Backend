from flask import jsonify, request, session
from app.database import *
from app.models import *

def traer_datos():
    print('Session data:', session)
    if 'usuario' in session:
        usuario_data = session['usuario']
        if usuario_data['tipo'] == 2:
            cliente = Cliente(usuario_data)
            print(cliente)
            return jsonify(cliente)
        elif usuario_data['tipo'] == 1:
            admin = Administrador(usuario_data)
            print(admin)
            return jsonify(admin)
    else:
        return jsonify({'Error': 'No hay usuario en sesión'})

def registrar_usuario():
    # crear_tablas()
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        tipo_usuario = data.get('tipoUsuario')
        if tipo_usuario == 'true':
            administrador_actual = Administrador(data)
            insertar_usuario(administrador_actual.to_dict(), 1)
            session['usuario'] = administrador_actual.to_dict()
            print('Session data:', session)
            print('Usuario registrado (admin):', session['usuario'])
            return jsonify(session['usuario'])
        else:
            cliente_actual = Cliente(data)
            insertar_usuario(cliente_actual.to_dict())
            session['usuario'] = cliente_actual.to_dict()
            print('Session data:', session)
            print('Usuario registrado (cliente):', session['usuario'])
            return jsonify(session['usuario'])
    else:
        return jsonify({'Error': 'Solicitud no válida.'}), 400

def loguear_usuario():
    if request.method == 'POST' and request.is_json:
        data = request.get_json()
        correo = data.get('correo')
        contraseña = data.get('contraseña')
        print('Datos recibidos:', data)
        usuario_encontrado = verificar_usuario(correo, contraseña)
        if usuario_encontrado:
            if usuario_encontrado[7] == 2:
                cliente_actual = Cliente(usuario_encontrado)
                session['usuario'] = cliente_actual.to_dict()
                print('Usuario logueado (cliente):', session['usuario'])
            elif usuario_encontrado[7] == 1:
                administrador_actual = Administrador(usuario_encontrado)
                session['usuario'] = administrador_actual.to_dict()
                print('Usuario logueado (admin):', session['usuario'])
            print('Session data:', session)
            return jsonify(session['usuario'])
        else:
            return jsonify({'Error': 'Contraseña o usuario no válidos.'}), 401
    else:
        return jsonify({'Error': 'Solicitud no válida.'}), 400
def traer_id_usuario():
    if 'usuario' in session:
        return jsonify(seleccionar_id_por_usuario(session['usuario']))
    else:
        return jsonify({'Error': 'No hay usuario en sesión'}), 401

def buscar_codigo_admin():
    codigoAdmin = seleccionar_codigo_admin()
    return jsonify({'codigo' : f'{codigoAdmin[1]}'})
    
def traer_correo():
    if 'usuario' in session:
        correo = session['usuario']['correo']
        return jsonify(correo)
    return jsonify({'Error': 'No hay usuario logueado'})

def logout():
    session.pop('usuario', None)
    return jsonify({'Mensaje': 'Sesión cerrada'})

def hacer_pedido():
    print('Session data:', session)
    if request.method == 'POST':
        if 'usuario' not in session:
            print('No hay usuario en sesión')
            return jsonify({'Error': 'No hay usuario en sesión'}), 401
        data = request.get_json()
        if not data:
            print('Datos de pedido no válidos')
            return jsonify({'Error': 'Datos de pedido no válidos'}), 400
        cliente = Cliente(session['usuario'])
        datos_pedido = {
            'idCliente': cliente.id,
            'descripcion': data.get('descripcion'),
            'estado': 'Pendiente',
            'fechaPedido': data.get('fechaActual'),
            'idAdmin': cliente.obtener_id_admin()  # Suponiendo que hay un método para obtener el ID del admin
        }
        print('Datos del pedido:', datos_pedido)
        cliente.hacer_pedido(datos_pedido)
        return jsonify({'Mensaje': 'Pedido creado exitosamente'})
    return jsonify({'Mensaje': 'error'})

def mostrar_pedidos():
    print('Session data:', session)
    usuario_data = session['usuario']
        
    if isinstance(session.get('usuario'), Cliente):
        cliente = Cliente(usuario_data)
        pedidos = cliente.mostrar_pedidos()
        return jsonify(pedidos)
    else:
        admin = Administrador(usuario_data)
        pedidos = admin.mostrar_todos_los_pedidos_clientes()
    return jsonify(pedidos)

def actualizar_estado_pedido():
    print('Session data:', session)
    if request.method == 'POST' and isinstance(session.get('usuario'), Administrador):
        id_pedido = request.form.get('id_pedido')
        nuevo_estado = request.form.get('estado')
        Pedido.actualizar_estado(id_pedido, nuevo_estado)
        return jsonify({'Mensaje': 'Estado del pedido actualizado'})
    return jsonify({'Error': 'No autorizado'})

def mostrar_pedidos_cliente():
    if request.method == 'POST' and isinstance(session.get('usuario'), Administrador):
        id_cliente = request.form.get('id_cliente')
        cliente_seleccionado = next((c for c in session['usuario'].lista_clientes if c.id == id_cliente), None)
        if cliente_seleccionado:
            pedidos = cliente_seleccionado.mostrar_pedidos()
            return jsonify(pedidos)
        return jsonify({'Error': 'Cliente no encontrado'})
    return jsonify({'Error': 'No autorizado'})
