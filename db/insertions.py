# db/insertions.py
from db.connection import get_connection
#from mysql.connector import Error

def insertar_deteccion_arma(fecha_hora, tipo_arma, confianza, ubicacion, imagen_path):
    conn = get_connection()
    if conn is None:
        return False

    try:
        cursor = conn.cursor()

        sql = """
        INSERT INTO detecciones_armas (fecha_hora, tipo_arma, confianza, ubicacion, imagen_path)
        VALUES (%s, %s, %s, %s, %s)
        """
        values = (fecha_hora, tipo_arma, confianza, ubicacion, imagen_path)
        cursor.execute(sql, values)
        conn.commit()
        #return cursor.lastrowid
        arma_id = cursor.lastrowid
        return arma_id

    except Exception as e:
        print(f"Error insertando detección de arma: {e}")
        return False
    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()


def insertar_alerta(tipo, mensaje, fecha_hora_envio, deteccion_facial_id=None, deteccion_arma_id=None):
    try:
        conn = get_connection()
        cursor = conn.cursor()

        sql = '''
            INSERT INTO alertas (tipo, mensaje, fecha_hora_envio, deteccion_facial_id, deteccion_arma_id)
            VALUES (%s, %s, %s, %s, %s)
        '''
        values = (tipo, mensaje, fecha_hora_envio, deteccion_facial_id, deteccion_arma_id)
        cursor.execute(sql, values)
        conn.commit()

        alerta_id = cursor.lastrowid
        return alerta_id

    except Error as e:
        print(f'Error al insertar alerta: {e}')
        return None

    finally:
        if conn.is_connected():
            cursor.close()
            conn.close()

