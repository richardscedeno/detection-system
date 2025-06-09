# db/queries.py
import mysql.connector
from db.connection import get_connection
import json

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


def obtener_persona_por_indice(indice):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM personas WHERE embedding_index = %s", (indice,))
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    return resultado


def obtener_persona_por_indicetest(indice):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    
    cursor.execute("""
        SELECT 
            id, tipo, identificacion, nombre, apellido, 
            datos_especificos, embedding_index, fecha_registro
        FROM personas 
        WHERE embedding_index = %s
    """, (indice,))
    
    resultado = cursor.fetchone()
    cursor.close()
    conn.close()
    
    if resultado:
        print("Datos de la persona encontrada:")
        print(f"ID: {resultado['id']}")
        print(f"Tipo: {resultado['tipo']}")
        print(f"Identificación: {resultado['identificacion']}")
        print(f"Nombre: {resultado['nombre']} {resultado['apellido']}")
        
        # Manejo seguro de datos_especificos (JSON)
        datos_especificos = resultado.get('datos_especificos')
        if datos_especificos:
            try:
                # Si es un string JSON, lo convertimos a dict
                if isinstance(datos_especificos, str):
                    datos_especificos = json.loads(datos_especificos)
                
                # Si es un dict (o ya fue convertido), mostramos los datos
                if isinstance(datos_especificos, dict):
                    print("Datos específicos:")
                    for key, value in datos_especificos.items():
                        print(f"  - {key}: {value}")
                else:
                    print(f"Datos específicos (formato no esperado): {datos_especificos}")
            except json.JSONDecodeError:
                print(f"Datos específicos (no es JSON válido): {datos_especificos}")
        else:
            print("No hay datos específicos registrados.")
        
        print(f"Índice de embedding: {resultado['embedding_index']}")
        print(f"Fecha de registro: {resultado['fecha_registro']}")
    else:
        print(f"No se encontró ninguna persona con embedding_index = {indice}")
    
    return resultado

# Ejemplo de uso
#obtener_persona_por_indice(5)
