import pygame
from sys import exit
from random import randint, choice
from games.jacob_game.main import GameOver

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
        player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
        self.player_walk = [player_walk_1, player_walk_2]
        self.player_index = 0
        self.player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (80, 300))
        self.gravity = 0

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            if self.rect.bottom >= 300:
                self.gravity = -20

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        if self.rect.bottom < 300:
            self.image = self.player_jump

        else:
            self.player_index += 0.1
            if self.player_index >= len(self.player_walk):
                self.player_index = 0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation_state()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type):
        super().__init__()
        
        if type == "fly":
            fly_1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
            fly_2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 200

        else:
            snail_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
            snail_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos = 300

        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(midbottom = (randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames):
            self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -= 6
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = text_font.render("Score: " + str(current_time), False, (64, 64, 64))
    score_rect = score_surface.get_rect(center = (400, 50))
    screen.blit(score_surface, score_rect)
    return current_time

def obstacle_movement(obstacle_list):
    if obstacle_list:
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= randint(5, 8)
            if obstacle_rect.bottom == 300:
                screen.blit(snail_surface, obstacle_rect)
            else:
                screen.blit(fly_surface, obstacle_rect)
        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]
        return obstacle_list
    
    else:
        return []
    
def collisions(player, obstacles):
    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def collision_sprite():
    if pygame.sprite.spritecollide(player.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True

def player_animation():
    global player_surface, player_index

    if player_rect.bottom < 300:
        player_surface = player_jump
    else:
        player_index += 0.1
        if player_index >= len(player_walk): 
            player_index = 0
        player_surface = player_walk[int(player_index)]

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 400

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Astro Runner")

text_font = pygame.font.Font("font/Pixeltype.ttf", 50)

player = pygame.sprite.GroupSingle()
player.add(Player())

start_time = 0

obstacle_group = pygame.sprite.Group()

sky_surface = pygame.image.load("graphics/Sky.png").convert()
ground_surface = pygame.image.load("graphics/ground.png").convert()

#score_surface = text_font.render("My Game", False, (64, 64, 64))
#score_rect = score_surface.get_rect(center = (400, 50))

snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
snail_frames = [snail_frame_1, snail_frame_2]
snail_frame_index = 0
snail_surface = snail_frames[snail_frame_index]

fly_frame_1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
fly_frame_2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()
fly_frames = [fly_frame_1, fly_frame_2]
fly_frame_index = 0
fly_surface = fly_frames[fly_frame_index]

obstacle_rect_list = []

player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
player_walk = [player_walk_1, player_walk_2]
player_index = 0
player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

player_surface = player_walk[player_index]
player_rect = player_surface.get_rect(midbottom = (80, 300))
player_gravity = 0

player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
player_stand_rect = player_stand.get_rect(center = (400, 200))

game_name = text_font.render("Astro Runner", False, (111, 196, 169))
game_name_rect = game_name.get_rect(center = (400, 80))

game_message = text_font.render("Press space to start", False, (111, 196, 169))
game_message_rect = game_message.get_rect(center = (400, 320))

obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer, randint(1000, 1150))

snail_animation_timer = pygame.USEREVENT + 2
pygame.time.set_timer(snail_animation_timer, 500)

fly_animation_timer = pygame.USEREVENT + 3
pygame.time.set_timer(fly_animation_timer, 200)

