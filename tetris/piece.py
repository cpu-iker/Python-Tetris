"""
Importar random para seleccionar piezas aleatorias, y constantes para formas, colores y dimensiones del tablero.
"""
import random
from tetris.constants import SHAPES, COLORS, COLS


class Piece:
    # Representa un bloque en el juego

    def __init__(self, shape_name: str = None):
        self.name = shape_name or random.choice(list(SHAPES.keys()))
        self.rotations = SHAPES[self.name]
        self.rotation_index = 0
        self.color = COLORS[self.name]


        self.row = 0
        self.col = COLS // 2 - 2

    @property
    def cells(self) -> list[list[int]]:
        
        return self.rotations[self.rotation_index]

    def get_absolute_cells(self, row=None, col=None) -> list[tuple[int, int]]:

        r = row if row is not None else self.row
        c = col if col is not None else self.col
        return [(r + dr, c + dc) for dr, dc in self.cells]

    def rotate(self):

        self.rotation_index = (self.rotation_index + 1) % len(self.rotations)

    def unrotate(self):

        self.rotation_index = (self.rotation_index - 1) % len(self.rotations)
