# Documentación de la BD
## Directorio: `db/schema.sql`

#### Diseño de `schema.sql`

##### Tablas del esquema

- **operations**:
    - Registra cada operación ejecutada por una estrategia.
    - Incluye detalles como el símbolo, la cantidad, precios de entrada/salida, tipo de operación (compra/venta), la estrategia asociada y el marco temporal de la operación.

    ```sql
        -- Tabla para registrar operaciones
    CREATE TABLE operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para cada operación
        strategyName TEXT NOT NULL, -- Nombre de la estrategia
        symbol TEXT NOT NULL, -- Símbolo del activo
        orderType TEXT NOT NULL, -- Tipo de orden (compra/venta)
        quantity REAL NOT NULL, -- Cantidad operada
        entryPrice REAL NOT NULL, -- Precio de entrada
        exitPrice REAL, -- Precio de salida (puede ser NULL si todavía está abierta)
        entryTime TIMESTAMP NOT NULL, -- Fecha y hora de entrada
        exitTime TIMESTAMP, -- Fecha y hora de salida
        profitLoss REAL, -- Ganancia o pérdida de la operación
        timeframe TEXT NOT NULL, -- Marco temporal en el que opera la estrategia
        notes TEXT -- Notas opcionales de la operación
    );
    ```

- **metrics**:
    - Almacena métricas de rendimiento de cada estrategia.
    - Registra datos agregados como ganancia total, drawdown, Sharpe ratio, entre otros.
    - Añadido un campo `timestamp` para registrar la fecha y hora exacta de la medición de las métricas.

    ```sql
        -- Tabla para registrar métricas de rendimiento
    CREATE TABLE metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT, -- ID único para cada registro de métricas
        strategyName TEXT NOT NULL, -- Nombre de la estrategia
        timestamp DATETIME, -- Fecha y hora de registro de las métricas
        sharpeRatio REAL, -- Ratio de Sharpe
        lossTrades INTEGER, -- Número de operaciones perdedoras
        winTrades INTEGER, -- Número de operaciones ganadoras
        win_loss_ratio REAL, -- Win/Loss ratio
        profitFactor REAL, -- Factor de ganancia (ganancias totales / pérdidas totales)
        maxDrawdown REAL, -- Máximo drawdown (%)
        PnL REAL, -- Retornos netos (PnL)
        annualReturn REAL, -- Retorno anualizado (%)
        notes TEXT -- Notas opcionales
    );
    ```
---
## Directorio: `db/connection.py`
#### Descripción: 
Este script contiene funciones para interactuar con una base de datos SQLite, incluyendo la creación de la conexión, la creación de tablas, la ejecución de consultas, y el cierre de la conexión.

---

### Función: `createConnection`
#### Descripción:
Establece una conexión con una base de datos SQLite utilizando el archivo de base de datos especificado. Si la conexión es exitosa, devuelve el objeto de conexión, de lo contrario, imprime un mensaje de error y devuelve `None`.

#### Parámetros: 
- `dbFile` (str): Ruta al archivo de la base de datos SQLite que se desea utilizar. Si el archivo no existe, SQLite creará una nueva base de datos en esa ubicación. Valor predeterminado: `'db/tradingEnviroment.db'`.

#### Valor de retorno:
- `conn` (objeto `sqlite3.Connection`): Un objeto de conexión a la base de datos. Si la conexión falla, devuelve `None`.

---

### Función: `createTables`
#### Descripción:
Lee y ejecuta un script SQL desde un archivo para crear las tablas necesarias en la base de datos.

#### Parámetros:
- `conn` (objeto `sqlite3.Connection`): El objeto de conexión a la base de datos.
- `schema` (str): Ruta del archivo SQL que contiene el script para crear las tablas. Valor predeterminado: `'db/schema.sql'`.

#### Valor de retorno:
- No retorna valor. Si el script se ejecuta correctamente, imprime un mensaje indicando que las tablas fueron creadas. Si hay un error, lo reporta.

---

### Función: `ejecuteQuery`
#### Descripción:
Ejecuta una consulta SQL en la base de datos. Puede manejar consultas de tipo `SELECT` para retornar resultados o consultas de modificación (`INSERT`, `UPDATE`, `DELETE`) que no retornan datos.

#### Parámetros:
- `conn` (objeto `sqlite3.Connection`): El objeto de conexión a la base de datos.
- `query` (str): La consulta SQL que se desea ejecutar.
- `params` (tuple, opcional): Los parámetros que se pasan a la consulta SQL. Valor predeterminado: `None`.
- `query_type` (str): El tipo de consulta a ejecutar. Puede ser `'SELECT'`, `'INSERT'`, `'UPDATE'`, o `'DELETE'`. Valor predeterminado: `'SELECT'`.

