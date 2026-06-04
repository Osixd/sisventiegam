from abc import ABC, abstractmethod
from util import *
from models import *

def main():#Función principal con menú para la tienda de videojuegos
    
    conexion = Conectar_bd() 
    if conexion is None:
        print("No se pudo conectar a la base de datos. El programa se cerrará.")
        return 
    try:
        usuario_activo = Login(conexion)
        if usuario_activo is None:
            return
        #Menu principal + opciones del usuario
        while True:
            print("\n--- Menú Principal ---")
            print("1. Mostrar productos")
            print("2. Buscar producto")
            print("3. Agregar producto")
            print("4. Actualizar producto")
            print("5. Eliminar producto")
            print("6. Mostrar usuarios")
            print("7. Buscar usuario")
            print("8. Agregar usuario")
            print("9. Eliminar usuario")
            print("10. Cerrar sesión")
            
            opcion = input("Seleccione una opción: ")
            
            if opcion == '1':
                productos = Mostrar_productos(conexion)
                if productos:
                    for p in productos:
                        print(f" Produto: {p['nombre']}\n Categoria: {p['categoria']}\n Precio(mxn): ${p['precio']:.2f}\n Descripcion: {p['descripcion']}\n Stock:{p['stock']}")
                else:
                    print("No se encontraron productos.")
            elif opcion == '2':
                nombre_producto = input("Ingrese el nombre del producto a buscar: ")
                productos = Buscar_producto(conexion, nombre_producto)
                if productos:
                    for p in productos:
                        print(f" Produto: {p['nombre']}\n Categoria: {p['categoria']}\n Precio(mxn): ${p['precio']:.2f}\n Descripcion: {p['descripcion']}\n Stock:{p['stock']}")
                else:
                    print("No se encontraron productos con ese nombre.")
            elif opcion == '3':
                Agregar_producto(conexion, usuario_activo)
            elif opcion == '4':
                Actualizar_producto(conexion, usuario_activo)
            elif opcion == '5':
                Eliminar_producto(conexion, usuario_activo)
            elif opcion == '6':
                Mostrar_usuarios(conexion, usuario_activo)
            elif opcion == '7':
                nombre_usuario = input("Ingrese el nombre de usuario a buscar: ")
                Buscar_usuario(conexion, nombre_usuario)
            elif opcion == '8':
                Agregar_usuario(conexion, usuario_activo)
            elif opcion == '9':
                Eliminar_usuario(conexion, usuario_activo)
            elif opcion == '10':
                Logout()
                break
            else:
                print("Opción no válida. Por favor, seleccione una opción del 1 al 10.")
        
        
    finally:
        conexion.close() #Cerramos la conexión a la base de datos al finalizar el programa
if __name__ == "__main__":
    main()  #Llamada a la función principal para iniciar el programa
