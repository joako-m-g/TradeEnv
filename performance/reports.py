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
    
    def createCSV(self):
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
            "Este reporte tiene como objetivo brindar una visión clara y general sobre el desempeño de la estrategia. "
            "Nota: Las métricas se encuentran anualizadas según el marco temporal en el que opera la estrategia."
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

if __name__ == "__main__":
    # Generar datos simulados para métricas no estacionarias y no estrictamente tendenciales
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=50, freq="D")

    # Fluctuaciones aleatorias y un componente cíclico para simular series no estacionarias
    sharpe_ratio = np.sin(np.linspace(0, 10, 50)) + np.random.normal(0, 0.2, 50)  # Componente cíclico + ruido
    win_loss_ratio = np.cos(np.linspace(0, 10, 50)) + np.random.normal(0, 0.3, 50)  # Componente cíclico + ruido
    profit_factor = np.sin(np.linspace(0, 20, 50)) + np.random.normal(0, 0.4, 50)  # Componente cíclico + ruido
    max_drawdown = np.random.uniform(-0.2, -0.05, 50) + np.random.normal(0, 0.05, 50)  # Ruido con fluctuaciones
    annual_return = np.random.uniform(0.05, 0.2, 50) + np.random.normal(0, 0.05, 50)  # Ruido con fluctuaciones
    pnl = np.random.uniform(3000, 9000, 50) + np.random.normal(0, 500, 50)  # Valores aleatorios con ruido

    # Datos de métricas no estacionarias y no estrictamente tendenciales
    metrics_data = {
        "id": range(1, 51),
        "strategyName": ["SMACross"] * 50,
        "timestamp": dates,
        "sharpeRatio": sharpe_ratio,
        "win_loss_ratio": win_loss_ratio,
        "profitFactor": profit_factor,
        "maxDrawdown": max_drawdown,
        "annualReturn": annual_return,
        "PnL": pnl,
        "winTrades": np.random.randint(20, 80, 50),
        "lossTrades": np.random.randint(10, 50, 50),
        "notes": ["" for _ in range(50)]
    }
    metrics_df = pd.DataFrame(metrics_data)

    # Generar datos simulados para operaciones con fluctuaciones cíclicas
    operations_data = {
        "entryTime": pd.date_range(start="2023-01-01", periods=50, freq="D"),
        "exitTime": pd.date_range(start="2023-01-02", periods=50, freq="D"),
        "PnL": np.sin(np.linspace(0, 10, 50)) + np.random.normal(0, 200, 50),  # Componente cíclico + ruido
        "notes": ["" for _ in range(50)]
    }
    operations_df = pd.DataFrame(operations_data)

    # Crear el reporte
    report_title = "SMACross"
    report = Reports(metrics_df, operations_df, report_title)

    # Crear CSV, PDF y gráficos
    #report.createCSV()
    report.createPDF()
    print("Informe generado correctamente.")