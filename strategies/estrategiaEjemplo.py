import backtrader as bt
from db.queries import registerOperation

class MovingAverageCrossStrategy(bt.Strategy):
    # Atributos fijos
    market = "Forex"
    timeframe = "Daily"

    def __init__(self):
        # Indicadores
        self.sma_fast = bt.indicators.SimpleMovingAverage(self.data.close, period=10)
        self.sma_slow = bt.indicators.SimpleMovingAverage(self.data.close, period=50)
        self.cross_signal = bt.indicators.CrossOver(self.sma_fast, self.sma_slow)

        # Diccionario para almacenar datos de operaciones
        self.operationData = {
            "strategyName": self.__class__.__name__,
            "symbol": None,
            "orderType": None,
            "quantity": None,
            "entryPrice": None,
            "exitPrice": None,
            "entryTime": None,
            "exitTime": None,
            "profitLoss": None,
            "timeframe": self.timeframe,
            "notes": None,
        }

        # Variables internas
        self.entry_order = None
        self.exit_order = None

    def log_operation_data(self):
        """Imprime los datos de la operación almacenados en operationData."""
        print("Operation Data:", self.operationData)

    def notify_order(self, order):
        """Notifica el estado de las órdenes."""
        if order.status in [order.Completed]:
            if order.isbuy():
                self.operationData["orderType"] = "Buy"
                self.operationData["entryPrice"] = order.executed.price
                self.operationData["entryTime"] = self.data.datetime.datetime()
            elif order.issell():
                self.operationData["exitPrice"] = order.executed.price
                self.operationData["exitTime"] = self.data.datetime.datetime()
                self.operationData["profitLoss"] = (self.operationData["exitPrice"] - self.operationData["entryPrice"]) * self.operationData["quantity"]
                self.operationData["notes"] = "Operation completed successfully."
                self.log_operation_data()
                registerOperation(self.operationData)

    def next(self):
        """Lógica principal de la estrategia."""
        if not self.position:  # Si no hay posición abierta
            if self.cross_signal > 0:  # Señal de compra
                self.operationData["symbol"] = self.data._name
                self.operationData["quantity"] = 100  # Cantidad fija para este ejemplo
                self.entry_order = self.buy(size=self.operationData["quantity"])
        else:  # Si ya hay una posición abierta
            if self.cross_signal < 0:  # Señal de venta
                self.exit_order = self.sell(size=self.operationData["quantity"])
