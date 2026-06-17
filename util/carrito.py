#==============================================================================
#                  MÓDULO DE GESTIÓN DE CARRITO
#==============================================================================
# Este módulo se encarga de manejar el carrito de compras del usuario
# Permite agregar, visualizar y eliminar productos del carrito
#==============================================================================

import psycopg2
from decimal import Decimal
from .productos import Mostrar_productos, Buscar_producto


#Función para verificar o crear carrito
def Verificar_carrito(conexion, id_usuario):
    """
    Verifica si el usuario tiene un carrito activo
    Si no existe, crea uno nuevo y lo retorna
    Retorna: id_carrito
    """
    
    try:
        
        cursor = conexion.cursor()
        
        #consultamos si existe un carrito activo para el usuario
        cursor.execute(""" 
                       SELECT id_carrito
                       FROM carrito 
                       WHERE id_usuario = %s 
                       AND estado = 'activo'""", 
                       (id_usuario,))
        carrito = cursor.fetchone()
        
        if carrito is not None:
            
            return carrito[0]
        
        else:
            
            #creamos un nuevo carrito si no existe
            cursor.execute("""
                           INSERT INTO carrito (id_usuario, estado) 
                           VALUES (%s, 'activo') RETURNING id_carrito""",
                           (id_usuario,))
            conexion.commit()
            nuevo_carrito = cursor.fetchone()
            return nuevo_carrito[0]
        
    except psycopg2.Error as e:
        
        print(f"Error al verificar el carrito: {e}")
        return None


#Función para agregar productos al carrito
def Agregar_al_carrito(conexion, id_carrito, id_usuario):
    """
    Agrega un producto al carrito del usuario
    Solicita cantidad y valida disponibilidad de stock
    """
    
    try:
        
        cursor = conexion.cursor()
        
        if id_carrito is None:  
            id_carrito = Verificar_carrito(conexion, id_usuario)

        #obtenemos todos los productos disponibles
        productos_encontrados = Mostrar_productos(conexion)
        
        if not productos_encontrados:
            print("Hubo un error inesperado")
            return
        
        #mostramos los productos disponibles
        for p in productos_encontrados:
            
            print(f"""Produto: {p['nombre']}
                Categoria:     {p['categoria']}
                Precio(mxn):  ${p['precio']:.2f}
                Stock:         {p['stock']}""")
        
        nombre_producto = input("¿Qué producto desea agregar al carrito?(solo selecciona uno por su nombre)")
        #buscamos el producto seleccionado
        productos_encontrados = Buscar_producto(conexion, nombre_producto)
        
        if not productos_encontrados:
            print("No se encontraron productos")
            return
        
        producto = productos_encontrados[0]   
        
        #solicitamos la cantidad
        try:
            cantidad = int(input("¿Cuántos quiere comprar?"))
        except ValueError:
            print("Por favor ingrese solo numeros")
            return

        #validamos que hay suficiente stock
        if cantidad > producto["stock"]:
            
            print("No hay suficiente stock")
            return

        #verificamos si el producto ya está en el carrito
        cursor.execute("""
                       SELECT cantidad
                       FROM detalle_carrito
                       WHERE id_carrito = %s
                       AND id_producto = %s""",
                       (id_carrito, producto["id"]))
        resultado = cursor.fetchone()
        cantidad_actual = 0
        
        if resultado is not None:
            
            cantidad_actual = resultado[0]

        #validamos stock total disponible para agregar
        if cantidad_actual + cantidad > producto["stock"]:
            
            print("No hay suficiente stock para agregar esa cantidad al carrito")
            return
        
        else:
            #agregamos o actualizamos el producto en el carrito
            cursor.execute("""
                           INSERT INTO detalle_carrito (id_carrito, id_producto, cantidad) 
                           VALUES (%s, %s, %s)
                           ON CONFLICT (id_carrito, id_producto)
                           DO UPDATE SET cantidad = detalle_carrito.cantidad + EXCLUDED.cantidad""",
                           (id_carrito, producto["id"], cantidad))
            conexion.commit()
            
        
    except psycopg2.Error as e:
        
        print(f"Error al agregar al carrito: {e}")
        conexion.rollback()
        

