from pygame.locals import (
    K_RIGHT,
    K_LEFT,
    K_SPACE,
    K_RETURN,
    K_ESCAPE,
    QUIT,
)

# Game window
WIDTH = 1400
HEIGHT = 900

# Assets
texture_player_r = "games/jacob_game/gfx/player_r.png"
texture_player_l = "games/jacob_game/gfx/player_l.png"
texture_floor = "games/jacob_game/gfx/ground.png"
texture_bg = "games/jacob_game/gfx/sky.png"
texture_platform_short = "games/jacob_game/gfx/platform_short.png"
font_retro = "games/jacob_game/gfx/computer.ttf"

# In-game
FPS = 60
WORLD_GRAVITY = 0.8

# Player settings
PLAYER_ACCELERATION = 2
PLAYER_FRICTION = -0.12

# colors
BG_COLOR = (34, 44, 48)
GREEN = (0, 255, 0)