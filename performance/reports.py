from fpdf import FPDF
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
import os
import numpy as np

class Reports:
    def __init__(self, metrics, operations, title):
        '''
        :param metrics: DataFrame con metricas de rendimiento
        '''
        self.metrics = metrics
        self.operations = operations
        self.title = title
    
    def createCSV(self, title):
        # Pasamos a CSV el DataFrame de metricas
        self.metrics.to_csv(f'TradeEnv/reports/{self.title}.csv', index=False, encoding='utf-8')
        print('Reporte creado exitosamente')

    def meansTable(self):
        df = self.metrics.copy()
        df = df.drop(['id', 'strategyName', 'timestamp', 'notes'], axis=1)
        averages = df.mean()
        return averages

    def plotMetrics(self):
        # Crear una figura
        plt.figure(figsize=(12, 6))
        # Asegúrate de que 'timestamp' está en formato datetime
        self.metrics['timestamp'] = pd.to_datetime(self.metrics['timestamp'])

        for metric in ['sharpeRatio', 'win_loss_ratio', 'profitFactor', 'maxDrawdown', 'annualReturn', 'PnL']:
            plt.plot(self.metrics['timestamp'], self.metrics[f'{metric}'], label='Sharpe Ratio')
            plt.gca().xaxis.set_major_locator(mdates.AutoDateLocator())
            plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
            plt.xticks(rotation=45)
            plt.xlabel('TimeStamp')
            plt.ylabel(f'{metric}')
            plt.title(f'{metric.replace("_", " ")}')
            plt.tight_layout()

            plt.savefig(f'reports/{self.title}_{metric}_plot.png')
            plt.close()  # Cerrar la figura para liberar memoria

    def operationsHistogram(self):
        '''Nota: Esta funcion recibe df de operaciones, no de metricas.'''
        # Convertir a datetime si es necesario
        self.operations['entryTime'] = pd.to_datetime(self.operations['entryTime'])

        # Crear una columna con el día de la semana
        self.operations['dayOfWeek'] = self.operations['entryTime'].dt.day_name()
        
        # Contar operaciones por día de la semana
        operationsCount = self.operations['dayOfWeek'].value_counts()
        
        # Ordenar por el orden natural de los días de la semana
        dayOrder = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        operationsCount = operationsCount.reindex(dayOrder, fill_value=0)
        #operationsCountMean = operationsCount.mean()
        
        # Crear el histograma
        plt.figure(figsize=(10, 6))
        pd.Series(operationsCount).plot(kind='bar', color='skyblue', edgecolor='black')
        plt.title('Histograma de Operaciones por Día de la Semana')
        plt.xlabel('Día de la Semana')
        plt.ylabel('Cantidad de Operaciones')
        plt.xticks(rotation=45)
        plt.tight_layout()
        
        # Guardar el gráfico
        plt.savefig(f'reports/{self.title}_operationsDays_histogram.png', format='png')
        plt.close()
        print('Histograma de operaciones generado exitosamente.')

    def plotPieChart(self):
        winTrades, lossTrades = self.metrics.loc[self.metrics.index[-1], 'winTrades'], self.metrics.loc[self.metrics.index[-1], 'lossTrades']
        data = [winTrades, lossTrades]
        labels = ['Ganadoras', 'Perdedoras']
        colors = ['#4CAF50', '#F44336']  # Verde para ganadoras, rojo para perdedoras

        # Crear el gráfico de pastel
        plt.figure(figsize=(6, 6))
        plt.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors, wedgeprops={'edgecolor': 'black'})
        plt.title('Comparación de Operaciones: Ganadoras vs Perdedoras', fontsize=14)
        plt.tight_layout()

        # Guardar o mostrar el gráfico
        plt.savefig(f'reports/{self.title}_pie_chart_operations.png', format='png')  # Guardar en archivo
        plt.close()

    def createPDF(self):
        pdf = FPDF()
        pdf.set_auto_page_break(auto=True, margin=15)
        pdf.add_page()

        # Rótulo principal
        pdf.set_font('Arial', 'B', 20)
        pdf.cell(0, 10, 'Análisis de Desempeño en Trading Algorítmico', align='C', ln=True)
        pdf.ln(10)

        # Texto introductorio
        pdf.set_font('Arial', '', 12)
        intro_text = (
            "Este informe presenta un análisis detallado de las métricas de desempeño generadas "
            f"por nuestra estrategia de trading algorítmico '{self.title}'. A lo largo del documento, se incluyen "
            "promedios clave de las métricas analizadas, gráficos que ilustran la evolución temporal de "
            "estas métricas, y una distribución visual de las operaciones por día de la semana. Además, "
            "se incorpora un análisis de la proporción de operaciones ganadoras frente a perdedoras. "
            "Este reporte tiene como objetivo brindar una visión clara y general sobre el desempeño de la estrategia."
            "Nota: Las metricas se encuentran anualizadas segun el marco temporal en el que opera la estrategia."
        )
        pdf.multi_cell(0, 10, intro_text, align='C')
        pdf.ln(10)

        # Tabla de promedios
        averages = self.meansTable()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Promedios de las Métricas', align='C', ln=True)
        pdf.ln(10)

        pdf.set_font('Arial', '', 12)
        for metric, avgValue in averages.items():
            pdf.cell(100, 10, f'{metric.replace("_", " ").capitalize()}', border=1, align='C')
            pdf.cell(80, 10, f'{avgValue:.2f}', border=1, align='C')
            pdf.ln()

        # Gráficos de evolución temporal
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Evolucion Temporal de las Metricas', align='C', ln=True)
        pdf.ln(10)
        self.plotMetrics()

        x_center = (210 - 150) / 2  # Centrar gráficos horizontalmente (A4 = 210mm ancho)
        y_position = 30
        max_height = 277

        for plot in sorted(os.listdir('reports')):
            if plot.endswith(('.png', '.jpg', '.jpeg')):
                if y_position + 90 > max_height:
                    pdf.add_page()
                    y_position = 30
                pdf.image(f'reports/{plot}', x=x_center, y=y_position, w=150)
                y_position += 110

        # Histograma de operaciones
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Distribucion de Operaciones por Semana', align='C', ln=True)
        pdf.ln(10)
        self.operationsHistogram()

        y_position = 30
        pdf.image(f'reports/{self.title}_operationsDays_histogram.png', x=x_center, y=y_position, w=150)
        y_position += 110

        # Gráfico de pie de operaciones
        pdf.add_page()
        pdf.set_font('Arial', 'B', 14)
        pdf.cell(0, 10, 'Operaciones Ganadoras vs Perdedoras', align='C', ln=True)
        pdf.ln(10)
        self.plotPieChart()

        y_position = 30
        pdf.image(f'reports/{self.title}_pie_chart_operations.png', x=x_center, y=y_position, w=150)

        # Guardar el PDF
        pdf.output(f'reports/{self.title}_informeDesempeño.pdf')
        print('Reporte PDF creado exitosamente')

data = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'strategyName': ['Estrategia Única'] * 10,
    'timestamp': [
        '2025-01-01 12:00:00', '2025-01-02 14:30:00', '2025-01-03 09:15:00', 
        '2025-01-04 11:00:00', '2025-01-05 15:45:00', '2025-01-06 10:30:00',
        '2025-01-07 14:00:00', '2025-01-08 13:30:00', '2025-01-09 09:00:00', 
        '2025-01-10 16:20:00'
    ],
    'sharpeRatio': [1.45, 2.10, 1.75, 1.60, 1.85, 2.05, 1.95, 2.15, 1.80, 1.90],
    'win_loss_ratio': [1.8, 2.2, 1.9, 1.6, 2.1, 1.8, 2.0, 1.9, 2.0, 2.3],
    'profitFactor': [1.7, 2.0, 1.8, 1.9, 2.0, 1.6, 1.8, 2.1, 1.9, 2.0],
    'maxDrawdown': [-12.5, -10.0, -13.0, -11.5, -9.5, -10.5, -12.0, -11.0, -9.0, -10.0],
    'annualReturn': [15.2, 18.0, 16.5, 17.0, 19.5, 14.0, 18.5, 17.8, 16.2, 20.0],
    'notes': [
        'Buena performance en mercados laterales.',
        'Adecuado para tendencias fuertes.',
        'Funciona mejor en alta volatilidad.',
        'Rendimiento estable en mercados en rango.',
        'Excelente en tendencias alcistas.',
        'Poco eficiente en mercados de baja volatilidad.',
        'Alta eficiencia en mercados volátiles.',
        'Buena relación riesgo/beneficio.',
        'Estrategia balanceada, adecuada para todo tipo de mercado.',
        'Excelente performance en mercados de fuerte tendencia.'
    ]
}

