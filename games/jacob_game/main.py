import pygame
from random import randint
from settings import *

# TODO: Make platform class, update graphics, literally finish the game by wednesday, etc.

# The player character 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # PLAYER SETTINGS
        self.side_length = 150   # l and w of rect (square)
        self.dimensions = (self.side_length, self.side_length)
        self.movement_speed = 10
        self.gravity = 0
        self.jump_height = -25  # gravity
        
        self.surf = pygame.image.load("games/jacob_game/gfx/player.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        
        self.player_rect = self.surf.get_rect(midbottom=(WIDTH//2, 800), # is there any end in sight
                                              bottomright=((WIDTH//2) + self.side_length, 800),
                                              bottomleft=((WIDTH//2) - self.side_length, 800))
        
    # Handle user input
    """
        For now, this function takes keyboard input.
        This will be changed when controller is implemented.
        Do I have any idea how that will work? notyet
    """
    def update(self, pressed):
        if pressed[K_LEFT]:
            self.player_rect.x -= self.movement_speed
            # if player goes off left of screen spawn at right
            if self.player_rect.bottomleft[0] == 0 - self.side_length:
                self.player_rect.x = WIDTH + self.side_length
        
        elif pressed[K_RIGHT]:
            self.player_rect.x += self.movement_speed
            # if player goes off right of screen spawn at left
            if self.player_rect.bottomright[0] == WIDTH + self.side_length:
                self.player_rect.x = 0 - self.side_length
                
        """
        # elif pressed[K_SPACE]:
            # self.gravity = -20  # physics?
            # space_down = True
        """

# Platforms you gotta jump on
class Platform(pygame.sprite.Sprite):
    def __init__(self,):
        super(Platform, self).__init__()
        
        # PLATFORM SETTINGS
        self.length = 150
        self.height = 50
        self.dimensions = (self.length, self.height)
        
        self.surf = self.pick_sprite()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        self.platform_rect = self.spawn()
    
    def pick_sprite(self):
        """
            Currently, there is only one platform.
            There will be different sizes but this
            is a proof of concept
        """
        size = 1    # will be randint later?
        
        match size:
            case 1:
                return pygame.image.load("games/jacob_game/gfx/platform_short.png").convert_alpha()
    
    def spawn(self):
        return self.surf.get_rect(topleft=(randint(0, WIDTH-self.length), randint(0, 800-self.height)))
        #return self.surf.get_rect(topleft=(500,700))   # debug version
    
    # I couldn't call it break() so
    # I went with the next best option
    def eviscerate(self):
        pass
            
def main():

    collidables = []
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    player = Player()
    
    # sky
    bg = pygame.image.load("games/jacob_game/gfx/sky.png").convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # ground that the game starts on
    ground = pygame.image.load("games/jacob_game/gfx/ground.png").convert()
    ground = pygame.transform.scale(ground, (WIDTH, 800))   # wide as screen and long af
    ground_rect = ground.get_rect(topleft=(0, 800))
    collidables.append(ground_rect)
    
    # platforms
    platforms = []
    #platform = Platform()
    #collidables.append(platform.platform_rect)
    
    # handle fps
    clock = pygame.time.Clock()

    # Main game loop
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False

        # there's no way this is the best solution
        #player_x_1 = player.player_rect.x
        #player_x_2 = player.player_rect.x
        #jumping = True if player_x_2 > player_x_1 else False
        jumping = False

        # create platforms
        if len(platforms) < 10:
            platforms.append(Platform())
        
        # this may cause a bug later
        for platform in platforms:
            collidables.append(platform.platform_rect)
        
        #for i in platforms:
            #print(f"num: {len(platforms)}")    # debug
            #print(i.platform_rect)

        # handle user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        # player is constantly jumping
        # check for collisions between 
        # player and all other objects
        ## TODO: fix platform jumping bug with player states
        for rect in collidables:
            if player.player_rect.colliderect(rect) and not jumping:
                player.gravity = player.jump_height
            
        # gravity does be existing
        player.gravity += 1
        player.player_rect.y += player.gravity
        jumping = False
        
        # update screen
        screen.blit(bg, (0, 0))
        screen.blit(ground, ground_rect)
        screen.blit(player.surf, player.player_rect)
        for platform in platforms:
            screen.blit(platform.surf, platform.platform_rect)
        #screen.blit(platform.surf, platform.platform_rect)     # debug
        
        pygame.display.flip()
        
        # keeps game at 60FPS
        clock.tick(FPS)
    
    # If game loop is broken
    exit()
                
if __name__ == "__main__":
    main()