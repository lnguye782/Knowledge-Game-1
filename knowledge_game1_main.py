import pygame
import sys
import knowledge_game1_module

pygame.init()

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (1, 170, 32)
BLUE = (0, 0, 255)
PINK = (170, 51, 106)

# Define font to render text
font = pygame.font.Font(None, 32)

# Set up main screen
window_size = (600, 720)
main_screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Knowledge Game 1")

# Define grid table
grid_size = 5
cell_size = window_size[0] // grid_size

# Load image choices
choice_bank = knowledge_game1_module.load_images("load_image_helper.csv")

# Assign random choices to cells
choice_cell, answer_cell, correctness_cell = knowledge_game1_module.assign_random_choice_to_cells(grid_size, choice_bank)

# Get team names from user input
team_names = knowledge_game1_module.get_team_names()

# Initialize game state
cell_selected = None
cell_answered = {}
current_player = 1
current_player_score = {1: 0, 2: 0}
running_main_screen = True
timer_start = pygame.time.get_ticks()
timer_limit = 30000 + 1000 # 30 seconds timer

# Game loop
while running_main_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running_main_screen = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            # Find x and y coordinates of the mouse
            mouse_col = mouse_x // cell_size
            mouse_row = (mouse_y-120) // cell_size
            # Test mouse and cell coordinates
            # print(f"Mouse clicked at: ({mouse_x}, {mouse_y} -> Cell: ({mouse_row}, {mouse_col}))")

            cell_selected = (mouse_row, mouse_col)
            if cell_selected in choice_cell and cell_selected not in cell_answered:
                current_choice = choice_cell[cell_selected]
                current_answer = answer_cell[cell_selected]
                cell_answered[cell_selected] = correctness_cell[cell_selected]
                # Update player score
                if cell_answered[cell_selected] == 1:
                    current_player_score[current_player] += 1
                # Reset timer since current player makes the choice
                timer_start = pygame.time.get_ticks()
                # Switch player turn
                current_player = 2 if current_player == 1 else 1
            
    # Switch player turn if current player runs out of time
    timer_elapsed = pygame.time.get_ticks() - timer_start
    if timer_elapsed > timer_limit:
        # Switch player turn
        current_player = 2 if current_player == 1 else 1
        # Reset timer
        timer_start = pygame.time.get_ticks()
                
    main_screen.fill(WHITE)

    # Draw grid table of the game
    for row in range(grid_size):
        for col in range(grid_size):
            cell_rect = pygame.Rect((col * cell_size), (row * cell_size) + cell_size, cell_size, cell_size)
            # Draw the rectangle cells with BLACK and border width of 1
            pygame.draw.rect(main_screen, BLACK, cell_rect, 1, 1)

            # Display the image choice in the cells
            choice_image = choice_cell[row, col]
            choice_image = pygame.transform.scale(choice_image, (cell_size - 2, cell_size - 50))
            choice_image_rect = choice_image.get_rect(center=cell_rect.center)
            main_screen.blit(choice_image, choice_image_rect)
            
            # Display the image answer in the cells
            if (row, col) in cell_answered:
                answer_image = answer_cell[row, col]
                answer_image = pygame.transform.scale(answer_image, (cell_size - 2, cell_size - 50))
                answer_image_rect = answer_image.get_rect(center=cell_rect.center)
                
                # Draw Blue box for correct choice or Red box for incorrect choice   
                answer_cell_rect = pygame.Rect((col * cell_size), (row * cell_size) + cell_size, cell_size, cell_size)
                if cell_answered[(row, col)] == 1:
                    pygame.draw.rect(main_screen, BLUE, answer_cell_rect)
                    main_screen.blit(answer_image, answer_image_rect)
                elif cell_answered[(row, col)] == 2:
                    pygame.draw.rect(main_screen, RED, answer_cell_rect)
                    main_screen.blit(answer_image, answer_image_rect)

    # Show both player scores
    text_player1_score = font.render("{}: {} points".format(team_names[1], current_player_score[1]), True, GREEN)
    text_player2_score = font.render("{}: {} points".format(team_names[2], current_player_score[2]), True, PINK)
    text_player1_score_rect = text_player1_score.get_rect(topleft=(20, 30))
    text_player2_score_rect = text_player2_score.get_rect(topleft=(20, 60))
    main_screen.blit(text_player1_score, text_player1_score_rect)
    main_screen.blit(text_player2_score, text_player2_score_rect)

    # Show player turn
    text_player_turn = font.render("{}'s Turn".format(team_names[current_player]), True, BLACK)
    text_player_turn_rect = text_player_turn.get_rect(center=(500, 100))
    main_screen.blit(text_player_turn, text_player_turn_rect)

    # Show the timer
    text_timer = font.render("{}".format(max(0, (timer_limit - timer_elapsed) // 1000)), True, RED)
    rect_timer = text_timer.get_rect(center=(window_size[0] - 30, window_size[1] - 700))
    main_screen.blit(text_timer, rect_timer)

    # Update display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()