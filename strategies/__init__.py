import os
import importlib

def loadStrategies():
    '''
    Funcion para importar estrategias y almacenarlas en un diccionario
    '''
    strategies = {}
    path = os.path.dirname(__file__)
    for file in os.listdir(path): # Leemos todos los archivos en la carperta
        if file.endswith('.py') and file != '__init__.py': 
            strategyName = file[:-3]
            # Importamos clase de la estrategia
            srategy = importlib.import_module(f'.{strategyName}', package='straegies')
            strategies[strategyName] = srategy
    return strategies