#Función para visualizar el carrito
def Ver_carrito(conexion, id_usuario):
    """
    Muestra todos los productos en el carrito del usuario
    Calcula y muestra el total más el IVA
    """
    
    try:
        
        id_carrito = Verificar_carrito(conexion, id_usuario)
        #obtenemos los productos del carrito
        productos = Obtener_productos_carrito(conexion, id_carrito)
        
        if not productos:
            
            print("Tu carrito esta vacio")
            return

        total = 0
        
        print("----------Tu carrito----------")
        for i, producto in enumerate(productos, 1):
            nombre = producto["nombre"]
            cantidad = producto["cantidad"]
            precio = producto["precio"]
            subtotal = producto["subtotal"]
            total += subtotal
            print(f"""{i}. Producto/servicio
Producto:  {nombre}
Cantidad:  {cantidad}
Precio:   ${precio:.2f}   (mxn)
Subtotal: ${subtotal:.2f} (mxn)
                """)
        
        print(f"El total es: ${total:.2f} (mxn)")
        print(f"El IVA es: {total * Decimal(.16):.2f}")
        
    except psycopg2.Error as e:
        
        print(f"Error al ver el carrito: {e}")


#Función para obtener productos del carrito
def Obtener_productos_carrito(conexion, id_carrito):
    """
    Obtiene todos los productos que están en el carrito
    Retorna: Lista de diccionarios con información de productos y cantidades
    """
    try:
        cursor = conexion.cursor()
        #consultamos los productos del carrito con sus cantidades y precios
        cursor.execute("""
                       SELECT p.id_producto, p.nombre_producto, dc.cantidad, p.precio, 
                       dc.cantidad * p.precio AS subtotal
                       FROM detalle_carrito dc
                       JOIN productos p ON dc.id_producto = p.id_producto
                       WHERE dc.id_carrito = %s""",
                       (id_carrito,))

        return [{
            "id": row[0],
            "nombre": row[1],
            "cantidad": row[2],
            "precio": row[3],
            "subtotal": row[4]
        } for row in cursor.fetchall()]

    except psycopg2.Error as e:
        
        print(f"Error al obtener productos del carrito: {e}")
        return None


#Función para eliminar productos del carrito
def Eliminar_del_carrito(conexion, usuario_activo, id_carrito):
    """
    Permite al usuario eliminar productos de su carrito
    Muestra opciones para seleccionar cantidad a eliminar
    """

    try:
        
        cursor = conexion.cursor()

        if id_carrito is None:

            id_carrito = Verificar_carrito(conexion, usuario_activo["id_usuario"])

        #obtenemos los productos del carrito
        productos = Obtener_productos_carrito(conexion, id_carrito)

        if not productos:
            
            print("Tu carrito esta vacio")
            return

        #mostramos los productos en el carrito
        print("----------Tu carrito----------")
        for i, producto in enumerate(productos, 1):
            print(f"""{i}. Producto/servicio
                Producto:  {producto['nombre']}
                Cantidad:  {producto['cantidad']}
                Precio:   ${producto['precio']:.2f}   (mxn)
                """)

        try:
            
            seleccion = int(input("¿Qué producto deseas quitar? "))
            
        except ValueError:
            
            print("Por favor solo ingresa numeros enteros")
            return

        if seleccion < 1 or seleccion > len(productos):
            print("Selección inválida")
            return

        producto = productos[seleccion - 1]

        try:
            
            cantidad = int(input("¿Cuántos deseas quitar del carrito? "))
            
        except ValueError:
            
            print("Por favor solo ingresa numeros enteros")
            return

        if cantidad <= 0:
            
            print("La cantidad debe ser mayor a 0")
            return

        if cantidad > producto["cantidad"]:
            
            print("No puedes quitar mas cosas de las que tienes en el carrito")
            return

        nueva_cantidad = producto["cantidad"] - cantidad

        if nueva_cantidad == 0:
            
            cursor.execute("""
                           DELETE FROM detalle_carrito
                           WHERE id_carrito = %s
                           AND id_producto = %s""",
                           (id_carrito, producto["id"]))
            
        else:
            
            cursor.execute("""
                           UPDATE detalle_carrito
                           SET cantidad = %s
                           WHERE id_carrito = %s
                           AND id_producto = %s""",
                           (nueva_cantidad, id_carrito, producto["id"]))

        conexion.commit()
        print("Carrito actualizado")

    except psycopg2.Error as e:
        
        print(f"Error al eliminar del carrito: {e}")
        conexion.rollback()
