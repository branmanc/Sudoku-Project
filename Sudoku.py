import pygame
import sys
from sudoku_generator import generate_sudoku


pygame.init()


# Our Constants
WIDTH, HEIGHT = 600, 700
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE
BUTTON_HEIGHT = 50
X_OFFSET = (WIDTH - GRID_SIZE * CELL_SIZE) // 2 #Did this to center the grid
FPS = 60


# Some Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (150, 200, 255)
RED = (255, 100, 100)
GREEN = (100, 255, 100)
LIGHTBLUE = (100, 150, 255)
YELLOW = (255,255,0)


screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku")
font = pygame.font.Font(None, 36)


# Function to draw a button
def draw_button(screen, text, x, y, width, height, color):
   pygame.draw.rect(screen, color, (x, y, width, height))
   text_surface = font.render(text, True, BLACK)
   text_rect = text_surface.get_rect(center=(x + width // 2, y + height // 2))
   screen.blit(text_surface, text_rect)


def draw_grid():
   for i in range(GRID_SIZE + 1):
       line_width = 3 if i % 3 == 0 else 1
       # Horizontal lines
       pygame.draw.line(
           screen, BLACK,
           (X_OFFSET, i * CELL_SIZE), (X_OFFSET + GRID_SIZE * CELL_SIZE, i * CELL_SIZE),
           line_width
       )
       # Vertical lines
       pygame.draw.line(
           screen, BLACK,
           (X_OFFSET + i * CELL_SIZE, 0), (X_OFFSET + i * CELL_SIZE, GRID_SIZE * CELL_SIZE),
           line_width
       )

