from abc import ABC, abstractmethod
from util import *
from models import *
import os



def clear():
    os.system('cls' if os.name == 'nt' else 'clear')


def pausar():
    input("\nPresione Enter para continuar.")


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



def Menu_inicio(conexion):
    while True:
        try:
            clear()
            print("-"*15, "Bienvenido", "-"*15)
            opcion = int(input("Presione 1 para iniciar seción o 2 para crear una cuenta\n"))
            
            if opcion == 1:
                
                usuario_activo = Login(conexion)
                
                return usuario_activo
                
            elif opcion == 2:
                
                Agregar_usuario(conexion)
                print("Inicie sesion nuevamente.")
                pausar()
                
            else:
                
                print("Opción invalida.")
                pausar()
                
        except:
            print("Por favor ingresa un número Entero valido (1-2)")
            pausar()



def Menu_principal(conexion, usuario_activo):
    
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
    
    while True:
        
        try:
                
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
            if usuario_activo["permisos"] == "admin":
                print("7.- Panel admin")
                opciones["7"] = "admin"
                opciones["admin"] = "admin"
            
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                continue
            
            accion = opciones[opcion]
            
            if accion == "productos":
                
                Menu_productos(conexion, usuario_activo)
                
            elif accion == "carrito":
                
                Menu_carrito(conexion, usuario_activo)
                
            elif accion == "billetera":
                
                Menu_billetera(conexion, usuario_activo)
                
            elif accion == "historial":
                
                Consultar_historial(conexion, usuario_activo)
                
            elif accion == "logout":
                
                Logout()
                pausar()
                return "logout"
                
            elif accion == "admin":
                
                Menu_admin(conexion, usuario_activo)
                
            elif accion == "salir":
                
                return "salir"
            
        except Exception as e:
            
            print(f"Hubo un error inesperado. {e}")
            pausar()



def Menu_productos(conexion, usuario_activo):
    
    while True:
        
        try:
            clear()
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
            
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                continue
            
            accion = opciones[opcion]
            
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
            


def Menu_carrito(conexion, usuario_activo):
    
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
            opcion = ""
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            accion = opciones[opcion]
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



def Menu_billetera(conexion, usuario_activo):
    
    opciones = {
        "1": "consultar",
        "consultar": "consultar",
        "saldo": "consultar",
        "2": "depositar",
        "depositar": "depositar",
        "3": "salir",
        "salir": "salir"
    }

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
            
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            accion = opciones[opcion]
            
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



def Menu_admin(conexion, usuario_activo):
    
    if usuario_activo["permisos"] != "admin":
        print("No tienes permiso para entrar al panel admin.")
        pausar()
        return
    
    opciones = {
        "1": "productos",
        "productos": "productos",
        "2": "usuarios",
        "usuarios": "usuarios",
        "3": "salir",
        "salir": "salir"
    }

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
            
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            accion = opciones[opcion]
            
            if accion == "productos":
                
                Menu_productos(conexion, usuario_activo)
                
            elif accion == "usuarios":
                
                Menu_usuarios_admin(conexion, usuario_activo)
                
            elif accion == "salir":
                
                break
            
        except:
            
            print("Ocurrio un error en el panel admin.")
            pausar()



def Menu_usuarios_admin(conexion, usuario_activo):
    
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
            
            opcion = input("Selecciona una opción(número o nombre).").strip().lower()
            
            if opcion not in opciones:
                print("Opción invalida.")
                pausar()
                continue
            
            accion = opciones[opcion]
            
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



def main():#Función principal con menú para la tienda de videojuegos
    
    conexion = Conectar_bd() 
    if conexion is None:
        print("No se pudo conectar a la base de datos. El programa se cerrará.")
        return 
    
    try:
        
        while True:
            
            usuario_activo = Menu_inicio(conexion)
            
            if usuario_activo is None:
                break
            
            accion = Menu_principal(conexion, usuario_activo)
            
            if accion == "salir":
                break
            
    finally:
        
        conexion.close() #Cerramos la conexión a la base de datos al finalizar el programa

if __name__ == "__main__":
    main()  #Llamada a la función principal para iniciar el programa
