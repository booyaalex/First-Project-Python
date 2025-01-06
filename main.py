import math
import random
import pygame


# Declare Variables
score = 0
game_over = False

PLAYER_SPRITE = pygame.image.load("images/cat.png")
PLAYER_SPRITE = pygame.transform.scale(PLAYER_SPRITE, (65, 65))
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 40
PLAYER_HEALTH = 3
PLAYER_SPEED = 5

BULLET_WIDTH = 15
BULLET_HEIGHT = 15
BULLET_SPEED = 10
BULLET_DAMAGE = 1

ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_HEALTH = 3
ENEMY_SPEED = 1.75
ENEMY_DAMAGE = 1
enemy_spawn_rate = 1500  # Starting Value
ENEMY_MIN_SPAWN_RATE = 500

pygame.init()
pygame.font.init()
text = pygame.font.SysFont("Comic Sans MS", 30)
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
deltatime = 0
running = True


class Bullet:
    x: 0
    y: 0
    width: 0
    height: 0
    dx: 0
    dy: 0
    speed: 0
    damage: 0

    def __init__(self, x, y, mx, my):
        self.x = int(x)
        self.y = int(y)
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.speed = BULLET_SPEED
        self.damage = BULLET_DAMAGE

        dx = mx - self.x
        dy = my - self.y
        self.dx = dx / math.sqrt(dx * dx + dy * dy) * self.speed
        self.dy = dy / math.sqrt(dx * dx + dy * dy) * self.speed


class Enemy:
    enemy_type: "normal"
    x: 0
    y: 0
    dx: 0
    dy: 0
    width: 0
    height: 0
    color: "blue"
    health: 0
    speed: 0
    damage: 0

    def __init__(self, enemy_type, x, y):
        self.enemy_type = enemy_type
        self.x = x
        self.y = y
        self.dx = player["x"] - x
        self.dy = player["y"] - y
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.health = ENEMY_HEALTH
        self.speed = ENEMY_SPEED
        self.damage = ENEMY_DAMAGE

        if enemy_type == "normal":
            self.color = "blue"
            self.damage = 1
        elif enemy_type == "rocket":
            self.color = "red"
            self.speed = 5
            self.damage = 1
            self.dx /= math.sqrt(self.dx * self.dx + self.dy * self.dy) / self.speed
            self.dy /= math.sqrt(self.dx * self.dx + self.dy * self.dy) / self.speed


# Events
def key_presses(keys):
    if keys[pygame.K_d]:
        player["x"] += player["speed"]
    if keys[pygame.K_a]:
        player["x"] -= player["speed"]
    if keys[pygame.K_s]:
        player["y"] += player["speed"]
    if keys[pygame.K_w]:
        player["y"] -= player["speed"]


def mouse_click():
    mx, my = pygame.mouse.get_pos()
    b = Bullet(player["x"], player["y"], mx, my)
    bullet_list.append(b)


def is_off_screen(self):
    if (
        self.x < 0
        or self.x + self.width > screen.get_width()
        or self.y < 0
        or self.y + self.height > screen.get_height()
    ):
        return True
    else:
        return False


# Player
player = {
    "x": screen.get_width() / 2,
    "y": screen.get_height() / 2,
    "width": PLAYER_WIDTH,
    "height": PLAYER_HEIGHT,
    "health": PLAYER_HEALTH,
    "speed": PLAYER_SPEED,
}
bullet_list = []

# Enemy
enemy_list = []

SPAWN_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(SPAWN_ENEMY, max(enemy_spawn_rate, ENEMY_MIN_SPAWN_RATE))


def spawn_enemy():
    e = Enemy("normal", 0, 0)
    x = random.randrange(0, screen.get_width())
    y = random.randrange(0, screen.get_height())
    while abs(x - player["x"]) < 100 and abs(y - player["y"]) < 100:
        x = random.randrange(0, screen.get_width())
        y = random.randrange(0, screen.get_height())
    if random.randrange(0, 5) == 4:
        e = Enemy("rocket", x, y)
    else:
        e = Enemy("normal", x, y)
    enemy_list.append(e)

    pygame.time.set_timer(SPAWN_ENEMY, max(enemy_spawn_rate, ENEMY_MIN_SPAWN_RATE))


while running:
    # Events
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONUP:
            mouse_click()
        if event.type == SPAWN_ENEMY:
            enemy_spawn_rate -= 10
            spawn_enemy()
        if event.type == pygame.QUIT:
            running = False
    key_presses(pygame.key.get_pressed())

    if not game_over:
        # Clear Screen
        screen.fill("white")

        # Player
        player_rect = pygame.Rect(
            player["x"], player["y"], player["width"], player["height"]
        )
        pygame.draw.rect(screen, "white", player_rect)
        screen.blit(
            PLAYER_SPRITE,
            (player["x"] - player["width"] / 2, player["y"] - player["height"] / 2),
        )

        if player["health"] <= 0:
            game_over = True

        for b in bullet_list:
            b.x += b.dx
            b.y += b.dy
            bullet_rect = pygame.Rect(b.x, b.y, b.width, b.height)
            pygame.draw.rect(screen, "black", bullet_rect)
            if is_off_screen(b):
                bullet_list.remove(b)

        # Enemies
        for e in enemy_list:
            if e.enemy_type == "normal":
                e.dx = player["x"] - e.x
                e.dy = player["y"] - e.y
                e.x += e.dx / math.sqrt(e.dx * e.dx + e.dy * e.dy) * e.speed
                e.y += e.dy / math.sqrt(e.dx * e.dx + e.dy * e.dy) * e.speed
            elif e.enemy_type == "rocket":
                e.x += e.dx
                e.y += e.dy
                if is_off_screen(e):
                    enemy_list.remove(e)
            enemy_rect = pygame.Rect(e.x, e.y, e.width, e.height)
            pygame.draw.rect(screen, e.color, enemy_rect)

            if len(bullet_list) < 0:
                break
            for b in bullet_list:
                if pygame.Rect.colliderect(
                    enemy_rect, pygame.Rect(b.x, b.y, b.width, b.height)
                ):
                    bullet_list.remove(b)
                    e.health -= b.damage
                    if e.health > 0:
                        break
                    enemy_list.remove(e)
                    score += 5
            if pygame.Rect.colliderect(enemy_rect, player_rect):
                player["health"] -= 1
                if e.enemy_type == "rocket":
                    enemy_list.remove(e)
                else:
                    e.x -= e.dx
                    e.y -= e.dy

        # UI
        pygame.draw.rect(screen, "red", pygame.Rect(5, 5, 200, 20))
        pygame.draw.rect(
            screen,
            "green",
            pygame.Rect(5, 5, (200 / PLAYER_HEALTH) * player["health"], 20),
        )

        score_text = text.render("Score: " + str(score), False, (0, 0, 0))
        screen.blit(score_text, (5, 30))

    else:
        game_over_text = text.render("Game Over", False, (0, 0, 0))
        screen.blit(
            game_over_text,
            (
                screen.get_width() / 2 - game_over_text.get_width() / 2,
                screen.get_height() / 2 - game_over_text.get_height() / 2,
            ),
        )

    pygame.display.flip()
    deltatime = clock.tick(60) / 1000


pygame.quit()