#### Valor de retorno:
- Si `query_type` es `'SELECT'`, retorna un DataFrame con los resultados de la consulta.
- Si `query_type` es diferente de `'SELECT'`, no retorna valor, pero realiza la modificación solicitada (inserta, actualiza o elimina datos).

---

### Función: `closeConnection`
#### Descripción:
Cierra la conexión con la base de datos.

#### Parámetros:
- `conn` (objeto `sqlite3.Connection`): El objeto de conexión a la base de datos.

#### Valor de retorno:
- No tiene valor de retorno. Solo cierra la conexión si está abierta.

---

### Ejemplo de uso:

```python
if __name__ == '__main__':
    # Ruta a la base de datos (se puede cambiar a otro DBMS como mySQL)
    database = 'db/tradingEnviroment.db'  # Nombre del schema de la BD

    # Crear conexión
    conn = createConnection(database)

    if conn:
        # Aquí puedes agregar más funciones para insertar, actualizar, y consultar datos
        
        # Cerrar conexión
        closeConnection(conn)
```
---
## Directorio: `operations.py`
#### Descripción:
Este script contiene funciones para registrar operaciones y métricas en una base de datos, así como para consultar las operaciones y métricas almacenadas para una estrategia específica.

---

### Función: `registerOperation`
#### Descripción:
Registra una nueva operación en la tabla `operations` de la base de datos. La función toma un objeto `operationData` que contiene los detalles de la operación y los inserta en la base de datos.

#### Parámetros:
- `operationData` (objeto): Un objeto que contiene los atributos de la operación. Los atributos necesarios incluyen:
    - `strategyName` (str): Nombre de la estrategia.
    - `symbol` (str): Símbolo del activo.
    - `orderType` (str): Tipo de orden (por ejemplo, "BUY" o "SELL").
    - `quantity` (float): Cantidad de activo.
    - `entryPrice` (float): Precio de entrada.
    - `exitPrice` (float): Precio de salida.
    - `entryTime` (datetime): Hora de entrada.
    - `exitTime` (datetime): Hora de salida.
    - `profitLoss` (float): Ganancia o pérdida de la operación.
    - `timeframe` (str): Marco temporal de la operación.
    - `notes` (str): Notas adicionales.

#### Valor de retorno:
- No retorna valor. Si la operación es registrada exitosamente, imprime un mensaje de confirmación.

---

### Función: `registerMetrics`
#### Descripción:
Registra las métricas de una estrategia en la tabla `metrics` de la base de datos. La función toma un objeto `metrics` que contiene las métricas y las inserta en la base de datos.

#### Parámetros:
- `metrics` (objeto): Un objeto que contiene las métricas de la estrategia. Los atributos necesarios incluyen:
    - `strategyName` (str): Nombre de la estrategia.
    - `sharpeRatio` (float): Ratio de Sharpe.
    - `lossTrades` (int): Número de operaciones con pérdida.
    - `winTrades` (int): Número de operaciones con ganancia.
    - `WLRratio` (float): Ratio de ganancias/pérdidas.
    - `Pfactor` (float): Factor de beneficio.
    - `maxDrawdown` (float): Máxima caída de capital.
    - `annualReturn` (float): Retorno anual.
    - `PnL` (float): Ganancia o pérdida total.
    - `notes` (str): Notas adicionales.

#### Valor de retorno:
- No retorna valor. Si las métricas son registradas exitosamente, imprime un mensaje de confirmación.

---

### Función: `getOperations`
#### Descripción:
Consulta la tabla `operations` para obtener las operaciones de una estrategia específica dentro de un rango de precios. Retorna los resultados como un DataFrame.

#### Parámetros:
- `strategyName` (str): Nombre de la estrategia cuyas operaciones queremos recuperar.
- `startPeriod` (float): El valor mínimo de `entryPrice` para filtrar las operaciones.
- `endPeriod` (float): El valor máximo de `entryPrice` para filtrar las operaciones.

#### Valor de retorno:
- `operations` (DataFrame): Un DataFrame con las operaciones que cumplen con los criterios de filtrado.

---

### Función: `getMetrics`
#### Descripción:
Consulta la tabla `metrics` para obtener las métricas de una estrategia específica dentro de un rango de fechas. Retorna los resultados como un DataFrame.

#### Parámetros:
- `strategyName` (str): Nombre de la estrategia cuyas métricas queremos recuperar.
- `startPeriod` (datetime): La fecha y hora mínima para filtrar las métricas.
- `endPeriod` (datetime): La fecha y hora máxima para filtrar las métricas.

#### Valor de retorno:
- `metrics` (DataFrame): Un DataFrame con las métricas que cumplen con los criterios de filtrado.

---
