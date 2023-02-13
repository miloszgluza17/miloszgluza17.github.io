import pygame
import os
import random

pygame.init()

#game Window
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1080

#create Game Window
GAME_WINDOW = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tower Jumper")

#music and sounds
pygame.mixer.music.load('assets/outerspace.mp3')
pygame.mixer.music.set_volume(0.25)
pygame.mixer.music.play(-1, 7)
landing_fx = pygame.mixer.Sound('assets/landing.mp3')
landing_fx.set_volume(0.25)
death_fx = pygame.mixer.Sound('assets/hit.mp3')
death_fx.set_volume(0.15)
game_over_fx = pygame.mixer.Sound('assets/gameover.mp3')
game_over_fx.set_volume(0.15)

#game variables
vec = pygame.math.Vector2
ACC = 1
FRIC = -0.15
GRAVITY = 1
MAX_PLATFORMS = 10
SCROLL_THRESH = 400
scroll = 0
bg_scroll = 0
game_over = False
score = 0


if os.path.exists('score.txt'):
	with open('score.txt', 'r') as file:
		high_score = int(file.read())
else:
	high_score = 0

#load images
bg_image = pygame.image.load('assets/seamless comos.png').convert_alpha()
bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
player_image = pygame.image.load('assets/astronaut.png').convert_alpha()
platform_image = pygame.image.load('assets/platform.png').convert_alpha()
asteroid_image = pygame.image.load('assets/asteroid.png').convert_alpha()

#set framerate
FPS = 60
FramePerSec = pygame.time.Clock()

#colors
WHITE = (255, 255, 255)

#font
font_small = pygame.font.SysFont('Lucida Sans', 20)
font_big = pygame.font.SysFont('Lucida Sans', 24)

#text onto screen
def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    GAME_WINDOW.blit(img, (x, y))

def draw_score():
    pygame.draw.line(GAME_WINDOW, WHITE, (0, 35), (SCREEN_WIDTH, 35), 2)
    draw_text('SCORE: ' + str(score), font_big, WHITE, 0, 0)

#drawing background
def draw_bg(bg_scroll):
    GAME_WINDOW.blit(bg_image, (0, 0 + bg_scroll))
    GAME_WINDOW.blit(bg_image, (0, -SCREEN_HEIGHT + 3 + bg_scroll))

#player class
class Player():
    def __init__(self, x, y):
        self.image = pygame.transform.scale(player_image, (70, 100))
        self.width = 50
        self.height = 93
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = (x, y)
        self.vel_y = 0
        self.flip = False

    def draw(self):
        GAME_WINDOW.blit(pygame.transform.flip(self.image, self.flip, False), (self.rect.x - 12, self.rect.y - 7))
        #pygame.draw.rect(GAME_WINDOW, WHITE, self.rect, 2)

    def move(self):
        #reset variables
        scroll = 0
        dx = 0
        dy = 0

        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[pygame.K_LEFT]:
            dx = -7
            self.flip = True
        if pressed_keys[pygame.K_RIGHT]:
            dx = 7
            self.flip = False

        if pressed_keys[pygame.K_a]:
            dx = -7
            self.flip = True
        if pressed_keys[pygame.K_d]:
            dx = 7
            self.flip = False

        # gravity
        self.vel_y += GRAVITY
        dy += self.vel_y

        #ensure player doesn't go off the screen
        if self.rect.left + dx < 0:
            dx = -self.rect.left
        if self.rect.right + dx > SCREEN_WIDTH:
            dx = SCREEN_WIDTH - self.rect.right

        #check collision with platforms
        for platform in platform_group:
            #collision in the y direction
            if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                #check if above the platform
                if self.rect.bottom < platform.rect.centery:
                    if self.vel_y > 0:
                        self.rect.bottom = platform.rect.top
                        dy = 0
                        self.vel_y = -25
                        landing_fx.play()

        #check collision with scroll threshold
        if self.rect.top <= SCROLL_THRESH:
            #check if player is jumping
            if self.vel_y < 0:
                scroll = -dy

        #update rectangle position
        self.rect.x += dx
        self.rect.y += dy + scroll

        #player mask
        self.mask = pygame.mask.from_surface(self.image)

        return scroll

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, moving):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(platform_image, (width, 18))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.moving = moving
        self.move_counter = random.randint(0, 50)
        self.move_direction = random.choice([-1, 1])

        self.speed = random.choice([1, 2])
        if score > 25000:
            self.speed = random.choice([7, 8])
            if score > 10000:
                self.speed = random.choice([5, 6])
                if score > 5000:
                    self.speed = random.choice([3, 4])

    def update(self, scroll):
        #moving platform
        if self.moving == True:
            self.move_counter += 1
            self.rect.x += self.move_direction * self.speed

        #change platform direction after some time or if it hits the wall
        if self.move_counter >= random.randint(70, 120) or self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
            self.move_direction *= -1
            self.move_counter = 0

        #update platforms vetical position
        self.rect.y += scroll

        #if platform has gone off the screen = delete
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



