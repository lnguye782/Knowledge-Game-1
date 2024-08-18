import pygame
import sys
import csv
import random

# Define some basic colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (1, 170, 32)
BLUE = (0, 0, 255)
PINK = (170, 51, 106)

def get_team_names():
    # Define font for rendering text
    font = pygame.font.Font(None, 45)

    # Set up team name screen
    window_size = (600, 720)
    team_name_screen = pygame.display.set_mode(window_size)

    # Initialize game state
    running_name_screen = True
    team_names = {1: "", 2: ""} # Dictionary to store team names
    current_team = 1 # Team 1 will pick team name first
    temp_text = '' # Temporary text to work with user input
    input_box = pygame.Rect(window_size[0] // 2 - 100, window_size[1] // 2 - 50, 400, 50) # Draw input box (x-coordinate, y-coordinate, width, height)
    input_box_active = False # Used to check if user is interacting with input box
    input_box_color = pygame.Color('lightskyblue3')

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
                    input_box_color = pygame.Color('dodgerblue2')
                else:
                    input_box_color = ('lightskyblue3')
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

        # Render input text
        input_text = font.render(temp_text, True, 'dodgerblue2')

        # Resize input box if user input is too long
        width = max(200, input_text.get_width() + 10)
        input_box.w = width

        # Update input box
        team_name_screen.blit(input_text, (input_box.x + 5, input_box.y + 10))

        pygame.draw.rect(team_name_screen, input_box_color, input_box, 1)

        instruction_text = font.render(f"Enter Team {current_team} Name:", True, BLACK)
        instruction_text_rect = instruction_text.get_rect(center=(window_size[0] // 2, window_size[1] // 2 - 100))
        team_name_screen.blit(instruction_text, instruction_text_rect)

        pygame.display.flip()
    
    return team_names

def load_images(file_helper):
    # Initialize dictionary
    question_dict = {
        1: [],  # Correct choice
        2: []   # Incorrect choice
    }
    with open(file_helper, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            value = int(row[0])
            question_key = row[1]
            answer_key = row[2]
            # Load images
            question_image = pygame.image.load(f'./Assets/{question_key}.png')
            answer_image = pygame.image.load(f'./Assets/{answer_key}.png')
            # Store images into dictionary
            question_dict[value].append((question_image, answer_image))
    
    return question_dict
    
def assign_random_choice_to_cells(grid_size, choice_bank):
    # Initialize dictionary
    choice_cell = {}
    answer_cell = {}
    correctness_cell = {}

    for row in range(grid_size):
        for col in range(grid_size):
            available_correct_choices = [c for c in choice_bank[1] if c not in choice_cell.values()]
            available_incorrect_choices = [i for i in choice_bank[2] if i not in choice_cell.values()]
            available_choices = available_correct_choices + available_incorrect_choices
            # Assign one random choice to the current cell
            if available_choices:
                selected_choice = random.choice(available_choices)
                choice_cell[(row, col)] = selected_choice[0]
                answer_cell[(row, col)] = selected_choice[1]
            # Determine correctness based on the choice bank
            if selected_choice in available_correct_choices:
                correctness_cell[(row, col)] = 1    # Correct choice
                # Remove the selected choice from choice bank to avoid repeating
                choice_bank[1].remove(selected_choice)
            else:
                correctness_cell[(row, col)] = 2    # Incorrect choice
                # Remove the selected choice from choice bank to avoid repeating
                choice_bank[2].remove(selected_choice)

    return choice_cell, answer_cell, correctness_cell