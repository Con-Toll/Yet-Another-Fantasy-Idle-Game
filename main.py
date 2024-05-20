import pygame
import pygame_gui
import sys
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

window = pygame_gui.UIManager((screen_width, screen_height),theme_path='assets/theme.json')

pygame.display.set_caption("Yet Another Idle Clicker")


# Main Menu
main_menu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -2), (screen_width+4, screen_height+4)),
                                              manager=window)
main_menu_status = True

button_game_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (150, 50)),
                                                 text="Start",
                                                 container=main_menu,
                                                 anchors={'center': 'center'})



#background image 
background = pygame.image.load("assets/background.png")
backgroundwidth = screen_width
backgroundheight = 0
background_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (screen_width, screen_height)),
                                              visible=0, 
                                              manager=window)

scroll = 0
sections = math.ceil(screen_width / backgroundwidth)


# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("assets/Chava-Regular.ttf", 26)

# Game Variables
# Pause
paused = True

# Clicking
click_power = 100000

# Currency
gold = 0

# Champions
total_champion = 0



# Main tab button
area_tabs = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-3, screen_height-31), (969, screen_height/3*2)))
button_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (966, 30)), 
                                          text="",
                                          container=area_tabs)
# False = Closed, True = Open
area_tabs_status = False


# Champion Area
container_champ = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((5, 90), (440, 230)),
                                                                container=area_tabs,
                                                                allow_scroll_x=False)
# Header that says "CHAMPIONS"
area_tab_champ = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((7, 32), (438, 56)),
                                          container=area_tabs)
text_tab_champ = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 2), (436, 52)),
                                               text="Champions",
                                               object_id=ObjectID(class_id="@text_tabs"),
                                               container=area_tab_champ)

# Upgrade Area
container_upgrade = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((450, 90), (440, 290)),
                                                                  container=area_tabs,
                                                                  allow_scroll_x=False)
# Header that says "UPGRADES"
area_tab_upgrade = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((450, 32), (440, 56)),
                                          container=area_tabs)
text_tab_upgrade = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 2), (283, 52)),
                                               text="Upgrades",
                                               object_id=ObjectID(class_id="@text_tabs"),
                                               container=area_tab_upgrade)

# Upgrade "Buy All" button
button_up_buyall = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((290, 6), (144, 44)),
                                             text="Buy All",
                                             container=area_tab_upgrade,
                                             )


# Containers for available and bought upgrades
area_upgrade_available = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (422, 315)),
                                                     container=container_upgrade)
area_upgrade_bought = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,319), (422, 315)),
                                                  container=container_upgrade)



# "Available" and "Bought" text
text_available = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,50)),
                                             text="Available:",
                                             container=area_upgrade_available,
                                            )

text_bought = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,50)),
                                          text="Bought:",
                                          container=area_upgrade_bought,
                                         )


# Tab switch buttons
current_tab = 1
button_next_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((901, 40), (50, 275)),
                                              text=">",
                                              container=area_tabs)
button_prev_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((14, 40), (50, 275)),
                                              text="<",
                                              container=area_tabs)

# Ascension wao
button_prestige = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 40), (160, 40)),
                                                text="Transcend")
area_prestige = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -2), (screen_width+4, screen_height+4)))
area_prestige.disable()
area_prestige.hide()
text_prestige = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (screen_width, 75)),
                                            text="T R A N S C E N D E N C E",
                                            container=area_prestige,
                                            object_id=ObjectID(class_id="@text_prestige"))


