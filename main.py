import pygame
import pygame_gui
import sys
import os
from pygame_gui.core import ObjectID
import math
import time
import threading

pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))

pygame.display.set_caption("Yet Another Idle Clicker")

#background image 
background = pygame.image.load("assets/background.png").convert()
backgroundwidth = background.get_width()

scroll = 0
sections = math.ceil(screen_width / backgroundwidth)
print(sections)


# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("assets/Chava-Regular.ttf", 26)
main_menu = 1

# Game Variables
# Clicking
click_power = 100
auto_click_power = 0
click_check_interval = 1000  # in milliseconds
last_click_update = pygame.time.get_ticks()

# Currency
gold = 0

# Champions
total_champion = 0
price_hire = 15


# Buttons
button_layout_rect = pygame.Rect(30,20,100,20)
window = pygame_gui.UIManager((screen_width, screen_height),theme_path='assets/theme.json')

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


#Misc Area
misc_1_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(300,200)),container=area_misc_container)
misc_2_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,200),(300,200)),container=area_misc_container)
misc_3_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,400),(300,200)),container=area_misc_container)
misc_4_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,600),(300,200)),container=area_misc_container)
misc_5_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,800),(300,200)),container=area_misc_container)


#Button
champ_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (320, 50)),
                                             text='Champions',
                                             container=area_champ,
                                             )
upgrade_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (320, 50)),
                                             text='Upgrades',
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


#Upgrade Picture

Upgrade_1_loaded_image = pygame.image.load("assets/images.png")
Upgrade_2_loaded_image = pygame.image.load("assets/images.png")
Upgrade_3_loaded_image = pygame.image.load("assets/images.png")
Upgrade_4_loaded_image = pygame.image.load("assets/images.png")
Upgrade_5_loaded_image = pygame.image.load("assets/images.png")
Upgrade_6_loaded_image = pygame.image.load("assets/images.png")
Upgrade_7_loaded_image = pygame.image.load("assets/images.png")
Upgrade_8_loaded_image = pygame.image.load("assets/images.png")
Upgrade_9_loaded_image = pygame.image.load("assets/images.png")
Upgrade_10_loaded_image = pygame.image.load("assets/images.png")
Upgrade_11_loaded_image = pygame.image.load("assets/images.png")
Upgrade_12_loaded_image = pygame.image.load("assets/images.png")

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


total_idle_power = 0

# Idle Power Display
def idle_power_display():
    if total_idle_power > 9999999999:
        idle_power_format = "{:.4e}".format(total_idle_power)
    else:
        idle_power_format = "{:,}".format(total_idle_power)
    idle_text = font.render(f"Idle: {idle_power_format}", True, black)
    idle_text_rect = idle_text.get_rect(center=(screen_width/6, 40))

    screen.blit(idle_text, idle_text_rect)


# Click Power Display
def click_power_display():
    if click_power > 9999999999:
        click_power_format = "{:.4e}".format(click_power)
    else:
        click_power_format = "{:,}".format(click_power)
    click_power_text = font.render(f"Clicks: {click_power_format}", True, black)
    click_power_text_rect = click_power_text.get_rect(center=(screen_width/3, 40))

    screen.blit(click_power_text, click_power_text_rect)


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


# Auto-click
current_time = pygame.time.get_ticks()
if current_time - last_click_update >= click_check_interval:
    gold += auto_click_power
    last_auto_click_time = current_time


