from backtrader_ib_insync import IBStore

def connectIBKR(host='127.0.0.1', port=7497, clientId=1):
    """
    Establece la conexión con Interactive Brokers usando la librería IB Insync.
    
    :param host: Dirección IP del servidor de IB (default '127.0.0.1')
    :param port: Puerto para la conexión (default 7497)
    :param clientId: ID del cliente para la conexión (default 1)
    :return: Un objeto IBStore para ser usado en Backtrader.
    """
    try:
        # Crear el store de IB para Backtrader
        ibstore = IBStore(host=host, port=port, clientId=clientId)
        print(f"Conexión establecida con Interactive Brokers en {host}:{port} con clientId {clientId}")
        return ibstore
    
    except Exception as e:
        print(f"Error al conectar con Interactive Brokers: {e}")
        return None
    
connectIBKR()