import sqlite3
from sqlite3 import Error
import pandas as pd


# Funcion para crear una conexion con la base de datos
def createConnection(dbFile='db/tradingEnviroment.db'):
    '''Crea una conexion con la base de datos SQLite'''
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        print(f'Conexion establecida a la base de datos. Version{sqlite3.version}')
    except Error as e: 
        print(f'Error al conectar a la base de datos: {e}')
    
    return conn

# Funcion para crear las tablas
def createTables(conn, schema='db\schema.sql'):
    sqlScript = ''
    try:
        with open(schema, 'r') as file:
            sqlScript = file.read()
        cursor = conn.cursor()
        cursor.executescript(sqlScript)
        conn.commit()
        print("Script SQL ejecutado correctamente y tablas creadas.")
    except sqlite3.Error as e:
        print(f"Error al ejecutar el script SQL: {e}")
    except FileNotFoundError:
        print(f"Archivo SQL no encontrado: {sqlScript}")

# Funcion para crear tablas
def ejecuteQuery(conn, query, params=None, query_type="SELECT"):
    try: 
        cursor = conn.cursor()
        if query_type == "SELECT":
            # Si es un SELECT, ejecutar y devolver el DataFrame
            df = pd.read_sql_query(query, conn, params=params)
            return df
        
        # Si no es un SELECT, ejecutar la consulta de modificación
        cursor.execute(query, params)
        conn.commit()  # Confirmar los cambios realizados

        return None  # No devolvemos nada para consultas de modificación (INSERT, UPDATE, DELETE)
    
    except Error as e:
        print(f'Error al ejecutar la consulta: {e}')
        return None

# Funcion para cerrar la conexion
def closeConnection(conn):
    '''Cierra la conexion con la base de datos'''
    if conn:
        conn.close()
        print('Conexion cerrada')

# Ejemplo de uso
if __name__ == '__main__':
    # Ruta a la base de datos (se puede cambiar a otro DBMS como mySQL)
    database = 'db/tradingEnviroment.db' # Nombre del schema de la BD

    # Crear conexion
    conn = createConnection(database)

    if conn:
        # Aquí puedes agregar más funciones para insertar, actualizar, y consultar datos
        
        # Cerrar conexión
        closeConnection(conn)