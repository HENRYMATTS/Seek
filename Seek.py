##### Seek  #####
# author: @henrymatts
# Copyright : Nah


# packages
import pygame,sys
import random
from pygame.locals import*
import numpy as np


pygame.init()
# global variables
screen_width = 460
screen_height = 460
fps =30
speed = 0.2
angle = 0
# inital player position
player_x = 240
player_y = 240
trigger = True
fov = 30# field of view
half_fov = np.radians(fov/2)

rays = 24 # No of rays to cast
max_depth = 460
TILE_SIZE = 20

#object initial pos
obj_x = 85
obj_y = 70




screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game:  Seek')
Clock = pygame.time.Clock()
font = pygame.font.Font('freesansbold.ttf', 14)



#map (walls are drawn according to the map 1 is a wall 0 is space)
env = np.array([
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1],
                 [1,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1],
                 [1,0,0,1,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,0,0,0,0,0,0,0,1,0,0,0,0,1,0,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,1,1,1],
                 [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,0,0,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,1,0,0,1],
                 [1,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0,0,0,1,0,0,0,1],
                 [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
               ])


    

#function to draw the environment/walls

def walls(env):
    for x in range(len(env)):
        for y in range(len(env)):
            if env[x,y]==1:
                rect = pygame.Rect(y*20,x*20,20,20)    
                pygame.draw.rect(screen,('brown'),rect)
                if (x,y)==(rand_x,rand_y):
                    pygame.draw.rect(screen,('blue'),rect)        
            else:
               continue



# player and player movement section
def player(player_x,player_y,angle):
    # 1 set the player direction
    stop_x = player_x + np.cos(angle)*10
    stop_y = player_y - np.sin(angle)*10
    pygame.draw.line(screen,'green',(player_x,player_y),(stop_x,stop_y))


     #the following two lines make a field of view of 30 degrees
    pygame.draw.line(screen,'green',(player_x,player_y),(
        player_x + np.cos(angle- half_fov)*10,
        player_y - np.sin(angle- half_fov)*10
    ))

    pygame.draw.line(screen,'green',(player_x,player_y),(
        player_x + np.cos(angle+ half_fov)*10,
        player_y - np.sin(angle+ half_fov)*10
    ))

    # draw the player
    pygame.draw.circle(screen,'red',(player_x,player_y),10)


   
   

# ray casting and vision cone
#distances = []   # to store distances of the ray
def ray():
   
    trigger = False
    step_angle = (angle - half_fov)
    for ray in range(rays):
        for depth in range(max_depth):
            target_x = player_x + np.cos(step_angle) * depth
            target_y = player_y - np.sin(step_angle) * depth
            col = int(target_x / TILE_SIZE)
            row = int(target_y / TILE_SIZE)

            if env[row, col] == 1:
                pygame.draw.rect(screen, (0, 255, 0), (col * TILE_SIZE, row * TILE_SIZE, TILE_SIZE , TILE_SIZE))
                pygame.draw.line(screen, (255, 255, 0), (player_x, player_y), (target_x, target_y),2)
                # Calculate distance and add to the list
                # distance = np.sqrt((player_x - target_x) ** 2 + (player_y - target_y) ** 2)
                # distances.append(distance)
                
                if (row,col)==(rand_x,rand_y):
                    env[rand_x,rand_y] = 0
                    trigger = True  
                break

        step_angle += np.radians(2)
  

    return trigger 



score = 0
run = True 
trigger = True
forward = True
while True:
    for event in pygame.event.get():
        if event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
            pygame.quit()
            sys.exit()

      
    # left & right are used to do rotation in any direction        
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        angle += speed
    if keys[pygame.K_RIGHT]:
        angle -= speed

    # Up and Down cause movement in the chosen direction
    if keys[pygame.K_UP]:
        forward = True
        player_x += np.cos(angle)*5
        player_y -= np.sin(angle)*5
    if keys[pygame.K_DOWN]:
        forward = False
        player_x -= np.cos(angle)*5
        player_y += np.sin(angle)*5

      # when the player hits the wall he does not go through collision detection
    col = int(player_x / TILE_SIZE)
    row = int(player_y / TILE_SIZE)
    if env[row,col] == 1:
        if forward :
             player_x -= np.cos(angle)*5
             player_y -= -np.sin(angle)*5
        else:
             player_x += np.cos(angle)*5
             player_y += -np.sin(angle)*5
    if trigger:
        while run:
            rand_x=random.randint(0,len(env)-1)
            rand_y=random.randint(0,len(env)-1)
            if env[rand_x,rand_y] == 0:
                env[rand_x,rand_y] = 1
                trigger = False
                break
        score += 1
        text = font.render(f"Score:{score}",True,'white')
        recta = text.get_rect(center=(50,30))
     
        
        
        
    # clearing the screen    
    screen.fill('black')
    
    # function calls
    screen.blit(text,recta) 
    walls(env)# call to draw the environment according to the map
    player(player_x,player_y,angle) # call to draw the player in the environment
    trigger  = ray()  # call to cast rays 
    pygame.display.flip()
    Clock.tick(fps)