class Enemy(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, y):
        pygame.sprite.Sprite.__init__(self)
        # variables for moving
        self.direction = random.choice([-1, 1])
        self.speed = 3
        if score > 10000:
            self.speed = random.randint(4, 8)

        self.image = pygame.transform.scale(asteroid_image, (70, 70))
        self.rect = self.image.get_rect()
        self.flip = False

        # flip enemy off of the direction
        if self.direction == 1:
            self.flip = True
            self.image = pygame.transform.flip(self.image, self.flip, False)

        if self.direction == 1:
            self.rect.x = -70
        else:
            self.rect.x = SCREEN_WIDTH + 70
        self.rect.y = y

    def update(self):
        #move enemy
        self.rect.x += self.direction * self.speed

        #update enemy vetical position
        self.rect.y += scroll

        #check to see if enemy goes off the screen
        if self.rect.x - 150 > SCREEN_WIDTH:
            self.rect.x = -70
        if self.rect.left + 150 < 0:
            self.rect.x = SCREEN_WIDTH

        #kill enemy after going off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.kill()



#player instance
player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)

#create sprite groups
platform_group = pygame.sprite.Group()
enemy_group = pygame.sprite.Group()

#create starting platform
platform = Platform(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, False)
platform_group.add(platform)


run = True
while run:
    FramePerSec.tick(FPS)

    if game_over == False:
        scroll = player.move()

        #draw background
        bg_scroll += scroll
        if bg_scroll >= SCREEN_HEIGHT:
            bg_scroll = 0
        draw_bg(bg_scroll)

        # game score
        if scroll > 0:
            score += scroll

        # generate platforms
        if len(platform_group) < MAX_PLATFORMS:
            p_w = random.randint(60, 140)
            p_x = random.randint(100, SCREEN_WIDTH - p_w - 100)
            p_y = platform.rect.y - random.randint(250, 300)
            p_type = random.randint(1, 2)
            if p_type == 1 and score > 1250:
                p_moving = True
            else:
                p_moving = False

            platform = Platform(p_x, p_y, p_w, p_moving)
            platform_group.add(platform)

        #update platforms
        platform_group.update(scroll)

        #generate enemies
        if len(enemy_group) == 0 and score > 3000:
            enemy = Enemy(SCREEN_WIDTH, -300)
            enemy_group.add(enemy)

        #update enemies
        enemy_group.update()

        #draw score
        draw_score()

        #draw high score
        pygame.draw.line(GAME_WINDOW, WHITE, (0, score - high_score + SCROLL_THRESH),
                         (SCREEN_WIDTH, score - high_score + SCROLL_THRESH), 5)
        draw_text('HIGH SCORE', font_small, WHITE, 100, score - high_score + SCROLL_THRESH)

        #draw sprites
        platform_group.draw(GAME_WINDOW)
        enemy_group.draw(GAME_WINDOW)
        player.draw()

        #check if game over
        if player.rect.top > SCREEN_HEIGHT:
            game_over = True
            death_fx.play()
            pygame.time.wait(600)
            game_over_fx.play()
        #check collision with enemies
        if pygame.sprite.spritecollide(player, enemy_group, False):
            if pygame.sprite.spritecollide(player, enemy_group, False, pygame.sprite.collide_mask):
                game_over = True
                death_fx.play()
                pygame.time.wait(600)
                game_over_fx.play()
    else:
        #save highscore
        pygame.mixer.music.stop()
        if score > high_score:
            high_score = score
            with open('score.txt', 'w') as file:
                file.write(str(high_score))
        #gameover text
        draw_text('GAME OVER', font_big, WHITE, 245, 400)
        draw_text('SCORE: ' + str(score), font_big, WHITE, 243, 480)
        draw_text('HIGHSCORE: ' + str(high_score), font_big, WHITE, 215, 520)
        draw_text('PRESS SPACE TO RESTART', font_big, WHITE, 165, 600)
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            #reset variables
            game_over = False
            score = 0
            scroll = 0
            #reposition player
            player.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150)
            #reset sprite groups
            platform_group.empty()
            enemy_group.empty()
            #recreate starting platform
            platform = Platform(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 60, 200, False)
            platform_group.add(platform)
            #restart music
            pygame.mixer.music.play()

            gov_counter = 0

    #events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            if score > high_score:
                high_score = score
                with open('score.txt', 'w') as file:
                    file.write(str(high_score))
            pygame.quit()
            run = False
    pygame.display.update()