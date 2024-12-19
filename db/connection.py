import sqlite3
from sqlite3 import Error

# Funcion para crear una conexion con la base de datos
def createConnection(dbFile):
    '''Crea una conexion con la base de datos SQLite'''
    conn = None
    try:
        conn = sqlite3.connect(dbFile)
        print(f'Conexion establecida a la base de datos. Version{sqlite3.version}')
    except Error as e: 
        print(f'Error al conectar a la base de datos: {e}')
    
    return conn

# Funcion para crear tablas
def createTables(conn): 
    '''Crea las tablas en la base de datos a partir del esquema SQL.'''
    try: 
        cursor = conn.cursor()
        # Ejecutar el script para crear las tablas
        with open('db/schema.sql', 'r') as f:
            cursor.executescript(f.read())

            print("Tablas creadas exitosamente.")
    except Error as e:
        print(f'Error al crear las tablas: {e}')

# Funcion para cerrar la conexion
def closeConnection(conn):
    '''Cierra la conexion con la base de datos'''
    if conn:
        conn.close()
        print('Conexion cerrada')

# Funcion para ejecutar una consulta (ej: insertar o seleccionar datos)
def ejecuteQuery(conn, query, params=None):
    '''Ejecuta una consulta SQL.'''
    cursor = conn.cursor()
    
    try: 
        if params:
            cursor.execute(query, params)
        else: 
            cursor.execute(query)
        conn.commit()
        return cursor
    
    except Error as e:
        print(f'Error al ejecutar la consulta: {e}')
        return None

# Ejemplo de uso
if __name__ == '__main__':
    # Ruta a la base de datos (se puede cambiar a otro DBMS como mySQL)
    database = 'tradingEnviroment.db' # Nombre del schema de la BD

    # Crear conexion
    conn = createConnection(database)

    if conn:
    # Aquí puedes agregar más funciones para insertar, actualizar, y consultar datos
        
        # Cerrar conexión
        closeConnection(conn)