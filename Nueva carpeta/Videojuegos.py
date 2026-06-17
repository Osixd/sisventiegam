from abc import ABC, abstractmethod

# Clase de utilidades para validación
class Validador:
    @staticmethod
    def obtener_numero(mensaje, tipo=int): #Metodo para validar entrada de números
        try:
            return tipo(input(mensaje))
        except ValueError:
            print("Entrada inválida")
            return None

# ── Clase Producto (Abstracta) ───────────────────────────────────────────────
# Clase base para todos los productos (atributos: título, plataforma, precio)
class Producto(ABC):
    def __init__(self, titulo, plataforma, precio):
        
        self.titulo = titulo
        self.plataforma = plataforma
        self._precio = None
        self.precio = precio
    
    @property   
    def precio(self): #Metodo para obtener el precio del producto
        return self._precio
    
    @precio.setter
    def precio(self, valor): #Metodo para establecer un nuevo precio al producto
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
    def __init__(self, titulo, genero, precio, plataforma): #Constructor: titulo, género, precio, plataforma
        super().__init__(titulo, plataforma, precio)
        self.genero = genero
        

    def mostrar_info(self): #Metodo para imprimir la información del videojuego
        return f"Titulo: {self.titulo}\nGenero: {self.genero}\nPrecio: ${self.precio:.2f}\nPlataforma: {self.plataforma}"

    def aplicar_descuento(self, porcentaje): #Metodo para aplicar descuento al videojuego
        descuento = self._precio * (porcentaje) / 100
        self._precio -= descuento
        
    def calcular_precio_final(self):
        pass
    
    def get_precio(self): #Metodo para obtener el precio del videojuego
        return self._precio


# ── Clase Usuario ────────────────────────────────────────────────────────────
# Usuario con saldo, carrito, y métodos de compra
class Usuario():
    def __init__(self, nombre, email, saldo): #Constructor: nombre, email, saldo inicial
        self.nombre = nombre
        self.email = email
        self._saldo = saldo
        self.carrito = Carrito()
        
    def saludar(self): #Metodo para saludar al usuario y mostrar su información
        return f"Hola, bienvenido {self.nombre}.\nTu correo electronico registrado es: {self.email}.\nTienes un saldo de ${self._saldo:.2f}"
    
    def tiene_saldo_suficiente(self, monto): #Metodo para verificar si el usuario tiene saldo suficiente
        if self._saldo >= monto:
            return True
        else:
            return False
        
    def get_saldo(self): #Metodo para obtener el saldo del usuario
        return self._saldo

    def depositar(self, monto): #Metodo para depositar saldo a la cuenta del usuario
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
            self._saldo -= videojuego.precio
            print(f"{self.nombre} ha comprado {videojuego.titulo} por ${videojuego.precio:.2f}")
        else:
            print(f"{self.nombre} no tiene suficiente saldo para comprar {videojuego.titulo}")


# ── Clase VideojuegoDigital ──────────────────────────────────────────────────
# Extiende de Videojuego: agrega tamaño en GB y requisito de internet
class VideojuegoDigital(Videojuego):
    def __init__(self, titulo, genero, precio, plataforma, tamano_gb, requiere_internet): #Constructor con atributos adicionales
        super().__init__(titulo, genero, precio, plataforma)
        self.tamano_archivo = tamano_gb
        self.requiere_internet = requiere_internet
        
    def mostrar_info(self):
        return f"Titulo: {self.titulo}\nGenero: {self.genero}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nEste  juego tiene un descuento del 10%\nPrecio final: ${self.calcular_precio_final():.2f}\nTamaño en GB: {self.tamaño_archivo}\nRequiere internet: {self.requiere_internet}"

    def calcular_precio_final(self): #Metodo para calcular precio final con descuento del 10%
        return self.precio * 0.9 

