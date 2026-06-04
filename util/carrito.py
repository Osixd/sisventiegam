import bcrypt
import psycopg2
from productos import Mostrar_productos, Buscar_producto


def Verificar_carrito(conexion, id_usuario):
    
    try:
        
        cursor = conexion.cursor()
        
        cursor.execute("""
            SELECT id_carrito FROM carrito 
            WHERE id_usuario = %s 
            AND estado = 'activo'""", (id_usuario,))
        carrito = cursor.fetchone()
        
        if carrito is not None:
            
            return carrito[0]
        
        else:
            
            cursor.execute("""
                INSERT INTO carrito (id_usuario, estado) 
                VALUES (%s, 'activo') RETURNING id_carrito""", (id_usuario,))
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

        productos_encontrados = Mostrar_productos(conexion)
        
        if not productos_encontrados:
            print("Hubo un error inesperado")
            return
        
        for p in productos_encontrados:
            
            print(f"""Produto: {p['nombre']}
                Categoria:     {p['categoria']}
                Precio(mxn):  ${p['precio']:.2f}
                Stock:         {p['stock']}""")
        
        nombre_producto = input("¿Qué producto desea agregar al carrito?(solo selecciona uno)")
        productos_encontrados = Buscar_producto(conexion, nombre_producto)
        
        if not productos_encontrados:
            print("No se encontraron productos")
            return
        
        producto = productos_encontrados[0]   
        
        try:
            cantidad = int(input("¿Cuántos quiere comprar?"))
        except ValueError:
            print("Por favor ingrese solo numeros")
            return

        if cantidad > producto["stock"]:
            
            print("No hay suficiente stock")
            return
        
        else:
            cursor.execute("""INSERT INTO detalle_carrito (id_carrito, id_producto, cantidad) 
                           VALUES (%s, %s, %s)
                           ON CONFLICT (id_carrito, id_producto)
                           DO UPDATE SET cantidad = detalle_carrito.cantidad + EXCLUDED.cantidad""",
                           (id_carrito, producto["id"], cantidad))
            conexion.commit()
            
        
    except psycopg2.Error as e:
        
        print(f"Error al agregar al carrito: {e}")
        conexion.rollback()
        


def Ver_carrito(conexion, id_usuario):
    
    try:
        cursor = conexion.cursor()

        id_carrito = Verificar_carrito(conexion, id_usuario)
        cursor.execute("""SELECT p.nombre_producto, dc.cantidad, p.precio,
                       dc.cantidad * precio AS subtotal
                       FROM detalle_carrito dc
                       JOIN productos p ON dc.id_producto = p.id_producto
                       WHERE dc.id_carrito = %s """, (id_carrito, ))
        productos = cursor.fetchall()
        
        if not productos:
            print("Tu carrito esta vacio")
            return

        total = 0
        print("----------Tu carrito----------")
        for producto in productos:
            nombre = producto[0]
            cantidad = producto[1]
            precio = producto[2]
            subtotal = producto[3]
            total += subtotal
            print(f"""
                Producto:  {nombre}
                Cantidad:  {cantidad}
                Precio:   ${precio:.2f}   (mxn)
                Subtotal: ${subtotal:.2f} (mxn)
                """)
        
        print(f"El total es: ${total:.2f} (mxn)")
        print(f"El IVA es: {total * .16}")
        
    except psycopg2.Error as e:
        
        print(f"Error al ver el carrito: {e}")