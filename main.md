# Documentación del Script de Trading

Este script configura y ejecuta un entorno de trading utilizando la librería Backtrader, se conecta a IBKR (Interactive Brokers) para obtener datos de mercado y realizar operaciones. Además, gestiona el cálculo de métricas y la generación de reportes de las estrategias de trading.

## Clases y Métodos

### `TradingEnvironment`

Esta clase maneja la configuración y ejecución del entorno de trading. Incluye la conexión a IBKR, la configuración de la base de datos y la ejecución de las estrategias en el motor de Backtrader.

#### Métodos

- **`__init__(self)`**  
  Constructor de la clase. Inicializa los atributos necesarios para el entorno de trading: 
  - `cerebro`: Motor de Backtrader donde se agregarán las estrategias y los datos.
  - `ibkrConnection`: Atributo que almacena la conexión a IBKR.
  - `dbConnection`: Atributo para almacenar la conexión a la base de datos.

- **`initialize(self)`**  
  Método encargado de inicializar todas las conexiones y configurar el entorno de trading.
  - **Conexión con IBKR**: Se conecta al broker utilizando la función `connectIBKR()`.
  - **Conexión con la base de datos**: Se establece una conexión con la base de datos utilizando la función `createConnection()`. Si la conexión es exitosa, se crean las tablas necesarias con la función `createTables()`.
  - **Cargar las estrategias**: Utiliza la función `loadStrategies()` para cargar las estrategias de trading.
  - **Agregar estrategias al motor de Backtrader**: Para cada estrategia cargada, se agrega a `cerebro` junto con los parámetros de tiempo y datos del mercado correspondientes.
  - **Conexión a IBKR Store**: Se obtiene la conexión al broker mediante `ibstore = connectIBKR()`.
  - **Configuración de los datos de mercado**: Se obtiene y configura el mercado a través de IBKR, asociando cada estrategia a su respectiva información de datos.

- **`run(self)`**  
  Este método se encarga de ejecutar el motor de Backtrader (`cerebro`). Llama al método `run()` de Backtrader para iniciar la ejecución de las estrategias de trading con los datos y parámetros configurados.

---

### `MetricsUpdater`

Esta clase maneja la actualización de métricas de las estrategias de trading a intervalos regulares (diario, semanal, mensual). Además, genera reportes mensuales.

#### Atributos

- **`dbConnection`**  
  Conexión a la base de datos para realizar consultas y registrar las métricas calculadas.

- **`dayInterval`, `weekInterval`, `monthInterval`**  
  Intervalos de tiempo (en días) para calcular las métricas de las estrategias. Los valores predeterminados son 1, 7 y 30 días, respectivamente.

- **`running`**  
  Indica si el bucle de actualización de métricas está en ejecución. Es un flag que controla el estado del proceso.

- **`strategies`**  
  Diccionario de las estrategias de trading cargadas en el entorno.

- **`starTime`, `lastTimeDay`, `lastTimeWeek`, `lastTimeMonth`**  
  Variables de tiempo que se utilizan para calcular los intervalos entre actualizaciones y para asegurarse de que las métricas se calculen a intervalos regulares.

#### Métodos

- **`__init__(self, dbConnection, dayInerval=1, weekInterval=7, monthInterval=30)`**  
  Constructor de la clase. Inicializa las variables de tiempo, la conexión a la base de datos y los intervalos de actualización de métricas. El parámetro `dbConnection` es necesario para interactuar con la base de datos.

- **`start(self)`**  
  Inicia el proceso de actualización de métricas. Si el bucle no está en ejecución (`running` es `False`), se configura un hilo para que ejecute el proceso de actualización.

- **`stop(self)`**  
  Detiene el bucle de actualización de métricas. Cambia el valor de `running` a `False` y termina el proceso.

- **`_startUpdaterThread(self)`**  
  Crea un hilo de ejecución independiente que ejecutará el método `_updateMetricsLoop`. Esto permite que las métricas se actualicen en segundo plano mientras el programa principal sigue ejecutándose.

