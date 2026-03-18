from tetris.constants import ROWS, COLS, SCORE_TABLE # Importamos constantes para el tablero


class Board:

    """
    Representa el tablero del Tetris como una matriz 2D
    Cada celda es None (es decir vacía) o un color (tupla RGB)
    """

    def __init__(self):
        # Inicializa el tablero vacío
        self.grid: list[list] = self._empty_grid()

    def _empty_grid(self):
        # Crea una matriz de Filas x Columnas llenas de None
        return [[None for _ in range(COLS)] for _ in range(ROWS)]

    def reset(self):
        # Método para reiniciar el tablero a vacío
        self.grid = self._empty_grid()


    #  Colisiones
    def is_valid_position(self, cells: list[tuple[int, int]]) -> bool:
        # Comprueba si una pieza puede colorarse en una posición dada sin colisionar
        for row, col in cells:
            if col < 0 or col >= COLS:
                return False
            if row >= ROWS:
                return False
            if row >= 0 and self.grid[row][col] is not None:
                return False
        return True


    # Fijar pieza
    def lock_piece(self, cells: list[tuple[int, int]], color: tuple):
        
        for row, col in cells:
            if 0 <= row < ROWS and 0 <= col < COLS:
                self.grid[row][col] = color

    
    # Elimintar líneas completadas
    def clear_lines(self) -> int:
        """
        Elimina las filas completas, las borra desde arriba y devuelve
        los puntos obtenidos según la tabla de puntuación.
        """
        full_rows = [r for r in range(ROWS) if all(self.grid[r])]

        for row in full_rows:
            del self.grid[row]
            self.grid.insert(0, [None] * COLS)

        return SCORE_TABLE.get(len(full_rows), 0)


    # Comprueba si la fila superior está ocupada, lo cual terminaría la partida
    def has_overflowed(self) -> bool:
        return any(self.grid[0])
