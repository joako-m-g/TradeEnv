from connection import createConnection, closeConnection, ejecuteQuery

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
    query = '''INSERT INTO metrics(strategyName, sharpeRatio, win_loss_ratio, profitFactor, maxDrawdown, annualReturn, notes)
            VALUES(?, ?, ?, ?, ?, ?, ?)
            '''
    values = (
        metrics.startegyName,
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
