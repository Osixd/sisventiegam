#==============================================================================
#                   Programa principal/main
#==============================================================================
#==============================================================================
#Aqui se manejan los menús y todo el flujo principal del codigo
#==============================================================================

# Importamos el archivo de utilidades (modulos)
from util import *
#Libreria para limpiar pantalla (solo se ocupa para eso xd)
import os


#==============================================================================
#                               Menús 
#==============================================================================

#Función que limpia pantalla ¿Qué hace? ...  Limpia pantalla 
def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

#Función para esperar interaccion y que no se pierdan los datos
def pausar():
    input("\nPresione Enter para continuar.")

#Función que muestra los productos en pantalla
# (noc pq la hice así ese dia estaba medio dormido) pero funciona asi que no toques
def imprimir_productos(productos):
    if not productos:
        print("No se encontraron productos.")
        return

    for p in productos:
        descripcion = p.get("descripcion", "Sin descripcion")
        print(f"""Producto:      {p['nombre']}
Categoria:     {p['categoria']}
Precio(mxn):  ${p['precio']:.2f}
Descripcion:   {descripcion}
Stock:         {p['stock']}
""")


# Primer menu, este solo es el "login", para crear o iniciar sesion
def Menu_inicio(conexion):
    
    # bucle para que se muestre el menú indeterminadamente(solo 3 por los intentos)
    while True:
        # try except, para casos donde el cliente use char en int, usuario inútil...
        try:
            #empiezamos limpiandeishon the pantalleishon
            clear()
            #Una  calida bienvenida
            print("-"*15, "Bienvenido", "-"*15)
            #primera interaccion
            opcion = int(input("Presione 1 para iniciar seción o 2 para crear una cuenta\n"))
            
            # opción para iniciar secion.
            if opcion == 1:
                
                #Si el resultado devuelve algo es porque devuelve algo.
                usuario_activo = Login(conexion)
                
                #retorna el usuario activo
                return usuario_activo
                
                #opción para crear una nueva cuenta
            elif opcion == 2:
                
                #se agrega el nuevo usuario y se solicita volver a iniciar secion.
                Agregar_usuario(conexion)
                print("Inicie sesion nuevamente.")
                pausar()
                
                #en caso que el hjp usuario elija algo x.
            else:
                
                #escribio mal el hjlv.
                print("Opción invalida.")
                pausar()
                
        #exepcion para los hjp usuarios que pongan caracteres.
        except:
            
            #pide un valor valido
            print("Por favor ingresa un número Entero valido (1-2)")
            pausar()


#menu principal
def Menu_principal(conexion, usuario_activo):
    
    #opciones es un diccionario para facilitar los posibles escenarios.
    opciones = {
    "1": "productos",
    "productos": "productos",
    "2": "carrito",
    "carrito": "carrito",
    "3": "billetera",
    "billetera": "billetera",
    "4": "historial",
    "historial": "historial",
    "5": "logout",
    "logout": "logout",    
    "6": "salir",
    "salir": "salir"
    }
    
    #bucle principal.
    while True:
        
        #try except para errores.
        try:
                
            #funcion para limpiar pantalla e imprime el menu inicial.
            clear()
            print("="*50, "\n")
            print("         Menú Principal")
            print("="*50)
            print("""   Por favor selecciona una opción.
                
1.- Productos.
2.- Carrito.
3.- Billetera.
4.- Historial de compras.
5.- logout (cerrar seción).
6.- Salir.
                """)
            
            #si el usuario tiene permisos de admin, se agrega a la seleccion una opción "admin"
            if usuario_activo["permisos"] == "admin":
                print("7.- Panel admin")
                opciones["7"] = "admin"
                opciones["admin"] = "admin"
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime.
            if opcion not in opciones:
                
                print("Opción invalida.")
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            
            #depende de la accion es el siguiente menu
            if accion == "productos":
                
                Menu_productos(conexion, usuario_activo)
                
            elif accion == "carrito":
                
                Menu_carrito(conexion, usuario_activo)
                
            elif accion == "billetera":
                
                Menu_billetera(conexion, usuario_activo)
                
            elif accion == "historial":
                
                Consultar_historial(conexion, usuario_activo)
                
            elif accion == "logout":
                
                #en caso de logout manda al menu.
                Logout()
                pausar()
                return "logout"
                
            elif accion == "admin":
                
                #aqui se accede al menu exclusivo
                Menu_admin(conexion, usuario_activo)
                
            elif accion == "salir":
                
                #sale del programa
                return "salir"
            
        except Exception as e:
            
            #aqui caen los errores y se reinicia el menu
            print(f"Hubo un error inesperado. {e}")
            pausar()


