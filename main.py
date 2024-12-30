from strategies import loadStrategies
from connectors import connectIBKR
import backtrader as bt


def runStrategy(strategyName):
    '''
    Cargamos y ejecutamos estrategia en IB
    '''
    # Nos conectamos a IBKR
    ibstore = connectIBKR(host='127.0.0.1', port=7497, clientId=1)
    if ibstore is None:
        print('Error al conectar a IBKR')
        return
    
    # Configuramos cerebro
    cerebro = bt.Cerebro()

    # Seleccionamos la estrategia del diccionario
    strategy = loadStrategies()[strategyName]
    cerebro.addstrategy(strategy)

    # Configuramos el broker
    cerebro.setbroker(ibstore.getbroker())

    # Ejecutar la estrategia
    print(f"Ejecutando la estrategia: {strategyName}")
    cerebro.run()

if __name__ == '__main__':
    # Ejecutar la estrategia dummy 'strategy_1'
    runStrategy('strategy_1')