from pygame.locals import (
    K_RIGHT,
    K_LEFT,
    K_SPACE,
    QUIT,
)

# Game window
from screeninfo import get_monitors

# this makes the game fullscreen no matter what
# monitor is being used
for monitor in get_monitors():
    if monitor.is_primary == True:
        screen = monitor

WIDTH = screen.width
HEIGHT = screen.height

# In-game
FPS = 60
WORLD_GRAVITY = 0.8