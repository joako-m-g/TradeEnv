# `loadStrategies` Function Documentation

## Descripción

La función `loadStrategies` se encarga de importar todas las estrategias disponibles en el directorio de estrategias y almacenarlas en un diccionario. Esta función recorre todos los archivos `.py` en el directorio, importa el contenido de cada archivo como un módulo, y guarda cada estrategia en un diccionario con el nombre del archivo (sin la extensión `.py`) como clave.

## Funcionamiento

1. **Obtención del Path**:
   - La función obtiene la ruta del directorio actual mediante `os.path.dirname(__file__)`, que retorna la ruta donde se encuentra el archivo que está ejecutando la función.

2. **Recorrido del Directorio**:
   - Se recorre todos los archivos del directorio actual mediante `os.listdir(path)`. Esto permite identificar todos los archivos presentes en el directorio.

3. **Filtrado de Archivos `.py`**:
   - La función filtra los archivos para seleccionar solo aquellos que terminan en `.py` (archivos de Python) y que no son el archivo `__init__.py`, ya que este último no representa una estrategia.

4. **Importación Dinámica**:
   - Para cada archivo identificado, se utiliza `importlib.import_module` para importar el módulo correspondiente. El nombre del módulo se obtiene quitando la extensión `.py` al nombre del archivo.
   
5. **Almacenamiento de Estrategias**:
   - Cada módulo importado (estrategia) se guarda en el diccionario `strategies`, donde la clave es el nombre de la estrategia y el valor es el módulo importado.

## Parámetros

- **Ninguno**: No recibe parámetros.

## Retorno

La función retorna un diccionario llamado `strategies`, donde cada clave es el nombre de una estrategia (nombre del archivo sin la extensión `.py`), y el valor es el módulo importado correspondiente a esa estrategia.

## Ejemplo de Uso

```python
# Llamada a la función para cargar las estrategias
strategies = loadStrategies()

# Acceder a una estrategia específica
print(strategies['strategy_name'])
