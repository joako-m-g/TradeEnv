-- Tabla para registrar operaciones
CREATE TABLE operations (
    id INT PRIMARY KEY AUTOINCREMENT, -- ID unico para cada operacion
    strategyName TEXT NOT NULL, -- Nombre de la estrategia
    symbol TEXT NOT NULL, -- Simbolo
    orderType TEXT NOT NULL, -- Tipo de orden
    quantity REAL NOT NULL, -- Cantidad operada
    entryPrice REAL NOT NULL, -- Precio de entrada
    exitPrice REAL, -- Precio de salida (puede ser NULL si todavia esta abierta)
    entryTime TIMESTAMP NOT NULL, -- Fecha y hora de entrada
    exitTime TIMESTAMP, -- Fecha y hora de salida
    profitLoss REAL, -- Ganancia o perdida de la operacion
    notes TEXT, -- Notas opcionales de la operacion
);

-- Tabla para registrar metricas de rendimiento
CREATE TABLE metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,  -- ID único para cada registro de métricas
    strategyName TEXT NOT NULL,           -- Nombre de la estrategia
    sharpeRatio REAL,                     -- Ratio de Sharpe
    win_loss_ratio REAL,                   -- Win/Loss ratio
    profitFactor REAL,                    -- Factor de ganancia (ganancias totales / pérdidas totales)
    maxDrawdown REAL,                     -- Máximo drawdown (%)
    annualReturn REAL,                    -- Retorno anualizado (%)
    notes TEXT                             -- Notas opcionales
);

