import pygame
import random

# Screen and scaling settings for a 16-bit style look
WIDTH, HEIGHT = 320, 240
SCALE = 2  # final window will be 640x480
FPS = 60

# Colours (bright 16-bit palette feel)
BLACK = (0, 0, 0)
STAR_COLOURS = [(255, 255, 255), (255, 255, 0), (0, 255, 255)]
PLAYER_COLOUR = (0, 255, 0)
BULLET_COLOUR = (255, 50, 50)
ENEMY_COLOUR = (180, 0, 255)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 8))
        self.image.fill(PLAYER_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.centery = HEIGHT // 2
        self.rect.x = 20
        self.speed = 3

    def update(self, keys):
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def shoot(self):
        bullet = Bullet(self.rect.right, self.rect.centery)
        return bullet

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((4, 2))
        self.image.fill(BULLET_COLOUR)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 5

    def update(self):
        self.rect.x += self.speed
        if self.rect.left > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((16, 8))
        self.image.fill(ENEMY_COLOUR)
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH + random.randint(0, 100)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)
        self.speed = 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

def main():
    pygame.init()
    pygame.display.set_caption("R-Type Style Shooter")
    screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
    clock = pygame.time.Clock()

    # Off-screen surface for low resolution rendering
    surface = pygame.Surface((WIDTH, HEIGHT))

    player = Player()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    all_sprites = pygame.sprite.Group(player)

    starfield = [[random.randrange(0, WIDTH), random.randrange(0, HEIGHT), random.choice(STAR_COLOURS)] for _ in range(50)]

    enemy_spawn = pygame.USEREVENT + 1
    pygame.time.set_timer(enemy_spawn, 1000)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == enemy_spawn:
                enemy = Enemy()
                enemies.add(enemy)
                all_sprites.add(enemy)
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bullet = player.shoot()
                bullets.add(bullet)
                all_sprites.add(bullet)

        keys = pygame.key.get_pressed()
        player.update(keys)
        bullets.update()
        enemies.update()

        # Collision detection
        pygame.sprite.groupcollide(bullets, enemies, True, True)

        # Scroll starfield
        for star in starfield:
            star[0] -= 1
            if star[0] < 0:
                star[0] = WIDTH
                star[1] = random.randrange(0, HEIGHT)

        # Draw everything on the low-res surface
        surface.fill(BLACK)
        for x, y, colour in starfield:
            surface.fill(colour, (x, y, 2, 2))
        all_sprites.draw(surface)

        # Scale up to give a chunky pixel look
        pygame.transform.scale(surface, (WIDTH * SCALE, HEIGHT * SCALE), screen)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
