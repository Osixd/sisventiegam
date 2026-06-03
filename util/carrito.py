import bcrypt
import psycopg2
from .auth import Verificar_permisos
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
    
    
def Agregar_al_carrito(conexion, id_carrito, ):
    
    try:
        
        cursor = conexion.cursor()
        

        if producto:
            

        
            
    except psycopg2.Error as e:
        
        print(f"Error al agregar al carrito: {e}")