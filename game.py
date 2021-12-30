# Import the pygame module
import pygame
import time
import math
from pygame.constants import K_SPACE

# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
# from pygame.locals import *
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

# Define base color tuples
white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_HEIGHT = 60
PLAYER_WIDTH = 100
BANANA_HEIGHT = 20
BANANA_WIDTH = 16
BASKET_HEIGHT = 40
BASKET_WIDTH = 80

# Define constants for the screen width and height
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

speed = 45
angle = 45


# Define the Player object by extending pygame.sprite.Sprite
# Instead of a surface, use an image for a better-looking sprite
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("./images/gorilla_wait.png").convert()
        self.surf = pygame.transform.scale(self.surf, ((PLAYER_HEIGHT, PLAYER_WIDTH)))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect()
        self.rect = self.surf.get_rect(
            center=(
                10 + PLAYER_WIDTH / 2,
                SCREEN_HEIGHT - PLAYER_HEIGHT
            )
        )
        self.has_thrown = False
    
    def update(self, key_pressed):
        if key_pressed[K_SPACE]:
            if self.has_thrown is False:
                self.surf = pygame.image.load("./images/gorilla_release.png").convert()
                self.surf = pygame.transform.scale(self.surf, ((PLAYER_HEIGHT, PLAYER_WIDTH)))
                new_banana = Banana()
                all_sprites.add(new_banana)
                bananas.add(new_banana)
                self.has_thrown = True


class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super(Banana, self).__init__()
        self.speed = speed
        self.time = 0
        self.acc = 0.98
        self.res = 0.000001
        self.angle = angle
        angled_rad = self.angle / 180 * math.pi
        self.v_y = self.speed * math.sin(angled_rad)
        self.v_x = self.speed * math.cos(angled_rad)
        self.surf = pygame.image.load("./images/bananna.png").convert()
        self.surf = pygame.transform.scale(self.surf, ((BANANA_HEIGHT, BANANA_WIDTH)))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                PLAYER_WIDTH / 2,
                SCREEN_HEIGHT - PLAYER_HEIGHT  - 40
            )
        )

    def update(self):
        if self.v_x > 0: 
            self.v_x = self.v_x - (self.res * self.time * self.time) 
        if self.v_x < 0: 
            self.v_x = 0
        self.v_y = self.v_y - self.acc * self.time * self.time
        self.time = self.time + 0.1
        self.rect.move_ip((self.v_x, -self.v_y))
        #add logic to kill banana when leaving play area
        if self.rect.centerx > SCREEN_WIDTH * 3: 
            self.kill()
            player.has_thrown = False
        if self.rect.centery > SCREEN_HEIGHT * 3: 
            print(self.rect.centery)
            self.kill()
            player.has_thrown = False


class BananaBasket(pygame.sprite.Sprite):
    def __init__(self):
        super(BananaBasket, self).__init__()
        self.surf = pygame.image.load("./images/banana_basket.png").convert()
        self.surf = pygame.transform.scale(self.surf, ((BASKET_WIDTH, BASKET_HEIGHT)))
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                SCREEN_WIDTH - BASKET_WIDTH,
                SCREEN_HEIGHT - BASKET_HEIGHT
            )
        )

# Initialize pygame
pygame.init()



# Create the screen object
# The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

player = Player()
basket = BananaBasket()
bananas = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(basket)

font = pygame.font.Font('./Fonts/font.ttf', 32)

img_speed = font.render("Speed 100", True, green)
rect_speed = img_speed.get_rect()
pygame.draw.rect(img_speed, blue, rect_speed, 1)

img_angle = font.render("Angle 45", True, green)
rect_angle = img_angle.get_rect()
pygame.draw.rect(img_angle, blue, rect_angle, 1)

screen.fill((0, 0, 0))# Fill the screen with white

pygame.display.flip()

# Variable to keep the main loop running
running = True

clock = pygame.time.Clock()

# Main loop
while running:# Fill the screen with white

    # Look at every event in the queue
    for event in pygame.event.get():
        # Did the user hit a key?
        if event.type == KEYDOWN:
            # Was it the Escape key? If so, stop the loop.
            if event.key == K_ESCAPE:
                running = False
            if event.key == K_UP:
                img_speed = font.render("Speed " + str(speed + 1), True, green)
                rect_speed = img_speed.get_rect()
                pygame.draw.rect(img_speed, blue, rect_speed, 1)
                speed = speed + 1
            if event.key == K_RIGHT:
                img_angle = font.render("Angle " + str(angle + 1), True, green)
                angle = angle + 1
                rect_angle = img_angle.get_rect()
                pygame.draw.rect(img_angle, blue, rect_angle, 1)
            if event.key == K_DOWN:
                img_speed = font.render("Speed " + str(speed - 1), True, green)
                rect_speed = img_speed.get_rect()
                pygame.draw.rect(img_speed, blue, rect_speed, 1)
                speed = speed - 1
            if event.key == K_LEFT:
                img_angle = font.render("Angle " + str(angle + 1), True, green)
                angle = angle - 1
                rect_angle = img_angle.get_rect()
                pygame.draw.rect(img_angle, blue, rect_angle, 1)

        # Did the user click the window close button? If so, stop the loop.
        elif event.type == QUIT:
            running = False

    collide = pygame.sprite.spritecollide(basket, bananas, True)

    for s in collide:
        print(s)

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with black
    screen.fill((255, 255, 255))
    
    screen.blit(img_speed, (20, 20))
    screen.blit(img_angle, (20, 60))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    bananas.update()

    # Update the display
    pygame.display.flip()

    clock.tick(30)