# db/insertions.py
from db.connection import get_connection

def insertar_deteccion_arma(tipo_arma, confianza, ubicacion, imagen_path):
    conn = get_connection()
    if conn is None:
        return False
    
    try:
        cursor = conn.cursor()
        sql = """
        INSERT INTO detecciones_armas (tipo_arma, confianza, ubicacion, imagen_path)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(sql, (tipo_arma, confianza, ubicacion, imagen_path))
        conn.commit()
        return cursor.lastrowid
    except Exception as e:
        print(f"Error insertando detección de arma: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

