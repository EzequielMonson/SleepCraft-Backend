import pymysql


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
                apellido VARCHAR(50),
                correo VARCHAR(50),
                contrasena VARCHAR(255),
                direccion VARCHAR(50),
                idTipoUsuario INT,
                FOREIGN KEY (idTipoUsuario) REFERENCES tipoUsuario (id)
            )
            """
            
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS producto (
                id INT AUTO_INCREMENT PRIMARY KEY,
                tipo VARCHAR(50)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS material (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50)
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS medidas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(50),
                alto INT,
                ancho INT
            )
            """
        )
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS stock (
                id INT AUTO_INCREMENT PRIMARY KEY,
                idTipoProducto INT,
                idMaterial INT,
                idMedidas INT,
                cantidad INT,
                precio DOUBLE,
                FOREIGN KEY (idTipoProducto) REFERENCES producto (id),
                FOREIGN KEY (idMaterial) REFERENCES material (id),
                FOREIGN KEY (idMedidas) REFERENCES medidas (id)
                
            )
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

def cargar_datos_tabla_tipo_usuario():
    try:
        conn = pymysql.connect(**DATABASE_CONFIG)
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO tipoUsuario (tipo)
            VALUES ('admin');
            """
        )
        cur.execute(
            """
            INSERT INTO tipoUsuario (tipo)
            VALUES ('user');
            """
        )
        conn.commit()
        mensaje = "Se inserto bien el tipo usuario"
    except BaseException as error:
        mensaje = f"Hubo un error al insertar tipo usuario {error}"
        
    finally:
        cur.close()
        conn.close()
        return mensaje