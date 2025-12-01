import pygame
import sys
import random

TILE_SIZE = 32
FPS = 60

# character colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)

DIR_UP = (0, -1)
DIR_DOWN = (0, 1)
DIR_LEFT = (-1, 0)
DIR_RIGHT = (1, 0)


def load_level():
    return [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 2, 0, 1, 2, 1],
        [1, 2, 1, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 2, 2, 1, 1, 1, 2, 1],
        [1, 2, 1, 0, 0, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 2, 2, 2, 2, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 1],
        [1, 1, 1, 0, 0, 1, 1, 1, 2, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 1, 2, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 1, 2, 1],
        [1, 2, 1, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 2, 1, 1, 1, 2, 1, 1, 2, 2, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 0, 2, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 2, 2, 1, 2, 1, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1, 1, 1, 2, 2, 2, 1],
        [1, 2, 1, 2, 1, 1, 2, 1, 2, 1, 0, 0, 2, 1, 2, 1, 0, 0, 2, 1, 0, 2, 1, 1, 1, 2, 2, 1, 1],
        [1, 0, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 1, 1, 1, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 2, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 2, 0, 1],
        [1, 2, 2, 2, 2, 2, 2, 1, 0, 0, 0, 1, 2, 2, 2, 1, 0, 0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 0, 1],
        [1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1, 2, 2, 2, 2, 2, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    ]


# Collision detection
def can_move(level, x, y, direction, speed):
    dx, dy = direction
    r = TILE_SIZE // 2 - 2
    new_x = x + dx * speed
    new_y = y + dy * speed

    corners = [
        (new_x - r, new_y - r),
        (new_x + r, new_y - r),
        (new_x - r, new_y + r),
        (new_x + r, new_y + r),
    ]

    for cx, cy in corners:
        col = cx // TILE_SIZE
        row = cy // TILE_SIZE

        if row < 0 or col < 0 or row >= len(level) or col >= len(level[0]):
            return False
        if level[row][col] == 1:
            return False

    return True


class Enemy:
    def __init__(self, x, y, color, speed):
        self.x = x
        self.y = y
        self.color = color
        self.speed = speed
        self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])

    def get_tile_pos(self):
        return (self.y // TILE_SIZE, self.x // TILE_SIZE)

    def at_tile_center(self):
        return (
            self.x % TILE_SIZE == TILE_SIZE // 2 and
            self.y % TILE_SIZE == TILE_SIZE // 2
        )

    def chase(self, level, player_tile):
        row, col = self.get_tile_pos()
        pr, pc = player_tile
        options = []

        if level[row - 1][col] != 1:
            options.append((abs(pr - (row - 1)) + abs(pc - col), DIR_UP))
        if level[row + 1][col] != 1:
            options.append((abs(pr - (row + 1)) + abs(pc - col), DIR_DOWN))
        if level[row][col - 1] != 1:
            options.append((abs(pr - row) + abs(pc - (col - 1)), DIR_LEFT))
        if level[row][col + 1] != 1:
            options.append((abs(pr - row) + abs(pc - (col + 1)), DIR_RIGHT))

        if not options:
            return self.direction

        _, best = min(options, key=lambda x: x[0])
        return best

    def move(self, level, player_tile):
        if self.at_tile_center():
            self.direction = self.chase(level, player_tile)

        dx, dy = self.direction
        nx = self.x + dx * self.speed
        ny = self.y + dy * self.speed

        col = nx // TILE_SIZE
        row = ny // TILE_SIZE
        if level[row][col] != 1:
            self.x = nx
            self.y = ny
        else:
            self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])

    def get_rect(self):
        return pygame.Rect(self.x - 12, self.y - 12, 24, 24)

    def draw(self, screen, sprite):
        screen.blit(sprite, (self.x - TILE_SIZE // 2, self.y - TILE_SIZE // 2))


dot_respawn_time = {}
DOT_RESPAWN_DELAY = 5000  # ms


def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    # player sprite
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # dot sprite
    dot_img = pygame.image.load("Diamond.png").convert_alpha()
    dot_img = pygame.transform.scale(dot_img, (10, 10))

    # rotated sprites
    player_sprites = {
        DIR_RIGHT: player_img,
        DIR_LEFT: pygame.transform.flip(player_img, True, False),
        DIR_UP: pygame.transform.rotate(player_img, 90),
        DIR_DOWN: pygame.transform.rotate(player_img, -90),
    }

    # enemy sprite
    enemy_img = pygame.image.load("enemy.png").convert_alpha()
    enemy_img = pygame.transform.scale(enemy_img, (TILE_SIZE, TILE_SIZE))

    level = load_level()

    # player start bottom row
    player_x = 1 * TILE_SIZE + TILE_SIZE // 2
    player_y = 13 * TILE_SIZE + TILE_SIZE // 2

    speed = 2
    score = 0
    game_over = False

    current_dir = DIR_RIGHT
    desired_dir = DIR_RIGHT

    enemies = [
        Enemy(320, 225, RED, 2),
        Enemy(640, 224, RED, 2),
        Enemy(400, 336, RED, 2),
    ]

    running = True
    while running:

        # EVENTS
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: desired_dir = DIR_LEFT
        elif keys[pygame.K_RIGHT]: desired_dir = DIR_RIGHT
        elif keys[pygame.K_UP]: desired_dir = DIR_UP
        elif keys[pygame.K_DOWN]: desired_dir = DIR_DOWN

        # center check
        on_center = (
            player_x % TILE_SIZE == TILE_SIZE // 2 and
            player_y % TILE_SIZE == TILE_SIZE // 2
        )

        if on_center and can_move(level, player_x, player_y, desired_dir, speed):
            current_dir = desired_dir

        # MOVE
        if can_move(level, player_x, player_y, current_dir, speed):
            dx, dy = current_dir
            player_x += dx * speed
            player_y += dy * speed

        # ENEMIES
        player_tile = (player_y // TILE_SIZE, player_x // TILE_SIZE)
        player_rect = pygame.Rect(player_x - 16, player_y - 16, 32, 32)

        for enemy in enemies:
            enemy.move(level, player_tile)
            if enemy.get_rect().colliderect(player_rect):
                game_over = True

        # DOTS
        col = player_x // TILE_SIZE
        row = player_y // TILE_SIZE
        if level[row][col] == 2:
            level[row][col] = 0
            score += 10
            dot_respawn_time[(row, col)] = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        for (r, c), t in list(dot_respawn_time.items()):
            if now - t > DOT_RESPAWN_DELAY:
                level[r][c] = 2
                del dot_respawn_time[(r, c)]

        # DRAW
        screen.fill(BLACK)

        for r, row_data in enumerate(level):
            for c, tile in enumerate(row_data):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if tile == 1:
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    screen.blit(dot_img, (x + TILE_SIZE//2 - 5, y + TILE_SIZE//2 - 5))

        screen.blit(player_sprites[current_dir],
                    (player_x - TILE_SIZE//2, player_y - TILE_SIZE//2))

        for enemy in enemies:
            enemy.draw(screen, enemy_img)

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

        # GAME OVER + RETRY
        if game_over:
            msg = font.render("GAME OVER!", True, RED)
            retry_msg = font.render("Press any key to retry", True, WHITE)

            screen.blit(msg, (640 - msg.get_width() // 2, 300))
            screen.blit(retry_msg, (640 - retry_msg.get_width() // 2, 360))
            pygame.display.flip()

            # Wait for key
            waiting = True
            while waiting:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        return main()  # restart

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
