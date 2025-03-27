import pygame
import pygame_menu
from main import run
import time
import threading
from search_methods import *

MAP_MAX_SIZE = 32
TILE_SIZE = 24
SCREEN_SIZE = MAP_MAX_SIZE * TILE_SIZE

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

        text_surface = pygame.font.Font(None, 36).render(str(curr_step), True, (255, 255, 255))

        screen.blit(text_surface, (10, 10))
            

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


def processing_loop():
    dots = ""
    running = True
    while running:
        screen.fill("black")
        text = font.render(f"Processing Simulation{dots}", True, "white")
        screen.blit(text, (SCREEN_SIZE // 2 - text.get_width() // 2, SCREEN_SIZE // 2 - text.get_height() // 2))
        pygame.display.flip()
        dots = "." * ((len(dots) + 1) % 4)  # Cycles through '', '.', '..', '...'
        clock.tick(1)  # Controls update speed
        if event.is_set():  # Stop when the thread finishes
            running = False

def start_run():
    global result
    global thread
    global event
    
    def run_and_store():
        global result
        result = run("../config.json")  # Assign result directly to states
        event.set()  # Signal that processing is complete
    
    event.clear()  # Reset the event
    thread = threading.Thread(target=run_and_store)
    thread.start()
    processing_loop()
    thread.join()  # Ensure the thread is finished before continuing

pygame.init()
screen = pygame.display.set_mode((SCREEN_SIZE, SCREEN_SIZE))
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

states = [] 
result = None 
event = threading.Event()  
start_run()

if not result.success:
    screen.fill("black")
    text_surface = pygame.font.Font(None, 36).render("No solution found", True, (255, 255, 255))

    screen.blit(text_surface, (10, 10))
    pygame.display.flip()
    time.sleep(5)
    pygame.quit

else:
    for node in result.solution:
        states.append(node)

    menu = pygame_menu.Menu("Simulation", SCREEN_SIZE, SCREEN_SIZE, theme=pygame_menu.themes.THEME_DARK)
    menu.add.button("Start", lambda: menu.disable())
    menu.add.button("Quit", pygame.quit)
    menu.mainloop(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        render()
        update()

        pygame.display.flip()

        clock.tick(30)  # limits FPS to 60

    pygame.quit()