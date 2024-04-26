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

#Overlap UIPanel
area_champ = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,490),(320,540)),manager=window)
area_upgrade = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((320,490),(320,540)),manager=window)
area_misc = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((640,490),(320,540)),manager=window)

#Container
area_champ_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0,50),(315,490)),container=area_champ,allow_scroll_x=False)
area_upgrade_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0,50),(315,490)),container=area_upgrade,allow_scroll_x=False)
area_misc_container = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((0,50),(315,490)),container=area_misc,allow_scroll_x=False)

#scroll
area_champ_container.set_scrollable_area_dimensions((315,400))
area_upgrade_container.set_scrollable_area_dimensions((315,400))
area_misc_container.set_scrollable_area_dimensions((315,400))

#Champion area
champ_1_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(300,200)),container=area_champ_container)
champ_2_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,200),(300,200)),container=area_champ_container)
champ_3_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,400),(300,200)),container=area_champ_container)
champ_4_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,600),(300,200)),container=area_champ_container)
champ_5_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,800),(300,200)),container=area_champ_container)

#Upgrade Area
upgrade_1_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(300,200)),container=area_upgrade_container)
upgrade_2_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,200),(300,200)),container=area_upgrade_container)
upgrade_3_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,400),(300,200)),container=area_upgrade_container)
upgrade_4_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,600),(300,200)),container=area_upgrade_container)
upgrade_5_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,800),(300,200)),container=area_upgrade_container)

#Misc Area
misc_1_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(300,200)),container=area_misc_container)
misc_2_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,200),(300,200)),container=area_misc_container)
misc_3_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,400),(300,200)),container=area_misc_container)
misc_4_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,600),(300,200)),container=area_misc_container)
misc_5_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,800),(300,200)),container=area_misc_container)


#Button
champ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (320, 50)),
                                             text='Champion',
                                             container=area_champ,
                                             )
upgrade_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (320, 50)),
                                             text='Upgrade',
                                             container=area_upgrade,
                                             )
misc_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0), (320, 50)),
                                             text='Misc.',
                                             container=area_misc,
                                             )

#Champion Button
champ_1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Champion 1',
                                             container=champ_1_area,
                                             )
champ_2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Champion 2',
                                             container=champ_2_area,
                                             )
champ_3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Champion 3',
                                             container=champ_3_area,
                                             )
champ_4_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Champion 4',
                                             container=champ_4_area,
                                             )
champ_5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Champion 5',
                                             container=champ_5_area,
                                             )
#Upgrade Button
upgrade_1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Upgrade 1',
                                             container=upgrade_1_area,
                                             )
upgrade_2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Upgrade 2',
                                             container=upgrade_2_area,
                                             )
upgrade_3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Upgrade 3',
                                             container=upgrade_3_area,
                                             )
upgrade_4_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Upgrade 4',
                                             container=upgrade_4_area,
                                             )
upgrade_5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Upgrade 5',
                                             container=upgrade_5_area,
                                             )
#Misc Button
misc_1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Misc 1',
                                             container=misc_1_area,
                                             )
misc_2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Misc 2',
                                             container=misc_2_area,
                                             )
misc_3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Misc 3',
                                             container=misc_3_area,
                                             )
misc_4_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Misc 4',
                                             container=misc_4_area,
                                             )
misc_5_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,150), (320, 50)),
                                             text='Misc 5',
                                             container=misc_5_area,
                                            )


#Champion loaded image
champion_1_loaded_image = pygame.image.load("")
champion_2_loaded_image = pygame.image.load("")
champion_3_loaded_image = pygame.image.load("")
champion_4_loaded_image = pygame.image.load("")
champion_5_loaded_image = pygame.image.load("")

#Champion embedded image
grid_image_1 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((20,20),(80,80)),
    image_surface=champion_1_loaded_image,
    container=champ_1_area)
grid_image_2 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((20,20),(80,80)),
    image_surface=champion_1_loaded_image,
    container=champ_1_area)
grid_image_3 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((20,20),(80,80)),
    image_surface=champion_1_loaded_image,
    container=champ_1_area)
grid_image_4 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((20,20),(80,80)),
    image_surface=champion_1_loaded_image,
    container=champ_1_area)
grid_image_5 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((20,20),(80,80)),
    image_surface=champion_1_loaded_image,
    container=champ_1_area)


#try creating a class
class Champion:
    def __init__(self, name, click_power, idle_power):
        self.name = name
        self.click_power = click_power
        self.idle_power = idle_power

    def __str__(self):
        return f"{self.name} (Click Power: {self.click_power}, Idle Power: {self.idle_power})"

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
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if champ_button.rect.collidepoint(mouse_pos):
                    if champion_y == 490:
                        champion_y = 0
                    else:
                        champion_y = 490
                    area_champ.set_position(position=(0, champion_y))
                elif upgrade_button.rect.collidepoint(mouse_pos):
                    if upgrade_y == 490:
                        upgrade_y = 0
                    else:
                        upgrade_y = 490
                    area_upgrade.set_position(position=(320, upgrade_y))
                    print("Upgrade button pressed")
                elif misc_button.rect.collidepoint(mouse_pos):
                    if misc_y == 490:
                        misc_y = 0
                    else:
                        misc_y = 490
                    area_misc.set_position(position=(640, misc_y))
                    print("Misc. button pressed")
                else:
                    gold += click_power
        window.process_events(event)
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



