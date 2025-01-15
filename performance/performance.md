## Directorio: `metrics.py`
#### Descripción:
Este script define una clase `Metrics` que contiene métodos para calcular diversas métricas de rendimiento de una estrategia de trading basándose en las operaciones ejecutadas. Las métricas incluyen PnL (ganancia y pérdida), relación de ganancias/pérdidas, factor de beneficio, drawdown, ratio de Sharpe y retorno anual.

---

### Clase: `Metrics`
#### Descripción:
La clase `Metrics` toma un DataFrame `operations` (que contiene las operaciones realizadas) y un `timeFrame` (que puede ser diario, semanal o mensual) para calcular métricas clave de rendimiento de la estrategia.

#### Métodos:

---

### Método: `__init__`
#### Descripción:
Inicializa una instancia de la clase `Metrics` con el DataFrame de operaciones y el `timeFrame`.

#### Parámetros:
- `operations` (DataFrame): Un DataFrame que contiene las operaciones realizadas, debe tener la columna `entryTime` con las fechas de las operaciones.
- `timeFrame` (str): El marco temporal para los cálculos de las métricas. Puede ser `'D'` para diario, `'W'` para semanal o `'M'` para mensual.

#### Valor de retorno:
- No retorna valor. Inicializa los atributos `operations` y `timeFrame`.

---

### Método: `PnL`
#### Descripción:
Calcula la ganancia o pérdida total acumulada de todas las operaciones.

#### Valor de retorno:
- `winnLossTotal` (float): La suma de todas las ganancias y pérdidas de las operaciones.

---

### Método: `winnLossTrades`
#### Descripción:
Cuenta el número de operaciones ganadoras y perdedoras.

#### Valor de retorno:
- `winTrades` (int): Número de operaciones ganadoras.
- `lossTrades` (int): Número de operaciones perdedoras.

---

### Método: `WLRratio`
#### Descripción:
Calcula la relación de ganancias/pérdidas (Win/Loss Ratio).

#### Valor de retorno:
- `winnLossRatio` (float): Relación entre el número de operaciones ganadoras y el número de operaciones perdedoras.

---

### Método: `Pfactor`
#### Descripción:
Calcula el factor de beneficio, que es la relación entre la ganancia total de las operaciones ganadoras y la pérdida total de las operaciones perdedoras.

#### Valor de retorno:
- `profitFactor` (float): El factor de beneficio calculado.

---

### Método: `drawDown`
#### Descripción:
Calcula el drawdown máximo, que es la mayor caída desde el punto máximo en la serie de ganancias acumuladas.

#### Valor de retorno:
- `maxDrawdown` (float): El máximo drawdown de las operaciones.

---

### Método: `sharpeRatio`
#### Descripción:
Calcula el ratio de Sharpe, que mide el rendimiento ajustado al riesgo de la estrategia. Ajusta el valor según el `timeFrame`.

#### Valor de retorno:
- `sharpeRatio` (float): El ratio de Sharpe ajustado al marco temporal.

---

### Método: `annualReturn`
#### Descripción:
Calcula el retorno anualizado de la estrategia basado en las ganancias y pérdidas acumuladas.

#### Parámetros:
- `initialCapital` (float, opcional): El capital inicial invertido. El valor predeterminado es 1.

#### Valor de retorno:
- `annualizedReturn` (float): El retorno anualizado calculado.

---
## Directorio: `reports.py`

### Clase: `Reports`

La clase `Reports` se utiliza para generar informes detallados sobre el desempeño de una estrategia de trading algorítmico. El informe incluye métricas clave de desempeño, gráficos de evolución temporal, distribución de operaciones por día de la semana y una comparación entre operaciones ganadoras y perdedoras.

### Métodos

#### `__init__(self, metrics, operations, title)`
**Parámetros:**
- `metrics`: DataFrame de pandas que contiene las métricas de rendimiento de la estrategia de trading.
- `operations`: DataFrame de pandas que contiene las operaciones realizadas por la estrategia.
- `title`: String que representa el título del informe.

El constructor inicializa la clase con los datos de métricas y operaciones y el título para los archivos generados.

#### `createCSV(self)`
Genera un archivo CSV con las métricas de rendimiento en el directorio `TradeEnv/reports/` y lo guarda con el título del informe.

#### `meansTable(self)`
Genera una tabla con los promedios de las métricas, excluyendo las columnas no numéricas. Devuelve una Serie con los valores promedio de cada métrica.

#### `plotMetrics(self)`
Genera gráficos de las métricas de rendimiento de la estrategia de trading a lo largo del tiempo. Los gráficos incluyen:
- `sharpeRatio`
- `win_loss_ratio`
- `profitFactor`
- `maxDrawdown`
- `annualReturn`
- `PnL`

Cada gráfico se guarda como una imagen en el directorio `reports/` con el nombre `title_metric_plot.png`.

#### `operationsHistogram(self)`
Genera un histograma que muestra la distribución de operaciones por día de la semana. La columna `entryTime` en el DataFrame de operaciones se convierte a `datetime`, y se crea una columna adicional con el nombre del día de la semana. Este histograma se guarda como una imagen en el directorio `reports/` con el nombre `title_operationsDays_histogram.png`.

#### `plotPieChart(self)`
Genera un gráfico de pastel que compara el número de operaciones ganadoras frente a las operaciones perdedoras. El gráfico se guarda como una imagen en el directorio `reports/` con el nombre `title_pie_chart_operations.png`.

#### `createPDF(self)`
Genera un informe en formato PDF que incluye:
- Una introducción con detalles sobre el análisis de la estrategia de trading.
- Una tabla con los promedios de las métricas.
- Gráficos que muestran la evolución temporal de las métricas.
- Un histograma de las operaciones por día de la semana.
- Un gráfico de pastel de operaciones ganadoras vs perdedoras.

El informe se guarda como un archivo PDF en el directorio `reports/` con el nombre `title_informeDesempeño.pdf`.

### Archivos generados
- **CSV**: Un archivo CSV con las métricas de rendimiento.
- **PNG**: Archivos de imagen con gráficos de métricas, distribución de operaciones y comparación de operaciones ganadoras vs perdedoras.
- **PDF**: Un informe completo en formato PDF con todos los gráficos y análisis.

### Requisitos
- `fpdf`: Para la generación del archivo PDF.
- `pandas`: Para manejar y manipular los DataFrames.
- `matplotlib` y `seaborn`: Para generar los gráficos.
- `os` y `numpy`: Para manejo de archivos y operaciones numéricas.

---

Esta clase facilita la creación de informes completos y visuales sobre el desempeño de las estrategias de trading, proporcionando métricas clave y su evolución, así como una distribución visual de las operaciones y sus resultados.