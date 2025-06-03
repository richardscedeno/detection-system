# db/queries.py
from db.connection import get_connection

def obtener_persona_por_identificacion(identificacion):
    conn = get_connection()
    if conn is None:
        return None

    try:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM personas WHERE identificacion = %s", (identificacion,))
        return cursor.fetchone()
    except Exception as e:
        print(f"Error en la consulta: {e}")
        return None
    finally:
        cursor.close()
        conn.close()

