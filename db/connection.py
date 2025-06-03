# db/connection.py
import mysql.connector
from mysql.connector import Error

def get_connection():
    try:
        conn = mysql.connector.connect(
            host='localhost',
            port=3306,
            database='detector_armas',
            user='root',
            password='chards00'
        )
        print('conectado con exito')
        return conn
    except Error as e:
        print(f'Error al conectar con la base de datos: {e}')
        return None