# Champions
class Champion():
    def __init__(self, name, title, level, idle_power, isUnlocked, shown, position, price_hire, price_level, image="assets/images.png"):
        self.name = name
        self.title = title
        self.level = level
        self.idle_power = idle_power
        self.isUnlocked = isUnlocked
        self.shown = shown
        self.pos = position
        self.image = image
        self.price_hire = price_hire
        self.price_level = price_level

        # Champion container
        self.container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((2, self.pos),(300, 200)),
                                                     container=area_champ_container)

        # Champion buttons

        # Champion info
        self.text_box = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((120, 55), (160, 70)),
                                                      html_text=f"<p>Level : {self.level}<p>",
                                                      container=self.container)

        # Champion image
        self.image_load = pygame.image.load(image)
        self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((20, 50),(80, 80)),
                                                 image_surface=self.image_load,
                                                 container=self.container)

        # Champion title
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 5),(300, 35)),
                                                 text=f"{self.title}",
                                                 container=self.container)
        

        # Level Champion
        self.button_level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,140), (150, 50)),
                                                         text="Level up",
                                                         container=self.container)
    
        self.price_level_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((160, 140),(150, 50)),
                                                               text=f"{self.price_level}",
                                                               container=self.container)


        # Hire Champion
        self.button_hire = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10,140), (150, 50)),
                                                        text="Hire",
                                                        container=self.container)

        self.price_hire_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((160, 140),(150, 50)),
                                                              text=f"{self.price_hire}",
                                                              container=self.container)

    def level_up(self):
        global gold
        gold = gold - self.price_level
        self.level += 1
        self.text_box.set_text(f"<p>Level : {self.level}<p>")
        self.price_level *= 2
        self.price_level_display.set_text(f"{self.price_level}")
        return self.price_level

    def hire(self):
        self.button_hire.disable()
        self.button_hire.hide()
        self.price_hire_display.disable()
        self.price_hire_display.hide()

        global gold
        global total_champion

        gold = gold - self.price_hire
        self.level += 1
        self.text_box.set_text(f"<p>Level : {self.level}<p>")
        total_champion += 1
        self.isUnlocked = True
        self.trigger(self.idle_power)

        index = champions.index(self)
        if index < len(champions) - 1:
            next_champion = champions[index + 1]
            next_champion.shown = True
            next_champion.showChamp()
        

    # Idle generation
    def trigger(self, idle_power):
        threading.Thread(target=self.increment_gold, args=(idle_power,)).start()

    def increment_gold(self, idle_power):
        while self.isUnlocked:
            time.sleep(1)
            global gold
            gold += idle_power

    # Enable/Disable champion container
    def showChamp(self):
        if self.shown == False:
            self.container.hide()
            self.container.disable()
            self.button_hire.hide()
            self.button_hire.disable()
        elif self.shown == True:
            self.container.show()
            self.container.enable()
            if self.isUnlocked == False:
                self.button_hire.show()
                self.button_hire.enable()

# Champions List
hero = Champion("hero", "You, the Hero", 0, 1, False, True, 0, 15, 20, "assets/images.png")
pyr = Champion("pyr", "Pyr, the Apprentice", 0, 2, False, False, 200, 1000, 1200, "assets/images.png")
avani = Champion("avani", "Avani, the Bright", 0, 0, False, False, 400, 2500, 3000, "assets/images.png")
obek = Champion("obek", "Obek, the Scavenger", 0, 0, False, False, 600, 10000, 12000, "assets/images.png")
# azura

champions = [hero, pyr, avani, obek]

# Champion initialization
pyr.showChamp()
avani.showChamp()
obek.showChamp()


# Level Champion



# Champion Unlocks
def heroUnlock():
    hero.hire()
    hero.trigger(hero.idle_power)
    pyr.shown = True
    pyr.showChamp()

def pyrUnlock():
    pyr.trigger(pyr.idle_power)
    avani.shown = True
    avani.showChamp()
    pyr.hire()

def avaniUnlock():
    # Activate champion stats


    # Display next champion's container
    obek.showChamp()


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

                # Tab buttons
                if champ_button.rect.collidepoint(mouse_pos):
                    if champion_y == 490:
                        champion_y = 0
                        upgrade_y = 490
                        misc_y = 490
                    else:
                        champion_y = 490
                    area_champ.set_position(position=(0, champion_y))
                    area_upgrade.set_position(position=(320, upgrade_y))
                    area_misc.set_position(position=(640, misc_y))
                elif upgrade_button.rect.collidepoint(mouse_pos):
                    if upgrade_y == 490:
                        champion_y = 490
                        upgrade_y = 0
                        misc_y = 490
                    else:
                        upgrade_y = 490
                    area_champ.set_position(position=(0, champion_y))
                    area_upgrade.set_position(position=(320, upgrade_y))
                    area_misc.set_position(position=(640, misc_y))
                    print("Upgrade button pressed")
                elif misc_button.rect.collidepoint(mouse_pos):
                    if misc_y == 490:
                        champion_y = 490
                        upgrade_y = 490
                        misc_y = 0
                    else:
                        misc_y = 490
                    area_champ.set_position(position=(0, champion_y))
                    area_upgrade.set_position(position=(320, upgrade_y))
                    area_misc.set_position(position=(640, misc_y))
                    print("Misc. button pressed")

                # Upgrade buttons
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
                    print("Misc. button pressed")

                for champion in champions:
                    # Level up button
                    if champion.button_level.rect.collidepoint(mouse_pos):
                        if gold >= champion.price_level and champion.isUnlocked:
                            champion.level_up()

                    # Hire button
                    if champion.button_hire.is_enabled:
                        if champion.button_hire.rect.collidepoint(mouse_pos):
                            if gold >= champion.price_hire and not champion.isUnlocked:
                                champion.hire()

                
                else:
                    gold += click_power

        window.process_events(event)

    
    click_power_display()
    idle_power_display()
    gold_display(gold)


    window.update(time_delta)
    window.draw_ui(screen)
    pygame.display.update
    pygame.display.flip()

pygame.quit()
sys.exit()



