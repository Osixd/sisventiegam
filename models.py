from abc import ABC, abstractmethod
from util import *


class Validador:
    @staticmethod
    def obtener_numero(mensaje, tipo=int):
        try:
            return tipo(input(mensaje))
        except ValueError:
            print("Entrada inválida")
            return None

class Servicio():
    def __init__(self, NombreServicio, TipoServicio, PrecioBase, ValorReparacion, TiempoEntrega, Garantia):
        self.NombreServicio = NombreServicio
        self.TipoServicio = TipoServicio
        self.PrecioBase = PrecioBase
        self.ValorReparacion = ValorReparacion
        self.TiempoEntrega = TiempoEntrega
        self.Garantia = bool(Garantia)
                
    def calcular_precio_final(self):
        if self.TipoServicio == "Reparación" or self.TipoServicio == "Mantenimiento":
            return (self.PrecioBase + self.ValorReparacion) * (self.TiempoEntrega * 0.5)
        else:
            return self.PrecioBase      
        
    def mostrar_info(self):
        if self.Garantia == True:
            return f"Garantia de 1 año para Consolas o Pc's\n Precio: ${self.calcular_precio_final():.2f}"
        else:            
            return f"Nombre del servicio: {self.NombreServicio}\nTipo de servicio: {self.TipoServicio}\nPrecio base: ${self.PrecioBase:.2f}\nValor de reparación: ${self.calcular_precio_final():.2f}\nTiempo de entrega: {self.TiempoEntrega} días."
          



class Producto(ABC):
    def __init__(self, titulo, plataforma, precio):
        self.titulo = titulo
        self.plataforma = plataforma
        self._precio = None
        self.precio = precio
    
    @property   
    def precio(self): #Metodo para obtener el precio del juego
        return self._precio
    
    @precio.setter
    def precio(self, valor): #Metodo para establecer un nuevo precio al juego
        if not isinstance(valor, (int, float)): #Validación para asegurarse de que el nuevo precio sea un número positivo
            print("Error, el valor ingresado no es un número.") 
        elif valor <= 0:
            print("Error: El precio debe ser mayor que cero.")
        else:
            self._precio = valor 
            
    @abstractmethod
    def mostrar_info(self):
        pass
    
    @abstractmethod
    def calcular_precio_final(self):
        pass



#Clase videojuego
class Videojuego(Producto):
    def __init__(self, titulo, genero, precio, plataforma): #constructor
        super().__init__(titulo, plataforma, precio)
        self.genero = genero
        

    #Metodo para imprimir la información"
    def mostrar_info(self, ):
        return f"Titulo: {self.titulo}\nGenero: {self.genero}\nPrecio: ${self.precio:.2f}\nPlataforma: {self.plataforma}"

    #Metodo para aplicar descuento
    def aplicar_descuento(self, porcentaje):
        descuento = self._precio * (porcentaje) / 100
        self._precio -= descuento
        
    def calcular_precio_final(self):
        pass
    
    def get_precio(self):
        return self._precio


#Clase de los Usuarios
class Usuario():
    def __init__(self, nombre, email, saldo): #constructor
        self.nombre = nombre
        self.email = email
        self._saldo = saldo
        
    def saludar(self): #Metodo para saludar al usuario
        return f"Hola, bienvenido {self.nombre}.\nTu correo electronico registrado es: {self.email}.\nTienes un saldo de ${self._saldo:.2f}"
    
    def tiene_saldo_suficiente(self, monto):#Metodo para verificar si el usuario tiene saldo suficiente para comprar un juego
        if self._saldo >= monto:
            return True
        else:
            return False
        
    def get_saldo(self): #Metodo para obtener el saldo del usuario
        return self._saldo

    def depositar(self, monto):
        if not isinstance(monto, (int, float)):
            print("Error: el monto a depositar debe ser un número.")
            return
        if monto <= 0:
            print("Error: el monto a depositar debe ser mayor a cero.")
            return
        self._saldo += monto
        print(f"Depósito exitoso. Nuevo saldo de {self.nombre}: ${self._saldo:.2f}")
    
    #Metodo para comprar un juego
    def comprar_juego(self, videojuego): 
        if self._saldo >= videojuego.precio:
            self._saldo -= videojuego.precio #Caso positivo
            print(f"{self.nombre} ha comprado {videojuego.titulo} por ${videojuego.precio:.2f}")
        else:
            print(f"{self.nombre} no tiene suficiente saldo para comprar {videojuego.titulo}")#Caso negativo


#Clase videojuego_digital
class VideojuegoDigital(Videojuego):
    def __init__(self, titulo, genero, precio, plataforma, tamano_gb, requiere_internet):
        super().__init__(titulo, genero, precio, plataforma)
        self.tamano_archivo = tamano_gb
        self.requiere_internet = requiere_internet
        
    def mostrar_info(self):
        return f"Titulo: {self.titulo}\nGenero: {self.genero}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nEste  juego tiene un descuento del 10%\nPrecio final: ${self.calcular_precio_final():.2f}\nTamaño en GB: {self.tamaño_archivo}\nRequiere internet: {self.requiere_internet}"

    def calcular_precio_final(self):    
        return self.precio * 0.9 

#Clase Consola 
class Consola(Producto):
    def __init__(self, titulo, precio, plataforma, almacenamiento_gb):
        super().__init__(titulo, plataforma, precio)
        self.almacenamiento = almacenamiento_gb

    def mostrar_info(self):
        return f"Titulo: {self.titulo}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nAlmacenamiento: {self.almacenamiento} GB"        
    
    def calcular_precio_final(self):
        if self._precio >= 10000:
            return self._precio * 0.90
        else:
            return self._precio


#Clase accesorio    
class Accesorio(Producto):
    def __init__(self, titulo, precio, plataforma, tipo):
        super().__init__(titulo, plataforma, precio)
        self.tipo_accesorio = tipo

    def mostrar_info(self):
        return f"Titulo: {self.titulo}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nTipo de accesorio: {self.tipo_accesorio}"
    
    def calcular_precio_final(self):
        if self._precio >= 500:
            return self._precio * 0.95
        else:
            return self._precio

    def get_precio(self):
        super().get_precio()
    
    def set_precio(self, nuevo_precio):
        super().precio = nuevo_precio
        
        
        

#Instanciamos juegos
videojuego1 = Videojuego("The Last of Us", "Accion", 59.99, "PlayStation")
videojuego2 = Videojuego("Cyberpunk 2077", "RPG", 49.99, "PC")
videojuego3 = Videojuego("Animal Crossing: New Horizons", "Simulacion", 59.99, "Nintendo Switch")

#Intancia consolas
consola1 = Consola("PlayStation 5", 499.99, "PlayStation", 825)
consola2 = Consola("Xbox Series X", 499.99, "Xbox", 1000)

#Instancia accesorios
accesorio1 = Accesorio("Control Inalámbrico DualSense", 69.99, "PlayStation", "Control")
accesorio2 = Accesorio("Headset Inalámbrico Xbox", 99.99, "Xbox", "Audífonos")


#Instanciamos usuario
usuario1 = Usuario("Juan", "juan@example.com", 100.00)
usuario2 = Usuario("Carmilla", "Mariaperez@example.com", 150.00)

usuario1.saludar()#Llamada al metodo saludar al usuario1
usuario2.saludar() # "" usuario2
