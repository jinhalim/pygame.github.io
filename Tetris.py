import pygame
from pygame.locals import *
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
 
pygame.init()

# Set the width and height of the screen [width, height]
size = (300, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("My Game")
 
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()
 
i = 0
MAX = 400
player_image1 = pygame.image.load("img/totoro2.png").convert()
position_List = []
x = 100
y = 0
position_List.append([x,y])

# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if not hasattr(event, 'key'):                    # 키 관련 이벤트가 아닐 경우, 건너뛰도록 처리하는 부분
            continue
        if event.type == KEYDOWN:
            if event.key == K_RIGHT:
                position_List[i][0] = position_List[i][0] + 10
            elif event.key == K_LEFT:
                position_List[i][0] = position_List[i][0] - 10
 

    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, (10, 10, 100, 50))

    for z in range(len(position_List)):
       screen.blit(player_image1,position_List[z])
       print(position_List)
    if i < 10:
        po_y = position_List[i][1]
        if po_y < MAX :
           position_List[i][1] = position_List[i][1] +2
        elif po_y >= MAX:
            position_List.append([x,y])
            i = i + 1
            MAX = MAX - 100

       

    pygame.display.flip()
 
    # --- Limit to 60 frames per second
    clock.tick(60)
 
# Close the window and quit.
pygame.quit()