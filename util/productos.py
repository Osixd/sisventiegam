#==============================================================================
#                  MÓDULO DE GESTIÓN DE PRODUCTOS
#==============================================================================
# Este módulo se encarga de CRUD de productos (crear, leer, actualizar, eliminar)
# Solo administradores pueden agregar, actualizar y eliminar productos
#==============================================================================

import psycopg2
import bcrypt
import getpass


#Función para mostrar todos los productos
def Mostrar_productos(conexion):
    """
    Obtiene y retorna todos los productos disponibles con su información
    Retorna: Lista de diccionarios con datos de productos
    """
    
    try:
        
        cursor = conexion.cursor()
        
        #consultamos todos los productos con su categoría
        cursor.execute("""
                       SELECT p.nombre_producto, c.nombre_categoria, p.precio, p.stock, p.descripcion_producto
                       FROM productos p
                       JOIN categorias c ON p.id_categoria = c.id_categoria """)
        datos_producto = cursor.fetchall()
        
        #convertimos los resultados en una lista de diccionarios
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


#Función para buscar un producto específico
def Buscar_producto(conexion, nombre_producto):
    """
    Busca productos por nombre usando búsqueda parcial (ILIKE)
    Retorna: Lista de diccionarios con productos encontrados
    """
    
    try:
        
        cursor = conexion.cursor()
        
        #consultamos productos con búsqueda parcial (insensible a mayúsculas)
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
    

#Función para agregar un nuevo producto (solo admin)
def Agregar_producto(conexion, usuario_activo):
    """
    Agrega un nuevo producto al sistema (solo admin)
    Solicita datos del producto y lo inserta en la BD
    """
    
    try:
        
        permisos = usuario_activo["permisos"]
        
        #verificamos que sea admin
        if permisos == 'admin':
            
            cursor = conexion.cursor()
            
            nombre_producto = input("Ingrese el nombre del producto: ")
            #obtenemos las categorías disponibles
            cursor.execute("SELECT nombre_categoria FROM categorias")
            categorias = cursor.fetchall()
            
            if categorias is None: 
                
                print("Categoria no encontrada.")
                return
            
            #mostramos las categorías disponibles
            for i, cat in enumerate(categorias, 1):
                
                print(f"{i}. {cat[0]}")
                
            categoria = input("Selecciona la categoría: ")
            #obtenemos el id de la categoría seleccionada
            cursor.execute("""
                           SELECT id_categoria 
                           FROM categorias 
                           WHERE nombre_categoria = %s""",
                           (categoria,))
            id_categoria = cursor.fetchone()
            
            if id_categoria is None:
                
                print("Categoría no encontrada.")
                return
            
            plataforma = input("Ingrese la plataforma del producto: ")
            descripcion = input("Ingrese la descripción del producto: ")
            precio = float(input("Ingrese el precio del producto: "))
            stock = int(input("Ingrese el stock del producto: "))
            #insertamos el nuevo producto en la BD
            cursor.execute("""
                           INSERT INTO productos (nombre_producto, id_categoria, plataforma, descripcion_producto, precio, stock)
                           VALUES (%s, %s, %s, %s, %s, %s)""", 
                           (nombre_producto, id_categoria[0], plataforma, descripcion, precio, stock))
            conexion.commit()
            print("Producto agregado exitosamente.")
            
        else:
            
            print("No tienes permiso para esto.")
            return
        
    except psycopg2.Error as e:
        
        conexion.rollback()
        print(f"Error al agregar el producto: {e}")
        
        