# Champions
class Champion():
    def __init__(self, index, name, title, level, base_idle_power, shown, price_hire, price_level, image="assets/images.png"):
        self.name = name
        self.title = title
        self.level = level
        self.base_idle_power = base_idle_power
        self.idle_power = 0
        self.isUnlocked = False
        self.shown = shown
        self.index = index
        self.image = image
        self.price_hire = price_hire
        self.price_level = price_level
        self.up_mult = 1

        # Champion container
        self.container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((2, (self.index * 100)), (416, 100)),
                                                     container=container_champ)

        # Champion info
        # Level icon + number
        self.image_level_load = pygame.image.load("assets/images.png")
        self.image_level = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((100, 29), (35, 35)),
                                                       image_surface=self.image_level_load,
                                                       container=self.container)
        
        self.text_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((135, 29), (140, 35)),
                                                                     text=f"{self.level}",
                                                                     container=self.container,
                                                                     object_id=ObjectID(class_id="@champ_info"))

        # Idle power icon + number
        self.image_idle_load = pygame.image.load("assets/images.png")
        self.image_idle = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((100, 64), (35, 35)),
                                                       image_surface=self.image_idle_load,
                                                       container=self.container)

        self.text_idle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((135, 64), (140, 35)),
                                                                     text=f"{self.idle_power} /s",
                                                                     container=self.container,
                                                                     object_id=ObjectID(class_id="@champ_info"))

        # Champion image
        self.image_load = pygame.image.load(image)
        self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((10, 10), (80, 80)),
                                                 image_surface=self.image_load,
                                                 container=self.container)

        # Champion title
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((100, 3), (320, 25)),
                                                 text=f"{self.title}",
                                                 container=self.container,
                                                 object_id=ObjectID(class_id="@champ_title"))

        # Level Champion button + price
        self.button_level = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((278, 28), (136, 35)),
                                                         text="Level up",
                                                         container=self.container,
                                                         object_id=ObjectID(class_id="@button_level"))
    
        self.price_level_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((280, 63), (132, 35)),
                                                               text=f"{self.price_level}",
                                                               container=self.container)
        
        # Hire Champion button + price
        self.button_hire = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((278, 28), (134, 35)),
                                                        text="Hire",
                                                        container=self.container)

        self.price_hire_display = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((280, 63),(128, 35)),
                                                              text=f"{self.price_hire}",
                                                              container=self.container)


    # Hire Champion Function
    def hire(self):
        # Disable Hire Button/Price Display
        self.button_hire.disable()
        self.button_hire.hide()
        self.price_hire_display.disable()
        self.price_hire_display.hide()
        # Enable level up buttons
        self.button_level.enable()
        self.button_level.show()

        global gold
        global total_champion

        # Deduct gold
        gold = gold - self.price_hire
        # Update champion variables and total champion
        self.level = 1
        total_champion += 1
        self.isUnlocked = True
        self.idle_power = self.base_idle_power * self.level * self.up_mult
        self.update_stats()
        self.thread_start()

        # Show next champion
        index = champions.index(self)
        if index < len(champions) - 1:
            next_champion = champions[index + 1]
            next_champion.shown = True
            next_champion.showChamp()

        return total_champion, self.idle_power
        

    # Level Up Function
    def level_up(self):
        global gold
        gold = gold - self.price_level
        self.level += 1
        self.price_level *= 2
        self.price_level_display.set_text(f"{self.price_level}")
        self.idle_power = self.base_idle_power * self.level * self.up_mult
        self.update_stats()
        return self.price_level, self.level, self.idle_power

    # Update champ info
    def update_stats(self):
        self.text_level.set_text(f"{self.level}")
        self.text_idle.set_text(f"{self.idle_power}/s")

    # Idle generation
    def thread_start(self):
        thread = threading.Thread(target=self.increment_gold)
        thread.daemon = True
        thread.start()

    def increment_gold(self):
        while True:
            time.sleep(1)
            global gold
            gold += self.idle_power


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
                self.button_level.hide()
                self.button_level.disable()

    # Champ upgrades
    def upgrade1(self, mult):
        self.up_mult = self.up_mult * mult
        self.idle_power = self.base_idle_power * self.level * self.up_mult
        self.update_stats()
        return self.idle_power



