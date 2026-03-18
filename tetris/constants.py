# Dimensiones del tablero 
COLS = 10
ROWS = 20
CELL_SIZE = 35

# Dimensiones de la ventana 
SIDEBAR_WIDTH = 200
SCREEN_WIDTH = COLS * CELL_SIZE + SIDEBAR_WIDTH
SCREEN_HEIGHT = ROWS * CELL_SIZE

FPS = 60

# Colores en formao RGB
BLACK      = (0,   0,   0)
WHITE      = (255, 255, 255)
GRAY       = (40,  40,  40)
DARK_GRAY  = (20,  20,  20)
LIGHT_GRAY = (100, 100, 100)

# Colores de los bloques
COLORS = {
    "I": (0,   240, 240),   # Cian
    "O": (240, 240,   0),   # Amarillo
    "T": (160,   0, 240),   # Morado
    "S": (0,   240,   0),   # Verde
    "Z": (240,   0,   0),   # Rojo
    "J": (0,     0, 240),   # Azul
    "L": (240, 160,   0),   # Naranja
}

# Formas de los bloques con coordenadas relativas, con las rotaciones posibles de cada forma
SHAPES = {
    "I": [
        [[0,0],[0,1],[0,2],[0,3]],
        [[0,0],[1,0],[2,0],[3,0]],
    ],
    "O": [
        [[0,0],[0,1],[1,0],[1,1]],
    ],
    "T": [
        [[0,1],[1,0],[1,1],[1,2]],
        [[0,0],[1,0],[2,0],[1,1]],
        [[0,0],[0,1],[0,2],[1,1]],
        [[0,1],[1,1],[2,1],[1,0]],
    ],
    "S": [
        [[0,1],[0,2],[1,0],[1,1]],
        [[0,0],[1,0],[1,1],[2,1]],
    ],
    "Z": [
        [[0,0],[0,1],[1,1],[1,2]],
        [[0,1],[1,0],[1,1],[2,0]],
    ],
    "J": [
        [[0,0],[1,0],[1,1],[1,2]],
        [[0,0],[0,1],[1,0],[2,0]],
        [[0,0],[0,1],[0,2],[1,2]],
        [[0,1],[1,1],[2,0],[2,1]],
    ],
    "L": [
        [[0,2],[1,0],[1,1],[1,2]],
        [[0,0],[1,0],[2,0],[2,1]],
        [[0,0],[0,1],[0,2],[1,0]],
        [[0,0],[0,1],[1,1],[2,1]],
    ],
}

# Puntajes por líneas eliminadas
SCORE_TABLE = {1: 100, 2: 300, 3: 500, 4: 800}

# Velocidad del juego (en milisegundos)
INITIAL_SPEED = 500        
SPEED_INCREMENT = 30       # ms que se resta por nivel
MIN_SPEED = 80             
LINES_PER_LEVEL = 10       # Cantidad de líneas para subir de nivel