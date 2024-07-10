import pymysql
from app.database import *

class Pedido:
    def __init__(self, registro):
        self.id = registro.get('id')
        self.idCliente = registro.get('idCliente')
        self.descripcion = registro.get('descripcion')
        self.estado = registro.get('estado')
        self.fechaPedido = registro.get('fechaPedido')
        self.fechaEntrega = registro.get('fechaEntrega')
        

    @staticmethod
    def crear_pedido(datos_pedido):
        insertar_pedido(datos_pedido)

    @staticmethod
    def actualizar_estado(id_pedido, nuevo_estado):
        actualizar_estado_pedido(id_pedido, nuevo_estado)

class Usuario:
    def __init__(self, registro):
        if type(registro) == tuple: 
            self.id = registro[0]
            self.nombre = registro[1]
            self.correo = registro[2]
            self.contraseña = registro[3]
            self.telefono = registro[4]
            self.ciudad = registro[5]
            self.direccion = registro[6]
        else:
            self.id = registro.get('id')
            self.nombre = registro.get('nombre')
            self.contraseña = registro.get('contraseña')
            self.correo = registro.get('correo')
            self.telefono = registro.get('telefono')
            self.ciudad = registro.get('ciudad')
            self.direccion = registro.get('direccion')

class Administrador(Usuario):
    def __init__(self, registro):
        super().__init__(registro)
        self.lista_clientes = self.obtener_clientes()

    def obtener_clientes(self):
        usuarios = seleccionar_usuario_por_tipo_y_ciudad(2,self.ciudad)
        clientes = [Cliente(usuario) for usuario in usuarios ]  # idTipoUsuario = 2 para clientes
        return clientes

    def mostrar_clientes(self):
        return [cliente.to_dict() for cliente in self.lista_clientes]

    def mostrar_todos_los_pedidos_clientes(self):
        pedidos = obtener_pedidos_por_admin(self.id)
        return pedidos

    def marcar_pedido_en_camino(self, pedido_id):
        Pedido.actualizar_estado(pedido_id, 'En Camino')

    def to_dict(self):
        return {
            'id' : self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'contraseña' : self.contraseña,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'ciudad': self.ciudad,
            'listaClientes': [cliente.to_dict() for cliente in self.lista_clientes],
        }

class Cliente(Usuario):
    def __init__(self, registro):
        super().__init__(registro)
        self.lista_pedidos = self.obtener_pedidos()

    def obtener_pedidos(self):
        return obtener_pedidos_por_cliente(self.id)

    def hacer_pedido(self, datos_pedido):
        datos_pedido.idAdmin = self.obtener_id_admin()
        insertar_pedido(datos_pedido)

    def obtener_id_admin(self):
        return obtener_id_admin_por_ciudad(self.ciudad)
    def mostrar_pedidos(self):
        return [pedido.__dict__ for pedido in self.lista_pedidos]

    def cancelar_pedido(self, id_pedido):
        actualizar_estado_pedido(id_pedido, 'Cancelado')

    def confirmar_pedido_enviado(self, id_pedido):
        actualizar_estado_pedido(id_pedido, 'Enviado')

    def to_dict(self):
        return {
            'id' : self.id,
            'nombre': self.nombre,
            'correo': self.correo,
            'contraseña' : self.contraseña,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'ciudad': self.ciudad,
            'listaPedidos': [pedido.__dict__ for pedido in self.lista_pedidos],
        }