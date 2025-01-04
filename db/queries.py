from connection import createConnection, closeConnection, ejecuteQuery
import pandas as pd

def registerOperation(operationData):
    '''Inserta una operacion en la tabla "operations"'''
    conn = createConnection() # Nos conectamos a ola bd
    query ='''
    INSERT INTO operations(strategyName, symbol,
                orderType, quantity, entryPrice, exitPrice, entryTime, exitTime, profitLoss, notes)
    VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
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
            VALUES(?, ?, ?, ?, ?, ?, ?, ?)
            '''
    values = (
        metrics.startegyName,
        metrics.timestamp, 
        metrics.sharpeRatio,
        metrics.win_loss_ratio,
        metrics.profitFactor, 
        metrics.maxDrawdown,
        metrics.annualReturn,
        metrics.notes
    )

    # Ejecutamos consulta usando el cursor y pasando valores como parametros
    ejecuteQuery(conn, query, values)
    conn.commit()
    closeConnection()
    print('Metricas registradas con exito')

def getOPerations(strategyName):
    '''
    Recuperamos operaciones de la base de datos para una estrategia especifica.

    :param strategyName: Nombre de la estrategia.
    :return: DataFrame con los datos de las operaciones.
    '''
    conn = createConnection()
    query = '''SELECT * FROM operations WHERE strategyName = ?'''
    operations = ejecuteQuery(conn, query, (strategyName,)) # Obtenemos los registros de las operaciones
    closeConnection()

    # Convertimos los resultados en un DataFrame
    columns = ['strategyName', 'symbol', 'orderType', 
               'quantity', 'entryPrice', 'exitPrice', 
               'entryTime', 'exitTime', 'profitLoss', 'notes']
    
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
    columns = ['strategyName', 'timestamp', 'sharpeRatio', 'win_loss_ratio', 
               'profitFactor', 'maxDrawdown', 'annualReturn', 'notes']
                
    df = pd.DataFrame(metrics, columns=columns)
    return df