- **`_updateMetricsLoop(self)`**  
  Método que se ejecuta en un hilo separado. En un bucle continuo, consulta las operaciones realizadas en la base de datos y calcula las métricas a intervalos regulares (diarios, semanales, mensuales).
  - **Intervalo diario**: Si ha pasado el número de días especificado, se actualizan las métricas para las estrategias configuradas con un `timeframe` de "Daily".
  - **Intervalo semanal**: Lo mismo, pero para estrategias con `timeframe` "Week".
  - **Intervalo mensual**: Se actualizan las métricas y se generan reportes mensuales (en CSV y PDF).
  - El bucle espera 60 segundos entre cada verificación.

- **`updateMetrics(self, currentTime, timeFrame)`**  
  Calcula las métricas para las estrategias que coinciden con el intervalo de tiempo especificado (`timeFrame`). Los pasos incluyen:
  - **Obtener operaciones**: Se obtienen las operaciones realizadas en el intervalo de tiempo especificado mediante `getOPerations()`.
  - **Calcular métricas**: Se calculan diversas métricas utilizando la clase `Metrics`, que incluye el PnL (beneficio neto), el número de operaciones ganadoras y perdedoras, el WLR (ratio de ganancia/perdida), el drawdown (máxima pérdida), el Sharpe Ratio, y el retorno anualizado.
  - **Registrar métricas**: Se guardan las métricas calculadas en la base de datos utilizando la función `registerMetrics()`.

- **`createReport(self, currentTime)`**  
  Este método genera reportes mensuales para cada estrategia. El proceso incluye:
  - **Obtener operaciones y métricas**: Para cada estrategia, se recuperan las operaciones realizadas durante el último mes, así como las métricas correspondientes.
  - **Generar reportes**: Se crean reportes en formato CSV y PDF utilizando la clase `Reports`. Estos reportes contienen las métricas y el rendimiento de la estrategia durante el último mes.

---

## Función Principal

### `if __name__ == "__main__":`

Este bloque se ejecuta cuando el script es ejecutado directamente. Realiza las siguientes acciones:

1. **Inicializa el entorno de trading**:  
   Crea una instancia de la clase `TradingEnvironment` y llama al método `initialize()` para establecer las conexiones necesarias (IBKR y base de datos), cargar las estrategias y configurar los datos de mercado.

2. **Inicia la actualización de métricas**:  
   Crea una instancia de la clase `MetricsUpdater`, pasando la conexión a la base de datos, y llama a `start()` para comenzar el proceso de actualización en segundo plano.

3. **Mantiene el programa en ejecución**:  
   Entra en un bucle infinito, permitiendo que el programa siga ejecutándose mientras espera la señal de interrupción del usuario (`Ctrl+C`).

### Manejo de Excepciones

- Si el usuario interrumpe el programa (`KeyboardInterrupt`), el script detiene la actualización de métricas con `metricsUpdater.stop()` y finaliza el proceso.
- Finalmente, cierra todas las conexiones abiertas y termina el script con un mensaje de finalización.

---

## Flujo del Script

1. **Inicialización**:  
   El entorno de trading se configura con las conexiones necesarias a IBKR y la base de datos. Las estrategias se cargan y se configuran en el motor de Backtrader.

2. **Ejecución de Estrategias**:  
   Una vez que el entorno está configurado, las estrategias se ejecutan utilizando el motor de Backtrader. El rendimiento de las estrategias se calcula y se almacenan las métricas.

3. **Actualización de Métricas**:  
   Las métricas de las estrategias se actualizan en intervalos regulares (diario, semanal y mensual), calculando los indicadores clave para cada periodo.

4. **Generación de Reportes**:  
   Cada mes, se generan reportes detallados (CSV y PDF) con las métricas y el rendimiento de las estrategias.

---

## Requisitos

- **Backtrader**: Librería de Python para crear y ejecutar estrategias de trading.
- **IBKR API**: Conexión con Interactive Brokers para obtener datos en tiempo real y ejecutar operaciones.
- **Base de Datos**: Utiliza una base de datos para almacenar operaciones y métricas de las estrategias.

---

## Dependencias

```bash
pip install backtrader
# Otros paquetes necesarios para conectarse a IBKR y manejar la base de datos