# ── Clase Consola ────────────────────────────────────────────────────────────
# Extiende de Producto: consolas de videojuegos con almacenamiento
class Consola(Producto):
    def __init__(self, titulo, precio, plataforma, almacenamiento_gb): #Constructor: titulo, precio, plataforma, almacenamiento
        super().__init__(titulo, plataforma, precio)
        self.almacenamiento = almacenamiento_gb

    def mostrar_info(self): #Metodo para mostrar información de la consola
        return f"Titulo: {self.titulo}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nAlmacenamiento: {self.almacenamiento} GB"        
    
    def calcular_precio_final(self): #Metodo para calcular precio final con descuento si es mayor a $10,000
        if self._precio >= 10000:
            return self._precio * 0.90
        else:
            return self._precio


# ── Clase Accesorio ──────────────────────────────────────────────────────────
# Extiende de Producto: accesorios para consolas (controles, audífonos, etc.)
class Accesorio(Producto):
    def __init__(self, titulo, precio, plataforma, tipo): #Constructor: titulo, precio, plataforma, tipo de accesorio
        super().__init__(titulo, plataforma, precio)
        self.tipo_accesorio = tipo

    def mostrar_info(self): #Metodo para mostrar información del accesorio
        return f"Titulo: {self.titulo}\nPlataforma: {self.plataforma}\nPrecio: ${self.precio:.2f}\nTipo de accesorio: {self.tipo_accesorio}"
    
    def calcular_precio_final(self): #Metodo para calcular precio final con descuento del 5% si es mayor a $500
        if self._precio >= 500:
            return self._precio * 0.95
        else:
            return self._precio

    def get_precio(self):
        super().get_precio()
    
    def set_precio(self, nuevo_precio): #Metodo para establecer nuevo precio del accesorio
        super().precio = nuevo_precio

# ── Instanciación de Productos ───────────────────────────────────────────────
# Creación de instancias de videojuegos, consolas y accesorios
#Instanciamos juegos
videojuego1 = Videojuego("The Last of Us", "Accion", 59.99, "PlayStation")
videojuego2 = Videojuego("Cyberpunk 2077", "RPG", 49.99, "PC")
videojuego3 = Videojuego("Animal Crossing: New Horizons", "Simulacion", 59.99, "Nintendo Switch")

#Instancia consolas
consola1 = Consola("PlayStation 5", 499.99, "PlayStation", 825)
consola2 = Consola("Xbox Series X", 499.99, "Xbox", 1000)

#Instancia accesorios
accesorio1 = Accesorio("Control Inalámbrico DualSense", 69.99, "PlayStation", "Control")
accesorio2 = Accesorio("Headset Inalámbrico Xbox", 99.99, "Xbox", "Audífonos")

# ── Instanciación de Usuarios ────────────────────────────────────────────────
# Creación de usuarios con saldo inicial
#Instanciamos usuario
usuario1 = Usuario("Juan", "juan@example.com", 100.00)
usuario2 = Usuario("Carmilla", "Mariaperez@example.com", 150.00)

usuario1.saludar()#Llamada al metodo saludar al usuario1
usuario2.saludar() # "" usuario2

servicio1 = Servicio("Reparación de Consola", "Reparación", 300.00, 20.00, 7, False)
servicio2 = Servicio("Mantenimiento de PC", "Mantenimiento", 200.00, 0.00, 3, False  )
servicio3 = Servicio("Garantia", "Reparación", 20.00, 10.00, 5, True)

# ── Instanciación de Servicios ───────────────────────────────────────────────
# Creación de servicios (reparación, mantenimiento, garantía)
servicio1 = Servicio("Reparación de Consola", "Reparación", 300.00, 20.00, 7, False)
servicio2 = Servicio("Mantenimiento de PC", "Mantenimiento", 200.00, 0.00, 3, False  )
servicio3 = Servicio("Garantia", "Reparación", 20.00, 10.00, 5, True)

