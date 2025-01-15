# Entorno de ejecucion de sistemas de Trading

## Descripcion
Este proyecto es una plataforma para la ejecución de sistemas de trading algorítmico mediante una conexión directa con Interactive Brokers.  
Entre sus principales características se incluyen:  
- Registro de operaciones en una base de datos SQL para análisis en profundidad.  
- Generación de reportes automáticos en formato PDF y CSV de forma mensual, detallando el rendimiento de cada sistema.  
- Integración con **Backtrader**, una potente librería para el desarrollo y ejecución de estrategias de trading.  

Este entorno está diseñado para facilitar la automatización y el análisis de estrategias financieras, ofreciendo una solución robusta y escalable.

## Instalación
Antes de comenzar, asegúrate de tener instalado **Python 3.11.3**.

Sigue estos pasos para instalar las dependencias necesarias:  
1. Clona este repositorio en tu máquina local:  
   ```bash
   git clone https://github.com/joako-m-g/TradeEnv.git
   cd TradeEnv
    ```

## Uso
1. Coloca tus estrategias de trading personalizadas en el directorio `strategies`. Asegúrate de que estén implementadas siguiendo el formato requerido por `Backtrader`. 
`Nota`: Las estraegias deben tener dos atributos fijos correspondientes al simbolo que operan y al timeframe que operan.
Si el timeframe es:
- <= 1d --> timeframe = 'Daily'
- <= 1week --> timeframe = 'Week'
- <= 1month --> timeframe = 'Month'

2. Configura los parámetros de conexión a Interactive Brokers
    -   Host: `127.0.0.1`
    -   Puerto: `7497`(para paper trading)
    -   ID del cliente: `1`

3. Configura la API dentro de TWS indicando ID, puerto, etc.

4. Ejecuta el archivo principal del proyecto:
```bash
python main.py
```
5. Una vez ejecutado, la plataforma conectará tus estrategias con la cuenta de Interactive Brokers configurada y comenzará a registrar las operaciones en la base de datos.

Para mas informacion sobre el funcionamiento, puede consultar la correspondiente documentacion que se encuentra en cada carpeta del proyecto.

## Requisitos
- Pyhon 3.11.3
- TWS para conexion con IB
- Backtrader
- backtrader_ib_insync

## Licencia
Este proyecto está bajo la Licencia MIT - consulta el archivo [LICENSE](LICENSE) para más detalles.

## Créditos

- **Backtrader**: Para las estrategias de trading algorítmico.
- **backtrader_ib_insync**: Para la integración con Interactive Brokers. Este es un puente entre `Backtrader` y la libreria actual que se utiliza para esablecer una conexion con la API de IB `ib_insync`.
