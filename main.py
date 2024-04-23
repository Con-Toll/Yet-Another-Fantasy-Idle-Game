import pygame
from pygame.locals import *
import sys

pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Yet Another Idle Clicker")

# FPS
fps = 60
pygame.time.Clock(fps)

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
main_menu = 1

# Clicking
clicks = 0
click_power = 1
auto_click_power = 0
click_check_interval = 1000  # in milliseconds
last_auto_click_time = pygame.time.get_ticks()

# Currency
gold = 0

# Game loop \o/
running = True
while running:
    screen.fill(white)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                clicks += click_power

    # Draw text
    score_text = font.render(f"Clicker Count: {clicks}", True, black)
    screen.blit(score_text, (20, 20))

    # Auto-click
    current_time = pygame.time.get_ticks()
    if current_time - last_auto_click_time >= click_check_interval:
        clicks += auto_click_power
        last_auto_click_time = current_time

    pygame.display.flip()

pygame.quit()
sys.exit()





