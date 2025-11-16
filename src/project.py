import pygame
import sys
import random

TILE_SIZE = 32
FPS = 60

# Colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)


# map
def load_level():
    """
    Returns a simple map as a 2D list.
    0 = empty space
    1 = wall
    2 = dot
    """
    level = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 ],
        [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1],
        [1, 2, 1, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 1],
        [1, 2, 1, 2, 0, 2, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]
    return level

def is_wall(level, x, y):
    """Check if a tile is a wall given pixel coordinates."""
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    if 0 <= row < len(level) and 0 <= col < len(level[0]):
        return level[row][col] == 1
    return True  

def random_direction():
    # Return a random movement direction vector
    return random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

def main():
    pygame.init()
    flags = pygame.RESIZABLE
    screen_size = (1280, 720)
    screen = pygame.display.set_mode((screen_size), flags)
    pygame.display.set_caption("Maze game")
    clock = pygame.time.Clock()

    level = load_level()
    player_x, player_y = 64, 64
    speed = 3
    score = 0

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #  Movement/ keybindings 
        keys = pygame.key.get_pressed()
        new_x, new_y = player_x, player_y
        if keys[pygame.K_LEFT]:
            new_x -= speed
        if keys[pygame.K_RIGHT]:
            new_x += speed
        if keys[pygame.K_UP]:
            new_y -= speed
        if keys[pygame.K_DOWN]:
            new_y += speed

        # enemies setup
        enemy_direction = random_direction()
        enemy_x, enemy_y = 320, 224
        ex, ey = enemy_x, enemy_y
        enemy_speed = 2
        enemy_timer = 0
        game_over = False

        # Enemy Movement
        enemy_timer += 1
        if enemy_timer > 30:  # Change direction every 30 frames
            enemy_direction = random_direction()
            enemy_timer = 0

        ex += enemy_x + enemy_direction[0] * enemy_speed
        ey += enemy_y + enemy_direction[1] * enemy_speed

        # enemy collision hits walls choose new direction
        if is_wall(level, ex, ey):
            enemy_direction = random_direction()
        else:
            enemy_x, enemy_y = ex, ey
        
        #collision with enemy
        if (abs(player_x - enemy_x) < TILE_SIZE) and (abs(player_y - enemy_y) < TILE_SIZE):
            game_over = True
            print("Game Over! Final Score:", score)
            running = False

        # Collision Detection 
        col = new_x // TILE_SIZE
        row = new_y // TILE_SIZE
        if level[row][col] != 1:  # Not a wall
            player_x, player_y = new_x, new_y

        # Dots
        col = player_x // TILE_SIZE
        row = player_y // TILE_SIZE
        if level[row][col] == 2:
            level[row][col] = 0
            score += 10

        # character and walls drawing
        screen.fill(BLACK)
        for row_idx, row in enumerate(level):
            for col_idx, tile in enumerate(row):
                x = col_idx * TILE_SIZE
                y = row_idx * TILE_SIZE
                if tile == 1:
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    pygame.draw.circle(screen, WHITE, (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 4)

        pygame.draw.circle(screen, RED, (player_x, player_y), TILE_SIZE // 2)

        # score
        font = pygame.font.SysFont(None, 30)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # game over message
        if game_over:
            msg = font.render("GAME OVER!", True, RED)
            screen.blit(msg, (screen_size[0] // 2 - msg.get_width() // 2, screen_size[1] // 2 - msg.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

