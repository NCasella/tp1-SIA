import pygame
import pygame_menu

MAP_MAX_SIZE = 32
TILE_SIZE = 16

maps = {
    "1": [
        "      ###       ",
        "      #.#       ",
        "  #####.#####   ",
        " ##         ##  ",
        "##  # # # #  ## ",
        "#  ##     ##  # ",
        "# ##  # #  ## # ",
        "#     $@$     # ",
        "####  ###  #### ",
        "   #### ####    "
    ],
    "2": [
        "###########",
        "##         ##",
        "#  $     $  #",
        "# $# #.# #$ #",
        "#    #*#    #####",
        "#  ###.###  #   #",
        "#  .*.@.*.      #",
        "#  ###.###  #   #",
        "#    #*#    #####",
        "# $# #.# #$ #",
        "#  $     $  #",
        "##         ##",
        " ###########"
    ],
    "3": [
        "     #####     ",
        "    ##   #     ",
        "    #    #     ",
        "  ###    ######",
        "  #.#.# ##.   #",
        "### ###  ##   #",
        "#   #  $  ## ##",
        "#     $@$     #",
        "#   #  $  #   #",
        "######   ### ##",
        " #  .## #### # ",
        " #           # ",
        " ##  ######### ",
        "  ####         "
    ],
    "4": [
        "     #####     ",
        "    ##   ##    ",
        "  ### $ $ ###  ",
        " ##   # #   ## ",
        "##           ## ",
        "# $#  ... #$  #",
        "#     .@.     #",
        "#  $# ...  #$ #",
        "##           ##",
        " ##   # #   ## ",
        "  ### $ $ ###  ",
        "    ##   ##    ",
        "     #####     "
    ],
    "5": [
        "   #########    ",
        "   #   #       ",
        "   # # ##########",
        "#### #  #   #   #",
        "#       # $   $ #####",
        "# ## #$ #   #   #   #",
        "# $  #  ## ## $   $ #",
        "# ## #####  #   #   #",
        "# $   #  #  ###### ##",
        "### $    @  ...# # # ",
        "  #   #     ...# # # ",
        "  #####  ###...# # ###",
        "      #### ##### #   #",
        "                 # $ #",
        "                 #   #",
        "                 #####"
    ],
    "6": [
        "     #     #    ",
        "    #########    ",
        "     #     #     ",
        "   ###     ###   ",
        " # # #     # # # ",
        "###### #.# ######",
        " #    $. .$    # ",
        " #   # #$# #   # ",
        " #   . $@$ .   # ",
        " #   # #$# #   # ",
        " #    $. .$    # ",
        "###### #.# ######",
        " # # #     # # # ",
        "   ###     ###   ",
        "     #     #     ",
        "    #########     ",
        "     #     #      "
    ],
    "7": [
        "####     ####    ",
        "# .#######. #    ",
        "#.         .#    ",
        "## ##   ## ##    ",
        " # #     # #     ",
        " #   #$#   #     ",
        " #   $@$   #     ",
        " #   #$#   #     ",
        " ###     ###     ",
        "##.## # ##.##    ",
        "#   $ # $   #    ",
        "#  ## # ##  #    ",
        "## #.   .# ##    ",
        " # $     $ #     ",
        " # ## # ## #     ",
        " #         #     ",
        " ###########     "
    ],
    "8": [
        "####",
        "#  #       #####",
        "# ##########   #",
        "###.#  #   ### #",
        "  #.# $#$# # ###",
        "  #.#    # $ #",
        "  #.##$# # # #",
        "  #        # #",
        "  #@   ###   #",
        "  #        ###",
        "  #.##$#$# #",
        "  #.#  # # ##",
        "  #.# $#  $ #",
        "###.#    #  #",
        "# ########  ###",
        "#  #     #### #",
        "####       #  #",
        "           ####"
    ],
    "9": [
        "         ####    ",
        "         #  #    ",
        "      ####$ #### ",
        "      #        # ",
        "      # ##.### # ",
        "      # ###### #####",
        "      #  +$ ## #   #",
        "  ######### #. $   #",
        "  #   ##.## ## #   #",
        "### #       ## #####",
        "# $   # $##### #",
        "# ###.#  #   $.#",
        "#   ######    ##",
        "#   $.     #### ",
        "############     "
    ],
    "10": [
        "      #########   ",
        "  #####       #####",
        "  #       .       #",
        "  # ##  #.#.#  ## #",
        "  #               #",
        "  ###  #$#$#$#  ###",
        "#   #           #   #",
        "### #@ #######  # ###",
        "#   #           #   #",
        "  ###  #$#$#$#  ###",
        "  #               #",
        "  # ##  #.#.#  ## #",
        "  #       .       #",
        "  #####       #####",
        "      #########    "
    ]
}

map_state = maps["1"]



def render():
    # update map state
    padded_map = add_padding(map_state, MAP_MAX_SIZE, MAP_MAX_SIZE, " ")

    for y, row in enumerate(padded_map):
        for x, char in enumerate(row):

            match (char):
                case " ": 
                    color = (0, 0, 0)
                case "#": 
                    color = (255, 0, 0)
                case ".": 
                    color = (0, 255, 0)
                case "$": 
                    color = (0, 0, 255)
                case "@": 
                    color = (255, 255, 0)
                case "+":
                    color = (255, 0, 255)
                case "*":
                    color = (0, 255, 255)

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
    black = "black"
    
def set_level(level_tuple):
    level_name = level_tuple[0]  # Extract the first element of the tuple, which is the level name
    print(f"Level selected: {level_name}")  # Debugging line to check what value is passed
    try:
        global map_state
        map_state = maps[level_name]  # Load new level based on the selected level_name
    except KeyError:
        print(f"Error: '{level_name}' not found in maps dictionary.")  # Error handling







# pygame setup
pygame.init()
screen = pygame.display.set_mode((MAP_MAX_SIZE * TILE_SIZE, MAP_MAX_SIZE * TILE_SIZE))
clock = pygame.time.Clock()

# Pygame Menu
menu = pygame_menu.Menu("Select Level", 500, 500, theme=pygame_menu.themes.THEME_DARK)
menu.add.dropselect("Level:", list(maps.keys()), onchange=set_level)  # When level is selected, call set_level
menu.add.button("Start", lambda: menu.disable())  # Close the menu and start the game
menu.add.button("Quit", pygame.quit)  # Quit the game

# Show the menu
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

    clock.tick(60)  # limits FPS to 60

pygame.quit()