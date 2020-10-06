#Import libraries
import pygame, os, sys
from pygame.locals import *
from time import sleep
from math import sin, cos, atan, atan2, radians, degrees, pi, sqrt
from random import randint

pygame.init() #Start pygame
pygame.mixer.init() #Start pygame mixer

#Functions
def parabolic_shot(arrow, arrow_copy, velocity, arrow_rect, angle, GRAVITY):
    angle_atan = -atan(velocity[1]/velocity[0])
    center_original = arrow_rect.center
    if angle <= 90 or angle > 270:
        arrow = pygame.transform.rotate(arrow_copy, degrees(angle_atan))
    else:
        arrow = pygame.transform.rotate(arrow_copy, degrees(angle_atan)+180)
    arrow_rect = arrow.get_rect()
    arrow_rect.center = center_original   
    velocity[1] += GRAVITY 
    arrow_rect.center = [arrow_rect.center[0] + velocity[0], arrow_rect.center[1] + velocity[1]]
    return arrow, arrow_rect

def initialization_variables_parabolic_shot(velocity, angle):
    velocity_arrow_x = cos(radians(angle)) * velocity
    velocity_arrow_y = sin(radians(angle)) * velocity
    velocity_x = +velocity_arrow_x
    velocity_y = -velocity_arrow_y   
    velocity = [velocity_x, velocity_y]
    return velocity

