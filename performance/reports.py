import pandas as pd

class Reports:
    def __init__(self, metrics):
        '''
        :param metrics: DataFrame con metricas de rendimiento
        '''
        self.metrics = metrics
    
    def createCSV(self, title):
        # Pasamos a CSV el DataFrame de metricas
        self.metrics.to_csv(f'TradeEnv/reports/{title}.csv', index=False, encoding='utf-8')
        print('Reporte creado exitosamente')

    def createPDF(self, title):
        pass