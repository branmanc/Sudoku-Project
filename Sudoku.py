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
# Draw the Sudoku board
def draw_board(board, locked_cells, selected_cell):
   for row in range(GRID_SIZE):
       for col in range(GRID_SIZE):
           value = board[row][col]
           x = X_OFFSET + col * CELL_SIZE
           y = row * CELL_SIZE


           # Highlight the selected cell
           if selected_cell == (row, col):
               pygame.draw.rect(screen, BLUE, (x, y, CELL_SIZE, CELL_SIZE))


           if (row, col) in locked_cells:
               text_surface = font.render(str(value), True, BLACK)
           elif value != 0:
               text_surface = font.render(str(value), True, WHITE)
           else:
               continue


           text_rect = text_surface.get_rect(center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2))
           screen.blit(text_surface, text_rect)


# Check if the board is correctly solved
def is_board_solved(board):
   def is_valid_group(group):
       return sorted(group) == list(range(1, 10))


   for row in board:
       if not is_valid_group(row):
           return False
   for col in zip(*board):  # Transpose to the columns (checks to make sure no repeats or invalid values)
       if not is_valid_group(col):
           return False
   for box_row in range(0, GRID_SIZE, 3):
       for box_col in range(0, GRID_SIZE, 3):
           box = [
               board[r][c]
               for r in range(box_row, box_row + 3)
               for c in range(box_col, box_col + 3)
           ]
           if not is_valid_group(box):
               return False
   return True

