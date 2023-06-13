import pygame #duh
import random
#these are some generic constants from pygame to use
#these constants are specific eventnames that happen in gameplay
from pygame.locals import (
    RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN, #presses a key down
    QUIT, #presses the x button on pygame window
)

#inits pygame, must run
pygame.init()
clock = pygame.time.Clock()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#creating a player class which extends the pygame Sprite class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.image.load("jet2.jpg").convert()
        self.surf.set_colorkey((255,255,255), RLEACCEL)
        self.rect = self.surf.get_rect()

    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)

        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)

        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)

        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)
        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

#Example of a common enemy type: This goes along the screen and dies on the other side
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20,10))
        self.surf.fill((255, 255, 255))
        self.rect = self.surf.get_rect(
            center = (
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), 
                random.randint(0, SCREEN_HEIGHT)
            )
        )
        self.speed = random.randint(5, 20)
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            #kill: removes the sprite from all sprite groups its in
            self.kill()

#this screen object is where you draw everything on
screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

player = Player()

#creation of a sprite group:
#a sprite group is essentially a list of sprites
#we create a sprite group because it contains valuable methods
#technically we could just have a list though

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

#creation of events:
#every event needs to have an associated number with it
#to create a unique event, you need to take the last number, pygame.USEREVENT, and add 1
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)


running = True
while running:

    #handling game events first
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
           running = False
        
        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
    
    #pygame.key.get_pressed returns a dict of all keys currently that have been pushed
    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()

    screen.fill((0,0,0))

    #surfaces are a type of pygame object that lets you draw on it
    #the screen display is also just a specific instance of surface
    """
    surf = pygame.Surface((50,50))
    surf.fill((0,0,0))
    rect = surf.get_rect()
    """

    #blit: Block transfer
    #essentially a blit copies the contents of one surface onto another
    #ie. screen.bilt(surf) copies surf onto screen
    #note that you can only bilt surfaces, but the screen is a surface so all g
    #bilt syntax is: (surface to draw, (where on screen to draw it) )
    """
    center =(
    (SCREEN_WIDTH-surf.get_width())/2,
    (SCREEN_HEIGHT-surf.get_height())/2
    )
    """
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
    
    #flip: flips the display changes for eye to see
    pygame.display.flip()
    clock.tick(30)

pygame.quit()