#Función para actualizar un producto (solo admin)
def Actualizar_producto(conexion, usuario_activo):
    """
    Permite actualizar los datos de un producto existente (solo admin)
    Requiere confirmación de contraseña por seguridad
    """
    
    try:
        
        cursor = conexion.cursor()
        
        #verificamos la identidad del admin solicitando su contraseña
        cursor.execute("""
                       SELECT contrasena
                       FROM usuarios 
                       WHERE nombre_usuario = %s""",
                       (usuario_activo["nombre_usuario"],))        
        resultado = cursor.fetchone()     
        contrasena_confirmacion = getpass.getpass("Por seguridad, vuelva a ingresar su contraseña: ")   

        if not bcrypt.checkpw(contrasena_confirmacion.encode('utf-8'), resultado[0].encode('utf-8')):
            
            print("Contraseña incorrecta.")
            return    

        #validamos que sea admin
        if usuario_activo["permisos"]== 'admin':
            
            nombre_producto = input("Ingrese el nombre del producto a actualizar: ")
            #buscamos el producto en la BD
            cursor.execute("""
                           SELECT id_producto 
                           FROM productos 
                           WHERE nombre_producto = %s""",
                           (nombre_producto, ))    
            resultado = cursor.fetchone()
            print(f"Producto encontrado: {resultado}")
            confirmacion = input("¿Desea actualizar este producto? (s/n): ")
            
            if confirmacion.lower() in ['s', 'sí', 'si']:
                
                #solicitamos qué dato actualizar
                dato_cambiar = input("Ingrese el dato que desea actualizar \n(nombre/categoria/plataforma/descripcion/precio/stock): ")
                
                if dato_cambiar.lower() == "nombre":
                    
                    nuevo_nombre = input("Ingrese el nuevo nombre del producto: ")
                    cursor.execute(f"""
                                   UPDATE productos SET nombre_producto = %s 
                                   WHERE nombre_producto = %s""", 
                                   (nuevo_nombre,nombre_producto))
                    
                elif dato_cambiar.lower() == "categoria":
                    
                    #mostramos categorías disponibles
                    cursor.execute("""
                                   SELECT nombre_categoria 
                                   FROM categorias""")
                    categorias = cursor.fetchall()
                    
                    for i, cat in enumerate(categorias, 1):
                        
                        print(f"{i}. {cat[0]}")
                    nueva_categoria = input("Ingrese la nueva categoría del producto: ")
                    #obtenemos el id de la nueva categoría
                    cursor.execute("""
                                   SELECT id_categoria 
                                   FROM categorias 
                                   WHERE nombre_categoria = %s""",
                                   (nueva_categoria,))
                    id_categoria = cursor.fetchone()
                    
                    if id_categoria is None:
                        
                        print("Categoria no encontrada.")
                        return
                    
                    cursor.execute(f"""
                                   UPDATE productos SET id_categoria = %s 
                                   WHERE nombre_producto = %s""", 
                                   (id_categoria[0],nombre_producto))
                    
                elif dato_cambiar.lower() == "plataforma":
                    
                    nueva_plataforma = input("Ingrese la nueva plataforma del producto: ")
                    cursor.execute(f"""
                                   UPDATE productos SET plataforma = %s
                                   WHERE nombre_producto = %s""", 
                                   (nueva_plataforma,nombre_producto))
                    
                elif dato_cambiar.lower() == "descripcion":
                    
                    nueva_descripcion = input("Ingrese la nueva descripción del producto: ")
                    cursor.execute(f"""
                                   UPDATE productos SET descripcion_producto = %s
                                   WHERE nombre_producto = %s""", 
                                   (nueva_descripcion,nombre_producto))
                    
                elif dato_cambiar.lower() == "precio":
                    
                    nuevo_precio = input("Ingrese el nuevo precio del producto: ")
                    cursor.execute(f"""
                                   UPDATE productos SET precio = %s 
                                   WHERE nombre_producto = %s""", 
                                   (nuevo_precio,nombre_producto))
                    
                elif dato_cambiar.lower() == "stock":
                    
                    nuevo_stock = input("Ingrese el nuevo stock del producto: ")
                    cursor.execute(f"""
                                   UPDATE productos SET stock = %s 
                                   WHERE nombre_producto = %s""", 
                                   (nuevo_stock,nombre_producto))
                    
                else:
                    
                    print("Opción inválida.")
                    return
                
                conexion.commit()
                print("Producto actualizado exitosamente.")
            
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al actualizar el producto: {e}")



#Función para eliminar un producto (solo admin)
def Eliminar_producto(conexion, usuario_activo):
    """
    Elimina un producto del sistema (solo admin)
    Requiere confirmación de contraseña por seguridad
    """
    
    try:
        
        cursor = conexion.cursor()
        #verificamos la identidad del admin solicitando su contraseña
        cursor.execute("""
                       SELECT contrasena 
                       FROM usuarios
                       WHERE nombre_usuario = %s""",
                       (usuario_activo["nombre_usuario"],))        
        resultado = cursor.fetchone()
        contrasena_confirmacion = getpass.getpass("Por seguridad, vuelve a ingresar su contraseña: ")   

        if not bcrypt.checkpw(contrasena_confirmacion.encode('utf-8'), resultado[0].encode('utf-8')):
            
            print("Contraseña incorrecta.")
            return    

        #validamos que sea admin
        if usuario_activo["permisos"] == 'admin':
            
            nombre_producto = input("Ingrese el nombre del producto a eliminar: ")
            #buscamos el producto en la BD
            cursor.execute("""
                           SELECT id_producto
                           FROM productos 
                           WHERE nombre_producto = %s""",
                           (nombre_producto, ))    
            resultado = cursor.fetchone()
            
            if resultado is None:
                
                print("Producto no encontrado.")
                return
            
            print(f"Producto encontrado: {resultado}")
            confirmacion = input("¿Desea eliminar este producto? (s/n): ")
            
            if confirmacion.lower() in ['s', 'sí', 'si']:
                cursor.execute(f"""
                               DELETE FROM productos 
                               WHERE nombre_producto = %s""",
                               (nombre_producto,))
                conexion.commit()
                print("Producto eliminado exitosamente.")
            
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al eliminar el producto: {e}")