# Champions List 
# (index, name, title, level, base_idle_power, shown, price_hire, price_level, image)
hero = Champion(0,"hero", "You, the Hero", 0, 1, True, 15, 20, "assets/images.png")
pyr = Champion(1, "pyr", "Pyr, the Apprentice", 0, 10, False, 1000, 1200, "assets/images.png")
avani = Champion(2, "avani", "Avani, the Bright", 0, 100, False, 2500, 3000, "assets/images.png")
obek = Champion(3, "obek", "Obek, the Scavenger", 0, 1000, False, 5000, 6000, "assets/images.png")
azura = Champion(4, "azura", "Azura, the Something", 0, 10000, False, 10000, 10000, "assets/images.png")

champions = [hero, pyr, avani, obek, azura]


# Champion initialization
for champion in champions:
    champion.showChamp()



# Upgrades
class Upgrade():
    def __init__(self,  num_id, requirement, price, name, origin, tooltip, mult, action=None):
        self.x = 10
        self.y = 60
        self.num_id = num_id
        self.requirement = requirement
        self.name = name
        self.origin = origin
        self.tooltip = tooltip
        self.shown = False
        self.price = price
        self.isUnlocked = False
        self.action = action
        self.mult = mult

        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (45, 45)),
                                                   text="",
                                                   tool_tip_text=f"{self.name}\n{self.tooltip}\nPrice: {self.price}",
                                                   container=area_upgrade_available)
        

    def available(self):
        if self.shown:
            self.button.enable()
            self.button.show()

        if not self.isUnlocked:
            index = list_available.index(self)
            # x values: 10, 55, 100, 145, 190, 235, 280, 325, 370, 415; the container is (422, 315)
            
            if index >= 8:
                self.x = 10 + ((index-8) * 49) + ((index-8) * 2)
                self.y = 60 + 51
            elif index >= 0:
                self.x = 10 + (index * 49) + (index * 2)
                self.y = 60

            # note for future improvement:
            # for index % 8 = 0, modifier = index, self.x = 10 + 

        self.button.set_relative_position((self.x, self.y))

        #print(self.num_id, self.x)

    # Purchase upgrades
    def purchase(self):
        global gold
        gold = gold - self.price
        self.isUnlocked = True
        
        self.button.set_container(container=area_upgrade_bought)
        self.action(self.mult)

        print("bought")


    def sort(self):
        if self.isUnlocked == True:
            index = list_bought.index(self)
            
            if index >= 8:
                self.x = 10 + ((index-8) * 49) + ((index-8) * 2)
                self.y = 60 + 51
            elif index >= 0:
                self.x = 10 + (index * 49) + (index * 2)
                self.y = 60

            self.button.set_relative_position((self.x, self.y))


# Upgrades
# num_id, requirement, price, name, origin, tooltip, mult, action

up_hero1 = Upgrade(1, 2, 100000, "Hero 1", hero, "This is hero upgrade 1", 2, action=(hero.upgrade1))
up_hero2 = Upgrade(2, 3, 100000, "Hero 2", hero, "This is hero upgrade 2", 2, action=(hero.upgrade1))
up_hero3 = Upgrade(3, 4, 100000, "Hero 3", hero, "This is hero upgrade 3", 2, action=(hero.upgrade1))
up_hero4 = Upgrade(4, 5, 100000, "Hero 4", hero, "This is hero upgrade 4", 2, action=(hero.upgrade1))
up_hero5 = Upgrade(5, 6, 100000, "Hero 5", hero, "This is hero upgrade 5", 2, action=(hero.upgrade1))
up_hero6 = Upgrade(6, 7, 100000, "Hero 6", hero, "This is hero upgrade 6", 2, action=(hero.upgrade1))
up_pyr1 = Upgrade(7, 2, 100000, "Pyr 1", pyr, "This is pyr upgrade 1", 2, action=(pyr.upgrade1))
up_pyr2 = Upgrade(8, 3, 100000, "Pyr 2", pyr, "This is pyr upgrade 2", 2, action=(pyr.upgrade1))
up_pyr3 = Upgrade(9, 4, 100000, "Pyr 3", pyr, "This is pyr upgrade 3", 2, action=(pyr.upgrade1))
up_pyr4 = Upgrade(10, 5, 100000, "Pyr 4", pyr, "This is pyr upgrade 4", 2, action=(pyr.upgrade1))
up_pyr5 = Upgrade(11, 6, 100000, "Pyr 5", pyr, "This is pyr upgrade 5", 2, action=(pyr.upgrade1))
up_pyr6 = Upgrade(12, 7, 100000, "Pyr 6", pyr, "This is pyr upgrade 6", 2, action=(pyr.upgrade1))

