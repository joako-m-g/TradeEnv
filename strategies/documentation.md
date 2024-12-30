# Documentación de carga de estrategias
## Directorio `strategies/__init__.py`

### Función `loadStrategies`
#### Descripción:
Esta función permite cargar dinámicamente todas las estrategias disponibles en el directorio `strategies/` y las almacena en un diccionario para su uso posterior. Esto facilita la modularidad y escalabilidad al permitir agregar nuevas estrategias sin necesidad de modificar el código base.

#### Parámetros: 
- **Ninguno**

#### Valor de retorno: 
- `strategies` (`dict`): Un diccionario donde las claves son los nombres de los archivos de las estrategias (sin la extensión `.py`) y los valores son los módulos importados correspondientes a cada estrategia.

#### Código de la función:
```python
def loadStrategies():
    '''
    Función para importar estrategias y almacenarlas en un diccionario.
    '''
    strategies = {}
    path = os.path.dirname(__file__)
    for file in os.listdir(path):  # Leemos todos los archivos en la carpeta
        if file.endswith('.py') and file != '__init__.py': 
            strategyName = file[:-3]
            # Importamos clase de la estrategia
            strategy = importlib.import_module(f'.{strategyName}', package='strategies')
            strategies[strategyName] = strategy
    return strategies