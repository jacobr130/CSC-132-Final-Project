import pygame
from random import randint
from settings import *

# The player character 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # PLAYER SETTINGS
        self.side_length = 150   # l and w of rect (square)
        self.dimensions = (self.side_length, self.side_length)
        self.movement_speed = 10
        self.gravity = 0
        self.jump_height = -25  # gravity offset
        
        self.surf = pygame.image.load("games/jacob_game/gfx/player.png").convert_alpha()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        
        self.rect = self.surf.get_rect(midbottom=(WIDTH//2, 800),
                                              bottomright=((WIDTH//2) + self.side_length, 800),
                                              bottomleft=((WIDTH//2) - self.side_length, 800))
        self.hitbox = self.rect.inflate(-35, 0)
        
    # Handle user input
    """
        For now, this function takes keyboard input.
        This will be changed when controller is implemented.
        Do I have any idea how that will work? notyet
    """
    def update(self, pressed):
        if pressed[K_LEFT]:
            self.rect.x -= self.movement_speed
            # if player goes off left of screen spawn at right
            if self.rect.bottomleft[0] == 0 - self.side_length:     
                self.rect.x = WIDTH + self.side_length
        
        elif pressed[K_RIGHT]:
            self.rect.x += self.movement_speed
            # if player goes off right of screen spawn at left
            if self.rect.bottomright[0] == WIDTH + self.side_length:
                self.rect.x = 0 - self.side_length
                
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
        self.rect = self.spawn()
    
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
        #return self.surf.get_rect(topleft=(500,700))   # debug 
    
    def eviscerate(self):   # i couldn't name it break()
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
    ground = pygame.transform.scale(ground, (WIDTH + (player.side_length*2), 800))
    ground_rect = ground.get_rect(topleft=(0, 800))
    collidables.append(ground_rect)
    
    # platforms
    platforms = []
    platform = Platform()
    #collidables.append(platform.rect)
    
    # handle fps
    clock = pygame.time.Clock()

    # Main game loop
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False

        # create platforms
        if len(platforms) < 10:
            platforms.append(Platform())
        
        # this may cause a bug later
        for platform in platforms:
            collidables.append(platform.rect)
        
        #for i in platforms:
            #print(f"num: {len(platforms)}")    # debug
            #print(i.rect)

        # handle user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        # player is constantly jumping; check for collisions between 
        # player and all other objects
        ## TODO: fix platform jumping bug: jump through platforms without
        ## auto jumping
        player.hitbox.center = player.rect.center
        for rect in collidables:
            if player.hitbox.colliderect(rect):
                player.gravity = player.jump_height
            
        player.gravity += WORLD_GRAVITY
        player.rect.y += player.gravity
        
        # update screen
        screen.blit(bg, (0, 0))
        screen.blit(ground, ground_rect)
        screen.blit(player.surf, player.rect)
        for platform in platforms:
            screen.blit(platform.surf, platform.rect)
        #screen.blit(platform.surf, (100, 700))     # debug
        
        pygame.display.flip()
        
        # keeps game at 60FPS
        clock.tick(FPS)
    
    # If game loop is broken
    exit()
                
if __name__ == "__main__":
    main()