list_upgrades = [
    up_hero1, up_hero2, up_hero3, up_hero4, up_hero5, up_hero6, 
    up_pyr1, up_pyr2, up_pyr3, up_pyr4, up_pyr5, up_pyr6
    ]
list_available = []
list_bought = []

for upgrade in list_upgrades:
    upgrade.button.disable()
    upgrade.button.hide()

clock = pygame.time.Clock()


total_idle_power = sum(champion.idle_power for champion in champions)


# Idle Power Display
def idle_power_display():
    idle_text = font.render(f"Idle P:", True, black)
    idle_text_rect = idle_text.get_rect(center=(screen_width/10, 40))
    if abs(total_idle_power) > 99999:
        idle_power_format = "{:.2e}".format(total_idle_power)
    else:
        idle_power_format = "{:,}".format(total_idle_power)
    idle_num = font.render(f"{idle_power_format}", True, black)
    idle_num_rect = idle_text.get_rect(center=(screen_width/10, 70))

    screen.blit(idle_text, idle_text_rect)
    screen.blit(idle_num, idle_num_rect)


# Click Power Display
def click_power_display():
    click_text = font.render(f"Click P:", True, black)
    click_text_rect = click_text.get_rect(center=(screen_width/3, 40))

    if abs(click_power) > 99999:
        click_power_format = "{:.2e}".format(click_power)
    else:
        click_power_format = "{:,}".format(click_power)
    click_power_text = font.render(f"{click_power_format}", True, black)
    click_power_text_rect = click_power_text.get_rect(center=(screen_width/3, 70))

    screen.blit(click_text, click_text_rect)
    screen.blit(click_power_text, click_power_text_rect)


# Gold Display
def gold_display(gold):
    score_text = font.render(f"Gold:", True, black)
    score_text_rect = score_text.get_rect(center=(screen_width/2, 40))
        
    if abs(gold) > 9999999999:
        gold_format = "{:.3e}".format(gold)
    else:
        gold_format = "{:,}".format(gold)

    gold_text = font.render(f"{gold_format}", True, black)
    gold_text_rect = gold_text.get_rect(center=(screen_width/2, 70))

    screen.blit(score_text, score_text_rect)
    screen.blit(gold_text, gold_text_rect)

    # Main menu
def init_main_menu():
    global paused
    area_tabs.hide()
    area_tabs.disable()
    button_prestige.hide()
    button_prestige.disable()
    main_menu.show()
    main_menu.enable()
    paused = True
    return paused
    
def game_start():
    global paused, main_menu_status
    area_tabs.show()
    area_tabs.enable()
    button_prestige.show()
    button_prestige.enable() 
    main_menu.hide()
    main_menu.disable()
    main_menu_status = False
    paused = False
    print("worked")
    return paused, main_menu_status


