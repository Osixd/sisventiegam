import bcrypt
import psycopg2
from .productos import Mostrar_productos, Buscar_producto

def Verificar_carrito(conexion, id_usuario):
    
    try:
        
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id_carrito FROM carrito WHERE id_usuario = %s AND estado = 'activo'""", (id_usuario,))
        carrito = cursor.fetchone()
        
        if carrito is not None:
            
            return carrito[0]
        
        else:
            
            cursor.execute("""
                INSERT INTO carrito (id_usuario, estado) VALUES (%s, 'activo') RETURNING id_carrito""", (id_usuario,))
            conexion.commit()
            nuevo_carrito = cursor.fetchone()
            return nuevo_carrito[0]
        
    except psycopg2.Error as e:
        
        print(f"Error al verificar el carrito: {e}")
        return None
    
    
def Agregar_al_carrito(conexion, id_carrito, id_usuario):
    
    try:
        
        cursor = conexion.cursor()
        
        if id_carrito is None:  
            id_carrito = Verificar_carrito(conexion, id_usuario)

        productos = Mostrar_productos(conexion)
        for p in productos:
            print(f" Produto: {p['nombre']}\n Categoria: {p['categoria']}\n Precio(mxn): ${p['precio']:.2f}\n Stock:{p['stock']}")
        
        nombre_producto = input("¿Qué producto desea agregar al carrito?(solo selecciona 1)")
        id_producto = Buscar_producto(conexion, nombre_producto)
        cantidad = int(input("¿Cuántos quiere comprar?"))
        
        if cantidad > nombre_producto['stock']:
            
            print("No hay suficiente stock")
            return
        
        else:
            cursor.execute("INSERT INTO detalle_carrito (id_carrito, id_producto, cantidad) VALUES (%s, %s, %s)",
                           (id_carrito, id_producto[0]["id"], cantidad))
            conexion.commit()
            
        
    except psycopg2.Error as e:
        
        print(f"Error al agregar al carrito: {e}")