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
SCREEN_WIDTH = 800 # width of the screen
SCREEN_HEIGHT = 600 #height of the screen
PLAYER_HEIGHT = 60 #gorilla height
PLAYER_WIDTH = 100
BANANA_HEIGHT = 20 
BANANA_WIDTH = 16
BASKET_HEIGHT = 40
BASKET_WIDTH = 80

#buildings are all based on the same image - but are differently scaled

BUILDING_1_WIDTH = 100
BUILDING_1_HEIGHT = 200
BUILDING_2_WIDTH = 100
BUILDING_2_HEIGHT = 300
BUILDING_3_WIDTH = 150
BUILDING_3_HEIGHT = 400

#initial values for speed and angle
speed = 45
angle = 45


#every time we get a new level we increase this value
level = 1

#a list of the levels a user can play - each level being represented as a tuple

levels = [[(1, 0), (2, 100), (3,-100)], [(2, 0), (1, 100), (3,-50)]]

#first value in the tuple is the type of building (1, 2, 3) and the second value is the offset from the center
#changing the values will give us a different level configuration
#we only use the first level for now


# Define the Player object 
# This is basically the monkey that is loaded from the png image
# In essence this is just a sprite

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

        #has_thrown indicates if the monkey has thrown the bananna or not
        # a monkey can only throw one bananna at a time

        self.has_thrown = False
    
    #this is the update function called everytime we update the sprite

    def update(self, key_pressed):
        if key_pressed[K_SPACE]:
            if self.has_thrown is False:
                self.surf = pygame.image.load("./images/gorilla_release.png").convert()
                self.surf = pygame.transform.scale(self.surf, ((PLAYER_HEIGHT, PLAYER_WIDTH)))
                new_banana = Banana()
                all_sprites.add(new_banana)
                bananas.add(new_banana)
                self.has_thrown = True

# The sprite class for bananas 

class Banana(pygame.sprite.Sprite):
    def __init__(self):
        super(Banana, self).__init__()
        self.speed = speed
        self.time = 0 # the initial time
        self.acc = 0.98 # vertical (gravitation acceleration)
        self.res = 0.000001 # horiyontal acceleration (air resistance)
        self.angle = angle
        angled_rad = self.angle / 180 * math.pi

        #initial speed values

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

        #here we just compute the equations of motions for the bananna 
        #since we throw from left to right - x increases
        #since we throw from down to ap the y will decrease when we throw

        if self.v_x > 0: 
            self.v_x = self.v_x - (self.res * self.time * self.time) 
        if self.v_x < 0: 
            self.v_x = 0
        self.v_y = self.v_y - self.acc * self.time * self.time
        self.time = self.time + 0.07 #the time integrator we use is 0.07, a smaller value would give us more resolution
        self.rect.move_ip((self.v_x, -self.v_y))

        #add logic to kill banana when leaving play area
        if self.rect.centerx > SCREEN_WIDTH * 3: 
            self.kill()
            player.has_thrown = False
        if self.rect.centery > SCREEN_HEIGHT * 3: 
            print(self.rect.centery)
            self.kill()
            player.has_thrown = False

#banana basket class/sprite - the actual target

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



class Building(pygame.sprite.Sprite):
    def __init__(self, type_of_building, building_offset):
        super(Building, self).__init__()
        self.surf = pygame.image.load("./images/building_1.png").convert()
        
        #in the contructor of the class we specify the type of building
        #based on the type we do different scaling as below
        
        if type_of_building == 1:
            self.surf = pygame.transform.scale(self.surf, ((BUILDING_1_WIDTH, BUILDING_1_HEIGHT)))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    SCREEN_WIDTH / 2 - building_offset,
                    SCREEN_HEIGHT - 20
                )
            )

        if type_of_building == 2:
            self.surf = pygame.transform.scale(self.surf, ((BUILDING_2_WIDTH, BUILDING_2_HEIGHT)))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    SCREEN_WIDTH / 2 + BUILDING_2_WIDTH,
                    SCREEN_HEIGHT - BASKET_HEIGHT
                )
            )

        if type_of_building == 3:
            self.surf = pygame.transform.scale(self.surf, ((BUILDING_3_WIDTH, BUILDING_3_HEIGHT)))
            self.surf.set_colorkey((255, 255, 255), RLEACCEL)
            self.rect = self.surf.get_rect(
                center=(
                    SCREEN_WIDTH / 2 - BUILDING_3_WIDTH,
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

#will contain bananas 
bananas = pygame.sprite.Group()

#will contain buildings
buildings = pygame.sprite.Group()

# we use groups for bananas and builings so its easier later on to calculate colissions

all_sprites = pygame.sprite.Group()
all_sprites.add(player)
all_sprites.add(basket)

#based on the levels list we create the buildings

for b in levels[0]:
    new_building = Building(b[0], b[1])
    all_sprites.add(new_building)
    buildings.add(new_building)

font = pygame.font.Font('./Fonts/font.ttf', 32)

font_message = pygame.font.Font('./Fonts/font.ttf', 64)

img_success = font.render("You hit the basket", True, (255, 255, 255))
rect_success = img_success.get_rect()
pygame.draw.rect(img_success, blue, rect_success, 1, 9)


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

    collide_basket = pygame.sprite.spritecollide(basket, bananas, True)

    collide_buildings = pygame.sprite.groupcollide(buildings, bananas, False, True)

    for s in collide_basket:
        print("Hit the basket")
        player.has_thrown = False
        img_success = font.render("You hit the basket", True, (255, 255, 0))
        rect_success = img_success.get_rect()
        pygame.draw.rect(img_success, blue, rect_success, 1, 9)

    for s in collide_buildings: 
        print(s)
        player.has_thrown = False

    # Get all the keys currently pressed
    pressed_keys = pygame.key.get_pressed()

    # Update the player sprite based on user keypresses
    player.update(pressed_keys)

    # Fill the screen with white
    screen.fill((255, 255, 255))
    
    screen.blit(img_speed, (20, 20))
    screen.blit(img_angle, (20, 60))
    screen.blit(img_success, (SCREEN_WIDTH-270, 30))

    # Draw all sprites
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    bananas.update()

    # Update the display
    pygame.display.flip()


    #we do around 30 frames / second - this correlated with the time integrator gives us the speed the user sees on the screen
    clock.tick(30)