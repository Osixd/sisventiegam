import psycopg2
import bcrypt
import getpass
from .auth import Verificar_permisos


def Mostrar_productos(conexion):
    
    try:
        
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT p.nombre_producto, c.nombre_categoria, p.precio, p.stock, p.descripcion_producto
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria """)
        datos_producto = cursor.fetchall()
        return [{
            'nombre': row[0],
            'categoria': row[1],
            'precio': row[2],
            'stock': row[3],
            'descripcion': row[4]
        } for row in datos_producto]
    
    except psycopg2.Error as e:
        
        print(f"Error al mostrar los productos: {e}")
        return None


def Buscar_producto(conexion, nombre_producto):
    
    try:
        
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT p.nombre_producto, c.nombre_categoria, p.precio, p.id_producto, p.stock
            FROM productos p
            JOIN categorias c ON p.id_categoria = c.id_categoria
            WHERE p.nombre_producto ILIKE %s""", (f"%{nombre_producto}%",))
        datos_producto = cursor.fetchall()
        
        return [{
                'nombre': row[0],
                'categoria': row[1],
                'precio': row[2],
                'id': row[3],
                'stock': row[4]
                }
                for row in datos_producto
                 ]
    
    except psycopg2.Error as e:
        
        print(f"Error al buscar el producto: {e}")
        return None
    

def Agregar_producto(conexion, usuario_activo):
    
    try:
        
        permisos = usuario_activo["permisos"]
        
        if permisos == 'admin':
            
            cursor = conexion.cursor()
            
            nombre_producto = input("Ingrese el nombre del producto: ")
            cursor.execute("SELECT nombre_categoria FROM categorias")
            categorias = cursor.fetchall()
            
            if categorias is None: 
                
                print("Categoria no encontrada.")
                return
            
            for i, cat in enumerate(categorias, 1):
                
                print(f"{i}. {cat[0]}")
                
            categoria = input("Selecciona la categoría: ")
            cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = %s", (categoria,))
            id_categoria = cursor.fetchone()
            
            if id_categoria is None:
                
                print("Categoría no encontrada.")
                return
            
            plataforma = input("Ingrese la plataforma del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            stock = int(input("Ingrese el stock del producto: "))
            cursor.execute("""
                INSERT INTO productos (nombre_producto, id_categoria, plataforma, descripcion_producto, precio, stock)
                VALUES (%s, %s, %s, %s, %s, %s)""", (nombre_producto, id_categoria[0], plataforma, descripcion, precio, stock))
            
            conexion.commit()
            
            print("Producto agregado exitosamente.")
            
        else:
            
            print("No tienes permiso para esto.")
            return
        
    except psycopg2.Error as e:
        
        conexion.rollback()
        print(f"Error al agregar el producto: {e}")
        
        
def Actualizar_producto(conexion,):
    
    try:
        
        cursor = conexion.cursor()
        
        print("Por seguridad, se volveran a pedir las credenciales del usuario.")
        admin = input("Ingrese su nombre de usuario: ")
        cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (admin,))        
        resultado = cursor.fetchone()
        permisos = Verificar_permisos(conexion, admin)        
        contrasena_confirmacion = getpass.getpass("Ingrese su contraseña: ")   

        if not bcrypt.checkpw(contrasena_confirmacion.encode('utf-8'), resultado[0].encode('utf-8')):
            
            print("Contraseña incorrecta.")
            return    

        if permisos == 'admin':
            
            nombre_producto = input("Ingrese el nombre del producto a actualizar: ")
            cursor.execute("SELECT id_producto FROM productos WHERE nombre_producto = %s", (nombre_producto, ))    
            resultado = cursor.fetchone()
            print(f"Producto encontrado: {resultado}")
            confirmacion = input("¿Desea actualizar este producto? (s/n): ")
            
            if confirmacion.lower() in ['s', 'sí', 'si']:
                
                dato_cambiar = input("Ingrese el dato que desea actualizar \n(nombre/categoria/plataforma/descripcion/precio/stock): ")
                
                if dato_cambiar.lower() == "nombre":
                    
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    cursor.execute(f"UPDATE productos SET nombre_producto = %s WHERE nombre_producto = %s", (nuevo_nombre,nombre_producto))
                    
                elif dato_cambiar.lower() == "categoria":
                    
                    cursor.execute("SELECT nombre_categoria FROM categorias")
                    categorias = cursor.fetchall()
                    
                    for i, cat in enumerate(categorias, 1):
                        
                        print(f"{i}. {cat[0]}")
                    nueva_categoria = input("Ingrese la nueva categoría del producto: ")
                    cursor.execute("SELECT id_categoria FROM categorias WHERE nombre_categoria = %s", (nueva_categoria,))
                    id_categoria = cursor.fetchone()
                    
                    if id_categoria is None:
                        
                        print("Categoria no encontrada.")
                        return
                    
                    cursor.execute(f"UPDATE productos SET id_categoria = %s WHERE nombre_producto = %s", (id_categoria[0],nombre_producto))
                    
                elif dato_cambiar.lower() == "plataforma":
                    
                    nueva_plataforma = input("Ingrese la nueva plataforma del producto: ")
                    cursor.execute(f"UPDATE productos SET plataforma = %s WHERE nombre_producto = %s", (nueva_plataforma,nombre_producto))
                    
                elif dato_cambiar.lower() == "descripcion":
                    
                    nueva_descripcion = input("Ingrese la nueva descripción del producto: ")
                    cursor.execute(f"UPDATE productos SET descripcion_producto = %s WHERE nombre_producto = %s", (nueva_descripcion,nombre_producto))
                    
                elif dato_cambiar.lower() == "precio":
                    
                    nuevo_precio = input("Ingrese el nuevo precio del producto: ")
                    cursor.execute(f"UPDATE productos SET precio = %s WHERE nombre_producto = %s", (nuevo_precio,nombre_producto))
                    
                elif dato_cambiar.lower() == "stock":
                    
                    nuevo_stock = input("Ingrese el nuevo stock del producto: ")
                    cursor.execute(f"UPDATE productos SET stock = %s WHERE nombre_producto = %s", (nuevo_stock,nombre_producto))
                    
                else:
                    
                    print("Opción inválida.")
                    return
                
                conexion.commit()
                print("Producto actualizado exitosamente.")
            
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al actualizar el producto: {e}")
        
        
def Eliminar_producto(conexion):
    try:
        cursor = conexion.cursor()
        print("Por seguridad, se volveran a pedir las credenciales del usuario.")
        admin = input("Ingrese su nombre de usuario: ")
        cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (admin,))        
        resultado = cursor.fetchone()
        permisos = Verificar_permisos(conexion, admin)        
        contrasena_confirmacion = getpass.getpass("Ingrese su contraseña: ")   

        if not bcrypt.checkpw(contrasena_confirmacion.encode('utf-8'), resultado[0].encode('utf-8')):
            print("Contraseña incorrecta.")
            return    

        if permisos == 'admin':
            nombre_producto = input("Ingrese el nombre del producto a eliminar: ")
            cursor.execute("SELECT id_producto FROM productos WHERE nombre_producto = %s", (nombre_producto, ))    
            resultado = cursor.fetchone()
            if resultado is None:
                print("Producto no encontrado.")
                return
            print(f"Producto encontrado: {resultado}")
            confirmacion = input("¿Desea eliminar este producto? (s/n): ")
            if confirmacion.lower() in ['s', 'sí', 'si']:
                cursor.execute(f"DELETE FROM productos WHERE nombre_producto = %s", (nombre_producto,))
                conexion.commit()
                print("Producto eliminado exitosamente.")
            
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al eliminar el producto: {e}")