def main():
    pygame.init()

    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 400

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Astro Runner")

    clock = pygame.time.Clock()

    text_font = pygame.font.Font("font/Pixeltype.ttf", 50)

    game_active = True

    start_time = 0

    score = 0

    # player = pygame.sprite.GroupSingle()
    # player.add(Player())

    # obstacle_group = pygame.sprite.Group()

    # sky_surface = pygame.image.load("graphics/Sky.png").convert()
    # ground_surface = pygame.image.load("graphics/ground.png").convert()

    # #score_surface = text_font.render("My Game", False, (64, 64, 64))
    # #score_rect = score_surface.get_rect(center = (400, 50))

    # snail_frame_1 = pygame.image.load("graphics/snail/snail1.png").convert_alpha()
    # snail_frame_2 = pygame.image.load("graphics/snail/snail2.png").convert_alpha()
    # snail_frames = [snail_frame_1, snail_frame_2]
    # snail_frame_index = 0
    # snail_surface = snail_frames[snail_frame_index]

    # fly_frame_1 = pygame.image.load("graphics/Fly/fly1.png").convert_alpha()
    # fly_frame_2 = pygame.image.load("graphics/Fly/fly2.png").convert_alpha()
    # fly_frames = [fly_frame_1, fly_frame_2]
    # fly_frame_index = 0
    # fly_surface = fly_frames[fly_frame_index]

    # obstacle_rect_list = []

    # player_walk_1 = pygame.image.load("graphics/Player/player_walk_1.png").convert_alpha()
    # player_walk_2 = pygame.image.load("graphics/Player/player_walk_2.png").convert_alpha()
    # player_walk = [player_walk_1, player_walk_2]
    # player_index = 0
    # player_jump = pygame.image.load("graphics/Player/jump.png").convert_alpha()

    # player_surface = player_walk[player_index]
    # player_rect = player_surface.get_rect(midbottom = (80, 300))
    # player_gravity = 0

    # player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
    # player_stand = pygame.transform.rotozoom(player_stand, 0, 2)
    # player_stand_rect = player_stand.get_rect(center = (400, 200))

    # game_name = text_font.render("Astro Runner", False, (111, 196, 169))
    # game_name_rect = game_name.get_rect(center = (400, 80))

    # game_message = text_font.render("Press space to start", False, (111, 196, 169))
    # game_message_rect = game_message.get_rect(center = (400, 320))

    # obstacle_timer = pygame.USEREVENT + 1
    # pygame.time.set_timer(obstacle_timer, randint(1000, 1150))

    # snail_animation_timer = pygame.USEREVENT + 2
    # pygame.time.set_timer(snail_animation_timer, 500)

    # fly_animation_timer = pygame.USEREVENT + 3
    # pygame.time.set_timer(fly_animation_timer, 200)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False

            if game_active == True:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if player_rect.bottom >= 300:
                            player_gravity = -20

            else:
                if event.type == pygame.KEYUP:
                    if event.type == pygame.K_r:
                        game_active = True
                        start_time = int(pygame.time.get_ticks() / 1000)

            if game_active:
                if event.type == obstacle_timer:
                    obstacle_group.add(Obstacle(choice(["fly", "snail", "snail", "snail"])))
                    #if randint(0, 2):
                        #obstacle_rect_list.append(snail_surface.get_rect(midbottom = (randint(900, 1100), 300)))
                
                    #else:
                        #obstacle_rect_list.append(fly_surface.get_rect(midbottom = (randint(900, 1100), 200)))

                if event.type == snail_animation_timer:
                    if snail_frame_index == 0:
                        snail_frame_index = 1

                    else:
                        snail_frame_index = 0

                    snail_surface = snail_frames[snail_frame_index]

                if event.type == fly_animation_timer:
                    if fly_frame_index == 0:
                        fly_frame_index = 1

                    else:
                        fly_frame_index = 0

                    fly_surface = fly_frames[fly_frame_index]

        if game_active == True:
            screen.blit(sky_surface, (0, 0))
            screen.blit(ground_surface, (0, 300))
            #pygame.draw.rect(screen, "#c0e8ec" , score_rect, 0, 10)
            #screen.blit(score_surface, score_rect)
            score = display_score()
        
            #snail_rect.x -= 4
            #if snail_rect.right <= -100:
                #snail_rect.left = 800
            #screen.blit(snail_surface, snail_rect)
        
            #player_gravity += 1
            #player_rect.y += player_gravity
            #if player_rect.bottom >= 300:
                #player_rect.bottom = 300
            #player_animation()
            #screen.blit(player_surface, player_rect)
            player.draw(screen)
            player.update()

            obstacle_group.draw(screen)
            obstacle_group.update()

            #obstacle_rect_list = obstacle_movement(obstacle_rect_list)

            game_active = collision_sprite()
            #game_active = collisions(player_rect, obstacle_rect_list)

        else:
            screen.fill((94, 129, 162))
            screen.blit(player_stand, player_stand_rect)
            obstacle_rect_list.clear()
            player_rect.midbottom = (80, 300)
            player_gravity = 0

            score_message = text_font.render(f"Your score: {score}", False, (111, 196, 169))
            score_message_rect = score_message.get_rect(center = (400, 320))
            screen.blit(game_name, game_name_rect)

            if score == 0:
                screen.blit(game_message, game_message_rect)

            else:
                screen.blit(score_message, score_message_rect)

        pygame.display.update()
        
        clock.tick(60)

    pygame.display.quit()
    raise GameOver

if __name__ == "__main__":
    main()
