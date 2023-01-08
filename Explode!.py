"""
Shield (controlled by arrows)
3 lives (loses one when a bomb hits the ground)
Everytime the player "shields" the bomb, they gain 10 points, a new bomb falls as well
When the bomb hits the ground it explodes
"""

import pygame, time, random
from pygame import mixer

pygame.init()

# set screen size
screen = pygame.display.set_mode([640, 640])

clock = pygame.time.Clock()

# image
bomb = pygame.image.load('bomb.png')
bckImg = pygame.image.load('backgroundImage.png')

# sound
explosion = pygame.mixer.Sound('Explosion+1.wav')
collide = pygame.mixer.Sound('collide.wav')
mixer.music.load("background.wav")
mixer.music.play(-1)

#*****************************************************

#define variable

FPS = 80 # Frames per second
shieldY = 510
cY = -50
cYMove = 2
num = random.randint(20, 600)
num2 = random.randint(10, 540)
shieldXSpeed = 15
shieldX = num2
scoreBest = 0
score = 0
lives = 3
introduction = 1

# define colours
white = (255, 255, 255)
red = (255, 50, 10)
yellow = (255, 255, 0)
blue = (0, 150, 225)
black = (0, 0, 0)
green = (127, 255, 0)


#*****************************************************

#create text
def displayText(text, color, x, y):

    #display text to screen
    #set the front type and size
    font = pygame.font.Font(None, 30)

    #convert text to an image
    textImage = font.render(text, True, color)
    screen.blit(textImage, (x, y))
   
#*****************************************************

def collision(rect1, rect2, cY, cX, shieldX, shieldY):
    if rect2.colliderect(rect1):
        return True
   
    else:
        cY += cYMove

#*****************************************************

def bombFall(cY, cX, shieldX, shieldY):
    if cY + 10 > shieldY +10:
        return True
    else:
        return False  
    
#****************************************************

def bigText(text, color, x, y):
    #display text to screen
    #set the front type and size
    font = pygame.font.Font(None, 50)

    #convert text to an image
    loseImage = font.render(text, True, color)
    screen.blit(loseImage, (x, y))  
    
#****************************************************

# main game loop
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
           
    # define location of bomb to make the bomb(s) move
    cX = num
    cY = cY + cYMove    
   
           
    #set up location of shield
    # Have shield move with the keys
   
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        shieldX += shieldXSpeed
    if keys[pygame.K_LEFT]:
        shieldX -= shieldXSpeed
       
    # make sure the shield does not go out of the screen
    # right edge lock
    if shieldX <= 0:
        shieldX = 0
       
    # left edge lock
    if shieldX + 100 >= 640:
        shieldX = 640 - 100
    
   
    # set up shapes
    rect1 = pygame.Rect([shieldX, shieldY, 100, 10])
    #rect2 = pygame.draw.circle(screen, yellow, (cX, cY), 10)
    rect2 = screen.blit(bomb, (cX, cY))
    
    
    # if collision happens
    # add points
    # drop bomb from sky
    # add sound
    # make the bomb fall faster (but not too fast, stop at certain speed)
    if collision(rect1, rect2, cY, cX, shieldX, shieldY):
        collide.play()
        num = random.randint(20, 600)
        if cYMove > 12:
            cYMove = 12
        else:
            cYMove += 1
        cY = -10
        score += 10
    
    # if the bomb falls to the ground
    # play sound
    # take away a life
    # have a new bomb fall
    # make the bomb fall faster (but not too fast, stop at certain speed)
    if bombFall(cY, cX, shieldX, shieldY):
        num = random.randint(20, 600)
        if cYMove > 12:
            cYMove = 12
        else:
            cYMove += 1
        cY = -10
        lives -= 1
        explosion.play()
       

    # Game draw    
    # Intro
    if introduction == 1:
        screen.fill(blue)
        #add backgorund image
        screen.blit(bckImg, (0, 0))
        cY = 0
        pygame.draw.rect(screen, green, (135, 230, 400, 170))
        bigText("Welcome to the", black, 230, 240)
        bigText("Bomb Shell Game!", black, 170, 290)
        
        displayText("Press anywhere on the screen to start", white, 150, 340)
        displayText("Press the 'exit' button to quit", white, 180, 370)
        
        # play game if the player clicked the screen
        click = pygame.mouse.get_pressed()
        if click[0] == 1:
            introduction = 2
            cY = 3
            
        pygame.display.flip() # displays all drawing on the screen
        
       
    else:
        screen.fill(blue)
        #add backgorund image
        screen.blit(bckImg, (0, 0))        
        displayText(f"Score: {score}", white, 10, 30)
        displayText(f"Lives: {lives}", white, 10, 50)    
       
        rect1 = pygame.draw.rect(screen, red, (shieldX, shieldY, 100, 10))
        #rect2 = pygame.draw.circle(screen, yellow, (cX, cY), 10)
        rect2 = screen.blit(bomb, (cX, cY))
        
        # exits game when player runs out of lives
        # must be placed here so words will show
        if lives < 1:
            cYMove = 0
            pygame.draw.rect(screen, red, (90, 230, 450, 190))
            bigText("You Lose!", black, 220, 240)
            displayText(f"Score: {score}", white, 250, 290)
            if score > scoreBest:
                scoreBest = score        
            displayText(f"Best Score: {scoreBest}", white, 230, 320)
            displayText("Press anywhere on the screen to play again", white, 100, 350)
            displayText("Press the 'exit' button to quit", white, 160, 380)
            
            # play game if player clicks the screen
            click = pygame.mouse.get_pressed()
            if click[0] == 1:
                score = 0
                lives = 3
                FPS = 80
                cYMove = 3
            
       
        else:
            done = False    
       
       
       
       
        pygame.display.flip() # displays all drawing on the screen
       
        clock.tick(FPS)



pygame.quit()  # allows pygame to quit   