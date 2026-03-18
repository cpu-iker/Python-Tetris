import pygame
from tetris.board import Board
from tetris.piece import Piece
from tetris.renderer import Renderer
from tetris.constants import (
    FPS, INITIAL_SPEED, SPEED_INCREMENT, MIN_SPEED, LINES_PER_LEVEL,
    SCREEN_WIDTH, SCREEN_HEIGHT
)


class Game:
    """
    Clase principal del juego.
    Se encarga de gestionar el bucle principal, controlar input, lógica, piezas...
    """

    def __init__(self):
        # Inicializar pygame
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen)
        self._reset()


    # Estado del juego
    def _reset(self):
        self.board = Board()
        self.current_piece = Piece()
        self.next_piece = Piece()
        self.score = 0
        self.lines = 0
        self.level = 1
        self.game_over = False
        self.paused = False
        self.fall_speed = INITIAL_SPEED     # ms entre caídas
        self.fall_timer = 0                 # ms acumulados desde la última caída


    # Game loop , el bucle principal
    def run(self):
        while True:
            dt = self.clock.tick(FPS)   # ms transcurridos en este frame

            self._handle_events()

            if not self.game_over and not self.paused:
                self._update(dt)
                self.renderer.draw(
                    self.board, self.current_piece, self.next_piece,
                    self.score, self.level, self.lines
                )
            elif self.paused:
                self.renderer.draw_pause()
            elif self.game_over:
                self.renderer.draw_game_over(self.score)


    # Input del usuario (eventos)
    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self._reset()
                    return

                if self.game_over:
                    return

                if event.key == pygame.K_p:
                    self.paused = not self.paused
                    return

                if self.paused:
                    return

                if event.key == pygame.K_LEFT:
                    self._move(0, -1)
                elif event.key == pygame.K_RIGHT:
                    self._move(0, 1)
                elif event.key == pygame.K_DOWN:
                    self._move(1, 0)
                elif event.key == pygame.K_UP:
                    self._rotate()
                elif event.key == pygame.K_SPACE:
                    self._hard_drop()


    # Actualización del juego
    def _update(self, dt: int):
        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed:
            self.fall_timer = 0
            if not self._move(1, 0):   # No pudo bajar → fijar
                self._lock_piece()

    
    # Movimientos
    def _move(self, drow: int, dcol: int) -> bool:

        new_cells = self.current_piece.get_absolute_cells(
            row=self.current_piece.row + drow,
            col=self.current_piece.col + dcol
        )
        if self.board.is_valid_position(new_cells):
            self.current_piece.row += drow
            self.current_piece.col += dcol
            return True
        return False

    def _rotate(self):

        self.current_piece.rotate()
        cells = self.current_piece.get_absolute_cells()

        if not self.board.is_valid_position(cells):
            for kick in (1, -1, 2, -2):
                kicked = self.current_piece.get_absolute_cells(
                    col=self.current_piece.col + kick
                )
                if self.board.is_valid_position(kicked):
                    self.current_piece.col += kick
                    return
            self.current_piece.unrotate()

    def _hard_drop(self):
        while self._move(1, 0):
            pass
        self._lock_piece()


    # Fijar pieza y limpiar líneas
    def _lock_piece(self):
        cells = self.current_piece.get_absolute_cells()
        self.board.lock_piece(cells, self.current_piece.color)

        points = self.board.clear_lines()
        if points:
            self.score += points * self.level
            # cleared = list(self.board.grid).count([None] * 10)  
            self.lines += len([r for r in range(20) if all(c is None for c in self.board.grid[r])])
            self._update_lines_and_level(points)

        if self.board.has_overflowed():
            self.game_over = True
            return

        self.current_piece = self.next_piece
        self.next_piece = Piece()

    def _update_lines_and_level(self, points: int):
        points_to_lines = {100: 1, 300: 2, 500: 3, 800: 4}
        cleared = points_to_lines.get(points // self.level, 0)
        self.lines += cleared
        new_level = self.lines // LINES_PER_LEVEL + 1
        if new_level != self.level:
            self.level = new_level
            self.fall_speed = max(MIN_SPEED, INITIAL_SPEED - (self.level - 1) * SPEED_INCREMENT)
