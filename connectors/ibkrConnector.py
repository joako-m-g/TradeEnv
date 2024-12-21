import backtrader as bt
from backtrader import brokers


def connectIBKR(host='127.0.0.1', port=7497, clientId=1):
    """
    Establece la conexión con Interactive Brokers.

    :param host: Dirección IP del servidor de IB (default '127.0.0.1')
    :param port: Puerto para la conexión (default 7497)
    :param clientId: ID del cliente para la conexión (default 1)
    :return: Un objeto IBBroker para ser usado en Backtrader.
    """
    try:
        # Crear el broker y establecer la conexión
        ibbroker = brokers.IBBroker(host=host, port=port, clientId=clientId)
        print(f"Conexión establecida con Interactive Brokers en {host}:{port} con clientId {clientId}")
        return ibbroker
    except Exception as e:
        print(f"Error al conectar con Interactive Brokers: {e}")
        return None