# ── Función Principal ────────────────────────────────────────────────────────
# Menú interactivo para la tienda de videojuegos
def main():#Función principal con menú para la tienda de videojuegos
    
    #Se crean listas para uso mas facil de los juegos/usuarios
    juegos = [videojuego1, videojuego2, videojuego3]
    usuarios = [usuario1, usuario2]
    catalogo = [videojuego1, videojuego2, videojuego3,
                consola1, consola2,
                accesorio1, accesorio2,
                servicio1, servicio2, servicio3]
    
    #Menu principal + opciones del usuario
    while True:
        print("\n" + "="*50)
        print("     TIENDA DE VIDEOJUEGOS - MENÚ PRINCIPAL")
        print("="*50)
        print("1. Ver catálogo completo")
        print("2. Aplicar promoción a un videojuego")
        print("3. Agregar producto al carrito")
        print("4. Ver carrito de un cliente")
        print("5. Pagar carrito")
        print("6. Agregar saldo a un cliente")
        print("7. Salir")
        print("="*50)
        
        #Solicitar al usuario que elija una opción          
        opcion = input("Elige una opción: ") 
        
        #Seleccion
        if opcion == "1": #Opción 1: Mostrar catálogo completo
            print("\n--- CATÁLOGO DE VIDEOJUEGOS ---")
            for i, productos in enumerate(catalogo, 1): #Enumerate para mostrar el numero del juego junto con su información
                print(f"\n{i}. {productos.mostrar_info()}") 
        
        elif opcion == "2": #Opción 2: Aplicar descuento a un videojuego
            print("\n--- APLICAR PROMOCIÓN ---")
            for i, juego in enumerate(juegos, 1): #Enumerate para mostrar el numero del juego junto con su título
                print(f"{i}. {juego.titulo}")
            
            num_juego = Validador.obtener_numero("Selecciona el número del juego: ", int)
            if num_juego is not None:
                num_juego -= 1
                porcentaje = Validador.obtener_numero("Ingresa el porcentaje de descuento: ", float)
                if porcentaje is not None and 0 <= num_juego < len(juegos):
                    juegos[num_juego].aplicar_descuento(porcentaje) #Aplicamos el descuento al juego seleccionado
                    print(f"Descuento aplicado. Nuevo precio: ${juegos[num_juego].precio:.2f}") #Mostramos el nuevo precio del juego después de aplicar el descuento
                else:
                    print("Opción inválida")#Opcion invalida
        
        elif opcion == "3":
            print("\n--- VERIFICAR COMPRA ---") 
            for i, usuario in enumerate(usuarios, 1): 
                print(f"{i}. {usuario.nombre} (Saldo: ${usuario.get_saldo():.2f})")
            
            num_usuario = Validador.obtener_numero("Selecciona el número del usuario: ", int)
            if num_usuario is not None:
                num_usuario -= 1
                if 0 <= num_usuario < len(usuarios):
                    comprables = [p for p in catalogo if isinstance(p, Producto)]
                    for i, producto in enumerate(comprables, 1):
                        print(f"{i}. {producto.titulo} - ${producto.precio:.2f}")
                    num_producto = Validador.obtener_numero("Selecciona el número del producto: ", int)
                    if num_producto is not None:
                        num_producto -= 1
                        if 0 <= num_producto < len(comprables):
                            usuarios[num_usuario].agregar_al_carrito(comprables[num_producto])
                        else:
                            print("Opción inválida")
                    else:
                        print("Opción inválida") #Opcion invalida
        
        elif opcion == "4":
            print("\n--- AGREGAR SALDO ---")
            for i, usuario in enumerate(usuarios, 1):
                print(f"{i}. {usuario.nombre} (Saldo: ${usuario.get_saldo():.2f})") #Enumerate para mostrar el numero del usuario junto con su nombre y saldo
            
            num_usuario = Validador.obtener_numero("Selecciona el número del usuario: ", int)
            if num_usuario is not None:
                num_usuario -= 1
                monto = Validador.obtener_numero("Ingresa el monto a depositar: ", float)
                if monto is not None and 0 <= num_usuario < len(usuarios):
                    usuarios[num_usuario].depositar(monto) #Agregamos el saldo al usuario seleccionado
                else:
                    print("Opción inválida") #Opcion invalida
            
            
            
        elif opcion == "5":        
            print("\n¡Hasta luego! Gracias por visitarnos.") #Mensaje de despedida al salir del programa
            break
        
        else:
            print("Opción no válida. Intenta de nuevo.")#Mensaje para opciones no válidas en el menú


# ── Punto de entrada ─────────────────────────────────────────────────────────
# Ejecución del programa principal
if __name__ == "__main__":
    main()  #Llamada a la función principal para iniciar el programa
