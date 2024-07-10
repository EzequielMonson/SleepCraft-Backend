import pymysql
import base64

DATABASE_CONFIG = {
    'host' : '127.0.0.1',
    'user' : 'root',
    'password' : '',
    'database' : 'Sleepcraft'
}

def crear_tablas():
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS tipoUsuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo VARCHAR(50)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS usuario (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                correo VARCHAR(50),
                contrasena VARCHAR(255),
                telefono VARCHAR(50),
                ciudad VARCHAR(50),
                direccion VARCHAR(50),
                idTipoUsuario INT,
                FOREIGN KEY (idTipoUsuario) REFERENCES tipoUsuario (id)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS codigo (
                id INT AUTO_INCREMENT PRIMARY KEY,
                codigo VARCHAR(50)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS pedido (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idCliente INT,
                idAdmin INT,
                descripcion VARCHAR(255),
                estado VARCHAR(255),
                fechaPedido DATE,
                FOREIGN KEY (idCliente) REFERENCES usuario(id),
                FOREIGN KEY (idAdmin) REFERENCES usuario(id)
            )
            """
        )
        # Pre-cargar datos en tipoUsuario
        cur.execute(
            """
            INSERT IGNORE INTO tipoUsuario (tipo)
            VALUES ('administrador');
            """
        )
        cur.execute(
            """
            INSERT IGNORE INTO codigo (codigo)
            VALUES ('123213jncjnvsvd');
            """
        )
        cur.execute(
            """
            INSERT IGNORE INTO tipoUsuario (tipo)
            VALUES ('cliente');
            """
        )
        conn.commit()
        mensaje = "TODO ANDO BIEN"
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return mensaje

def obtener_registros_usuarios():
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM usuario
            """
        )
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return True
    
def insertar_usuario(registro: dict, tipoUsuario = 2):
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('INSERT INTO usuario (nombre, correo, contrasena, telefono, ciudad, direccion, idTipoUsuario) VALUES (%s, %s, %s, %s, %s, %s, %s)',
            (registro.get('nombre'), registro.get('correo'), registro.get('contraseña'), registro.get('telefono'), registro.get('ciudad'), registro.get('direccion'),tipoUsuario))
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()

def verificar_usuario(correo, contraseña):
    usuario = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuario WHERE correo = %s AND contrasena = %s', (correo, contraseña))
        usuario = cur.fetchone()
        cur.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return usuario
    
def seleccionar_codigo_admin():
    codigo = 0
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM codigo WHERE id = 1
            """
        )
        codigo = cur.fetchone()
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return codigo
    
def seleccionar_id_por_usuario(usuario):
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
        """
        SELECT id FROM usuario WHERE idTipoUsuario = %s AND ciudad = %s AND nombre = %s AND direccion = %s AND contraseña = %s
        """, (usuario['idTipoUsuario'], usuario['ciudad'], usuario['nombre'], usuario['direccion'], usuario['contraseña'])
        )
        
        id = cur.fetchone()
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return id
def seleccionar_usuario_por_id(id):
    usuario = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
        """
        SELECT * FROM usuario WHERE id = %s
        """, (id)
        )

        usuario = cur.fetchone()
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return usuario
def seleccionar_usuario_por_tipo_y_ciudad(ciudad, tipo):
    usuarios = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
        """
        SELECT * FROM usuario WHERE idTipoUsuario = %s AND ciudad = %s
        """, (tipo, ciudad)
        )

        usuarios = cur.fetchall()
        conn.commit()
    except BaseException as error:
        mensaje =  f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return usuarios
    
def insertar_pedido(pedido):
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            'INSERT INTO pedido (idCliente, descripcion, estado, fechaPedido, idAdmin) VALUES (%s, %s, %s, %s, %s)',
            (pedido.idCliente, pedido.descripcion, pedido.estado, pedido.fechaPedido, pedido.idAdmin)
        )
        conn.commit()
    except BaseException as error:
        mensaje = f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()

def obtener_pedidos_por_admin(id_admin):
    pedidos = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM pedido WHERE idAdmin = %s
            """, (id_admin)
        )
        pedidos = cur.fetchall()
        conn.commit()
    except BaseException as error:
        mensaje = f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return pedidos

def obtener_id_admin_por_ciudad(ciudad):
    admin = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM usuario WHERE ciudad = %s AND idTipoUsuario = 1
            """, (ciudad)
        )
        admin = cur.fetchone()
        conn.commit()
    except BaseException as error:
        mensaje = f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return admin
def obtener_pedidos_por_cliente(id_cliente):
    pedidos = []
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            SELECT * FROM pedido WHERE idCliente = %s
            """, (id_cliente)
        )
        pedidos = cur.fetchall()
        conn.commit()
    except BaseException as error:
        mensaje = f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()
        return pedidos
def actualizar_estado_pedido(id_pedido, nuevo_estado):
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            'UPDATE pedido SET estado = %s WHERE id = %s',
            (nuevo_estado, id_pedido)
        )
        conn.commit()
    except BaseException as error:
        mensaje = f"NO ANDA PORQUE {error}"
    finally:
        cur.close()
        conn.close()