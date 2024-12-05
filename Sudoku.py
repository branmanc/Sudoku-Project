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
# Main function
def main():
   clock = pygame.time.Clock()
   running = True
   game_state = "start"  # "start", "play", "win", "lose"
   board = []
   original_board = []
   locked_cells = set()
   selected_cell = None
   difficulty = 0


   while running:
       screen.fill(LIGHTBLUE)


       # Event handling
       for event in pygame.event.get():
           if event.type == pygame.QUIT:
               running = False


           if game_state == "start" and event.type == pygame.MOUSEBUTTONDOWN:
               x, y = event.pos
               if 200 <= x <= 400 and 200 <= y <= 250:  # Easy button
                   difficulty = 30
                   board = generate_sudoku(9, difficulty)
                   original_board = [row[:] for row in board]
                   locked_cells = {(r, c) for r in range(9) for c in range(9) if board[r][c] != 0}
                   game_state = "play"
               elif 200 <= x <= 400 and 300 <= y <= 350:  # Medium button
                   difficulty = 40
                   board = generate_sudoku(9, difficulty)
                   original_board = [row[:] for row in board]
                   locked_cells = {(r, c) for r in range(9) for c in range(9) if board[r][c] != 0}
                   game_state = "play"
               elif 200 <= x <= 400 and 400 <= y <= 450:  # Hard button
                   difficulty = 50
                   board = generate_sudoku(9, difficulty)
                   original_board = [row[:] for row in board]
                   locked_cells = {(r, c) for r in range(9) for c in range(9) if board[r][c] != 0}
                   game_state = "play"


           if game_state == "play":
               if event.type == pygame.MOUSEBUTTONDOWN:
                   x, y = event.pos
                   if y < WIDTH:  # Inside the board
                       col = x // CELL_SIZE
                       row = y // CELL_SIZE
                       selected_cell = (row, col)


                   # Buttons
                   if 50 <= x <= 150 and 620 <= y <= 670:  # Reset button
                       board = [row[:] for row in original_board]
                   elif 250 <= x <= 350 and 620 <= y <= 670:  # Restart button
                       game_state = "start"
                   elif 450 <= x <= 550 and 620 <= y <= 670:  # Exit button
                       running = False


               if event.type == pygame.KEYDOWN:
                   if selected_cell and selected_cell not in locked_cells:
                       row, col = selected_cell
                       if event.key in range(pygame.K_1, pygame.K_9 + 1):
                           board[row][col] = event.key - pygame.K_0  # Update board
                       elif event.key == pygame.K_BACKSPACE:
                           board[row][col] = 0  # Clear cell


               # Check winning condition
               if all(all(row) for row in board) and is_board_solved(board):
                   game_state = "win"
               elif all(all(row) for row in board):
                   game_state = "lose"


       # Game states
       if game_state == "start":
           draw_button(screen, "Easy", 200, 200, 200, 50, BLUE)
           draw_button(screen, "Medium", 200, 300, 200, 50, BLUE)
           draw_button(screen, "Hard", 200, 400, 200, 50, BLUE)


       elif game_state == "play":
           draw_grid()
           draw_board(board, locked_cells, selected_cell)


           # Draw buttons
           draw_button(screen, "Reset", 50, 620, 100, 50, BLUE)
           draw_button(screen, "Restart", 250, 620, 100, 50, BLUE)
           draw_button(screen, "Exit", 450, 620, 100, 50, BLUE)




       elif game_state == "win":
           draw_button(screen, "You Win!", 100, 300, 400, 100, BLUE)
           draw_button(screen, "Exit", 200, 450, 200, 50, BLUE)
           if event.type == pygame.MOUSEBUTTONDOWN:
               x, y = event.pos
               if 200 <= x <= 400 and 450 <= y <= 500:  # Exit button
                   running = False  # Quit the game


       elif game_state == "lose":
           draw_button(screen, "Game Over", 100, 300, 400, 100, BLUE)
           draw_button(screen, "Restart", 200, 450, 200, 50, BLUE)
           if event.type == pygame.MOUSEBUTTONDOWN:
               x, y = event.pos
               if 200 <= x <= 400 and 450 <= y <= 500:  # Restart button
                   game_state = "start"  # Restart the game
                   board = []
                   original_board = []
                   locked_cells = set()
                   selected_cell = None


       pygame.display.flip()
       clock.tick(FPS)


   pygame.quit()
   sys.exit()


if __name__ == "__main__":
   main()



