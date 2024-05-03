import pygame
import pygame_gui
import sys
import os
from pygame_gui.core import ObjectID
import math

pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Yet Another Idle Clicker")

#background image 
background = pygame.image.load("textures/background.png").convert()
backgroundwidth = background.get_width()

scroll = 0
sections = math.ceil(screen_width / backgroundwidth)
print(sections)


# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("assets/Chava-Regular.ttf", 30)
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



#Upgrade Area
upgrade_1_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(300,400)),container=area_upgrade_container)
upgrade_2_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,400),(300,400)),container=area_upgrade_container)





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


#Upgrade Button
BuyAll_1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0,0), (320, 50)),
                                             text='Buy All',
                                             container=upgrade_1_area,
                                             )

#Upgrade Picture

Upgrade_1_loaded_image = pygame.image.load("images.png")
Upgrade_2_loaded_image = pygame.image.load("images.png")
Upgrade_3_loaded_image = pygame.image.load("images.png")
Upgrade_4_loaded_image = pygame.image.load("images.png")
Upgrade_5_loaded_image = pygame.image.load("images.png")
Upgrade_6_loaded_image = pygame.image.load("images.png")
Upgrade_7_loaded_image = pygame.image.load("images.png")
Upgrade_8_loaded_image = pygame.image.load("images.png")
Upgrade_9_loaded_image = pygame.image.load("images.png")
Upgrade_10_loaded_image = pygame.image.load("images.png")
Upgrade_11_loaded_image = pygame.image.load("images.png")
Upgrade_12_loaded_image = pygame.image.load("images.png")

#Upgrade embedded image
upgrade_grid_image_1 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((10,135),(45,45)),
    image_surface=Upgrade_1_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_2 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((70,135),(45,45)),
    image_surface=Upgrade_2_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_3 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((130,135),(45,45)),
    image_surface=Upgrade_3_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_4 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((190,135),(45,45)),
    image_surface=Upgrade_4_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_5 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((250,135),(45,45)),
    image_surface=Upgrade_5_loaded_image,
    container=upgrade_1_area)

upgrade_grid_image_6 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((10,200),(45,45)),
    image_surface=Upgrade_6_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_7 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((70,200),(45,45)),
    image_surface=Upgrade_7_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_8 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((130,200),(45,45)),
    image_surface=Upgrade_8_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_9 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((190,200),(45,45)),
    image_surface=Upgrade_9_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_10 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((250,200),(45,45)),
    image_surface=Upgrade_10_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_11 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((10,265),(45,45)),
    image_surface=Upgrade_11_loaded_image,
    container=upgrade_1_area)
upgrade_grid_image_12 = pygame_gui.elements.UIImage(
    relative_rect=pygame.Rect((70,265),(45,45)),
    image_surface=Upgrade_12_loaded_image,
    container=upgrade_1_area)

#Upgrade "Available Text"

Available_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,50),(200,50)),text="Available :",
                                             container=upgrade_1_area,
                                            )

Bought_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,10),(200,50)),text="Bought :",
                                             container=upgrade_2_area,
                                            )


#try creating a class
class Container:
    def __init__(self,position,name) -> None:
        self.pos_y = position
        self.recog = name
    
    def container(self,name):
        self.recog  = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,self.pos_y),(300,200)),
                                         container=name
                                            )
        return self.recog
    
    
    
# Champion Class ( just need to fill the argument and it will automatically add into champion scrollable container)

class Champion:
    def __init__(self, name="", click_power=1, idle_power=1, position=0,level=1):
        self.name = name
        self.click_power = click_power
        self.idle_power = idle_power
        self.position = position
        self.level = level

        # UIPanel 
        self.container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (320, 200)), container=area_champ_container)

        # UIButton 
        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 150), (320, 50)), text=f"Level: default ", container=self.container)

        # UITextBox 
        self.text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((120, 60), (180, 70)), html_text=f"<p>Level : {self.level}<p>", container=self.container)

        # UIImage 
        self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((20, 20), (80, 80)), image_surface=pygame.image.load("images.png"), container=self.container)
        
        # Label
        self.label = pygame_gui.elements.UILabel(text=name,relative_rect=pygame.Rect((150,5),(100,50)),container=self.container)


    def __str__(self):
        return f"{self.name} (Click Power: {self.click_power}, Idle Power: {self.idle_power})"
    
    def set_container_pos(self,pos_y):
        self.container.set_position(0,pos_y)
        
    def set_image(self,image):
        self.image.set_image(pygame.image.load(f"{image}"))
        
    def  set_text(self,level):
        self.text_box.set_text(html_text=f"<p>Level : {level} <p><p>Power : {self.click_power}<p>")
        
    def set_label(self,text):
        self.label.set_text(text=text)
    
    

Champion_1 = Champion("Alucard",100,1,0)



clock = pygame.time.Clock()


champion_y = 490
upgrade_y = 490
misc_y = 490


# Game loop \o/
running = True
while running:
    screen.fill(white)
    time_delta = clock.tick(60)/1000.0

    for i in range(0, sections + 1):  
     screen.blit(background, (i * backgroundwidth + scroll, 0))
    
    
    #scrolling background
     scroll -= 1
    
    if abs(scroll) > backgroundwidth:
      scroll = 0



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
                elif upgrade_grid_image_1.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_1.set_container(container=upgrade_2_area)
                    upgrade_grid_image_1.set_relative_position(position=(10,80))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_2.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_2.set_container(container=upgrade_2_area)
                    upgrade_grid_image_2.set_relative_position(position=(70,80))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_3.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_3.set_container(container=upgrade_2_area)
                    upgrade_grid_image_3.set_relative_position(position=(130,80))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_4.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_4.set_container(container=upgrade_2_area)
                    upgrade_grid_image_4.set_relative_position(position=(190,80))

                    print("Misc. button pressed")   
                elif upgrade_grid_image_5.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_5.set_container(container=upgrade_2_area)
                    upgrade_grid_image_5.set_relative_position(position=(250,80))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_6.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_6.set_container(container=upgrade_2_area)
                    upgrade_grid_image_6.set_relative_position(position=(10,145))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_7.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_7.set_container(container=upgrade_2_area)
                    upgrade_grid_image_7.set_relative_position(position=(70,145))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_8.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_8.set_container(container=upgrade_2_area)
                    upgrade_grid_image_8.set_relative_position(position=(130,145))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_9.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_9.set_container(container=upgrade_2_area)
                    upgrade_grid_image_9.set_relative_position(position=(190,145))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_10.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_10.set_container(container=upgrade_2_area)
                    upgrade_grid_image_10.set_relative_position(position=(250,145))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_11.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_11.set_container(container=upgrade_2_area)
                    upgrade_grid_image_11.set_relative_position(position=(10,210))

                    print("Misc. button pressed")    
                elif upgrade_grid_image_12.rect.collidepoint(mouse_pos):
                    upgrade_grid_image_12.set_container(container=upgrade_2_area)
                    upgrade_grid_image_12.set_relative_position(position=(70,210))
                    
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
    pygame.display.update
    pygame.display.flip()

pygame.quit()
sys.exit()