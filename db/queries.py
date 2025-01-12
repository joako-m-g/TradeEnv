from connection import createConnection, closeConnection, ejecuteQuery
import pandas as pd
import datetime

def registerOperation(operationData):
    '''Inserta una operacion en la tabla "operations"'''
    conn = createConnection() # Nos conectamos a ola bd
    query ='''
    INSERT INTO operations(strategyName, symbol,
                orderType, quantity, entryPrice, exitPrice, entryTime, exitTime, profitLoss, timeframe, notes)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
    # Tuplas con los valores de los atributos de la clase
    values = (
        operationData.strategyName,
        operationData.symbol,
        operationData.orderType,
        operationData.quantity,
        operationData.entryPrice,
        operationData.exitPrice,
        operationData.entryTime,
        operationData.exitTime,
        operationData.profitLoss,
        operationData.timeframe,
        operationData.notes
    )

    # Ejecutamos consulta usando el cursor y pasando valores como parametros
    ejecuteQuery(conn, query, values)
    conn.commit()
    closeConnection()
    print('Operacion registrada con exito')

def registerMetrics(metrics):
    '''Inserta metricas en la tabla "metrics"'''
    conn = createConnection() # Nos conectamos a ola bd
    query = '''INSERT INTO metrics(strategyName, timestamp, sharpeRatio, win_loss_ratio, profitFactor, maxDrawdown, annualReturn, notes)
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            '''
    values = (
        metrics.startegyName,
        datetime.datetime.now(), 
        metrics.sharpeRatio,
        metrics.lossTrades,
        metrics.winTrades,
        metrics.win_loss_ratio,
        metrics.profitFactor, 
        metrics.maxDrawdown,
        metrics.annualReturn,
        metrics.PnL,
        metrics.PnLmean,
        metrics.notes
    )

    # Ejecutamos consulta usando el cursor y pasando valores como parametros
    ejecuteQuery(conn, query, values)
    conn.commit()
    closeConnection()
    print('Metricas registradas con exito')

def getOPerations(strategyName, startPeriod, endPeriod):
    '''
    Recuperamos operaciones de la base de datos para una estrategia especifica.

    :param strategyName: Nombre de la estrategia.
    :return: DataFrame con los datos de las operaciones.
    '''
    conn = createConnection()
    query = '''SELECT * FROM operations WHERE strategyName = ? AND entryPrice >= ? AND entryPrice < ?'''
    operations = ejecuteQuery(conn, query, (strategyName, startPeriod, endPeriod)) # Obtenemos los registros de las operaciones
    closeConnection()

    # Convertimos los resultados en un DataFrame
    columns = ['strategyName', 'symbol', 'orderType', 
               'quantity', 'entryPrice', 'exitPrice', 
               'entryTime', 'exitTime', 'profitLoss', 'timeframe', 'notes']
    
    df = pd.DataFrame(operations, columns=columns)
    return df

def getMetrics(strategyName, startPeriod, endPeriod):
    '''Funcion para consultar metricas de la estrategia "strategyName"
    :param strategyName: Nombre de la estrategia
    :return: DataFrame con los datos de las operaciones
    '''
    conn = createConnection()
    query = '''Select * FROM metrics WHERE strategyName = ? AND timestamp > ? AND timestamp < ?'''
    metrics = ejecuteQuery(conn, query, (strategyName, startPeriod, endPeriod))
    closeConnection()

    # Convertiumos los resultados en un DataFrame
    columns = ['strategyName', 'timestamp', 'sharpeRatio', 'lossTrades', 'winTrades', 
               'win_loss_ratio', 'profitFactor', 'maxDrawdown', 'annualReturn', 'PnL', 'PnLmean', 'notes']
                
    df = pd.DataFrame(metrics, columns=columns)
    return df # Retornamos df de metricas
