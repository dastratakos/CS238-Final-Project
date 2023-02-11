TITLE = "Geometry Dash AI"
BLOCK_SIZE = 32
SCREEN_BLOCKS = (25, 18)
SCREEN_SIZE = tuple(x * BLOCK_SIZE for x in SCREEN_BLOCKS)
GRAVITY = 0.86
MAX_FALL_VELOCITY = 100

# Player
JUMP_VELOCITY = 10
VELOCITY_X = 6

# Images
PLAYER_IMG_FILENAME = "assets/player.png"
BACKGROUND_IMG_FILENAME = "assets/background.png"
GROUND_IMG_FILENAME = "assets/ground.png"
HIGHLIGHT_IMG_FILENAME = "assets/highlight.png"