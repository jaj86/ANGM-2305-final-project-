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


def tile_is_wall(level, x, y):
    col = x // TILE_SIZE
    row = y // TILE_SIZE
    return level[row][col] == 1


# Collision detection for player
def can_move(level, x, y, direction, speed):
    dx, dy = direction

    # Player hitbox radius
    r = TILE_SIZE // 2 - 2

    # Proposed new position
    new_x = x + dx * speed
    new_y = y + dy * speed

    # player hitbox
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
        self.timer = 0

    def move(self, level):
        self.timer += 1
        if self.timer > 30:
            self.direction = random.choice([DIR_UP, DIR_DOWN, DIR_LEFT, DIR_RIGHT])
            self.timer = 0

        dx, dy = self.direction
        nx = self.x + dx * self.speed
        ny = self.y + dy * self.speed

        if not tile_is_wall(level, nx, ny):
            self.x = nx
            self.y = ny

    def get_rect(self):
        return pygame.Rect(self.x - 12, self.y - 12, 24, 24)

    def draw(self, screen, sprite):
        screen.blit(sprite, (self.x - TILE_SIZE//2, self.y - TILE_SIZE//2))




def main():
    pygame.init()
    screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)
    pygame.display.set_caption("Maze Game")
    clock = pygame.time.Clock()

    # player sprite
    player_img = pygame.image.load("player.png").convert_alpha()
    player_img = pygame.transform.scale(player_img, (TILE_SIZE, TILE_SIZE))

    # Direction-based sprite rotation
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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]: desired_dir = DIR_LEFT
        elif keys[pygame.K_RIGHT]: desired_dir = DIR_RIGHT
        elif keys[pygame.K_UP]: desired_dir = DIR_UP
        elif keys[pygame.K_DOWN]: desired_dir = DIR_DOWN

        # direction change by grid
        on_center = (
            player_x % TILE_SIZE == TILE_SIZE // 2 and
            player_y % TILE_SIZE == TILE_SIZE // 2
        )

        if on_center and can_move(level, player_x, player_y, desired_dir, speed):
            current_dir = desired_dir

        # MOVEMENT 
        if can_move(level, player_x, player_y, current_dir, speed):
            dx, dy = current_dir
            player_x += dx * speed
            player_y += dy * speed

        else:
            # Slide like pacman
            dx, dy = current_dir
            if dx != 0:  # horizontal slide
                if can_move(level, player_x, player_y, (0, 1), speed):
                    player_y += speed
                elif can_move(level, player_x, player_y, (0, -1), speed):
                    player_y -= speed
            else:  # vertical slide
                if can_move(level, player_x, player_y, (1, 0), speed):
                    player_x += speed
                elif can_move(level, player_x, player_y, (-1, 0), speed):
                    player_x -= speed

        # ENEMY
        player_rect = pygame.Rect(player_x - 16, player_y - 16, 32, 32)

        for enemy in enemies:
            enemy.move(level)
            if enemy.get_rect().colliderect(player_rect):
                game_over = True

        # DOT COLLECTION
        col = player_x // TILE_SIZE
        row = player_y // TILE_SIZE
        if level[row][col] == 2:
            level[row][col] = 0
            score += 10

        # DRAW
        screen.fill(BLACK)

        for r, row_data in enumerate(level):
            for c, tile in enumerate(row_data):
                x = c * TILE_SIZE
                y = r * TILE_SIZE
                if tile == 1:
                    pygame.draw.rect(screen, BLUE, (x, y, TILE_SIZE, TILE_SIZE))
                elif tile == 2:
                    pygame.draw.circle(screen, WHITE, (x + 16, y + 16), 4)

        sprite = player_sprites[current_dir]
        screen.blit(sprite, (player_x - TILE_SIZE//2, player_y - TILE_SIZE//2))

        for enemy in enemies:
            enemy.draw(screen, enemy_img)

        font = pygame.font.SysFont(None, 30)
        screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))

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

