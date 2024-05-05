import pygame 
import math
import random
import time
import sys
import pygame_gui
import pygame_gui.ui_manager

pygame.init()

height = 400
width = 600

screen = pygame.display.set_mode((height,width))
pygame.display.set_caption("Lucky Perk")

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
main_menu = 1

window = pygame_gui.ui_manager.UIManager(window_resolution=((height),(width)))

Container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((200,50),(200,300)),
                                        manager=window)


Running = True

while Running == True:
    screen.fill(white)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Running = False

    pygame.display.update
    pygame.display.flip()
    
pygame.quit()
sys.exit()