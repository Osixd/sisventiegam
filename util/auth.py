#==============================================================================
#                     MÓDULO DE AUTENTICACIÓN
#==============================================================================
# Este módulo se encarga de manejar login, logout y verificación de permisos
# Utiliza bcrypt para encriptación de contraseñas
#==============================================================================

import bcrypt
import getpass


#Función para iniciar sesión
def Login(conexion):
    """
    Permite a un usuario iniciar sesión en el sistema
    Retorna: Un diccionario con datos del usuario o None si falla
    """
    
    #número de intentos permitidos
    intentos = 3
    cursor = conexion.cursor()
    
    while intentos > 0:    
        
        try:
            
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            #solicitamos la contraseña sin mostrar en pantalla
            contrasena = getpass.getpass("Ingrese su contraseña: ")
            #consultamos en la BD si existe el usuario
            cursor.execute("""
                           SELECT contrasena, id_usuario, permisos 
                           FROM usuarios 
                           WHERE nombre_usuario = %s""", 
                           (nombre_usuario,))
            resultado = cursor.fetchone()
            
            #verificamos la contraseña encriptada con bcrypt
            if resultado is not None and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[0].encode('utf-8')):
                
                print("Inicio de sesión exitoso.")
                #retornamos los datos del usuario autenticado
                return {
                    "nombre_usuario": nombre_usuario,
                    "id_usuario": resultado[1],
                    "permisos": resultado[2]
                }
            
            else:
                
                intentos -= 1
                print("Nombre de usuario o contraseña incorrectos.")
                
                if intentos > 0:
                    
                    print(f"Te quedan {intentos} intento(s).")
                    
                else:
                    
                    print("Has agotado tus intentos. Por favor, inténtalo de nuevo más tarde.")
                    return None
                
        except Exception as e:
            
            print(f"Error al iniciar sesión: {e}")
            return None


#Función para cerrar sesión
def Logout():
    """
    Realiza el logout del usuario mostrando un mensaje de confirmación
    """
    
    print("Has cerrado sesión exitosamente.")
    return None

#Función para verificar permisos (obsoleta)
def Verificar_permisos(conexion, usuario):
    """
    Verifica los permisos de un usuario en la BD
    Nota: Esta función se utilizaba antes y ahora es innecesaria ya que se integró en Login
    """
    
    try:
        
        cursor = conexion.cursor()
        #consultamos el nivel de permisos del usuario
        cursor.execute("""
                       SELECT permisos 
                       FROM usuarios 
                       WHERE nombre_usuario = %s""",
                       (usuario,))
        resultado = cursor.fetchone()
        
        if resultado:
            
            return resultado[0]
        
        else:
            
            print("Usuario no encontrado.")
            return None
        
    except Exception as e:
        
        print(f"Error al verificar permisos: {e}")
        return None