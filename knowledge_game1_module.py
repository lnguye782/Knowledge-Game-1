import pygame
import sys

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

def get_team_names():
    # Define font for rendering text
    font = pygame.font.Font(None, 45)

    # Set up team name screen
    window_size = (600, 600)
    team_name_screen = pygame.display.set_mode(window_size)

    # Initialize game state
    running_name_screen = True
    team_names = {1: "", 2: ""} # Dictionary to store team names
    current_team = 1 # Team 1 will pick team name first
    temp_text = '' # Temporary text to work with user input
    input_box = pygame.Rect(200, 250, 400, 50) # Draw input box (x-coordinate, y-coordinate, width, height)
    input_box_active = False # Used to check if user is interacting with input box
    input_box_color = (173, 216, 230) # Light blue

    # Screen loop
    while running_name_screen:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if user interacted with input box
                if input_box.collidepoint(event.pos):
                    input_box_active = True
                else:
                    input_box_active = False
                # Change color if input box is interacted
                if input_box_active:
                    input_box_color = (0, 0, 139) # Dark blue
                else:
                    input_box_color = (173, 216, 230) # Light blue
            elif event.type == pygame.KEYDOWN:
                if input_box_active:
                    if event.key == pygame.K_RETURN: # Key = Enter/Return
                        team_names[current_team] = temp_text
                        temp_text = '' # Reset temporary text
                        current_team += 1 # Team 2 now picks the name
                        if current_team > 2:
                            running_name_screen = False
                    elif event.key == pygame.K_BACKSPACE: # Key = Backspace/Delete
                        temp_text = temp_text[:-1]
                    else:
                        temp_text += event.unicode
        
        # Fill background of name screen with WHITE
        team_name_screen.fill(WHITE)

        # Render text
        text_surface = font.render(temp_text, True, BLACK)

        # Resize input box if user input is too long
        width = max(200, text_surface.get_width() + 10)
        input_box.w = width

        # Update input box
        team_name_screen.blit(text_surface, (input_box.x + 5, input_box.y + 10))

        pygame.draw.rect(team_name_screen, input_box_color, input_box, 1)

        instruction_text = font.render(f"Enter Team {current_team} Name:", True, BLACK)
        instruction_text_rect = instruction_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 100))
        team_name_screen.blit(instruction_text, instruction_text_rect)

        pygame.display.flip()
    
    return team_names

def read_csv(file_name):
    # Initialize dictionary
    choice_dict = {
        1: [], # Correct choice
        2: []  # Incorrect choice
    }

    with open(file_name, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        # Skip header
        next(csv_reader)
        for row in csv_reader:
            correct_choice = row[0]
            incorrect_choice = row[1]
            choice_dict[1].append(correct_choice)
            choice_dict[2].append(incorrect_choice)
    
    return choice_dict
