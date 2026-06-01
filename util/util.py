import os
import bcrypt
import psycopg2
from  conexion import Conectar_bd

conexion = Conectar_bd()

def Mostrar_usuarios(conexion, usuario_buscar):
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s AND permisos = 'admin'", (usuario_buscar,))
        resultado = cursor.fetchone()
        if resultado:
            cursor.execute("SELECT * FROM usuarios")
            rows = cursor.fetchall()
            for row in rows:
                print(row)
        else:
            print("No tienes permiso para ver esto.")
    except psycopg2.Error as e:
        print(f"Error al mostrar los usuarios: {e}")

def Buscar_usuario(conexion, usuario_buscar):
    if not usuario_buscar:
        print("No se ha ingresado un nombre de usuario.")
        return
    try:
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE nombre_usuario = %s", (usuario_buscar,))
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
        NombreUsuario = input("Ingrese el nombre de usuario: ")
        Correo = input("Ingrese el correo electrónico: ")
        Contrasena = input("Ingrese la contraseña: ")
        contrasena_encriptada = bcrypt.hashpw(Contrasena.encode('utf-8'), 
                                            bcrypt.gensalt()
                                            ).decode('utf-8')
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




conn = Conectar_bd()
usuario_buscar = input("¿Qué usuario deseas buscar? ")
Buscar_usuario(conn, usuario_buscar)
