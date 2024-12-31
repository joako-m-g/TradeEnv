---

### Clase: `Metrics`

#### Descripción: 
La clase `Metrics` permite calcular métricas financieras clave sobre las operaciones realizadas en una estrategia de trading, agrupándolas por un marco temporal especificado (`timeFrame`). Esto incluye cálculos como PnL (Profit and Loss), ratio de operaciones ganadoras/perdedoras, factor de ganancias, drawdown máximo y ratio de Sharpe.

#### Constructor: 
- `__init__(self, operations, timeFrame)`: 
  - Inicializa la clase con un DataFrame de operaciones y un marco temporal.
  - Convierte las fechas de entrada (`entryTime`) en el formato adecuado y agrupa las operaciones según el marco temporal.

#### Parámetros del Constructor:
- `operations` (`pd.DataFrame`): 
  - DataFrame que contiene las operaciones realizadas, con las columnas requeridas:
    - `'entryTime'`: Fecha y hora de la entrada.
    - `'profitLoss'`: Ganancia o pérdida de la operación.
- `timeFrame` (`str`): 
  - Marco temporal para agrupar las operaciones:
    - `'D'`: Diario.
    - `'W'`: Semanal.
    - `'M'`: Mensual.

#### Métodos: 

1. **`PnL(self)`**
   - **Descripción**: Calcula el Profit and Loss (ganancia/pérdida total) acumulado para las operaciones.
   - **Retorno**: 
     - `float`: Suma total de las ganancias/pérdidas.

2. **`winnLossTrades(self)`**
   - **Descripción**: Divide las operaciones en ganadoras y perdedoras.
   - **Retorno**: 
     - `tuple`: 
       - `lossTrades` (`pd.DataFrame`): Operaciones perdedoras.
       - `winTrades` (`pd.DataFrame`): Operaciones ganadoras.

3. **`WLRratio(self)`**
   - **Descripción**: Calcula el ratio entre operaciones ganadoras y perdedoras.
   - **Retorno**: 
     - `float`: Razón entre la cantidad de operaciones ganadoras y perdedoras.

4. **`Pfactor(self)`**
   - **Descripción**: Calcula el Profit Factor, que mide la relación entre las ganancias obtenidas y las pérdidas incurridas.
   - **Retorno**: 
     - `float`: Valor del Profit Factor.

5. **`drawDown(self)`**
   - **Descripción**: Calcula el drawdown máximo, que mide la mayor caída desde un máximo acumulado en las ganancias/pérdidas.
   - **Retorno**: 
     - `float`: Valor del drawdown máximo.

6. **`sharpeRatio(self)`**
   - **Descripción**: Calcula el ratio de Sharpe ajustado al marco temporal, que mide el rendimiento ajustado al riesgo.
   - **Retorno**: 
     - `float`: Valor del Sharpe Ratio ajustado al `timeFrame`.

#### Código de la clase: 
```python
class Metrics:
    def __init__(self, operations, timeFrame):
        self.operations = operations
        self.timeFrame = timeFrame

        # Convertir el campo 'entryTime' a tipo datetime si no lo es
        self.operations['entryTime'] = pd.to_datetime(self.operations['entryTime'])
        
        # Agrupar las operaciones por el timeframe
        if self.timeFrame == 'D':  # Daily
            self.operations['date'] = self.operations['entryTime'].dt.date
        elif self.timeFrame == 'W':  # Weekly
            self.operations['date'] = self.operations['entryTime'].dt.to_period('W')
        elif self.timeFrame == 'M':  # Monthly
            self.operations['date'] = self.operations['entryTime'].dt.to_period('M')
        
        # Agrupamos las ganancias por cada grupo de tiempo
        self.operationsGrouped = self.operations.groupby('date')['profitLoss'].sum().reset_index()

    def PnL(self):
        winnLossTotal = self.operationsGrouped['profitLoss'].sum()
        return winnLossTotal
    
    def winnLossTrades(self):
        winTrades = self.operations[self.operations['profitLoss'] > 0]
        lossTrades = self.operations[self.operations['profitLoss'] <= 0] 
        return lossTrades, winTrades
    
    def WLRratio(self):
        lossTrades, winTrades = self.winnLossTrades()
        winnLossRatio = len(winTrades) / max(1, len(lossTrades))
        return winnLossRatio
    
    def Pfactor(self):
        lossTrades, winTrades = self.winnLossTrades()
        profitFactor = winTrades['profitLoss'].sum() / abs(lossTrades['profitLoss'].sum())
        return profitFactor
    
    def drawDown(self):
        self.operationsGrouped['cumulativeProfit'] = self.operationsGrouped['profitLoss'].cumsum()
        maxDrawdown = self.operationsGrouped['cumulativeProfit'].cummax() - self.operationsGrouped['cumulativeProfit']
        maxDrawdown = maxDrawdown.max()
        return maxDrawdown
    
    def sharpeRatio(self): 
        sharpeRatio = self.operationsGrouped['profitLoss'] - 0.01 / self.operationsGrouped['profitLoss'].std()
        if self.timeFrame == 'D':  # Daily
            sharpeRatio = sharpeRatio * (252**(1/2))
        elif self.timeFrame == 'W':  # Weekly
            sharpeRatio = sharpeRatio * (52**(1/2))
        elif self.timeFrame == 'M':  # Monthly
            sharpeRatio = sharpeRatio * (12**(1/2))
        return sharpeRatio
