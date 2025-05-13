import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 390
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Geometry Dash Replica")

# Colors
WHITE = (230, 230, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game constants
GRAVITY = 0.5
JUMP_STRENGTH = -10
OBSTACLE_SPEED = 5

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.y = SCREEN_HEIGHT - 100
        self.velocity = 0

    def update(self):
        # Apply gravity
        self.velocity += GRAVITY
        self.rect.y += self.velocity

        # Prevent player from falling below the ground
        if self.rect.y >= SCREEN_HEIGHT - 100:
            self.rect.y = SCREEN_HEIGHT - 100
            self.velocity = 0

    def jump(self):
        if self.rect.y == SCREEN_HEIGHT - 100:  # Can only jump if on the ground
            self.velocity = JUMP_STRENGTH

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= OBSTACLE_SPEED
        if self.rect.x < -self.rect.width:
            self.kill()  # Remove obstacle when it goes offscreen

# Initialize player and obstacles
player = Player()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

obstacles = pygame.sprite.Group()

# Function to spawn obstacles
def spawn_obstacle():
    obstacle_height = random.randint(30, 100)
    obstacle = Obstacle(SCREEN_WIDTH, SCREEN_HEIGHT - 100 - obstacle_height, 30, obstacle_height)
    all_sprites.add(obstacle)
    obstacles.add(obstacle)

# Game loop
running = True
spawn_timer = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.jump()

    # Spawn obstacles periodically
    spawn_timer += 1
    if spawn_timer > 60:  # Spawn obstacle every 60 frames
        spawn_obstacle()
        spawn_timer = 0

    # Update
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollide(player, obstacles, False):
        print("Game Over!")
        running = False

    # Draw everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Refresh display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

pygame.quit()
