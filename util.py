import os
import pyodbc 

def Conectar_bd():
    ruta_bd = r"C:\Users\Osiris\Desktop\Nueva carpeta (2)\PythonLearn\POO\videojuegos\BD\BSP1.accdb"
    
    conexion = (r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + ruta_bd + ';'
                f"DBQ={ruta_bd};")
    try:
        conn = pyodbc.connect(conexion)
        print("Conexión exitosa a la base de datos.")
        return conn
    except pyodbc.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None
    finally: 
        #conn.close()
        pass
    
    
def Buscar_usuario(conn, x):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BDUSERS WHERE Nombre_Usuario = ?",(x))
    if cursor.fetchone() == None:
        print("Usuario no encontrado.")
        interactuar = input("¿Deseas agregar un nuevo usuario? (s/n) ")
        if interactuar.lower() == 's':
            Agregar_usuario(conn)
    rows = cursor.fetchall()
    for row in rows:
        print(row)


def Agregar_usuario(conn):
    cursor = conn.cursor()
    NombreUsuario = input("Ingrese el nombre de usuario: ")
    Correo = input("Ingrese el correo electrónico: ")
    Contraseña = input("Ingrese la contraseña: ")
    Saldo_Cuenta = float(input("Ingrese el saldo inicial: "))
    Permisos = "Usuario"
    Nombres = input("Ingrese su nombre(s): ")
    Apellido1 = input("Ingrese su primer apellido: ")
    Apellido2 = input("Ingrese su segundo apellido: ")
    cursor.execute(r"INSERT INTO BDUSERS (Nombre_Usuario, Correo, Contraseña, Saldo_Cuenta, Permisos, Nombre(s), Apellido1, Apellido2) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (NombreUsuario, Correo, Contraseña, Saldo_Cuenta, Permisos, Nombres, Apellido1, Apellido2))
    conn.commit()
    print("Usuario agregado exitosamente.")

conn = Conectar_bd()
x = input("¿Qué usuario deseas buscar? ")
Buscar_usuario(conn, x)