#Menu para ver, buscar y gestionar productos
#Si el usuario es admin, tiene opciones adicionales para agregar, actualizar y eliminar productos
def Menu_productos(conexion, usuario_activo):
    
    #bucle para que se muestre el menú indeterminadamente
    while True:
        
        try:
            clear()
            #se define un diccionario con las opciones disponibles
            opciones = {
                "1": "ver",
                "ver": "ver",
                "2": "buscar",
                "buscar": "buscar",
                "3": "salir",
                "salir": "salir"
                }
                
            print("""Por favor selecciona una de las siguientes opciones.
1.- Ver todos los productos(ver)
2.- Buscar un producto(buscar)
3.- Salir.
                    """)
            
            #si el usuario tiene permisos de admin, se agrega a la seleccion opciones adicionales
            if usuario_activo["permisos"] == "admin":
                
                print("4.- Agregar un producto(agregar)")
                opciones["4"] = "agregar"
                opciones["agregar"] = "agregar"
                print("5.- Actuazar un producto(actualizar)  ")
                opciones["5"] = "actualizar"
                opciones["actualizar"] = "actualizar"
                print("6.- Eliminar un producto(eliminar)")  
                opciones["6"] = "eliminar"
                opciones["eliminar"] = "eliminar"
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime
            if opcion not in opciones:
                print("Opción invalida.")
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            
            #depende de la accion es la siguiente operacion
            if accion == "ver":
                    
                productos = Mostrar_productos(conexion)
                imprimir_productos(productos)
                pausar()
                    
            elif accion == "buscar":
                    
                nombre_producto = input("Ingrese el nombre del producto a buscar.")
                productos = Buscar_producto(conexion, nombre_producto)
                imprimir_productos(productos)
                pausar()
                    
            elif accion == "agregar":
                    
                Agregar_producto(conexion, usuario_activo)
                pausar()
                    
            elif accion == "actualizar":
                    
                Actualizar_producto(conexion, usuario_activo)
                pausar()
                    
            elif accion == "eliminar":
                    
                Eliminar_producto(conexion, usuario_activo)
                pausar()
                    
            elif accion == "salir":
                    
                break
        
        except:
            
            print("Ocurrio un error al mostrar los productos")
            pausar()
            return


#Menu para gestionar el carrito de compras del usuario
#Permite ver, agregar, eliminar productos y realizar el pago
def Menu_carrito(conexion, usuario_activo):
    
    #opciones es un diccionario para facilitar los posibles escenarios
    opciones = {
        "1": "ver",
        "ver": "ver",
        "2": "agregar",
        "agregar": "agregar",
        "3": "eliminar",
        "eliminar": "eliminar",
        "quitar": "eliminar",
        "4": "pagar",
        "pagar": "pagar",
        "5": "salir",
        "salir": "salir"
    }

    #bucle principal del carrito
    while True:
        
        try:
            
            clear()
            print("="*50)
            print("                 Carrito")
            print("="*50)
            print("""Por favor selecciona una opción.
1.- Ver carrito(ver)
2.- Agregar producto(agregar)
3.- Quitar producto(eliminar/quitar)
4.- Pagar carrito(pagar)
5.- Salir.
                    """)
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            #obtenemos el id del usuario activo y verificamos su carrito
            id_usuario = usuario_activo["id_usuario"]
            id_carrito = Verificar_carrito(conexion, id_usuario)
            
            if accion == "ver":
                
                Ver_carrito(conexion, id_usuario)
                pausar()
                
            elif accion == "agregar":
                
                Agregar_al_carrito(conexion, id_carrito, id_usuario)
                pausar()
                
            elif accion == "eliminar":
                
                Eliminar_del_carrito(conexion, usuario_activo, id_carrito)
                pausar()
                
            elif accion == "pagar":
                
                Pagar_carrito(usuario_activo, conexion)
                pausar()
                
            elif accion == "salir":
                
                break
            
        except:
            
            print("Ocurrio un error en el menu del carrito.")
            pausar()


#Menu para gestionar la billetera del usuario
#Permite consultar el saldo y realizar depositos de dinero
def Menu_billetera(conexion, usuario_activo):
    
    #opciones es un diccionario para facilitar los posibles escenarios
    opciones = {
        "1": "consultar",
        "consultar": "consultar",
        "saldo": "consultar",
        "2": "depositar",
        "depositar": "depositar",
        "3": "salir",
        "salir": "salir"
    }

    #bucle principal de la billetera
    while True:
        
        try:
            
            clear()
            print("="*50)
            print("                Billetera")
            print("="*50)
            print("""Por favor selecciona una opción.
1.- Consultar saldo(consultar/saldo)
2.- Depositar saldo(depositar)
3.- Salir.
                    """)
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            
            #depende de la accion es la siguiente operacion
            if accion == "consultar":
                
                Consultar_saldo(conexion, usuario_activo)
                
            elif accion == "depositar":
                
                Depositar_saldo(conexion, usuario_activo)
                pausar()
                
            elif accion == "salir":
                
                break
            
        except:
            
            print("Ocurrio un error en el menu de billetera.")
            pausar()


