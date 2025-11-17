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

# Directions
DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)


# --- MAP ---
def load_level():
    return [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
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
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]


def is_wall(level, x, y):
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    return level[row][col] == 1


# ENEMY CLASS —
class Enemy:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
        self.timer = 0

    def move(self, level):
        self.timer += 1
        if self.timer > 30:
            self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
            self.timer = 0

        dx, dy = self.direction
        new_x = self.x + dx * self.speed
        new_y = self.y + dy * self.speed

        if not is_wall(level, new_x, new_y):
            self.x = new_x
            self.y = new_y

    def draw(self, screen):
        pygame.draw.polygon(
            screen, RED,
            [(self.x, self.y - 12), (self.x - 12, self.y + 12), (self.x + 12, self.y + 12)]
        )

    def get_rect(self):
        return pygame.Rect(self.x - 12, self.y - 12, 24, 24)


# MAIN GAME —
def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    level = load_level()

    # Start on bottom row
    player_x = 1 * TILE_SIZE + TILE_SIZE // 2
    player_y = 13 * TILE_SIZE + TILE_SIZE // 2

    speed = 2
    score = 0
    game_over = False

    current_dir = DIR_RIGHT
    desired_dir = DIR_RIGHT

    # Correct collision check
    def can_move(direction):
        dx, dy = direction

        check_x = player_x + dx * (TILE_SIZE // 2 + speed)
        check_y = player_y + dy * (TILE_SIZE // 2 + speed)

        col = check_x // TILE_SIZE
        row = check_y // TILE_SIZE

        if row < 0 or col < 0 or row >= len(level) or col >= len(level[0]):
            return False

        return level[int(row)][int(col)] != 1

    enemies = [
        Enemy(320, 225, RED, 2),
        Enemy(640, 224, RED, 2),
        Enemy(400, 336, RED, 2),
    ]

    running = True
    while running:
        # INPUT —
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            desired_dir = DIR_LEFT
        elif keys[pygame.K_RIGHT]:
            desired_dir = DIR_RIGHT
        elif keys[pygame.K_UP]:
            desired_dir = DIR_UP
        elif keys[pygame.K_DOWN]:
            desired_dir = DIR_DOWN

        # Center check
        on_center = (
            player_x % TILE_SIZE == TILE_SIZE // 2 and
            player_y % TILE_SIZE == TILE_SIZE // 2
        )

        # Try turning
        if on_center and can_move(desired_dir):
            current_dir = desired_dir

        # Move + anti-sticking fix
        if can_move(current_dir):
            dx, dy = current_dir
            player_x += dx * speed
            player_y += dy * speed
        else:
            # NEW — SLIDE FIX
            dx, dy = current_dir
            if dx != 0:  # moving horizontally
                if can_move((0, 1)):
                    player_y += speed
                elif can_move((0, -1)):
                    player_y -= speed
            else:  # moving vertically
                if can_move((1, 0)):
                    player_x += speed
                elif can_move((-1, 0)):
                    player_x -= speed

        # ENEMY MOVEMENT —
        player_rect = pygame.Rect(player_x - 16, player_y - 16, 32, 32)

        for enemy in enemies:
            enemy.move(level)
            if enemy.get_rect().colliderect(player_rect):
                game_over = True

        # DOT COLLECTION —
        col = player_x // TILE_SIZE
        row = player_y // TILE_SIZE
        if level[row][col] == 2:
            level[row][col] = 0
            score += 10

        # DRAW —
        screen.fill(BLACK)

        # Walls and dots
        for r, row_data in enumerate(level):
            for c, tile in enumerate(row_data):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if tile == 1:
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    pygame.draw.circle(screen, WHITE, (x + 16, y + 16), 4)

        # Player
        pygame.draw.circle(screen, GREEN, (player_x, player_y), TILE_SIZE // 2)

        # Enemies
        for enemy in enemies:
            enemy.draw(screen)

        # Score
        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        # Game over screen
        if game_over:
            msg = font.render("GAME OVER!", True, RED)
            screen.blit(msg, (640 - msg.get_width() // 2, 360 - msg.get_height() // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
