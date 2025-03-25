import pygame
import pygame_menu
from main import run
import time

MAP_MAX_SIZE = 32
TILE_SIZE = 24

states = []
global curr_step 
curr_step = 1

def render():
    # update map state
    # padded_map = add_padding(states[curr_step].state.matrix, MAP_MAX_SIZE, MAP_MAX_SIZE, " ")
    
    padded_map = states[curr_step].state.matrix
    for y, row in enumerate(padded_map):
        for x, char in enumerate(row):

            if char == " ":
                color = (0, 0, 0)
            elif char == "#":
                color = (255, 0, 0)
            elif char == ".":
                color = (0, 255, 0)
            elif char == "$":
                color = (0, 0, 255)
            elif char == "@":
                color = (255, 255, 0)
            elif char == "+":
                color = (255, 0, 255)
            elif char == "*":
                color = (0, 255, 255)
            else:
                color = (0, 0, 0)  # Default color in case of an unknown character

            pygame.draw.rect(screen, color, (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            

def add_padding(map_state, max_width, max_height, pad_char=" "):
    height = len(map_state)
    width = max(len(row) for row in map_state)

    top_padding = (max_height - height) // 2
    bottom_padding = max_height - height - top_padding
    left_padding = (max_width - width) // 2
    right_padding = max_width - width - left_padding

    padded_level = [pad_char * left_padding + row + pad_char * right_padding for row in map_state]

    padded_level = [pad_char * max_width] * top_padding + padded_level + [pad_char * max_width] * bottom_padding

    return padded_level

def update():
    global curr_step
    if curr_step < len(states) - 1:
        curr_step += 1


# pygame setup
pygame.init()
screen = pygame.display.set_mode((MAP_MAX_SIZE * TILE_SIZE, MAP_MAX_SIZE * TILE_SIZE))
clock = pygame.time.Clock()

# Pygame Menu
menu = pygame_menu.Menu("Select Level", 500, 500, theme=pygame_menu.themes.THEME_DARK)
menu.add.button("Start", lambda: menu.disable())  # Close the menu and start the game
menu.add.button("Quit", pygame.quit)  # Quit the game

# Show the menu
menu.mainloop(screen)

running = True

states = run("config.json")

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("black")

    render()
    update()

    pygame.display.flip()

    clock.tick(60)  # limits FPS to 60
    time.sleep(0.1)

pygame.quit()