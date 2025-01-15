import time
import threading
import backtrader as bt
from connectors.ibkrConnector import connectIBKR
from strategies import loadStrategies
from performance.metrics import Metrics
from performance.reports import Reports
from db.queries import getOPerations, registerMetrics, getMetrics
from db.connection import createConnection, createTables, closeConnection
from datetime import datetime, timedelta


class TradingEnvironment:
    def __init__(self):
        self.cerebro = bt.Cerebro()
        self.ibkrConnection = None
        self.dbConnection = None

    def initialize(self):
        # Conexión a IBKR
        self.ibkrConnection = connectIBKR()
        
        # Configuración de la base de datos
        self.dbConnection = createConnection()
        if self.dbConnection:
            print('Conexión establecida con la BD correctamente')
            createTables(self.dbConnection)
            print('Tablas creadas correctamente')
            closeConnection(self.dbConnection)
        
        # Conexión con IBKR Store
        ibstore = connectIBKR()
        
        # Cargar estrategias
        strategies = loadStrategies()
        print('Estrategias cargadas correctamente')
        
        # Configurar estrategias en Cerebro (agregamos todas las estrategias del diccionario)
        for key in strategies.keys():
            self.cerebro.addstrategy(strategies[key])
            broker = ibstore.getbroker()
            self.cerebro.setbroker(broker)
            market = strategies[key].market
            print('Estrategia agregada al cerebro')
            timeframe = strategies[key].timeframe
            ibdata = ibstore.getdata
            datakwargs = dict(
                timeframe=bt.TimeFrame.TFrame(timeframe),
                compression=1,
                historical=False,
                rtbar=True,
                qcheck=1,
                backfill_start=True,
                backfill=True,
                latethrough=True,
                tz=None,
                useRTH=False,
                hist_tzo=None,
            )
            data = ibdata(dataname=market, **datakwargs)
            self.cerebro.adddata(data)
            print('Data agregada al cerebro')

    def run(self):
        print('Iniciando Backtrader...')
        self.cerebro.run()

class MetricsUpdater:
    def __init__(self, dbConnection, dayInerval=1, weekInterval=7, monthInterval=30):
        self.dbConnection = dbConnection
        self.dayInterval = dayInerval
        self.weekInterval = weekInterval
        self.monthInterval = monthInterval
        self.running = False
        self.strategies = loadStrategies()
        self.starTime = datetime.now()
        self.lastTimeDay = datetime.now()
        self.lastTimeWeek = datetime.now()
        self.lastTimeMonth = datetime.now()

    def start(self):
        '''Inicia bucle'''
        if not self.running:
            self.running = True
            self._startUpdaterThread()

    def stop(self):
        '''Detiene el bucle'''
        self.running = False

    def _startUpdaterThread(self):
        updaterThread = threading.Thread(target=self._updateMetricsLoop)
        updaterThread.daemon = True  # Permite que el hilo termine cuando termine el programa principal
        updaterThread.start()

    def _updateMetricsLoop(self):
        '''Bucle que consulta a la bd operaciones de a intervalos regulares'''
        print("Hilo iniciado: comenzando bucle de métricas...")
        while self.running:
            now = datetime.now()
            print(f'Fecha y hora: {datetime.now()}')

            # Verificamos si ha pasado el intervalo diario
            if (now - self.lastTimeDay).days >= self.dayInterval:
                self.updateMetrics(now, 'Daily')
                self.lastTimeDay = now

            # Verificamos si ha pasado el intervalo semanal
            if (now - self.lastTimeWeek).days >= self.weekInterval:
                self.updateMetrics(now, 'Week')
                self.lastTimeWeek = now

            # Verificamos si ha pasado el intervalo mensual
            if (now - self.lastTimeMonth).days >= self.monthInterval:
                self.updateMetrics(now, 'Month')
                self.createReport(now)
                self.lastTimeMonth = now

            # Esperar un poco antes de la siguiente verificación
            time.sleep(60)  # Esperamos 1 minuto antes de verificar nuevamente

    def updateMetrics(self, currentTime, timeFrame):
        '''Calcculamos metricas del ultimo periodo transcurrido'''
        print('Calculando metricas...')
        # Creamos lista de las estraegias de mi diccionario que tienen el mismo 'timeFrame'
        listStrategies = [key for key in self.strategies.keys() if self.strategies[key].timeframe == timeFrame]
        for strategy in listStrategies:
            if self.strategies[strategy].timeframe == 'Daily':
                interval = self.dayInerval
            elif self.strategies[strategy].timeframe == 'Week':
                interval = self.weekInterval
            elif self.strategies[strategy].timeframe == 'Month':
                interval = self.monthInterval
            operations = getOPerations(self.strategies[strategy], currentTime - timedelta(days=interval), currentTime)
            metrics = Metrics(operations, self.strategies[strategy].timeframe)
            metricas = {
                'PnL' : metrics.PnL(), # Retornos netos
                'lossTrades' : metrics.winnLossTrades()[1], # Trades perdedores
                'winTrades' : metrics.winnLossTrades()[0], # Trades ganadores
                'WLRratio' : metrics.WLRratio(), # Win Loss ratio
                'Pfactor' : metrics.Pfactor(), # Factor profit
                'maxDrawdown' : metrics.drawDown(), # Drawdown %
                'sharpeRatio' : metrics.sharpeRatio(), # Raio de sharpe anualizado
                'annualReturn' : metrics.annualReturn(), # Retornos anualizados
                'strategyName' : strategy, # Nombre de la estrategia
                'notes' : '-' 
            }
        registerMetrics(metricas) # Registramos metricaas en la BD
        print('Mericas calculadas exitosamente')

    def createReport(self, currentTime):
        print('Creando reporte mensual de las estrategias...')
        for strategy in self.strategies.keys():
            # Obtenemos metricas y operaciones del ultimo mes
            operations = getOPerations(strategy, currentTime - timedelta(days=self.monthInterval), currentTime)
            metrics = getMetrics(strategy, currentTime - timedelta(days=self.monthInterval), currentTime)
            reports = Reports(metrics, operations, strategy)
            reports.createCSV() # Creamos CSV de las metricas del ultimo mes
            reports.createPDF() # Creamos PDF con los rendimientos del ultimo mes
        print('Reportes creados exitosamente')

if __name__ == "__main__":
    try:
        # Inicializamos el entorno de trading
        tradingEnvironment = TradingEnvironment()
        tradingEnvironment.initialize()
        tradingEnvironment.run()

        # Iniciamos la actualización de métricas
        dbConnection = createConnection()
        metricsUpdater = MetricsUpdater(dbConnection)
        metricsUpdater.start()

        # Mantenemos el programa en ejecución
        print("Programa en ejecución. Presiona Ctrl+C para detener.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Programa detenido por el usuario.")
        metricsUpdater.stop()
    finally:
        print("Finalizando programa.")