import pygame, pygame.locals
from sys import exit
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        self.surf = pygame.image.load("images/player.png").convert()
        
        # TODO: CHANGE THIS TO MAKE IT WORK
        self.surf.set_colorkey((0, 0, 0), pygame.locals.RLEACCEL)
        
        # Resize sprite to be bigger on screen
        self.surf = pygame.transform.scale(self.surf, (200, 200))
        
        # Print sprite size (debug)
        #print(self.surf.get_size())
        
        self.rect = self.surf.get_rect()
        
    # Handle user input
    def update(self):
        pass

def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    player = Player()
    RUNNING = True
    
    # Main game loop
    while RUNNING:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                RUNNING = False
        
        screen.blit(player.surf, player.rect)
        pygame.display.flip()
    
    # If game loop is broken
    exit()
                
if __name__ == "__main__":
    main()