# Menu screen and game runner
#import RPi.GPIO as rp
#from threading import Thread    # depends on performance
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
"""

#PINS = [16, 17, 18] # whatever pins the buttons are wired to
jacob_game = "games/jacob_game/main.py"

def main_menu():
    pygame.init()
    screen = pygame.display.set_mode(ASPECT)
    screen.fill("White")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        """
            This will be implemented with GPIO instead of pygame 
            later tonight
        """
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_a]:
            game1_running = True
            while game1_running:
                try:
                    exec(open(jacob_game).read()) # oh my god it works
                except GameOver:
                    game1_running = False
                    main_menu()

        pygame.display.flip()
    
    exit()

if __name__ == "__main__":
    main_menu()