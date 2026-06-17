#==============================================================================
#                        MÓDULO DE CONEXIÓN A BD
#==============================================================================
# Este módulo se encarga de establecer la conexión a la base de datos PostgreSQL
# Utiliza variables de entorno para mayor seguridad
#==============================================================================

import psycopg2
from dotenv import load_dotenv
import os
from pathlib import Path

#Cargamos las variables de entorno desde el archivo .env
load_dotenv(dotenv_path=Path(__file__).parent.parent / ".env")

#Función para conectar a la base de datos
def Conectar_bd():
    """
    Conecta a la base de datos PostgreSQL utilizando credenciales del archivo .env
    Retorna: Una conexión a la BD o None si hay error
    """
    try:
        #realizamos la conexión con los datos del archivo .env
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

