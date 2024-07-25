import pygame
import sys
import knowledge_game1_module

pygame.init()

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Define font to render text
font = pygame.font.Font(None, 20)

# Set up main screen
window_size = (600, 600)
main_screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Knowledge Game 1")

# Define grid table
grid_size = 5
cell_size = window_size[0] // grid_size
grid_table = [
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""],
    ["", "", "", "", ""]
]

# Get team names from user input
team_names = knowledge_game1_module.get_team_names()

# Get choice bank
choice_bank = knowledge_game1_module.read_csv("math_choice_bank")
print(choice_bank)

# Game loop
running_main_screen = True
while running_main_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_main_screen = False

    main_screen.fill(WHITE)

    # Draw grid table of the game
    for row in range(grid_size):
        for col in range(grid_size):
            cell_rect = pygame.Rect((col * cell_size), (row * cell_size), cell_size, cell_size)
            pygame.draw.rect(main_screen, BLACK, cell_rect, 1)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()