# Documentacion de conexion a INKR
## Directorio `connectors/ibkrConnector.py`

### Funcion `connectIBKR`
#### Descripcion:
En esta funcion lo que hacemos es establecer una conexion con una cuenta de Interactive Brokers para posteriormente realizar operaciones en la misma. 

#### Parametros: 
- `host` (`str`): Dirección IP o el nombre de dominio del servidor de Interactive Brokers al que deseas conectarte.
- `port` (`int`): Puerto a través del cual se realiza la conexión con el servidor de Interactive Brokers. El valor por defecto es 7497, que es el puerto estándar utilizado para conectarse a TWS en modo "paper trading" (simulación). Para IB Gateway o conexiones reales, podría ser 7496.
- `clientId` (`int`): Identificador único para la sesión de conexión que estás estableciendo con Interactive Brokers.

#### Valor de retorno: 
- `ibbroker`(objeto `IBBroker`): Objeto de tipo `IBBroker` para su uso con backtrader
- `None`: En caso de no poder establecer la conexion devolvemos `None`

#### Codigo de la funcion:
```python 
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


```