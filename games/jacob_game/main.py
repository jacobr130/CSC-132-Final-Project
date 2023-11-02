import pygame
from pygame.math import Vector2
from random import randint
import shelve
import os
from games.jacob_game.settings import * # console version

# Center window on screen
os.environ['SDL_VIDEO_CENTERED'] = '1'

class GameOver(Exception):
    def __init__(self):
        super().__init__()

# The player character 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        
        # PLAYER SETTINGS
        self.side_length = 150   # l and w of rect (square)
        self.dimensions = (self.side_length, self.side_length)
        self.gravity = 0
        self.jump_height = -26  # gravity offset
        
        self.surf = pygame.image.load(texture_player_r).convert_alpha()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        
        self.rect = self.surf.get_rect(midbottom=(WIDTH//2, HEIGHT-280))
        self.hitbox = self.rect.inflate(-35, 0)
        
        self.pos = Vector2(self.rect.topleft[0], self.rect.topleft[1])
        self.velocity = Vector2(0, 0)
        self.acceleration = Vector2(0, 0)
        
    # Handle user input
    def update(self, pressed):
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
            self.pos.x = WIDTH + self.side_length   # updating rect.x by pos so pos is changing
        
        # if player goes off right of screen spawn at left   
        if self.rect.left >= WIDTH + self.side_length:
            self.pos.x = 0 - self.side_length 

# Platforms you gotta jump on
class Platform(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        super(Platform, self).__init__()
        
        # PLATFORM SETTINGS
        self.length = 250
        self.height = 50
        self.dimensions = (self.length, self.height)
        
        self.surf = self.pick_sprite()
        self.surf = pygame.transform.scale(self.surf, self.dimensions)
        self.rect = self.surf.get_rect(topleft=(x_pos, y_pos))
    
    def pick_sprite(self):
        """
            Yes, this function is pointless
        """
        return pygame.image.load(texture_platform_short).convert_alpha()
            
def main():

    collidables = pygame.sprite.Group()   # maybe later
    
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Computer Jump!")
    
    player = Player()
    
    # sky
    bg = pygame.image.load(texture_bg).convert()
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    
    # ground that the game starts on
    ground = pygame.sprite.Sprite()
    ground.surf = pygame.image.load(texture_floor).convert()
    ground.surf = pygame.transform.scale(ground.surf, (WIDTH*2, HEIGHT-280))
    ground.rect = ground.surf.get_rect(topleft=(-800, 800))
    collidables.add(ground)
    
    # platforms at game start
    platforms = [Platform(100, HEIGHT-500), Platform(WIDTH-300, 300), Platform(300, HEIGHT-300)]
    
    # handle fps
    clock = pygame.time.Clock()
    
    dead = False
    score = 0

    # Main game loop
    RUNNING = True
    while RUNNING:
        for event in pygame.event.get():
            if event.type == QUIT:
                RUNNING = False
        
        # this may cause a bug later
        for platform in platforms:
            collidables.add(platform)
            
        # handle user input
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        
        # player is constantly jumping; check for collisions between 
        # player and all other objects if player is falling
        player.hitbox.center = player.rect.center
        if player.velocity.y > 0:
            collision = pygame.sprite.spritecollide(player, collidables, False)
            if collision and player.hitbox.colliderect(collision[0].rect):
                if player.hitbox.bottom < collision[0].rect.bottom:
                    player.pos.y = collision[0].rect.top - player.side_length    # because pos is rect topleft
                    player.rect.y = player.pos.y

                    player.velocity.y = player.jump_height
        
        # scroll screen up (aka move sprites down)
        if player.rect.top <= HEIGHT / 4:
            player.pos.y += abs(player.velocity.y)
            for platform in platforms:
                platform.rect.y += abs(player.velocity.y)
                # delete platforms that go offscreen
                if platform.rect.top > HEIGHT:
                    platforms.remove(platform)
                    platform.kill()
            if ground.rect.top < HEIGHT:
                ground.rect.y += abs(player.velocity.y)
            
            score += int(abs(player.velocity.y))
            
        # create new platforms
        while len(platforms) < 6:
            # ensure platforms don't intersect
            while True:
                x, y = randint(0, WIDTH-250), randint(-20, -18)
                
                temp_rect = pygame.Rect(x, y, 250, 50)
                if not any(plat for plat in platforms if temp_rect.colliderect(plat.rect)):
                    break
                
            p = Platform(x, y)
            platforms.append(p)
        
        # update screen
        screen.blit(bg, (0, 0))
        if ground.rect.top < HEIGHT:
            screen.blit(ground.surf, ground.rect)
        screen.blit(player.surf, player.rect)
        for platform in platforms:
            screen.blit(platform.surf, platform.rect)
        
        # score keeper
        font = pygame.font.Font(font_retro, 32)
        score_text = font.render(f"Score: {score}", True, GREEN, None)
        score_text_rect = score_text.get_rect(topleft=(WIDTH-550, 50))
        screen.blit(score_text, score_text_rect)
        
        # show fps (right of score)
        fps_text = font.render(f"FPS: {int(clock.get_fps() // 1)}", True, GREEN, None)
        fps_text_rect = fps_text.get_rect(topleft=(WIDTH-200, 50))
        screen.blit(fps_text, fps_text_rect)
        
        # if the player dies (r.i.p.)
        if player.rect.bottom >= HEIGHT:
            dead = True
            break
        
        pygame.display.flip()
        
        # keeps game at 60FPS
        clock.tick(FPS)
    
    # game loop is broken
    # read or update high score
    high_score = 20000
    #disk = shelve.open('games\jacob_game\score.txt')
    #high_score = disk["high_score"]
    if score > high_score:
        high_score = score
        #disk["high_score"] = high_score
        #disk.close()
    #disk.close()
        
    font = pygame.font.Font(font_retro, 100)
    
    # a bunch of stuff that should have been a class method
    text1 = font.render("You Lose!", True, GREEN, BG_COLOR)
    text1_rect = text1.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
    
    font = pygame.font.Font(font_retro, 50)
    text2 = font.render(f"Your Score: {score}", True, GREEN, BG_COLOR)
    text2_rect = text2.get_rect(center=(text1_rect.center[0], text1_rect.midbottom[1] + 20))
    
    text3 = font.render(f"High Score: {high_score}", True, GREEN, BG_COLOR)
    text3_rect = text3.get_rect(center=(text2_rect.center[0], text2_rect.midbottom[1] + 20))
    
    text4 = font.render("Press enter to restart or esc to quit", True, GREEN, BG_COLOR)
    text4_rect = text4.get_rect(center=(text2_rect.center[0], text2_rect.midbottom[1] + 100)) 
      
    while dead:    # probably should have made the game a class too
        
        for event in pygame.event.get():
            if event.type == QUIT:
                dead = False
            
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_RETURN]:
            main()
        elif pressed_keys[K_ESCAPE]:
            dead = False
        
        screen.blit(text1, text1_rect)
        screen.blit(text2, text2_rect)
        screen.blit(text3, text3_rect)
        screen.blit(text4, text4_rect)
        pygame.display.flip()
        
    # if the player is dead and quits (keep main menu running)
    pygame.display.quit()
    raise GameOver
                
if __name__ == "__main__":
    main()