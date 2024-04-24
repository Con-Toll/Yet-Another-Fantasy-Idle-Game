import pygame
import pygame_gui
import sys
import os

pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 854
screen_height = 480
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Yet Another Idle Clicker")

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.SysFont(None, 36)
main_menu = 1

# Clicking
click_power = 1
auto_click_power = 0
click_check_interval = 1000  # in milliseconds
last_click_update = pygame.time.get_ticks()

# Currency
gold = 54235235230

def champ_menu(x,y,width,height):
    champ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((x,y), (width, height)),
                                               text='Champion',
                                               manager=window,
                                               )
    return champ_button


#button
button_layout_rect = pygame.Rect(30,20,100,20)
window = pygame_gui.UIManager((screen_width, screen_height),theme_path='theme.json')



champ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 400), (200, 50)),
                                             text='Champion',
                                             manager=window,
                                             )
upgrade_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((325, 400), (200, 50)),
                                             text='Upgrade',
                                             manager=window,
                                             )
misc_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((625, 400), (200, 50)),
                                             text='Misc.',
                                             manager=window,
                                             )


clock = pygame.time.Clock()

# Game loop \o/
running = True
while running:
    screen.fill(white)
    time_delta = clock.tick(60)/1000.0

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            window.process_events(event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
            if champ_button.rect.collidepoint(mouse_pos):
                champ_menu(100,200,200,50)
            elif upgrade_button.rect.collidepoint(mouse_pos):
                print("Upgrade button pressed")
            elif misc_button.rect.collidepoint(mouse_pos):
                print("Misc. button pressed")
            else:
                gold += click_power


    # Draw text
    def gold_display():
        score_text = font.render(f"Gold:", True, black)
        score_text_rect = score_text.get_rect(center=(screen_width/2, 40))

        gold_text = font.render(f"{gold}", True, black)
        gold_text_rect = gold_text.get_rect(center=(screen_width/2, 70))

        screen.blit(score_text, score_text_rect)
        screen.blit(gold_text, gold_text_rect)

    gold_display()

    # Auto-click
    current_time = pygame.time.get_ticks()
    if current_time - last_click_update >= click_check_interval:
        gold += auto_click_power
        last_auto_click_time = current_time
    

    window.update(time_delta)
    window.draw_ui(screen)
    
    pygame.display.flip()

pygame.quit()
sys.exit()





