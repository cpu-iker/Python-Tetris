import pygame
from tetris.constants import (
    CELL_SIZE, COLS, ROWS, SIDEBAR_WIDTH,
    BLACK, GRAY, DARK_GRAY, LIGHT_GRAY, WHITE
)

# Clase  encargada de dibujar todo el juego en pantalla usando Pygame
class Renderer:

    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.font_large = pygame.font.SysFont("monospace", 28, bold=True)
        self.font_small = pygame.font.SysFont("monospace", 18)
        self.board_surface = pygame.Surface((COLS * CELL_SIZE, ROWS * CELL_SIZE))

    # Dibuja el estado actual del juego
    def draw(self, board, current_piece, next_piece, score, level, lines):
        # Limpia la pantalla
        self.screen.fill(BLACK)

        # Dibuja el tablero y la interfaz
        self._draw_board(board, current_piece)

        # Actualiza la pantalla
        self._draw_sidebar(next_piece, score, level, lines)
        pygame.display.flip()


    # Tablero
    def _draw_board(self, board, current_piece):
        surf = self.board_surface
        surf.fill(DARK_GRAY)

        # Líneas de cuadrícula
        for r in range(ROWS):
            for c in range(COLS):
                rect = pygame.Rect(c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE)
                pygame.draw.rect(surf, GRAY, rect, 1)

        # Celdas fijadas
        for r in range(ROWS):
            for c in range(COLS):
                color = board.grid[r][c]
                if color:
                    self._draw_cell(surf, r, c, color)

        ghost_cells = self._get_ghost_cells(board, current_piece)
        for r, c in ghost_cells:
            if r >= 0:
                rect = pygame.Rect(c * CELL_SIZE + 2, r * CELL_SIZE + 2,
                                   CELL_SIZE - 4, CELL_SIZE - 4)
                pygame.draw.rect(surf, LIGHT_GRAY, rect, 2)

        # Pieza actual
        for r, c in current_piece.get_absolute_cells():
            if r >= 0:
                self._draw_cell(surf, r, c, current_piece.color)

        self.screen.blit(surf, (0, 0))

    def _draw_cell(self, surf, row, col, color):
        rect = pygame.Rect(col * CELL_SIZE + 1, row * CELL_SIZE + 1,
                           CELL_SIZE - 2, CELL_SIZE - 2)
        pygame.draw.rect(surf, color, rect)
        highlight = tuple(min(255, c + 60) for c in color)
        pygame.draw.rect(surf, highlight, rect, 2)

    def _get_ghost_cells(self, board, piece):

        drop = 0
        while True:
            test = piece.get_absolute_cells(
                row=piece.row + drop + 1, col=piece.col
            )
            if board.is_valid_position(test):
                drop += 1
            else:
                break
        return piece.get_absolute_cells(row=piece.row + drop, col=piece.col)


    # Sidebar
    def _draw_sidebar(self, next_piece, score, level, lines):
        x = COLS * CELL_SIZE + 10
        board_height = ROWS * CELL_SIZE

   
        self._label(x, 20, "NEXT")
        self._draw_preview(next_piece, x, 50)


        self._label(x, 200, "SCORE")
        self._value(x, 228, str(score))

        self._label(x, 290, "LEVEL")
        self._value(x, 318, str(level))


        self._label(x, 380, "LINES")
        self._value(x, 408, str(lines))

        # Controles
        controls = [
            "← → : mover",
            "↑    : rotar",
            "↓    : bajar",
            "ESC  : caída",
            "P    : pausa",
            "R    : reiniciar",
        ]
        y_ctrl = board_height - len(controls) * 22 - 10
        for line in controls:
            txt = self.font_small.render(line, True, LIGHT_GRAY)
            self.screen.blit(txt, (x, y_ctrl))
            y_ctrl += 22

    def _draw_preview(self, piece, x, y):

        mini = CELL_SIZE - 8
        for dr, dc in piece.cells:
            rect = pygame.Rect(x + dc * mini, y + dr * mini, mini - 2, mini - 2)
            pygame.draw.rect(self.screen, piece.color, rect)

    def _label(self, x, y, text):
        surf = self.font_small.render(text, True, LIGHT_GRAY)
        self.screen.blit(surf, (x, y))

    def _value(self, x, y, text):
        surf = self.font_large.render(text, True, WHITE)
        self.screen.blit(surf, (x, y))


    def draw_game_over(self, score):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        cx = self.screen.get_width() // 2

        t1 = self.font_large.render("GAME OVER", True, (240, 50, 50))
        t2 = self.font_small.render(f"Score: {score}", True, WHITE)
        t3 = self.font_small.render("Pulsa R para reiniciar", True, LIGHT_GRAY)

        self.screen.blit(t1, t1.get_rect(center=(cx, 280)))
        self.screen.blit(t2, t2.get_rect(center=(cx, 330)))
        self.screen.blit(t3, t3.get_rect(center=(cx, 365)))
        pygame.display.flip()

    def draw_pause(self):
        overlay = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        cx = self.screen.get_width() // 2
        t = self.font_large.render("PAUSA", True, WHITE)
        self.screen.blit(t, t.get_rect(center=(cx, self.screen.get_height() // 2)))
        pygame.display.flip()
