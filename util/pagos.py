#==============================================================================
#                   MÓDULO DE PAGOS Y BILLETERA
#==============================================================================
# Módulo para manejar billetera digital, consulta de saldo, depósitos y pagos
# También gestiona el histórico de pedidos del usuario
#==============================================================================

#Libreria para manejar bases de datos
import psycopg2
#Libreria para convertir valores decimales de la BD
from decimal import Decimal
#Importación de funciones del módulo carrito
from util import Verificar_carrito, Obtener_productos_carrito


#==============================================================================
#                          FUNCIONES DE BILLETERA
#==============================================================================
#Función para verificar o crear billetera
def Verificar_billetera(conexion, usuario_activo):
    """
    Verifica si el usuario tiene una billetera
    Si no existe, crea una nueva con saldo 0 y la retorna
    Retorna: Tupla (id_billetera, saldo)
    """
    try:
        cursor = conexion.cursor()
        #consultamos si existe billetera para el usuario
        cursor.execute("""
                    SELECT id_billetera, saldo
                    FROM billeteras
                    WHERE id_usuario = %s
                    """, (usuario_activo["id_usuario"],))
        
        saldo_cliente = cursor.fetchone()
        
        if saldo_cliente is None:
            #creamos una nueva billetera si no existe
            cursor.execute("""
                INSERT INTO billeteras (id_usuario, saldo)
                VALUES (%s, 0.00)
                RETURNING id_billetera, saldo
            """, (usuario_activo["id_usuario"],))
            saldo_cliente = cursor.fetchone()
            conexion.commit()
        
        return saldo_cliente

    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al verificar o crear la billetera: {e}") 
        return None


#Función para obtener saldo
def Obtener_saldo(conexion, usuario_activo):
    """
    Obtiene el saldo actual de la billetera del usuario
    Retorna: Tupla (id_billetera, saldo)
    """
    
    try:
        saldo_cliente = Verificar_billetera(conexion, usuario_activo)
        return saldo_cliente

    except psycopg2.Error as e:
        print(f"Error al obtener la billetera. {e}") 
        return None           


#Función para consultar saldo
def Consultar_saldo(conexion, usuario_activo):
    """
    Muestra el saldo actual de la billetera del usuario
    """
    
    try:
        saldo_cliente = Verificar_billetera(conexion, usuario_activo)
        
        if saldo_cliente is None:
            print("No hay dinero en tu cuenta.")
            return None
            
        print(f"Hola {usuario_activo['nombre_usuario']}, \nTu saldo actual es de: {saldo_cliente[1]}")
        input("Precione cualquier tecla para continuar.")
        return
        
    except psycopg2.Error as e:
        print(f"Ocurrio un error al mostrar tu saldo {e}")
        return


#Función para depositar dinero
def Depositar_saldo(conexion, usuario_activo):
    """
    Permite al usuario depositar dinero en su billetera
    Validación: el monto debe ser mayor que 0
    """
    
    try:
        saldo_cliente = Verificar_billetera(conexion, usuario_activo)
        if saldo_cliente is None:
            print("No se pudo obtener o crear la billetera para depositar saldo.")
            return
            
        cursor = conexion.cursor()
        
        try:
            
            #solicitamos el monto a depositar
            deposito = float(input("¿Cuánto dinero desea ingresar a su cuenta?"))
            
            if deposito <= 0:
                print("El saldo ingresado debe ser mayor que 0")
                return
                
        except:
            
            print("Por favor ingresa un numero valido")
            return
        
        #actualizamos el saldo en la BD
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


#==============================================================================
#                          FUNCIONES DE PAGO
#==============================================================================

#Función para pagar el carrito
def  Pagar_carrito(usuario_activo, conexion):
    """
    Realiza el pago del carrito del usuario
    Crea un pedido, verifica saldo, descuenta del carrito y actualiza stock
    """
    
    try:

        
        cursor = conexion.cursor()
        
        id_usuario = usuario_activo["id_usuario"]
        #verificamos el carrito del usuario
        id_carrito = Verificar_carrito(conexion, id_usuario)
        #obtenemos los productos del carrito
        objetos_carrito = Obtener_productos_carrito(conexion, id_carrito)
        total = Decimal('0.00')
        
        if not objetos_carrito:
            print("El carrito esta vacío.")
            return
        
        #calculamos el total
        for producto in objetos_carrito:
            total += producto["subtotal"]
        
        #verificamos que el usuario tenga saldo suficiente
        saldo_cliente = Obtener_saldo(conexion, usuario_activo)
        
        if saldo_cliente is None:
            print("No hay dinero en tu cartera digital.")
            return

        saldo = saldo_cliente[1]

        if saldo < total:
            print("Saldo insuficiente.")
            return
        
        #creamos el pedido en la BD
        cursor.execute("""
            INSERT INTO pedidos (id_usuario, total)
            VALUES (%s, %s)
            RETURNING id_pedido
            """, (id_usuario, total))

        id_pedido = cursor.fetchone()[0]
        
        #insertamos los detalles de cada producto del pedido
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
            
        #actualizamos el stock de cada producto
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
        
        #descontamos del saldo de la billetera    
        cursor.execute("""
                    UPDATE billeteras
                    SET saldo = saldo - %s
                    WHERE id_usuario = %s
                """, (total, id_usuario))
        
        #registramos el pago en la BD               
        cursor.execute("""
                    INSERT INTO pagos (id_pedido, metodo_pago, monto, estado_pago)
                    VALUES (%s, 'saldo_ficticio', %s, 'aprobado')
                    """, (id_pedido, total))
        
        #actualizamos el estado del pedido a pagado
        cursor.execute("""
                    UPDATE pedidos
                    SET estado = 'pagado'
                    WHERE id_pedido = %s
                    """, (id_pedido,))

        #actualizamos el estado del carrito a comprado
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


#Función para consultar histórico de pedidos
def Consultar_historial(conexion, usuario_activo):
    """
    Muestra el historial de todos los pedidos realizados por el usuario
    Muestra: ID pedido, fecha, total y estado
    """
    try:
        cursor = conexion.cursor()
        #consultamos todos los pedidos del usuario ordenados por fecha descendente
        cursor.execute("""
            SELECT id_pedido, fecha_pedido, total, estado
            FROM pedidos
            WHERE id_usuario = %s
            ORDER BY fecha_pedido DESC
        """, (usuario_activo["id_usuario"],))
        
        pedidos = cursor.fetchall()
        
        if not pedidos:
            print("No tienes pedidos registrados en tu historial.")
            return
            
        print("="*50)
        print("               Historial de Compras")
        print("="*50)
        
        for i, pedido in enumerate(pedidos, 1):
            id_pedido, fecha, total, estado = pedido
            print(f"\nPedido #{i} | Fecha: {fecha} | Estado: {estado} | Total: ${total:.2f} (mxn)")
            print("-" * 50)
            
            cursor.execute("""
                SELECT nombre_producto, cantidad, precio_unitario
                FROM detalle_pedido
                WHERE id_pedido = %s
            """, (id_pedido,))
            
            detalles = cursor.fetchall()
            for detalle in detalles:
                nombre_prod, cantidad, precio = detalle
                subtotal = cantidad * precio
                print(f"  - {nombre_prod} | Cantidad: {cantidad} | Precio: ${precio:.2f} | Subtotal: ${subtotal:.2f}")
            print("="*50)
            
        input("Presione Enter para continuar.")
    except psycopg2.Error as e:
        print(f"Ocurrió un error al obtener tu historial de compras: {e}")



