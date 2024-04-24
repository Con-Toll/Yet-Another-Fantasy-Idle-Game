import pygame
import pygame_gui
import sys
import os

pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 960
screen_height = 540
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
gold = 0


# =========PLACEHOLDER IDLE GENERATION VARIABLE=========
idle_power = 0


# Buttons
button_layout_rect = pygame.Rect(30,20,100,20)
window = pygame_gui.UIManager((screen_width, screen_height),theme_path='theme.json')



champ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5, 490), (320, 50)),
                                             text='Champion',
                                             manager=window,
                                             )
upgrade_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((320, 490), (320, 50)),
                                             text='Upgrade',
                                             manager=window,
                                             )
misc_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((635, 490), (320, 50)),
                                             text='Misc.',
                                             manager=window,
                                             )
#container
area_champ = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((5,0),(320,540)),manager=window)
area_upgrade = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((320,0),(320,540)),manager=window)
area_misc = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((635,0),(320,540)),manager=window)
area_champ.hide()
area_upgrade.hide()
area_misc.hide()

clock = pygame.time.Clock()


champion_y = 490
upgrade_y = 490
misc_y = 490


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
                if champion_y == 490:
                    champion_y = 0
                else:
                    champion_y = 490
                champ_button.set_position(position=(5, champion_y))
            elif upgrade_button.rect.collidepoint(mouse_pos):
                if upgrade_y == 490:
                    upgrade_y = 0
                else:
                    upgrade_y = 490
                upgrade_button.set_position(position=(320, upgrade_y))
                print("Upgrade button pressed")
            elif misc_button.rect.collidepoint(mouse_pos):
                if misc_y == 490:
                    misc_y = 0
                else:
                    misc_y = 490
                misc_button.set_position(position=(635, misc_y))
                print("Misc. button pressed")
            else:
                gold += click_power


    # Click Power Display
    def idle_power_display():
        idle_text = font.render(f"Idle: {idle_power}", True, black)
        idle_text_rect = idle_text.get_rect(center=(screen_width/6, 40))

        screen.blit(idle_text, idle_text_rect)

    idle_power_display()

    def click_power_display():
        click_power_text = font.render(f"Clicks: {click_power}", True, black)
        click_power_text_rect = click_power_text.get_rect(center=(screen_width/3, 40))

        screen.blit(click_power_text, click_power_text_rect)

    click_power_display()

    # Gold Display
    def gold_display(gold):
        score_text = font.render(f"Gold:", True, black)
        score_text_rect = score_text.get_rect(center=(screen_width/2, 40))
        
        if gold > 9999999999:
            gold_format = "{:.4e}".format(gold)
        else:
            gold_format = "{:,}".format(gold)

        gold_text = font.render(f"{gold_format}", True, black)
        gold_text_rect = gold_text.get_rect(center=(screen_width/2, 70))

        screen.blit(score_text, score_text_rect)
        screen.blit(gold_text, gold_text_rect)

    gold_display(gold)

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





