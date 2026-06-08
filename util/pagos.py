import psycopg2
from util import *



def Obtener_saldo(conexion, usuario_activo):
    
    try:
        
        cursor = conexion.cursor()
        cursor.execute("""
                    SELECT id_billetera, saldo
                    FROM billeteras
                    WHERE id_usuario = %s
                    """, (usuario_activo["id_usuario"],))
        
        saldo_cliente = cursor.fetchone()
        
        if saldo_cliente is None:
            print("No hay dinero en tu cuenta.")
            return None

        return saldo_cliente

    except psycopg2.Error as e:
        print(f"Error al obtener la billetera. {e}") 
        return None           



def Consultar_saldo(conexion, usuario_activo):
    
    try:
    
        cursor = conexion.cursor()
        cursor.execute("""
                       SELECT id_billetera, saldo
                       FROM billeteras
                       WHERE id_usuario = %s
                       """, (usuario_activo["id_usuario"],))
        saldo_cliente = cursor.fetchone()
        
        if saldo_cliente is None:
            print("No hay dinero en tu cuenta.")
            return None
            
        
        print(f"Hola {usuario_activo['nombre_usuario']}, \nTu saldo actual es de: {saldo_cliente[1]}")
        input("Precione cualquier tecla para continuar.")
        return
        
        
    except psycopg2.Error as e:
        print(f"Ocurrio un error al mostrar tu saldo {e}")
        return



def Depositar_saldo(conexion, usuario_activo):
    
    try:
        cursor = conexion.cursor()
        
        try:
            
            deposito = float(input("¿Cuánto dinero desea ingresar a su cuenta?"))
            
            if deposito <= 0:
                print("El saldo ingresado debe ser mayor que 0")
                return
                
        except:
            
            print("Por favor ingresa un numero valido")
            return
        
        cursor.execute("""
                       UPDATE billeteras
                       SET saldo = saldo +  %s
                       WHERE id_usuario = %s
                       """, (deposito, usuario_activo["id_usuario"]))
        conexion.commit()
        print("Saldo actualizado satisfactoriamente")
    
    except psycopg2.Error as e:
        print(f"Ocurrio un error al depositar a tu saldo. {e}")
        return



def  Pagar_carrito(usuario_activo, conexion):
    
    try:
        
        cursor = conexion.cursor()
        
        id_usuario = usuario_activo["id_usuario"]
        id_carrito = Verificar_carrito(conexion, id_usuario)
        objetos_carrito = Obtener_productos_carrito(conexion, id_carrito)
        total = 0.00
        
        if not objetos_carrito:
            print("El carrito esta vacío.")
            return
        
        for producto in objetos_carrito:
            total += producto["subtotal"]
        
        saldo_cliente = Obtener_saldo(conexion, usuario_activo)
        
        if saldo_cliente is None:
            print("No hay dinero en tu cartera digital.")
            return

        saldo = saldo_cliente[1]

        if saldo < total:
            print("Saldo insuficiente.")
            return
        
        cursor.execute("""
            INSERT INTO pedidos (id_usuario, total)
            VALUES (%s, %s)
            RETURNING id_pedido
            """, (id_usuario, total))

        id_pedido = cursor.fetchone()[0]
        
        for producto in objetos_carrito: 
            
            cursor.execute("""
                INSERT INTO detalle_pedido (
                    id_pedido,
                    id_producto,
                    nombre_producto,
                    cantidad,
                    precio_unitario
                )
                VALUES (%s, %s, %s, %s, %s)
                """, (
                id_pedido,
                producto["id"],
                producto["nombre"],
                producto["cantidad"],
                producto["precio"]
                ))
            
        for producto in objetos_carrito:
            cursor.execute("""
                    UPDATE productos
                    SET stock = stock - %s
                    WHERE id_producto = %s AND stock >= %s
                    """, (producto["cantidad"], producto["id"], producto["cantidad"]))
        
            if cursor.rowcount == 0:
                print("No hay stock suficiente para completar la compra.")
                conexion.rollback()
                return
        
            
        cursor.execute("""
                    UPDATE billeteras
                    SET saldo = saldo - %s
                    WHERE id_usuario = %s
                """, (total, id_usuario))
                        
        cursor.execute("""
                    INSERT INTO pagos (id_pedido, metodo_pago, monto, estado_pago)
                    VALUES (%s, 'saldo_ficticio', %s, 'aprobado')
                    """, (id_pedido, total))
        
        cursor.execute("""
                    UPDATE pedidos
                    SET estado = 'pagado'
                    WHERE id_pedido = %s
                    """, (id_pedido,))

        cursor.execute("""
                    UPDATE carrito
                    SET estado = 'comprado'
                    WHERE id_carrito = %s
                    """, (id_carrito,))
        
        conexion.commit()
        print("Pago realizado correctamente")
        
    except psycopg2.Error as e:
        print(f"Ocurrio un error al pagar el carrito. {e}")
        conexion.rollback()
        return


