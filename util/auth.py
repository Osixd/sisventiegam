import bcrypt
import getpass

def Login(conexion):
    
    intentos = 3
    cursor = conexion.cursor()
    
    while intentos > 0:    
        
        try:
            
            nombre_usuario = input("Ingrese su nombre de usuario: ")
            contrasena = getpass.getpass("Ingrese su contraseña: ")
            cursor.execute("""
                            SELECT contrasena, id_usuario, permisos 
                            FROM usuarios 
                            WHERE nombre_usuario = %s
                            """, (nombre_usuario,))
            resultado = cursor.fetchone()
            
            if resultado is not None and bcrypt.checkpw(contrasena.encode('utf-8'), resultado[0].encode('utf-8')):
                
                print("Inicio de sesión exitoso.")
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
        

def Logout():
    
    print("Has cerrado sesión exitosamente.")
    return None

def Verificar_permisos(conexion, usuario): #Esta funcion se utilizaba antes, despues se volvio inutil.
    
    try:
        
        cursor = conexion.cursor()
        cursor.execute("SELECT permisos FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        
        if resultado:
            
            return resultado[0]
        
        else:
            
            print("Usuario no encontrado.")
            return None
        
    except Exception as e:
        
        print(f"Error al verificar permisos: {e}")
        return None