import pygame
from pygame.math import Vector2
from random import randint
from settings import *

# The player character 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # PLAYER SETTINGS
        self.side_length = 150   # l and w of rect (square)
        self.dimensions = (self.side_length, self.side_length)
        self.gravity = 0
        self.jump_height = -25  # gravity offset
        
        self.surf = pygame.image.load(texture_player_r).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        
        self.rect = self.surf.get_rect(midbottom=(WIDTH//2, 800))
        self.hitbox = self.rect.inflate(-35, 0)
        
        self.pos = Vector2(self.rect.topleft[0], self.rect.topleft[1])
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        
    # Handle user input
    def update(self, pressed):
        """
            For now, this function takes keyboard input.
            This will be changed when controller is implemented.
            Do I have any idea how that will work?
        """
        self.acceleration = Vector2(0, WORLD_GRAVITY)
        
        if pressed[K_LEFT]:
            self.surf = pygame.image.load(texture_player_l).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, self.dimensions)
            
            self.acceleration.x = PLAYER_ACCELERATION * -1
        
        if pressed[K_RIGHT]:
            self.surf = pygame.image.load(texture_player_r).convert_alpha()
            self.surf = pygame.transform.scale(self.surf, self.dimensions)
            
            self.acceleration.x = PLAYER_ACCELERATION
        
        # physics
        self.acceleration.x += self.velocity.x * PLAYER_FRICTION
        self.velocity += self.acceleration
        self.pos += self.velocity + 0.5 * self.acceleration
        self.rect.x = self.pos.x
        self.rect.y = self.pos.y
        
        # if player goes off left of screen spawn at right
        if self.rect.right <= 0 - self.side_length:
            print("left side triggering")     
            self.pos.x = WIDTH + self.side_length   # updating rect.x by pos so pos is changing
        
        # if player goes off right of screen spawn at left   
        if self.rect.left >= WIDTH + self.side_length:
            self.pos.x = 0 - self.side_length 
        
            
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
                return pygame.image.load(texture_platform_short).convert_alpha()
    
    def spawn(self):
        return self.surf.get_rect(topleft=(randint(0, WIDTH-self.length), randint(0, 800-self.height)))
        #return self.surf.get_rect(topleft=(500,700))   # debug 
    
    def eviscerate(self):   # i couldn't name it break()
        pass
            
def main():

    #collidables = []
    collidables2 = pygame.sprite.Group()   # maybe later
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    
    player = Player()
    
    # sky
    bg = pygame.image.load(texture_bg).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # ground that the game starts on
    ground = pygame.sprite.Sprite()
    ground.surf = pygame.image.load(texture_floor).convert()
    ground.surf = pygame.transform.scale(ground.surf, (WIDTH*2, 800))
    ground.rect = ground.surf.get_rect(topleft=(-800, 800))
    #collidables.append(ground_rect)
    collidables2.add(ground)
    
    # platforms
    platforms = []
    #platform = Platform()
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
            collidables2.add(platform)
            
        # handle user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        # player is constantly jumping; check for collisions between 
        # player and all other objects if player is falling
        player.hitbox.center = player.rect.center
        if player.velocity.y > 0:
            collision = pygame.sprite.spritecollide(player, collidables2, False)
            if collision and player.hitbox.colliderect(collision[0].rect):
                if player.hitbox.bottom < collision[0].rect.bottom:
                    player.pos.y = collision[0].rect.top - player.side_length    # because pos is rect topleft
                    player.rect.y = player.pos.y

                    player.velocity.y = player.jump_height
        
        # update screen
        screen.blit(bg, (0, 0))
        screen.blit(ground.surf, ground.rect)
        screen.blit(player.surf, player.rect)
        for platform in platforms:
            screen.blit(platform.surf, platform.rect)
        #screen.blit(platform.surf, platform.rect)     # debug
        
        pygame.display.flip()
        
        # keeps game at 60FPS
        clock.tick(FPS)
    
    # If game loop is broken
    exit()
                
if __name__ == "__main__":
    main()