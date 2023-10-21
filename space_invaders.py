import pygame
import random
import time
import math
from decimal import *

pygame.init()
getcontext().prec = 3


f_counter = 0
speed_P = 5
speed_E = 3

#Display
largura = 800
altura = 600
screen = pygame.display.set_mode((largura,altura))

pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('assets/logo.png')
pygame.display.set_icon(icon)

BG = pygame.image.load('assets/background.png')

#Score

score_value = 0
font = pygame.font.SysFont("comicsansms", 16)
textX = 10
textY = 10


#Player
playerImg = pygame.image.load('assets/player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerY_change = 0

#Enemy
enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []

num_enemies = 6

for i in range(num_enemies):
    enemyImg.append(pygame.image.load('assets/enemy.png'))
    enemyX.append(random.randint(32,750))
    enemyY.append(32)
    enemyX_change.append(3)
    enemyY_change.append(20)

#Bullet
bulletImg = pygame.image.load('assets/bullet.png')
bulletX = playerX
bulletY = playerY
bulletX_change = 0
bulletY_change = 10
bullet_state = "Ready"

def show_score(x,y,score_value):
    score = font.render("Score:"+str(score_value),True,(255,255,255))
    screen.blit(score,(x,y))

def show_FPS(x,y,FPS):
    fps = font.render(str(FPS)+" FPS",True,(255,255,255))
    screen.blit(fps,(x,y))

def player(x,y):
    screen.blit(playerImg,(x,y))

def enemy(x,y,i):
    screen.blit(enemyImg[i],(x,y))

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "Fire"
    screen.blit(bulletImg,(x+16,y+16))

def isCollision(enemyX,enemyY,bulletX,bulletY):
    distance = math.sqrt( math.pow((enemyX-bulletX),2)+ math.pow((enemyY-bulletY),2) )
    if distance < 27:
        return True
    else:
        return False

running = True

while running:
    start = time.time()
    screen.blit(BG,(0,0))
    f_counter +=1
    
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            
            if event.key == pygame.K_LEFT:
                playerX_change = -speed_P
                
            if event.key == pygame.K_RIGHT:
                playerX_change = speed_P
                
            if event.key == pygame.K_UP:
                playerY_change = -speed_P
                
            if event.key == pygame.K_DOWN:
                playerY_change = speed_P

            if event.key == pygame.K_SPACE and bullet_state =="Ready":
                bulletX = playerX
                bulletY = playerY
                fire_bullet(bulletX,bulletY)
                
        if event.type == pygame.KEYUP:
            
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                
                playerX_change = 0
                
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN :
                
                playerY_change = 0
            
        if event.type == pygame.QUIT:
            running = False
        
    
# Player movement  
    playerX += playerX_change
    playerY += playerY_change
    
    if playerX <=0:
        playerX = 0
    elif playerX >= largura - 32:
        playerX = largura-32
        
    if playerY <=0:
        playerY = 0
    elif playerY >= altura - 32:
        playerY = altura-32
        
# Enemy movement
    for i in range(num_enemies):
        enemyX[i] += enemyX_change[i]

        if enemyX[i] <=0:
            enemyX_change[i] = speed_E
            enemyY[i] += enemyY_change[i]
        
        elif enemyX[i] >= largura - 32:
            enemyX_change[i] = -speed_E
            enemyY[i] += enemyY_change[i]
            
        collision = isCollision(enemyX[i],enemyY[i],bulletX,bulletY)

        if collision is True:
            bulletY = playerY
            bullet_state = "Ready"
            score_value += 1
            enemyX[i] = random.randint(32,750)
            enemyY[i] = 32
            
        enemy(enemyX[i],enemyY[i],i)
        
#Bullet movement
    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "Ready"
        
    if bullet_state is "Fire":
        fire_bullet(bulletX,bulletY)
        bulletY -= bulletY_change
        
    player(playerX,playerY)
    
    
    
    end = time.time()
    if (end-start)<0.014:
        time.sleep(0.015 - (end-start) )
    end = time.time()
    total_time = end-start
    FPS = Decimal(1)/Decimal(total_time)
    
    
    show_score(textX,textY,score_value)
    show_FPS(textX,textY+32,FPS)
    
    pygame.display.update()


pygame.display.quit()
pygame.quit()
