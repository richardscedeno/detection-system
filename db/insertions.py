# db/insertions.py
from db.connection import get_connection
import json
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


def insertar_persona1(tipo, identificacion, nombre, apellido, embedding_index, datos_especificos=None):
    conn = get_connection()
    cursor = conn.cursor()

    if tipo == "estudiante":
        datos_json = json.dumps(datos_especificos)
    else:
        datos_json = None

    sql = """
        INSERT INTO personas (tipo, identificacion, nombre, apellido, datos_especificos, embedding_index)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    values = (tipo, identificacion, nombre, apellido, datos_json, embedding_index)

    try:
        cursor.execute(sql, values)
        conn.commit()
        print("✅ Persona registrada exitosamente.")
    except Exception as e:
        print(f"❌ Error al registrar persona: {e}")
    finally:
        cursor.close()
        conn.close()
        

def insertar_persona2(tipo, identificacion, nombre, apellido, datos_especificos, embedding_index):
    conn = get_connection()
    cursor = conn.cursor()

    # Verificar si ya existe alguien con ese embedding_index
    cursor.execute("SELECT id FROM personas WHERE embedding_index = %s", (embedding_index,))
    existing = cursor.fetchone()
    if existing:
        conn.close()
        return False, "El índice ya ha sido registrado. Persona ya existente."

    try:
        sql = """
            INSERT INTO personas (tipo, identificacion, nombre, apellido, datos_especificos, embedding_index)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            tipo,
            identificacion,
            nombre,
            apellido,
            json.dumps(datos_especificos),
            embedding_index
        ))
        conn.commit()
        conn.close()
        return True, "Persona registrada exitosamente."
    except Exception as e:
        conn.rollback()
        conn.close()
        return False, f"Error al registrar persona: {str(e)}"



def insertar_persona(tipo, identificacion, nombre, apellido, datos_especificos, embedding_index):
    conn = get_connection()
    if conn is None:
        return False, "Error de conexión con la base de datos."

    try:
        cursor = conn.cursor()

        # Verificar si ya está registrado ese índice
        cursor.execute("SELECT * FROM personas WHERE embedding_index = %s", (embedding_index,))
        if cursor.fetchone():
            return False, "El índice ya ha sido registrado."

        # Convertir el diccionario de datos_especificos a JSON si existe
        datos_json = json.dumps(datos_especificos) if datos_especificos else None

        sql = """
            INSERT INTO personas (tipo, identificacion, nombre, apellido, datos_especificos, embedding_index)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (
            tipo, identificacion, nombre, apellido,
            datos_json,
            embedding_index
        ))
        conn.commit()
        return True, "Persona registrada exitosamente."
    except Exception as e:
        return False, f"Error al registrar persona: {e}"
    finally:
        cursor.close()
        conn.close()
