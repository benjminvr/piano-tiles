import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Screen setup
WIDTH, HEIGHT = 400, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Piano Tiles (Simple Version)")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 50, 50)

# Tile settings
TILE_WIDTH = WIDTH // 4
TILE_HEIGHT = 150
TILE_SPEED = 4
SPEED_INCREMENT = 0.5  # Speed increase over time
BASE_SPAWN_INTERVAL = 800

# Game state
clock = pygame.time.Clock()
tiles = []
last_spawn_time = 0
running = True
game_over = False
score = 0
speed = TILE_SPEED
font = pygame.font.SysFont("arial", 30)

def spawn_row():
    """Spawn a new row of tiles (one black, three white)."""
    black_index = random.randint(0, 3)
    for i in range(4):
        color = BLACK if i == black_index else WHITE
        rect = pygame.Rect(i * TILE_WIDTH, -TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
        tiles.append({"rect": rect, "color": color, "clicked": False})

def draw_tiles():
    """Draw all tiles on screen."""
    for tile in tiles:
        pygame.draw.rect(SCREEN, tile["color"], tile["rect"])
        pygame.draw.rect(SCREEN, GRAY, tile["rect"], 1)  # borders

def reset_game():
    """Reset game state."""
    global tiles, score, speed, game_over, last_spawn_time
    tiles.clear()
    score = 0
    speed = TILE_SPEED
    game_over = False
    last_spawn_time = pygame.time.get_ticks()
    spawn_row()

# Start with one row
reset_game()

# Main game loop
while running:
    SCREEN.fill(WHITE)
    current_time = pygame.time.get_ticks()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            break

        if game_over:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                reset_game()
            continue

        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()
            for tile in tiles:
                if tile["rect"].collidepoint(x, y) and not tile["clicked"]:
                    if tile["color"] == BLACK:
                        tile["color"] = GRAY
                        tile["clicked"] = True
                        score += 1
                        # Slightly increase speed as player succeeds
                        speed += SPEED_INCREMENT / 10
                    else:
                        game_over = True
                    break

    if game_over:
        text = font.render(f"Game Over! Score: {score}", True, RED)
        tip = font.render("Press R to restart", True, RED)
        SCREEN.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - 40))
        SCREEN.blit(tip, (WIDTH/2 - tip.get_width()/2, HEIGHT/2))
        pygame.display.flip()
        clock.tick(60)
        continue

    # Spawn new tiles periodically
    spawn_interval = BASE_SPAWN_INTERVAL * (TILE_SPEED / speed)
    if current_time - last_spawn_time > spawn_interval:
        spawn_row()
        last_spawn_time = current_time
        # Gradually increase falling speed
        speed += SPEED_INCREMENT

    # Move tiles downward
    for tile in tiles:
        tile["rect"].y += speed

    # Check if a black tile reached bottom unclicked -> game over
    for tile in tiles:
        if tile["rect"].bottom >= HEIGHT and tile["color"] == BLACK and not tile["clicked"]:
            game_over = True
            break

    # Remove off-screen tiles
    tiles = [t for t in tiles if t["rect"].top < HEIGHT]

    # Draw tiles and score
    draw_tiles()
    score_text = font.render(f"Score: {score}", True, BLACK)
    SCREEN.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