data_operations = {
    'id': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'strategyName': ['Estrategia Única'] * 10,
    'symbol': ['AAPL', 'TSLA', 'GOOG', 'AMZN', 'MSFT', 'NFLX', 'META', 'NVDA', 'AMD', 'BABA'],
    'orderType': ['Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell', 'Buy', 'Sell'],
    'quantity': [100, 150, 200, 250, 180, 130, 170, 220, 160, 140],
    'entryPrice': [150.00, 650.00, 2700.00, 3300.00, 280.00, 550.00, 330.00, 240.00, 140.00, 200.00],
    'exitPrice': [155.00, 640.00, 2750.00, 3350.00, 290.00, 530.00, 340.00, 250.00, 150.00, 190.00],
    'entryTime': [
        '2025-01-01 09:00:00', '2025-01-02 11:30:00', '2025-01-03 13:15:00', 
        '2025-01-04 10:45:00', '2025-01-05 14:20:00', '2025-01-06 15:10:00', 
        '2025-01-07 12:00:00', '2025-01-08 09:30:00', '2025-01-09 10:00:00', 
        '2025-01-10 14:00:00'
    ],
    'exitTime': [
        '2025-01-01 15:00:00', '2025-01-02 13:30:00', '2025-01-03 14:45:00', 
        '2025-01-04 17:00:00', '2025-01-05 16:00:00', '2025-01-06 17:30:00', 
        '2025-01-07 15:30:00', '2025-01-08 14:00:00', '2025-01-09 12:30:00', 
        '2025-01-10 16:30:00'
    ],
    'profitLoss': [500, -1500, 10000, 12500, 1800, -2600, 6800, 2200, 1600, -1400],
    'notes': [
        'Operación exitosa, buen movimiento en tendencia.',
        'Operación cerrada con pérdidas debido a la volatilidad.',
        'Buena ganancia en un movimiento alcista.',
        'Beneficio alto por fuerte tendencia alcista.',
        'Ganancia moderada en tendencia alcista.',
        'Pérdida por salida prematura.',
        'Excelente rendimiento en una acción volátil.',
        'Buena relación riesgo/recompensa en operación.',
        'Operación balanceada, cierre adecuado.',
        'Pérdida por movimiento inesperado del mercado.'
    ]
}

df = pd.DataFrame(data)
# Agregar las columnas de winTrades y lossTrades con valores inventados
df['PnL'] = [10, 20, 30, 12, 24, 20, 5, 35, 67, 70]
df['winTrades'] = [50, 75, 60, 45, 80, 55, 70, 65, 68, 85]  # Ejemplo de número de operaciones ganadoras
df['lossTrades'] = [20, 15, 18, 25, 10, 22, 18, 20, 15, 12]  # Ejemplo de número de operaciones perdedoras

df_op = pd.DataFrame(data_operations)
a = Reports(df, df_op, 'puta')
a.createPDF()
a.operationsHistogram()
a.plotPieChart()
