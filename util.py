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
        conn.close()
    
    
def Leer_datos(conn):
    pass


Conectar_bd()