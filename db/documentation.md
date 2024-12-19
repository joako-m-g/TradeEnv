# Documentacion de la BD
## Directorio: `db/schema.sql`


#### Diseño de schema.sql

##### Tablas del esquema

- operations:

    - Registra cada operación ejecutada por una estrategia.
    
    - Incluye detalles como el símbolo, la cantidad, precios de entrada/salida, tipo de operación (compra/venta), y la estrategia asociada.

    ```sql
        -- Tabla para registrar operaciones
    CREATE TABLE operations (
        id INT PRIMARY KEY AUTOINCREMENT, -- ID unico para cada operacion
        strategyName TEXT NOT NULL, -- Nombre de la estrategia
        symbol TEXT NOT NULL, -- Simbolo
        orderType TEXT NOT NULL, -- Tipo de orden
        quantity REAL NOT NULL, -- Cantidad operada
        entryPrice REAL NOT NULL, -- Precio de entrada
        exitPrice REAL, -- Precio de salida (puede ser NULL si todavia esta abierta)
        entryTime TIMESTAMP NOT NULL, -- Fecha y hora de entrada
        exitTime TIMESTAMP, -- Fecha y hora de salida
        profitLoss REAL, -- Ganancia o perdida de la operacion
        notes TEXT, -- Notas opcionales de la operacion
    )


    ```

- metrics:

    - Almacena métricas de rendimiento de cada estrategia.
    - Registra datos agregados como ganancia total, drawdown, Sharpe ratio, y más. 

    ```sql 
        -- Tabla para registrar metricas de rendimiento
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada registro de métricas
        strategyName TEXT NOT NULL,           -- Nombre de la estrategia
        sharpeRatio REAL,                     -- Ratio de Sharpe
        win_loss_ratio REAL,                   -- Win/Loss ratio
        profitFactor REAL,                    -- Factor de ganancia (ganancias totales / pérdidas totales)
        maxDrawdown REAL,                     -- Máximo drawdown (%)
        annualReturn REAL,                    -- Retorno anualizado (%)
        notes TEXT                             -- Notas opcionales
    );
    ```
---
## Directorio: `db/connection.py`
#### Descripcion: 

En el script `connection.py` encontramos funciones para establecer una conexion con la BD, crear tablas y hacer consultas.

### Funcion: `createConnection`
#### Descripcion: 

La función createConnection se encarga de establecer una conexión con una base de datos SQLite utilizando el archivo de base de datos especificado. Si la conexión se establece correctamente, la función devuelve el objeto de conexión. Si ocurre un error, imprime un mensaje de error y devuelve None.

#### Parameros: 
- `dbfile` `(str)`:  
    - Ruta del archivo de la base de datos SQLite con el cual se desea establecer la conexión.
    - Si el archivo no existe, SQLite creará una nueva base de datos en esa ubicación.

#### Valor de retorno:
- `conn` (objeto `sqlite3.Connection`): Un objeto de conexion que se puede usar para interactuar con la base de datos
- Si ocurre un error durante la conexion, la funcion devuelve None

#### Codigo de la funcion: 
```python
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
```

#### Ejemplo de uso: 
```python
# Llamada a la función para establecer conexión con una base de datos
connection = createConnection('example.db')

# Verifica si la conexión fue exitosa
if connection:
    print("Conexión exitosa!")
else:
    print("No se pudo establecer la conexión.")
```
---
### Funcuion: `createTables`

#### Descripcion: 
La función createTables se encarga de crear las tablas de la base de datos a partir de un esquema SQL previamente definido. Utiliza el archivo schema.sql para ejecutar el script que contiene las instrucciones necesarias para crear las tablas. Si la operación es exitosa, imprime un mensaje de confirmación; en caso contrario, maneja los errores y muestra un mensaje detallado.

#### Parameteros: 
- `conn` (`sqlite3.connection`):
    - Objeto de conexion a la bd SQLite que se obtiene al establecer una conexion con la bd mediante la funcion `createConnect`
    - Esta conexion es utilizada paea interactuar con la bd

#### Valor de retorno: 
- La función no retorna ningún valor, pero imprime un mensaje en consola que indica si la operación fue exitosa o si ocurrió algún error.

