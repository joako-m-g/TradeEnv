import pandas as pd

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
        # Calculamos el retorno hasta este punto
        winnLossTotal = self.operationsGrouped['profitLoss'].sum()
        winnlosstotalMean = self.operationsGrouped['profitLoss'].mean()
        return winnLossTotal, winnlosstotalMean
    
    def winnLossTrades(self):
        winTrades = self.operations[self.operations['profitLoss'] > 0]
        lossTrades = self.operations[self.operations['profitLoss'] <= 0] 
        return len(winTrades), len(lossTrades)
    
    def WLRratio(self):
        lenLossTrades, lenWinTrades = self.winnLossTrades()
        winnLossRatio = lenWinTrades / max(1, lenLossTrades)
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
    
    def annualReturn(self, initialCapital=1):
        # Calculamos el retorno acumulado total
        totalReturn = self.operationsGrouped['profitLoss'].sum()

        # Calculamos la cantidad de períodos (grupos de tiempo) en el data set
        numPeriods = len(self.operationsGrouped)

        # Determinamos la frecuencia anual en función del timeFrame
        if self.timeFrame == 'D':  # Diario
            annualFreq = 252
        elif self.timeFrame == 'W':  # Semanal
            annualFreq = 52
        elif self.timeFrame == 'M':  # Mensual
            annualFreq = 12
        else:
            raise ValueError("TimeFrame no soportado para cálculo anualizado.")

        # Calculamos el retorno anualizado
        annualizedReturn = (1 + totalReturn / initialCapital) ** (annualFreq / numPeriods) - 1
        return annualizedReturn
