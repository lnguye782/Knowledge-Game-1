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
font = pygame.font.Font(None, 30)

# Set up main screen
window_size = (800, 960)
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
# team_names = knowledge_game1_module.get_team_names()

# Get choice bank
choice_bank = knowledge_game1_module.read_csv("math_choice_bank.csv")

# Assign random choices to cells
choice_cell, answer_cell, correctness_cell = knowledge_game1_module.assign_random_choice_to_cells(grid_size, choice_bank)

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
            cell_rect = pygame.Rect((col * cell_size), (row * cell_size) + cell_size, cell_size, cell_size)
            pygame.draw.rect(main_screen, BLACK, cell_rect, 1, 1)

            # Get the choice for the current cell
            choice = choice_cell.get((row, col), "")

            # Wrap the choice to fit the cell
            words = choice.split(' ')
            # Calculate the width and height of a space character
            space_width, space_height = font.size(' ')
            # Set the initial position to start drawing text
            x = cell_rect.centerx - 80
            y = cell_rect.centery - 50
            # Get the maximum width and height for the text area
            max_width, max_height = cell_rect.size
            # Get the height of a line of text
            line_height = font.get_linesize()
            # Iterate over each line in the text
            for word in words:
                word_text = font.render(word, True, BLACK)
                # Get the width and height of the rendered word
                word_width, word_height = word_text.get_size()
                # Check if the word exceeds the maximum width of the rect
                if (x + word_width) >= max_width:
                    x = cell_rect.left
                    y += line_height
                # Draw the word on the surface at the current position
                main_screen.blit(word_text, (x, y))
                # Move the x position to the right by the width of word plus a space
                x += word_width + space_width

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()