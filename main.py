import pygame
import os
pygame.font.init() # This will initialise pygame font library
pygame.mixer.init() # Sound effect library

# Dimension of the window
WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("First Game")  # Name of the window

WHITE = (255, 255, 255)  # Background color white is set inside the variable 'WHITE'
BLACK = (0, 0, 0) # Color of the border in the middle
RED = (255, 0, 0) # Color of the red spaceship bullets
YELLOW = (255, 255, 0) # Color of the yellow spaceship bullets

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('comicsans',40)
WINNER_FONT = pygame.font.SysFont('comicsans',100)

FPS = 60
VEL = 5 # Velocity
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 # user event 
RED_HIT = pygame.USEREVENT + 2 # user event. (+2) is used not (+1) to make difference between this two event 

YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))  # Yellow spaceship is loaded
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)  # Yellow spaceship is resized to (55, 40) and rotated 90 degree

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))  # Red spaceship is loaded
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)  # Red spaceship is resized to (55, 40) and rotated 275 degree

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH,HEIGHT))  # Space pic (background) is loaded

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0,0)) # Here the background (Space) is drawn from the position (0,0)
    pygame.draw.rect(WIN, BLACK, BORDER)  # Border is drawn in the middle
    
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("Health: " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # Here the yellow spaceship is placed at position (yellow.x, yellow.y)
    WIN.blit(RED_SPACESHIP, (red.x, red.y))  # Here the red spaceship is placed at position (red.x, red.y)


    for bullet in red_bullets: # Red spaceship bullet is draw on the window
            pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets: # Yellow spaceship bullet is draw on the window
            pygame.draw.rect(WIN, YELLOW, bullet)
    
    pygame.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0: # Left
            yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x : # Right
            yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0: # Up
            yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 10: # Down
            yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width: # Left
            red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH: # Right
            red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0: # Up
            red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 10: # Down
            red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red):
        for bullet in yellow_bullets:
                bullet.x += BULLET_VEL
                if red.colliderect(bullet): # it checks if the yellow bullet hits the red character
                        pygame.event.post(pygame.event.Event(RED_HIT))
                        yellow_bullets.remove(bullet) # if it hits the bullet disappears
                elif bullet.x > WIDTH: # the bullet disappears if the bullet goes out of the window 
                        yellow_bullets.remove(bullet)

        
        for bullet in red_bullets:
                bullet.x -= BULLET_VEL
                if yellow.colliderect(bullet): # it checks if the red bullet hits the yellow character
                        pygame.event.post(pygame.event.Event(YELLOW_HIT))
                        red_bullets.remove(bullet) # if it hits the bullet disappears
                elif bullet.x < 0: # the bullet disappears if the bullet goes out of the window
                        red_bullets.remove(bullet) 

def draw_winner(text):
        draw_text = WINNER_FONT.render(text, 1, WHITE)
        WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()/2, HEIGHT/2 - draw_text.get_height()/2)) # Winning text pop up position
        pygame.display.update()
        pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # (x,y,width, height)
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)  # (x,y,width, height)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN: # when the ctrl key gets pressed one time, spaceship shoots
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2 - 2, 10, 5) # size of the red bullet
                        yellow_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()
               
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                        bullet = pygame.Rect(red.x, red.y + red.height//2 - 2, 10, 5) # size of the red bullet                        
                        red_bullets.append(bullet)
                        BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT: # When the red spaceship gets hit, its health decrease by one
                        red_health -= 1
                        BULLET_HIT_SOUND.play()

            if event.type == YELLOW_HIT:  # When the yellow spaceship gets hit, its health decrease by one
                        yellow_health -= 1
                        BULLET_HIT_SOUND.play()

        winner_text = ""
        if red_health <= 0:
                winner_text = "YELLOW WINS!"

        if yellow_health <= 0:
                winner_text = "RED WINS!"
        
        if winner_text != "":
                draw_winner(winner_text)
                break

        keys_pressed = pygame.key.get_pressed()  # This line will tell us which keys are currently pressed and store it in the variable 'keys_pressed'
        
        yellow_handle_movement(keys_pressed, yellow)  # Yellow spaceship movement function
        
        red_handle_movement(keys_pressed, red)  # Red spaceship movement function
        
        handle_bullets(yellow_bullets, red_bullets, yellow, red)  #  this function will handle if the bullets hits the opponent
        
        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health) # In this function spaceships and border in the middle is drawn
        

    #pygame.quit()
    main() # This will take us back to the main function so we have to write (pygame.quit()) at line 126 otherwise we cannot quit the game


if __name__ == "__main__":
    main()