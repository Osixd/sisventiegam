import bcrypt
import psycopg2

def Conectar_bd():
    
    psycopg2.connect(
    host= "localhost",
    database= "videogames_db",
    user= "postgres",
    password= "Espacio1",
    port= 5432
    )
    
    if psycopg2.connect:
        print("Conexión exitosa a la base de datos.")
    else:
        print("Error al conectar a la base de datos.")
    

def mostrar_usuarios(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    
def Buscar_usuario(conn, x):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM BDUSERS WHERE Nombre_Usuario = %s", (x,))
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
    contraseña_encriptada = bcrypt.hashpw(Contraseña.encode('utf-8'), bcrypt.gensalt())
    Saldo_Cuenta = float(input("Ingrese el saldo inicial: "))
    Permisos = "Usuario"
    Nombres = input("Ingrese su nombre(s): ")
    Apellido1 = input("Ingrese su primer apellido: ")
    Apellido2 = input("Ingrese su segundo apellido: ")
    cursor.execute(r"INSERT INTO BDUSERS (Nombre_Usuario, Correo, Contraseña, Saldo_Cuenta, Permisos, Nombre(s), Apellido1, Apellido2) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (NombreUsuario, Correo, contraseña_encriptada, Saldo_Cuenta, Permisos, Nombres, Apellido1, Apellido2))
    conn.commit()
    print("Usuario agregado exitosamente.")

conn = Conectar_bd()
x = input("¿Qué usuario deseas buscar? ")
Buscar_usuario(conn, x)