def calculate_angle(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    angle = abs(degrees(atan2(y,x))- 180)
    return angle

def calculate_distance(point_1, point_2):
    x = point_2[0] - point_1[0]
    y = point_2[1] - point_1[1]
    distance = sqrt(x**2+y**2)
    return distance

def rotate_image(screen, image, pos, originPos, angle):
    w, h = image.get_size()
    box = [pygame.math.Vector2(p) for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
    box_rotate = [p.rotate(angle) for p in box]
    min_box = (min(box_rotate, key=lambda p: p[0])[0], min(box_rotate, key=lambda p: p[1])[1])
    max_box = (max(box_rotate, key=lambda p: p[0])[0], max(box_rotate, key=lambda p: p[1])[1])
    pivot = pygame.math.Vector2(originPos[0], -originPos[1])
    pivot_rotate = pivot.rotate(angle)
    pivot_move = pivot_rotate - pivot
    origin = (pos[0] - originPos[0] + min_box[0] - pivot_move[0], pos[1] - originPos[1] - max_box[1] + pivot_move[1])
    rotated_image = pygame.transform.rotate(image, angle)
    screen.blit(rotated_image, origin)

def choose_operation():
    option = randint(1,3)
    n1 = randint(1,99)
    n2 = randint(1,99)
    operator = ''
    a = 0
    if option == 1:
        a = n1 + n2
        operator = '+'
    elif option == 2:
        a = n1 - n2
        operator = '-'
    elif option == 3:
        n1 = randint(1,10)
        n2 = randint(1,20)
        a = n1 * n2
        operator = 'x'
    return n1,n2,operator,a

def collision_rect(arrow_rect, block_rect):
    ar = pygame.Rect(arrow_rect.center[0] + 5,arrow_rect.center[1]+10, 120,9)
    collision = False
    z = None
    for y in range(12):
        if ar.colliderect(block_rect[y]):
            print("\nBloque "+str(y+1)+": ")
            collision = True
            z = y
            return collision, z
    return collision, z
    
def save_time(minutes, seconds):
    time = [str(minutes), str(seconds)]
    outFile = open('dataTime.txt', 'w')
    for d in time:
        outFile.write(d+"\n")
    outFile.close()
    
def load_time():
    inFile = open('dataTime.txt', 'r')
    loaded_time = []
    for line in inFile:
        loaded_time.append(int(line.strip()))
    inFile.close()
    return loaded_time
                
#Constants
SCREEN_SIZE = 800, 600
GRAVITY = 0.2
FPS = 60

screen = pygame.display.set_mode((SCREEN_SIZE))
pygame.display.set_caption("Math Arrow")
background = pygame.image.load("Sprites/background.jpg").convert()
arrow = pygame.sprite.Sprite()
arrow = pygame.image.load("Sprites/arrow.png").convert_alpha()
block = pygame.sprite.Sprite()
block = pygame.image.load("Sprites/block.png").convert_alpha()
block = pygame.transform.scale(block, (50, 50))
arrow_sound = pygame.mixer.Sound("Sounds/arrow_shot.wav")
correct_sound = pygame.mixer.Sound("Sounds/correct.wav")
incorrect_sound = pygame.mixer.Sound("Sounds/incorrect.wav")

#Lists
start_point = []
end_point = []
velocity = []
block_rect = []
index_block = []
loaded_time = []
aux_position_block = [(520,15), (520,115), (520,215), (520,315), (520,415), (520,515), (670,15), (670,115), (670,215), (670,315), (670,415), (670,515)]
position_block = [(520,15), (520,115), (520,215), (520,315), (520,415), (520,515), (670,15), (670,115), (670,215), (670,315), (670,415), (670,515)]
block = [block] * 12

#Variables
position_initial_arrow =(45,285)
velocity_arrow = 0
arrow_copy = arrow.copy()
arrow_rect = arrow.get_rect()  
arrow_rect.center = position_initial_arrow 
angle = 0
w, h = arrow.get_size()
draw_line = False
shoot = False
initialization = True
arrow_visible = True
rotate_arrow = True
operation = True
collision = False
frames = 0
minutes = 0
seconds = 0
    
clock = pygame.time.Clock()

for j in range(12):
    br = pygame.Rect((position_block[j]), (50,50))
    block_rect.append(br)

while True:
    clock.tick(FPS)
    
    frames += 1
    if frames == 60:
        frames = 0
        seconds += 1
    
    if seconds == 60:
        seconds = 0
        minutes += 1
    
    screen.blit(background, (0,0))

    for i in range(12):
        screen.blit(block[i], position_block[i])
        block_rect[i] = pygame.Rect((position_block[i]), (50, 50))
        
    if arrow_rect.right >= 500:
        collision, z = collision_rect(arrow_rect, block_rect)
        if collision:
            arrow = arrow_copy
            shoot = False
            initialization = True
            rotate_arrow = True
            n1,n2,operator,a = choose_operation()
            answer = int(input(str(n1)+" "+operator+" "+str(n2)+" = "))
            if answer == a:
                correct_sound.play()
                print("¡Correcto!")
                position_block[z] = (1000, 1000)
                index_block.append(z)
                if len(index_block) == 12:
                    print("\n¡Felicidades has ganado!")
                    loaded_time = load_time()
                    if loaded_time[0] > minutes:
                        print("¡Nuevo record!")
                        save_time(minutes, seconds)
                    elif loaded_time[0] == minutes and loaded_time[1] > seconds:
                        print("¡Nuevo record!")
                        save_time(minutes, seconds)
                    
                    print("Tiempo final: ", end="")
                    if minutes < 10 and seconds < 10:
                        print("0"+str(minutes)+":0"+str(seconds))
                    elif minutes < 10:
                        print("0"+str(minutes)+":"+str(seconds))
                    elif seconds < 10:
                        print(str(minutes)+":0"+str(seconds))
                    else:
                        print(str(minutes)+":"+str(seconds))  
                    sys.exit()
            else:
                incorrect_sound.play()
                print("¡Incorrecto!")
                if len(index_block) != 0:
                    position_block[index_block[len(index_block)-1]] = aux_position_block[index_block[len(index_block)-1]]
                    index_block.pop(len(index_block)-1)
                
    for event in pygame.event.get():
        if event.type == pygame.QUIT or pygame.key.get_pressed()[pygame.K_ESCAPE]:
            sys.exit()
            
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            start_point = event.pos
        
        if event.type == pygame.MOUSEMOTION and event.buttons[0] == 1:
            end_point = event.pos
            draw_line = True
         
        if event.type == pygame.MOUSEBUTTONUP:
            arrow_sound.play()
            draw_line = False
            shoot = True         
    
    if draw_line and rotate_arrow:
        distance = calculate_distance(start_point, end_point)
        pygame.draw.aaline(screen, (0,0,0),(start_point), (end_point), 1)
        
        angle = calculate_angle(start_point, end_point)
        pos = (100, 300)
        rotate_image(screen, arrow, pos, (w/2, h/2), angle)
        if distance > 300:
            velocity_arrow = 15
        else:
            velocity_arrow = distance * 0.05
    else:
        if shoot == True: 
            if initialization == True:
                velocity = initialization_variables_parabolic_shot(velocity_arrow, angle)
                initialization = False
            
            if arrow_rect.center[0] > 850 or arrow_rect.center[1] > 650 or arrow_rect.center[0] < -200:
                shoot = False
                initialization = True
                rotate_arrow = True
                sleep(0.3)
            else:
                rotate_arrow = False
                arrow, arrow_rect = parabolic_shot(arrow, arrow_copy, velocity, arrow_rect, angle, GRAVITY)
                screen.blit(arrow, arrow_rect.center)
                arrow = arrow_copy
        else:
            arrow_rect.center = position_initial_arrow
            screen.blit(arrow, arrow_rect.center)
    
    pygame.display.update()
pygame.quit()