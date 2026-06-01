import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

def Conectar_bd():
    try:
        conexion = psycopg2.connect(
            host= os.getenv("DB_HOST"),
            database= os.getenv("DB_NAME"),
            user= os.getenv("DB_USER"),
            password= os.getenv("DB_PASSWORD"),
            port= os.getenv("DB_PORT")
        )
        return conexion
    
    except psycopg2.Error as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