#Menu del panel admin
#Solo accesible si el usuario tiene permisos de admin
#Permite administrar productos y usuarios del sistema
def Menu_admin(conexion, usuario_activo):
    
    #verificamos que el usuario tenga permisos de admin antes de continuar
    if usuario_activo["permisos"] != "admin":
        print("No tienes permiso para entrar al panel admin.")
        pausar()
        return
    
    #opciones es un diccionario para facilitar los posibles escenarios
    opciones = {
        "1": "productos",
        "productos": "productos",
        "2": "usuarios",
        "usuarios": "usuarios",
        "3": "salir",
        "salir": "salir"
    }

    #bucle principal del panel admin
    while True:
        
        try:
            
            clear()
            print("="*50)
            print("              Panel Admin")
            print("="*50)
            print("""Por favor selecciona una opción.
1.- Administrar productos(productos)
2.- Administrar usuarios(usuarios)
3.- Salir.
                    """)
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            
            #depende de la accion es el siguiente menu
            if accion == "productos":
                
                Menu_productos(conexion, usuario_activo)
                
            elif accion == "usuarios":
                
                Menu_usuarios_admin(conexion, usuario_activo)
                
            elif accion == "salir":
                
                break
            
        except:
            
            print("Ocurrio un error en el panel admin.")
            pausar()


#Menu de administración de usuarios
#Permite ver, buscar, agregar y eliminar usuarios del sistema
def Menu_usuarios_admin(conexion, usuario_activo):
    
    #opciones es un diccionario para facilitar los posibles escenarios
    opciones = {
        "1": "ver",
        "ver": "ver",
        "2": "buscar",
        "buscar": "buscar",
        "3": "agregar",
        "agregar": "agregar",
        "4": "eliminar",
        "eliminar": "eliminar",
        "5": "salir",
        "salir": "salir"
    }

    #bucle principal de administracion de usuarios
    while True:
        
        try:
            
            clear()
            print("="*50)
            print("          Administración de usuarios")
            print("="*50)
            print("""Por favor selecciona una opción.
1.- Ver usuarios(ver)
2.- Buscar usuario(buscar)
3.- Agregar usuario(agregar)
4.- Eliminar usuario(eliminar)
5.- Salir.
                    """)
            
            #esta interaccion automaticamente pone como minusculas las letras
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            #si el usuario pone algo que no este en el diccionario, lo imprime
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            #accion es igual a la seleccion en el diccionario
            accion = opciones[opcion]
            
            #depende de la accion es la siguiente operacion
            if accion == "ver":
                
                Mostrar_usuarios(conexion, usuario_activo)
                pausar()
                
            elif accion == "buscar":
                
                nombre_usuario = input("Ingrese el nombre de usuario a buscar.")
                Buscar_usuario(conexion, nombre_usuario)
                pausar()
                
            elif accion == "agregar":
                
                Agregar_usuario(conexion)
                pausar()
                
            elif accion == "eliminar":
                
                Eliminar_usuario(conexion, usuario_activo)
                pausar()
                
            elif accion == "salir":
                
                break
            
        except:
            
            print("Ocurrio un error en el menu de usuarios.")
            pausar()


#Función principal con menú para la tienda de videojuegos
#Gestiona la conexión a la base de datos y controla el flujo general del programa
def main():
    
    #realizamos la conexion a la base de datos
    conexion = Conectar_bd()
    #validamos que la conexion sea exitosa
    if conexion is None:
        print("No se pudo conectar a la base de datos. El programa se cerrará.")
        return
    
    try:
        
        #bucle principal del programa
        while True:
            
            #menu de inicio y login
            usuario_activo = Menu_inicio(conexion)
            
            #si el usuario es None, se sale del programa
            if usuario_activo is None:
                break
            
            #menu principal donde el usuario puede navegar las diferentes opciones
            accion = Menu_principal(conexion, usuario_activo)
            
            #si el usuario presiona salir, se cierra el programa
            if accion == "salir":
                break
            
    finally:
        
        #cerramos la conexion a la base de datos al finalizar el programa
        conexion.close()

#Punto de entrada del programa
if __name__ == "__main__":
    #Llamada a la función principal para iniciar el programa
    main()