# Game loop \o/
running = True
while running:
    screen.fill(white)
    time_delta = clock.tick(60)/1000.0

    for i in range(0, sections + 1):  
     screen.blit(background, (i * backgroundwidth + scroll, backgroundheight))
    
    
    #scrolling background
     scroll -= 1
    
    if abs(scroll) > backgroundwidth:
      scroll = 0


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:
            if event.ui_element == button_prestige:
                paused = not paused
                area_tabs.hide()
                area_tabs.disable()
                area_prestige.show()
                area_prestige.enable()
                button_prestige.hide()
                button_prestige.disable()
                text_prestige.set_active_effect(pygame_gui.TEXT_EFFECT_FADE_IN)

                for champion in champions:
                    champion.isUnlocked = False


            
            if not paused:
                if event.ui_element == button_next_tab:
                    current_tab = 2

                elif event.ui_element == button_prev_tab:
                    current_tab = 1

                # Tab buttons
                elif event.ui_element == button_tab:
                    if area_tabs_status:
                        area_tabs.set_relative_position((-3, screen_height-31))
                        background_area.set_relative_position((0, 0-31))
                        area_tabs_status = False
                        backgroundheight = 0
                    elif not area_tabs_status:
                        area_tabs.set_relative_position((-3, screen_height/2.5))
                        background_area.set_relative_position((0, 0-324))
                        area_tabs_status = True
                        backgroundheight = (0-screen_height/2.9)
                        
                # Champion buttons
                for champion in champions:
                    # Level up button
                    if event.ui_element == champion.button_level:
                        if gold >= champion.price_level and champion.isUnlocked:
                            champion.level_up()
                            total_idle_power = sum(champion.idle_power for champion in champions)

                    # Hire button
                    if champion.button_hire.is_enabled:
                        if event.ui_element == champion.button_hire:
                            if gold >= champion.price_hire and not champion.isUnlocked:
                                champion.hire()
                                total_idle_power = sum(champion.idle_power for champion in champions)


                # Upgrade buttons
                for upgrade in list_available:
                    if event.ui_element == upgrade.button:
                        if gold >= upgrade.price and not upgrade.isUnlocked and upgrade.shown:
                            # Buy upgrade
                            upgrade.purchase()
                            # Move bought upgrade from available to bought                        lists make me wanna commit a crime
                            list_available.remove(upgrade)
                            print(list_available)
                            list_bought.append(upgrade)
                            print(list_bought)
                            # Update list of available upgrades
                            for upgrade in list_available:
                                upgrade.available()
                            # Update list of bought upgrades
                            for upgrade in list_bought:
                                upgrade.sort()
                            total_idle_power = sum(champion.idle_power for champion in champions)

            if event.ui_element == button_game_start:
                game_start()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if not paused:
                    if background_area.rect.collidepoint(mouse_pos):
                        gold += click_power

        window.process_events(event)




    # Tab
    if current_tab == 1 and not paused:
        button_next_tab.show()
        button_next_tab.enable()
        button_prev_tab.hide()
        button_prev_tab.disable()
    elif current_tab == 2 and not paused:
        button_prev_tab.show()
        button_prev_tab.enable()
        button_next_tab.hide()
        button_next_tab.disable()

    # Champion button gray-out
    for champion in champions:
        if champion.shown and gold >= champion.price_hire:
            champion.button_hire.enable()
        else:
            champion.button_hire.disable()

        if champion.isUnlocked and gold >= champion.price_level:
            champion.button_level.enable()
        else:
            champion.button_level.disable()

    # Upgrade button gray-out
    for upgrade in list_upgrades:
        if upgrade not in list_available:
            if upgrade not in list_bought: # God I feel like a genius figuring this out after 3 #$*&ing days
                if upgrade.shown:
                    list_available.append(upgrade)
                    upgrade.available()

        
        if upgrade.origin.level >= upgrade.requirement:
            upgrade.shown = True


    
    click_power_display()
    idle_power_display()
    gold_display(gold)
    
    if main_menu_status == True:
        init_main_menu()


    window.update(time_delta)
    window.draw_ui(screen)
    pygame.display.update
    pygame.display.flip()

pygame.quit()
sys.exit()
