# Menu screen and game runner by Jacob Rice
import RPi.GPIO as rp
from screeninfo import get_monitors
# Make window fullscreen automatically
for monitor in get_monitors():
    if monitor.is_primary == True:
        screen = monitor
ASPECT = (screen.width, screen.height)

import pygame
from games.jacob_game.settings import *
from games.jacob_game.main import *

"""
    GAME REQUIREMENTS FOR THIS FILE TO WORK:

        - Game must be put into main function using
            if __name__ == "__main__"
        
        - Game must import games.jacob_game.GameOver
            When mainloop is broken:
                call pygame.display.quit()
                and then raise GameOver
        
        - Pygame must be imported as 'pygame' and nothing 
            else e.g. 'pg'

        - Any other local modules used in game must also be 
            imported here e.g. game settings, and must be 
            imported in original file with full path
            e.g. games.jacob_game.settings
    
    THERE IS ONE PROBLEM (if using a local import):
    
        The games no longer run on their own and must be run 
        through main_menu.py
        
        This is because in order for exec(file.read()) to work,
        local imports have to use their full relative path,
        e.g. games.jacob_game.settings
        
        However, when main.py is run on its own, 
        (python games/jacob_game/main.py), the shell
        has no idea what games is when encountering
        games.jacob_game.settings
        
        This will most likely just have to be a compromise.
"""
rp.setmode(rp.BCM)
button1 = 12
button2 = 13
button3 = 16
rp.setup(button1, rp.IN, pull_up_down=rp.PUD_DOWN)
rp.setup(button2, rp.IN, pull_up_down=rp.PUD_DOWN)
rp.setup(button3, rp.IN, pull_up_down=rp.PUD_DOWN)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   

jacob_game = "games/jacob_game/main.py"
jackson_game = "games/jackson_game/dinosaur_game.py"
steven_game = "games/steven_game/PyTron.py"

def main_menu():
    pygame.init()
    pygame.display.init()
    screen = pygame.display.set_mode(ASPECT)
    screen.fill((255, 255, 255))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        """
            This will be implemented with GPIO instead of pygame 
            later tonight
        """
        #pressed = pygame.key.get_pressed()
        #if pressed[pygame.K_a]:
        if rp.input(button1) == rp.HIGH:
            print("working")
            game1_running = True
            while game1_running:
                try:
                    exec(open(jacob_game).read()) # oh my god it works
                except GameOver:
                    game1_running = False
                    main_menu()
        
        """
        elif rp.input(button2) == rp.HIGH:
            print("WORKING: JACKYSONSON")
            game2_running = True
            while game2_running:
                try:
                    exec(open(jackson_game).read())
                except GameOver:
                    game2_running = False
                    main_menu()

        elif rp.input(button3) == rp.HIGH:
            print("WORKING")
            game3_running = True
            while game3_running:
                try:
                    exec(open(steven_game).read())
                except GameOver:
                    game3_running = False
                    main_menu()
        """

        pygame.display.flip()
    
    exit()

if __name__ == "__main__":
    main_menu()