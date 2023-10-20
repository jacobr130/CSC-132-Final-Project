import pygame
from settings import *

# TODO: Make platform class, update graphics, literally finish the game by wednesday, etc.

# The player character 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # PLAYER SETTINGS
        # TODO: change
        self.side_length = 100   # l and w of rect (square)
        self.dimensions = (self.side_length, self.side_length)
        self.x = WIDTH // 2
        self.y = 500
        self.movement_speed = 5
        self.gravity = 0
        
        self.surf = pygame.image.load("games/jacob_game/images/player.png")
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        
        self.player_rect = self.surf.get_rect(midbottom=(WIDTH//2, 600))
        
        '''print sprite size (debug)'''
        #print(self.surf.get_size())
        
    # Handle user input
    """
        For now, this function takes keyboard input.
        This will be changed when controller is implemented.
        Do I have any idea how that will work? notyet
    """
    def update(self, pressed):
        if pressed[K_LEFT]:
            self.player_rect.x -= self.movement_speed
        
        elif pressed[K_RIGHT]:
            self.player_rect.x += self.movement_speed
        
        #elif pressed[K_SPACE]:
            #self.gravity = -20  # physics?
            #space_down = True

# Platforms you gotta jump on
class Platform(pygame.sprite.Sprite):
    def __init__(self,):
        super(Platform, self).__init__()
        pass
            
def main():
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    screen.fill((255, 255, 255))
    
    player = Player()
    
    # sky
    bg = pygame.image.load("games/jacob_game/images/sky.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # ground that the game starts on
    ground = pygame.image.load("games/jacob_game/images/ground.png")
    ground = pygame.transform.scale(ground, (WIDTH, 800))   # wide as screen and long af
    
    # TODO: clean code up
    ground_rect = ground.get_rect()
    
    # handle fps
    clock = pygame.time.Clock()
    
    # Main game loop
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False
        
        # handle user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        #player is constantly jumping
        if player.player_rect.midbottom[1] == 600:
            player.gravity = -20
            
        # gravity does be existing tho
        player.gravity += 1
        player.player_rect.y += player.gravity
        
        # keep player on ground
        if player.player_rect.midbottom[1] > 600:
            player.player_rect.midbottom[1] == 600
        
        # update screen
        screen.blit(bg, (0, 0))
        screen.blit(ground, (0, 600))
        screen.blit(player.surf, player.player_rect)
        
        pygame.display.flip()
        
        # keeps game at 60FPS
        clock.tick(FPS)
    
    # If game loop is broken
    exit()
                
if __name__ == "__main__":
    main()