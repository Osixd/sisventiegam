import bcrypt
import psycopg2
import getpass
from .auth import Verificar_permisos

def Mostrar_usuarios(conexion, usuario):
    try:
        cursor = conexion.cursor()
        permisos = Verificar_permisos(conexion, usuario)
        if permisos == 'admin':
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        else:
            print("No tienes permiso para ver esto.")
    except psycopg2.Error as e:
        print(f"Error al mostrar los usuarios: {e}")

def Buscar_usuario(conexion, usuario):
    if not usuario:
        print("No se ha ingresado un nombre de usuario.")
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario,))
        resultado = cursor.fetchone()
        
        if resultado is None:
            print("Usuario no encontrado.")
            interactuar = input("¿Deseas agregar un nuevo usuario? (si/no) ")
            
            if interactuar.lower() in ['si', 'sí', 's']:
                Agregar_usuario(conexion)
            return
        else:
            print(f"Usuario encontrado: {resultado}")
            
    except psycopg2.Error as e:
        print(f"Error al buscar el usuario: {e}")
        return



def Agregar_usuario(conexion):
    try:
        cursor = conexion.cursor()

        while True:
            NombreUsuario = input("Ingrese el nombre de usuario: ")
            cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (NombreUsuario,))
            if cursor.fetchone():
                print("El nombre de usuario ya existe, intente otro.")
            else:
                break  

        while True:
            Correo = input("Ingrese el correo electrónico: ")
            cursor.execute("SELECT * FROM usuarios WHERE correo = %s", (Correo,))
            if cursor.fetchone():
                print("El correo ya está registrado, intente otro.")
            else:
                break

        while True:
            Contrasena = getpass.getpass("Ingrese la contraseña: ")
            contrasena_encriptada = bcrypt.hashpw(Contrasena.encode('utf-8'), 
                                                bcrypt.gensalt()
                                                ).decode('utf-8')
            contrasena_confirmacion = getpass.getpass("Confirme la contraseña: ")
            if Contrasena != contrasena_confirmacion:
                print("Las contraseñas no coinciden, intente nuevamente.")
            else: 
                break
            
        Nombres = input("Ingrese su nombre(s): ")
        Apellido_paterno = input("Ingrese su apellido paterno: ")
        Apellido_materno = input("Ingrese su apellido materno: ")
        cursor.execute("INSERT INTO usuarios (nombre_usuario, nombres, apellido_paterno, apellido_materno, correo, contrasena) VALUES (%s, %s, %s, %s, %s, %s)", (NombreUsuario, Nombres, Apellido_paterno, Apellido_materno, Correo, contrasena_encriptada))
        conexion.commit()
        print("Usuario agregado exitosamente.")
        
    except psycopg2.errors.UniqueViolation as e:
        conexion.rollback()
        if "correo" in str(e):
            print("El correo ya está registrado.")
        elif "nombre_usuario" in str(e):
            print("El nombre de usuario ya existe.")
        print("El nombre de usuario o el correo electrónico ya están en uso.")
                
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al agregar el usuario: {e}")

def Eliminar_usuario(conexion):
    try:
        cursor = conexion.cursor()
        admin = input("Ingrese su nombre de usuario para verificar permisos: ")
        permisos = Verificar_permisos(conexion, admin)
        cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (admin,))
        resultado = cursor.fetchone()
        contrasena_confirmacion = getpass.getpass("Ingrese su contraseña para confirmar: ")
        
        if not bcrypt.checkpw(contrasena_confirmacion.encode('utf-8'), resultado[0].encode('utf-8')):
            print("Contraseña incorrecta.")
            return
        
        if permisos == 'admin':
            usuario = input("Ingrese el nombre de usuario a eliminar: ")
            cursor.execute("SELECT contrasena FROM usuarios WHERE nombre_usuario = %s", (usuario,))
            resultado = cursor.fetchone()
            
            if resultado is None:
                print("Usuario no encontrado.")
                return
            
            else:
                confirmacion = input(f"¿Estás seguro de que deseas eliminar al usuario '{usuario}'? (si/no) ")
                if confirmacion.lower() in ['si', 'sí', 's']:
                    cursor.execute("DELETE FROM usuarios WHERE nombre_usuario = %s", (usuario,))
                    conexion.commit()
                    print("Usuario eliminado exitosamente.")
                else:
                    print("Eliminación cancelada.")
        else:
            print("Contraseña incorrecta o no tienes permisos suficientes.")
            return
      
    except psycopg2.Error as e:
        conexion.rollback()
        print(f"Error al eliminar el usuario: {e}")
        