#### Codigo de la funcion: 
```python

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
```
#### Ejemplo de uso:
```python
# Suponiendo que ya se tiene una conexión establecida con la base de datos
connection = createConnection('example.db')

# Verificar si la conexión fue exitosa
if connection:
    # Crear las tablas en la base de datos
    createTables(connection)
else:
    print("No se pudo establecer la conexión a la base de datos.")
```
---

### Funcion: `closeConnection`
#### Descripcion
La función closeConnection se encarga de cerrar la conexión con la base de datos SQLite. Esto es importante para liberar los recursos del sistema y garantizar que las operaciones pendientes en la base de datos se completen correctamente. Si la conexión está abierta, la función cierra la conexión y muestra un mensaje de confirmación.

#### Parametros: 
- `conn` (`sqlite3.connection`):
    - Objeto de conexion a la bd SQLite que se obtiene al establecer una conexion con la bd mediante la funcion `createConnect`
    - Esta conexion es utilizada paea interactuar con la bd

#### Valor de retorno: 
- La función no retorna ningún valor. Su propósito es cerrar la conexión y mostrar un mensaje indicando si la operación fue exitosa.

#### Codigo de la funcion: 
```python
def closeConnection(conn):
    '''Cierra la conexion con la base de datos'''
    # Verificar si la conexión es válida (no es None)
    if conn:
        # Cerrar la conexión con la base de datos
        conn.close()
        # Imprimir un mensaje de confirmación
        print('Conexion cerrada')
```

#### Ejemplo de uso: 
```python
# Suponiendo que ya tienes una conexión abierta
connection = createConnection('example.db')

# Realizar algunas operaciones con la base de datos...

# Cerrar la conexión después de completar las operaciones
closeConnection(connection)
```
---

### Funcion: `ejecuteQuery`
#### Descripcion: 
- La función `ejecuteQuery` se utiliza para ejecutar consultas SQL en una base de datos SQLite. Puede ejecutar tanto consultas de lectura (como SELECT) como de modificación (como INSERT, UPDATE o DELETE). La función maneja parámetros opcionales para evitar la inyección de SQL y permitir la ejecución dinámica de consultas.

#### Parametros de la funcion:
- `conn` (`sqlite3.connection`):
    - Objeto de conexion a la bd SQLite que se obtiene al establecer una conexion con la bd mediante la funcion `createConnect`
    - Esta conexion es utilizada paea interactuar con la bd

- `query` (`str`): La consulta SQL a ejecutar. Esta cadena debe contener la consulta que se desea ejecutar, ya sea de selección (SELECT), inserción (INSERT), actualización (UPDATE), eliminación (DELETE), etc.

- `params` (`tuple` o `None` opcional): 
    - Parámetros opcionales que se pasan a la consulta. Si la consulta requiere valores dinámicos (como los valores de una fila para INSERT), estos deben pasar como un tuple de valores.

    - Si no se requieren parámetros, el valor predeterminado es None.

#### Valor de retorno:
- `cursor` (`sqlite3.Cursor` o `None`): 
    - Retorna un objeto `cursor` que permite acceder a los resultados de la consulta (en caso de que sea una consulta de selección) o None si ocurrió un error en la ejecución de la consulta.

#### Codigo de la funcion:
```python
def ejecuteQuery(conn, query, params=None):
    '''Ejecuta una consulta SQL.'''
    # Crear un cursor para ejecutar la consulta
    cursor = conn.cursor()
    
    try: 
        # Si se pasan parámetros, ejecutar la consulta con ellos
        if params:
            cursor.execute(query, params)
        else: 
            # Si no se pasan parámetros, ejecutar la consulta directamente
            cursor.execute(query)
        
        # Realizar commit para guardar cambios si es necesario
        conn.commit()
        
        # Retornar el cursor para poder acceder a los resultados
        return cursor
    
    except Error as e:
        # Si ocurre un error, imprimir el mensaje y retornar None
        print(f'Error al ejecutar la consulta: {e}')
        return None
```
#### Ejemplo de uso: 
```python
query = '''
    INSERT INTO metrics (strategy_name, period_start, period_end, total_trades, winning_trades, losing_trades, total_profit, total_loss, drawdown, sharpe_ratio)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
'''
params = ('Strategy A', '2024-01-01', '2024-01-31', 100, 60, 40, 5000.0, 2000.0, 10.0, 1.5)

ejecuteQuery(conn, query, params)
```
---
