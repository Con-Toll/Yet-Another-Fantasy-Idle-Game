import pygame
import pygame_gui
import sys
from pygame_gui.core import ObjectID
import math
import time
import threading
import json
import os
import Class_file
import random
import Spinning_Wheel






pygame.init()


# -- VARIABLES --
# Screen info
screen_width = 960
screen_height = 540
screen = pygame.display.set_mode((screen_width, screen_height))

window = pygame_gui.UIManager((screen_width, screen_height),theme_path='assets/theme.json')

pygame.display.set_caption("Yet Another Idle Clicker")


# Main Menu
#main_menu = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -2), (screen_width+4, screen_height+4)),
 #                                             manager=window)
#main_menu_status = True

#button_game_start = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (150, 50)),
 #                                                text="Start",
  #                                               container=main_menu,
   #                                              anchors={'center': 'center'})



#background image 
background = pygame.image.load("assets/background.png")
backgroundwidth = screen_width
backgroundheight = 0
generatable_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (screen_width, screen_height)),
                                              visible=0, 
                                              manager=window)


scroll = 0
sections = math.ceil(screen_width / backgroundwidth)
print(sections)
start_game = False

# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("assets/Chava-Regular.ttf", 26)
window.add_font_paths("canva", "assets/Chava-Regular.ttf")
window.preload_fonts([{'name': 'canva', 'point-size': 14, 'style': 'regular'}])

# Game Variables
paused = False
base_click_power = 100000 # Change this number for testing :3
money = 0
prestige_2a_status = 1

# Info bar container
container_info_bars = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2,-2), (screen_width+4, 102)))

# Main tab button
area_tabs = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-3, screen_height-31), (969, screen_height/3*2)))
button_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (966, 30)), 
                                          text="^",
                                          container=area_tabs)
# False = Closed, True = Open
area_tabs_status = False

def tab_openclose():
    global backgroundheight, area_tabs_status
    if area_tabs_status:
        area_tabs.set_relative_position((-3, screen_height-31))
        generatable_area.set_relative_position((0, 0-31))
        area_tabs_status = False
        backgroundheight = 0
        button_tab.set_text("^")
        return area_tabs_status

    if not area_tabs_status:
        area_tabs.set_relative_position((-3, screen_height/2.5))
        generatable_area.set_relative_position((0, 0-324))
        area_tabs_status = True
        backgroundheight = (0-screen_height/2.9)
        button_tab.set_text("v")
        return area_tabs_status

# debug button
#button_test = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((400, 400), (150, 75)), 
 #                                         text="",
  #                                        container=None)

# Champion Area
container_champ = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((5, 90), (440, 230)),
                                                                container=area_tabs,
                                                                allow_scroll_x=False)
# Header that says "CHAMPIONS"
area_tab_champ = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((7, 32), (438, 56)),
                                          container=area_tabs)
text_tab_champ = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 2), (436, 52)),
                                               text="\"Champions\"",
                                               object_id=ObjectID(class_id="@text_tabs"),
                                               container=area_tab_champ)

# Upgrade Area
container_upgrade = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((450, 90), (440, 130)),
                                                                  container=area_tabs,
                                                                  allow_scroll_x=False)
# Header that says "UPGRADES"
area_tab_upgrade = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((450, 32), (440, 56)),
                                          container=area_tabs)
text_tab_upgrade = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 2), (283, 52)),
                                               text="Upgrades",
                                               object_id=ObjectID(class_id="@text_tabs"),
                                               container=area_tab_upgrade)



# Containers for available and bought upgrades
area_upgrade_available = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (422, 500)),
                                                     container=container_upgrade)
area_upgrade_bought = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,504), (422, 500)),
                                                  container=container_upgrade)



# "Available" and "Bought" text
text_available = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,30)),
                                             text="Available:",
                                             container=area_upgrade_available,
                                            )

text_bought = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,30)),
                                          text="Bought:",
                                          container=area_upgrade_bought,
                                         )

# Upgrade tooltip
tooltip_upgrade = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((448, 218), (444, 100)),
                                                html_text="",
                                                container=area_tabs,
                                                object_id=ObjectID(class_id="@upgrade_tooltip"))

# Tab switch buttons
current_tab = 1
button_next_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((901, 40), (50, 275)),
                                              text=">",
                                              container=area_tabs)
button_prev_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((14, 40), (50, 275)),
                                              text="<",
                                              container=area_tabs)

# Tab 2
area_tab2 = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((70, 32), (890, 288)),
                                        container=area_tabs)
button_prestige = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((345, 92), (200, 60)),
                                                text="IT'S TIME",
                                                container=area_tab2)
text_tab2 = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5, 5), (880, 52)),
                                               text="SEMESTER BREAK",
                                               object_id=ObjectID(class_id="@text_tabs"),
                                               container=area_tab2)



# Prestige waoooo
area_prestige = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-2, -2), (964, 544)))
bg_prestige_load = pygame.image.load("assets/prestige_bg.png")
bg_prestige = pygame_gui.elements.UIImage(relative_rect=((0,0), (screen_width, screen_height)),
                                          image_surface=bg_prestige_load,
                                          container=area_prestige,
                                          starting_height=0
                                         )
area_prestige.disable()
area_prestige.hide()
text_prestige = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((220, 0), (screen_width-440, 80)),
                                            text="Sembreak Start !!",
                                            container=area_prestige,
                                            object_id=ObjectID(class_id="@text_prestige"))
#button_prestige_respec = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 11), (200, 60)),
 #                                                     text="RESPEC",
  #                                                    container=area_prestige)
button_prestige_continue = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 11), (200, 60)),
                                                        text="Back to\n campus\n ",
                                                        container=area_prestige,
                                                        object_id=ObjectID(class_id="@prestige_continue"))

class UILabel:
    def __init__(self, text, position, font_size):
        self.text = text
        self.position = position
        self.font_size = font_size

    def to_dict(self):
        return {
            "text": self.text,
            "position": self.position,
            "font_size": self.font_size
        }

# Champions
class Champion():
    def __init__(self, index, name, title, base_idle_power, forHire, price_hire, base_price_level, image="assets/images.png"):
        self.name = name
        self.title = title
        self.level = 0
        self.base_idle_power = base_idle_power
        self.idle_power = 0
        self.isUnlocked = False
        self.forHire = forHire
        self.index = index
        self.image = image
        self.price_hire = price_hire
        self.base_price_level = base_price_level
        self.price_level = self.base_price_level
        self.up_mult = 0
        self.pres_mult = 0

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
        self.image_idle_load = pygame.image.load("assets/champ_idle.png")
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

    def to_dict(self):
        return {
            "level": self.level,
            "idle_power": self.idle_power,
            "isUnlocked": self.isUnlocked,
            "forHire": self.forHire,
            "price_hire": self.price_hire,
            "price_level": self.price_level,
            "up_mult": self.up_mult,
            "pres_mult": self.pres_mult
        }

    @classmethod
    def from_dict(cls, data):
        champ = cls(
            forHire=data["forHire"],
            price_hire=data["price_hire"],
            price_level=data["price_level"]
        )
        champ.level = data["level"]
        champ.idle_power = data["idle_power"]
        champ.isUnlocked = data["isUnlocked"]
        champ.up_mult = data["up_mult"]
        champ.pres_mult = data["pres_mult"]
        return champ
    
    # Hire Champion Function
    def hire(self):
        global money

        # Deduct money
        money = money - self.price_hire
        # Update champion variables and total champion
        self.level = 1
        self.isUnlocked = True
        bought_champs.append(self)

        if self.pres_mult != 0:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult * self.pres_mult
            else:
                self.idle_power = self.base_idle_power * self.level * self.pres_mult
        else:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult
            else:
                self.idle_power = self.base_idle_power * self.level
                
        if self.isUnlocked == True:
            self.button_level.show()
            self.price_level_display.show()
            self.price_level_display.enable()
            self.button_hire.hide()
            self.price_hire_display.hide()
            self.price_hire_display.disable()

        # Show next champion
        index = champions.index(self)
        if index < len(champions) - 1:
            next_champion = champions[index + 1]
            next_champion.forHire = True
            next_champion.showChamp()
            
        return self.level, self.idle_power
        

    # Level Up Function
    def level_up(self):
        global money, click_power
        money = money - self.price_level
        self.level += 1
        self.price_level = math.floor((5 + self.base_price_level) * (1.07 ** (self.level-1)))
        click_power = base_click_power + (math.floor(hero.idle_power * hero_up_status)) * prestige_2a_status

        if self.pres_mult != 0:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult * self.pres_mult
            else:
                self.idle_power = self.base_idle_power * self.level * self.pres_mult
        else:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult
            else:
                self.idle_power = self.base_idle_power * self.level
        return self.idle_power

        return self.price_level, self.level, self.idle_power


    # Enable/Disable champion container
    def showChamp(self):
        if self.forHire == False:
            self.container.hide()
            self.container.disable()
            self.button_hire.hide()
            self.button_hire.disable()

        if self.isUnlocked == False and self.forHire == True:
                self.container.show()
                self.container.enable()
                self.button_hire.show()
                self.price_hire_display.show()
                self.price_hire_display.enable()
                self.button_level.hide()
                self.price_level_display.hide()
                self.price_level_display.disable()

    def load_save(self):
        if self.isUnlocked:
            self.container.show()
            self.container.enable()
            self.button_level.show()
            self.price_level_display.show()
            self.price_level_display.enable()
            self.button_hire.hide()
            self.price_hire_display.hide()
            self.price_hire_display.disable()

    # Champ upgrades
    def upgrade1(self):
        self.up_mult += 2

        if self.pres_mult != 0:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult * self.pres_mult
            else:
                self.idle_power = self.base_idle_power * self.level * self.pres_mult
        else:
            if self.up_mult != 0:
                self.idle_power = self.base_idle_power * self.level * self.up_mult
            else:
                self.idle_power = self.base_idle_power * self.level
        return self.idle_power
    
    def upgrade2(self):
        self.pres_mult = 2

        self.idle_power = self.base_idle_power * self.level
        if self.up_mult != 0:
            self.idle_power *= self.up_mult
        if self.pres_mult != 0:
            self.idle_power *= self.pres_mult
        return self.idle_power, self.pres_mult



# Champions List 
# (index, name, title, base_idle_power, forHire, price_hire, price_level, image)
hero = Champion(0, "hero", "The Protagonist", 1, True, 15, 20, "assets/champs/hero.PNG")
reliable = Champion(1, "reliable", "The Reliable", 10, False, 200, 220, "assets/champs/reli.PNG")
incon = Champion(2, "incon", "The Inconsistent", 200, False, 2500, 2750, "assets/champs/incon.PNG")
leader = Champion(3, "leader", "The Group Leader", 500, False, 7500, 8000, "assets/champs/lead.PNG")
perfect = Champion(4, "perfect", "The Perfectionist", 1000, False, 30000, 32000, "assets/champs/perf.PNG")
president = Champion(5, "president", "The Club President", 1625, False, 80000, 84000, "assets/champs/pres.PNG")
lect = Champion(6, "lect", "The Lecturer", 3325, False, 140000, 150000, "assets/champs/lect.PNG")
gpt = Champion(7, "gpt", "ChatGGEZ", 10000, False, 500000, 550000, "assets/champs/gpt.PNG")

champions = [hero, reliable, incon, leader, perfect, president, lect, gpt]
bought_champs = []
total_champion = len(bought_champs)
hero_up_status = 0
click_power = base_click_power + (math.floor(hero.idle_power * hero_up_status)) * prestige_2a_status
# Champion initialization
for champion in champions:
    champion.showChamp()



# Upgrades
class Upgrade():
    def __init__(self, num_id, requirement, price, name, origin, tooltip, mult, action=None):
        self.x = 10
        self.y = 40
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
        self.object_id = f"@upgrade_{self.num_id}"

        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (45, 45)),
                                                   text="",
                                                   container=area_upgrade_available,
                                                   manager=window,
                                                   object_id=ObjectID(class_id=self.object_id))
    
        


    def available(self):
        if self.shown:
            self.button.enable()
            self.button.show()
        else:
            self.button.disable()
            self.button.hide()


        if not self.isUnlocked and self.shown:
            self.button.set_container(container=area_upgrade_available)
            index = list_available.index(self)
            #the container is (422, 315)
            self.x = 10 + ((index % 8) * 49) + ((index % 8) * 2)
            self.y = 40 + ((index // 8) * 51)
            print(index, self.x, self.y)

            # note for future improvement:
            # for index % 8 = 0, modifier = index, self.x = 10 + 

        self.button.set_relative_position((self.x, self.y))

        #print(self.num_id, self.x)

    # Purchase upgrades
    def purchase(self):
        global money
        money = money - self.price
        self.isUnlocked = True
        
        self.button.set_container(container=area_upgrade_bought)
        self.action()

        print("bought")


    def sort(self):
        if self.shown:
            self.button.enable()
            self.button.show()
        else:
            self.button.disable()
            self.button.hide()

        if self.isUnlocked == True:
            self.button.set_container(container=area_upgrade_bought)
            index = list_bought.index(self)
            self.x = 10 + ((index % 8) * 49) + ((index % 8) * 2)
            self.y = 40 + ((index // 8) * 51)
            self.button.set_relative_position((self.x, self.y))

    def to_dict(self):
            return {
                "shown": self.shown,
                "isUnlocked": self.isUnlocked
            }

    @classmethod
    def from_dict(cls, data):
        upgrade = cls(
        )
        upgrade.shown = data["shown"]
        upgrade.isUnlocked = data["isUnlocked"]
        return upgrade


# Upgrades
# num_id, requirement, price, name, origin, tooltip, mult, action
def set_clickpower_status():
    global hero_up_status, click_power
    hero_up_status = 1
    click_power = base_click_power + (math.floor(hero.idle_power * hero_up_status)) * prestige_2a_status
    hero.upgrade1()

# Hero
up_hero1 = Upgrade(1, 5, 100, "Freshman", hero, "Protagonist's Idle Power is added to Click Power. (Also 2x Protag's Idle Power)", 2, action=(set_clickpower_status))
up_hero2 = Upgrade(2, 25, 1000, "Sophomore", hero, "Doubles the Idle Power of the Protagonist", 2, action=(hero.upgrade1))
up_hero3 = Upgrade(3, 50, 5000, "Junior", hero, "Doubles the Idle Power of the Protagonist", 2, action=(hero.upgrade1))
up_hero4 = Upgrade(4, 75, 7500, "Senior", hero, "Doubles the Idle Power of the Protagonist", 2, action=(hero.upgrade1))
up_hero5 = Upgrade(5, 100, 10000, "Graduate", hero, "Doubles the Idle Power of the Protagonist", 2, action=(hero.upgrade1))

# reliable
up_reliable1 = Upgrade(6, 10, 2000, "reliable 1", reliable, "Doubles the Idle Power of the Reliable", 2, action=(reliable.upgrade1))
up_reliable2 = Upgrade(7, 25, 5500, "reliable 2", reliable, "Doubles the Idle Power of the Reliable", 2, action=(reliable.upgrade1))
up_reliable3 = Upgrade(8, 50, 42500, "reliable 3", reliable, "Doubles the Idle Power of the Reliable", 2, action=(reliable.upgrade1))
up_reliable4 = Upgrade(9, 75, 124320, "reliable 4", reliable, "Doubles the Idle Power of the Reliable", 2, action=(reliable.upgrade1))
up_reliable5 = Upgrade(10, 100, 342700, "reliable 5", reliable, "Doubles the Idle Power of the Reliable", 2, action=(reliable.upgrade1))

# incon
up_incon1 = Upgrade(11, 10, 30000, "incon 1", incon, "Doubles the Idle Power of the Inconsistent", 2, action=(incon.upgrade1))
up_incon2 = Upgrade(12, 25, 70000, "incon 2", incon, "Doubles the Idle Power of the Inconsistent", 2, action=(incon.upgrade1))
up_incon3 = Upgrade(13, 50, 200000, "incon 3", incon, "Doubles the Idle Power of the Inconsistent", 2, action=(incon.upgrade1))
up_incon4 = Upgrade(14, 75, 500000, "incon 4", incon, "Doubles the Idle Power of the Inconsistent", 2, action=(incon.upgrade1))
up_incon5 = Upgrade(15, 100, 1000000, "incon 5", incon, "Doubles the Idle Power of the Inconsistent", 2, action=(incon.upgrade1))

# leader
up_leader1 = Upgrade(16, 10, 100000, "leader 1", leader, "Doubles the Idle Power of the Group Leader", 2, action=(leader.upgrade1))
up_leader2 = Upgrade(17, 25, 155620, "leader 2", leader, "Doubles the Idle Power of the Group Leader", 2, action=(leader.upgrade1))
up_leader3 = Upgrade(18, 50, 432000, "leader 3", leader, "Doubles the Idle Power of the Group Leader", 2, action=(leader.upgrade1))
up_leader4 = Upgrade(19, 75, 1234560, "leader 4", leader, "Doubles the Idle Power of the Group Leader", 2, action=(leader.upgrade1))
up_leader5 = Upgrade(20, 100, 3451930, "leader 5", leader, "Doubles the Idle Power of the Group Leader", 2, action=(leader.upgrade1))

# perfect
up_perfect1 = Upgrade(21, 10, 333333, "perfect 1", perfect, "Doubles the Idle Power of the Perfectionist", 2, action=(perfect.upgrade1))
up_perfect2 = Upgrade(22, 25, 888888, "perfect 2", perfect, "Doubles the Idle Power of the Perfectionist", 2, action=(perfect.upgrade1))
up_perfect3 = Upgrade(23, 50, 12341234, "perfect 3", perfect, "Doubles the Idle Power of the Perfectionist", 2, action=(perfect.upgrade1))
up_perfect4 = Upgrade(24, 75, 53355335, "perfect 4", perfect, "Doubles the Idle Power of the Perfectionist", 2, action=(perfect.upgrade1))
up_perfect5 = Upgrade(25, 100, 99999999, "perfect 5", perfect, "Doubles the Idle Power of the Perfectionist", 2, action=(perfect.upgrade1))

# Champ 6
up_president_1 = Upgrade(26, 10, 1333337, "president 1", president, "Doubles the Idle Power of the Club President", 2, action=(president.upgrade1))
up_president_2 = Upgrade(27, 25, 8008135, "president 2", president, "Doubles the Idle Power of the Club President", 2, action=(president.upgrade1))
up_president_3 = Upgrade(28, 50, 42069420, "president 3", president, "Doubles the Idle Power of the Club President", 2, action=(president.upgrade1))
up_president_4 = Upgrade(29, 75, 91234801, "president 4", president, "Doubles the Idle Power of the Club President", 2, action=(president.upgrade1))
up_president_5 = Upgrade(30, 100, 112344313, "president 5", president, "Doubles the Idle Power of the Club President", 2, action=(president.upgrade1))

# Champ 7
up_lect_1 = Upgrade(31, 10, 5000000, "lect 1", lect, "Doubles the Idle Power of the Lecturer", 2, action=(lect.upgrade1))
up_lect_2 = Upgrade(32, 25, 10000000, "lect 2", lect, "Doubles the Idle Power of the Lecturer", 2, action=(lect.upgrade1))
up_lect_3 = Upgrade(33, 50, 50000000, "lect 3", lect, "Doubles the Idle Power of the Lecturer", 2, action=(lect.upgrade1))
up_lect_4 = Upgrade(34, 75, 100000000, "lect 4", lect, "Doubles the Idle Power of the Lecturer", 2, action=(lect.upgrade1))
up_lect_5 = Upgrade(35, 100, 500000000, "lect 5", lect, "Doubles the Idle Power of the Lecturer", 2, action=(lect.upgrade1))

# Champ 8
up_gpt_1 = Upgrade(36, 10, 25000000, "Legally Distinct AI Model", gpt, "Doubles the Idle Power of ChatGGEZ", 2, action=(gpt.upgrade1))
up_gpt_2 = Upgrade(37, 25, 100000000, "As an AI language model,", gpt, "Doubles the Idle Power of ChatGGEZ", 2, action=(gpt.upgrade1))
up_gpt_3 = Upgrade(38, 50, 500000000, "Introducing GGEZ-4", gpt, "Doubles the Idle Power of ChatGGEZ", 2, action=(gpt.upgrade1))
up_gpt_4 = Upgrade(39, 75, 1000000000, "gpt 4", gpt, "Doubles the Idle Power of ChatGGEZ", 2, action=(gpt.upgrade1))
up_gpt_5 = Upgrade(40, 100, 10000000000, "gpt 5", gpt, "Doubles the Idle Power of ChatGGEZ", 2, action=(gpt.upgrade1))



list_upgrades = [
    up_hero1, up_hero2, up_hero3, up_hero4, up_hero5,
    up_reliable1, up_reliable2, up_reliable3, up_reliable4, up_reliable5,
    up_incon1, up_incon2, up_incon3, up_incon4, up_incon5,
    up_leader1, up_leader2, up_leader3, up_leader4, up_leader5,
    up_perfect1, up_perfect2, up_perfect3, up_perfect4, up_perfect5,
    up_president_1, up_president_2, up_president_3, up_president_4, up_president_5,
    up_lect_1, up_lect_2, up_lect_3, up_lect_4, up_lect_5,
    up_gpt_1, up_gpt_2, up_gpt_3, up_gpt_4, up_gpt_5
    ]
list_available = []
list_bought = []

for upgrade in list_upgrades:
    upgrade.button.disable()
    upgrade.button.hide()



class Prestige():
    def __init__(self, x, y, price, name, tooltip, mult, action=None):
        self.x = x
        self.y = y
        self.canBuy = False
        self.price = price
        self.name = name
        self.tooltip = tooltip
        self.mult = mult
        self.isUnlocked = False
        self.action = action
        self.not_chosen = False

        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (150, 75)),
                                                   text=f"{self.name}",
                                                   anchors={"center": "center"},
                                                   container=area_prestige,
                                                   object_id=ObjectID(class_id="@prestige_available"))
        
    def to_dict(self):
        return {
            "canBuy": self.canBuy,
            "isUnlocked": self.isUnlocked,
            "not_chosen": self.not_chosen
        }

    @classmethod
    def from_dict(cls, data):
        prestige = cls(
        )
        prestige.canBuy = data["canBuy"]
        prestige.isUnlocked = data["isUnlocked"]
        prestige.not_chosen = data["not_chosen"]
        return prestige
    
    def load_save(self):
        if self.isUnlocked:
            self.canBuy = False
            self.button.enable()
            self.button.change_object_id("@prestige_bought")

        if self.not_chosen:
            self.button.enable()
            self.button.change_object_id("@prestige_not_chosen")

        if self.canBuy:
            self.button.enable()
            self.button.change_object_id("@prestige_available")
    

def set_clickpower_status_but_prestige():
    global prestige_2a_status, click_power
    prestige_2a_status = 10
    click_power = base_click_power + (math.floor(hero.idle_power * hero_up_status)) * prestige_2a_status
    hero.upgrade1()
    print("worked")

def set_prestige2b():
    for champion in champions:
        champion.upgrade2()
    print("worked")

# x, y, price, name, tooltip, mult, action
# requirement is for prestige branches
prestige1 = Prestige(-380, -55, 0, "Foundation", "The start of your first year!", 0)
prestige2a = Prestige(-190, -115, 1, "Become FCM", "Live a life of never-ending deadlines. (This is the \"Active\" path, for art students can never catch a break.) \n( Click Power * 10)", 0, action=(set_clickpower_status_but_prestige))
prestige2b = Prestige(-190, 5, 1, "Turn to FCI", "Learn to make computers do your work for you! (This is the \"Passive\" path, 'cause screw manual labour!) \n(+100% Idle Power)", 0, action=(set_prestige2b))
prestige3 = Prestige(0, -55, 1, "Electives", "I wish electives weren't mandatory :(", 1)
prestige3a = Prestige(0, -140, 1, "Art Spec.", "Time for a specialization!", 1)
prestige3b = Prestige(0, 30, 1, "CS Spec.", "Time for a specialization!", 1)
prestige4a = Prestige(190, -115, 1, "Art Degree", "Take an Art Degree!", 1)
prestige4b = Prestige(190, 5, 1, "CS Degree", "Take a Comp. Science Degree!", 1)
prestige5 = Prestige(380, -55, 1, "Graduation", "Congratulations, it's finally over! (+The End)", 1)

list_prestige = [prestige1, prestige2a, prestige2b, prestige3, prestige3a, prestige3b, prestige4a, prestige4b, prestige5]

for upgrade in list_prestige:
    upgrade.button.disable()
    
prestige1.button.enable()
prestige1.canBuy = True

credits_total = 0
credits_onhand = 0
show_credits = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((480, 350), (480, 60)),
                                           text=f"Credits: {credits_onhand}/{credits_total}",
                                           container=area_prestige,
                                           object_id=ObjectID(class_id="@prestige_credits"))

clock = pygame.time.Clock()


# Prestige progress bar
class MyProgressBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, x, y, w, h, ui_container):
        super().__init__(relative_rect=pygame.Rect((x, y), (w, h)), container=ui_container)
        global money, credits_total
        self.current_progress = money
        self.maximum_progress = 1000000 + (1000000 * credits_total)

    def status_text(self):
        return f"{self.current_progress:,}/{self.maximum_progress:,}"
    
    def set_current_progress(self, progress: float):
        return super().set_current_progress(progress)
    
progress_prestige = MyProgressBar(5, 62, 875, 25, area_tab2)



total_idle_power = sum(champion.idle_power for champion in champions)

# Prestige Tooltips
prestige_show_price = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 350), (480, 60)),
                                              text="",
                                              container=area_prestige,
                                              object_id=ObjectID(class_id="@prestige_price"))
        
prestige_show_tooltip = pygame_gui.elements.UITextBox(relative_rect=pygame.Rect((0, 410), (960, 130)),
                                                html_text="",
                                                container=area_prestige,
                                                object_id=ObjectID(class_id="@prestige_tooltip"))

# Info bars
container_info_click = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((211, 4), (210, 49)),
                                                  container=container_info_bars)
icon_click_power_load = pygame.image.load("assets/click.png")
icon_click_power = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((1, 1), (46, 46)),
                                              image_surface=icon_click_power_load,
                                              container=container_info_click)
info_num_click = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((49, 1), (163, 47)),
                                             text=f"{click_power}",
                                             container=container_info_click)


container_info_idle = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((211, 51), (210, 49)),
                                                  container=container_info_bars)
icon_idle_power_load = pygame.image.load("assets/idle.png")
icon_idle_power = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((1, 1), (46, 46)),
                                              image_surface=icon_idle_power_load,
                                              container=container_info_idle)
info_num_idle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((49, 1), (163, 47)),
                                             text=f"{total_idle_power}",
                                             container=container_info_idle)


container_info_money = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((420, 4), (250, 96)),
                                                  container=container_info_bars)
info_text_money = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 2), (248, 47)),
                                             text="money",
                                             container=container_info_money)
info_num_money = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((2, 47), (248, 47)),
                                             text=f"{money}",
                                             container=container_info_money)

button_settings = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((860, 16), (70, 70)),
                                               text="",
                                               container=container_info_bars,
                                               object_id=ObjectID(class_id="@button_settings"))

# Format
def format_num(value):
    if abs(value) > 99999:
        return f"{value:.2e}"
    else:
        return f"{value:,}"

def format_money(value):
    if abs(value) > 999999999:
        return f"{value:.2e}"
    else:
        return f"{value:,}"

    # Main menu
#def init_main_menu():
 #   global paused
  #  area_tabs.hide()
   # area_tabs.disable()
#    button_prestige.hide()
 #   button_prestige.disable()
  #  main_menu.show()
   # main_menu.enable()
#    paused = True
 #   return paused
    
#def game_start():
#    global paused, main_menu_status
 #   area_tabs.show()
  #  area_tabs.enable()
   # button_prestige.show()
#    button_prestige.enable() 
 #   main_menu.hide()
  #  main_menu.disable()
   # main_menu_status = False
#    paused = False
 #   print("worked")
  #  return paused, main_menu_status

    # Idle generation

# Money generation
status_thread = False

def thread_start():
    global status_thread
    thread = threading.Thread(target=increment_money)
    thread.daemon = True
    thread.start()
    status_thread = True

def increment_money():
    while True:
        time.sleep(1)
        global money, total_idle_power
        money += total_idle_power

# GAME SAVES WAAAAAAAAA
def save_game_state():
    global money, click_power, total_idle_power, champions, list_upgrades, list_prestige, credits_total, credits_onhand, hero_up_status, prestige_2a_status
    game_state = {
        "click_power": click_power,
        "money": money,
        "total_idle_power": total_idle_power,
        "champions": [champion.to_dict() for champion in champions],
        "list_upgrades": [upgrade.to_dict() for upgrade in list_upgrades],
        "list_prestige": [prestige.to_dict() for prestige in list_prestige],
        "credits_total": credits_total,
        "credits_onhand": credits_onhand,
        "hero_up_status": hero_up_status,
        "prestige_2a_status": prestige_2a_status
    }
    with open('game_state.json', 'w') as file:
        json.dump(game_state, file)
    print("Game state saved.")

def load_game_state():
    global money, click_power, total_idle_power, champions, list_upgrades, list_prestige, credits_total, credits_onhand, hero_up_status, prestige_2a_status
    if os.path.exists('game_state.json'):
        try:
            with open('game_state.json', 'r') as file:
                game_state = json.load(file)
                money = game_state.get('money', 0)
                click_power = game_state.get('click_power', 1)
                credits_total = game_state.get("credits_total", 0)
                credits_onhand = game_state.get("credits_onhand", 0)
                hero_up_status = game_state.get("hero_up_status", 0)
                prestige_2a_status = game_state.get("prestige_2a_status", 1)

                champions_data = game_state["champions"]
                # Reinitialize champions based on saved data
                for i, champ_data in enumerate(champions_data):
                    champions[i].level = champ_data["level"]
                    champions[i].idle_power = champ_data["idle_power"]
                    champions[i].isUnlocked = champ_data["isUnlocked"]
                    champions[i].forHire = champ_data["forHire"]
                    champions[i].price_hire = champ_data["price_hire"]
                    champions[i].price_level = champ_data["price_level"]
                    champions[i].up_mult = champ_data["up_mult"]
                    champions[i].price_level_display.set_text(f"{champions[i].price_level}")
                    champions[i].price_hire_display.set_text(f"{champions[i].price_hire}")
                    if champions[i].isUnlocked:
                        champions[i].load_save()
                    if champions[i].forHire:
                        champions[i].showChamp()

                upgrade_data = game_state["list_upgrades"]
                for i, up_data in enumerate(upgrade_data):
                    list_upgrades[i].shown = up_data["shown"]
                    list_upgrades[i].isUnlocked = up_data["isUnlocked"]

                prestige_data = game_state["list_prestige"]
                for i, pres_data in enumerate(prestige_data):
                    list_prestige[i].canBuy = pres_data["canBuy"]
                    list_prestige[i].isUnlocked = pres_data["isUnlocked"]
                    list_prestige[i].not_chosen = pres_data["not_chosen"]
                    list_prestige[i].load_save()
                

                total_idle_power = sum(champion.idle_power for champion in champions)
        except json.JSONDecodeError:
            print("Error: The game state file contains invalid JSON. Initializing default game state.")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")

def reset_game_state():
    save_file_path = 'game_state.json'
    if os.path.exists(save_file_path):
        save_game_state()
        with open(save_file_path, 'w') as file:
            pass
        print("Game state file cleared.")
    else:
        print("No save file found to clear.")

# Load game state on startup
load_game_state()
thread_start()

QTE_Button = Class_file.moving_button()
QTE_Button.x = random.randint(1000,5000)
QTE_Button.y =screen_height//2

class Event_gui(pygame.sprite.Sprite):
    def __init__(self,pos,direc,name="none") -> None:
        super().__init__()
        self.name = name
        self.perk = money
        self.sprite = []
        self.sprite.append(pygame.image.load(f"assets\{direc}\pixil-frame-0.png"))
        self.sprite.append(pygame.image.load(f"assets\{direc}\pixil-frame-1.png"))
        self.is_animating = True
        self.current_sprite = 0
        self.image = self.sprite
        self.image = self.sprite[self.current_sprite]
        self.fade = False
        self.rect = self.image.get_rect()
        self.rect= [pos,pos]
        self.alpha = 255
        self.direc = direc
        self.access = False
        self.nice = False
    
    
    def key(self):
        if self.access == True:
            if event.type == pygame.KEYUP:
                if event.key == getattr(pygame,f"K_{self.direc}"):
                    self.fade=True
                    self.access = False
                    self.nice = True
                    
                            
    def update(self):
        if self.is_animating==True:
            self.current_sprite += 0.1
            if self.current_sprite >= len(self.sprite):
                self.current_sprite = 0
                
            self.image = self.sprite[int(self.current_sprite)]
            
            
    
    def fadeout(self):
            if self.fade == True:
                self.alpha=max(0,self.alpha-5)
                self.image.fill((255,255,255,self.alpha),special_flags=pygame.BLEND_RGBA_MULT)
                if self.alpha <= 0:
                    self.kill()
                    
                
moving_image = pygame.sprite.Group()

class QTE(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.reset = (0,0)
        self.position = {
            1: (150, 200),
            2: (350, 200),
            3: (550, 200),
            4: (750, 200)
        }
        self.different = ["UP","DOWN","LEFT","RIGHT"]
        self.Up = Event_gui(self.position[1], random.choice(self.different))#1
        self.Down = Event_gui(self.position[2], random.choice(self.different))#2
        self.Left = Event_gui(self.position[3], random.choice(self.different))#3
        self.Right = Event_gui(self.position[4],random.choice(self.different))
        self.current_key = 0
        self.prev_key = None
        self.exe =False
        self.randomise = False
      
        self.after = (0,0)
        
        
    def key(self):
        global money
        if self.exe == True:
            self.Up.access = True
            self.Up.key()
            if self.Up.nice == True:
                self.Down.key()
                self.Down.access = True
                if self.Down.nice == True:
                    self.Left.key() == True
                    self.Left.access = True
                    if self.Left.nice == True:
                        self.Right.key()
                        self.Right.access = True
                        if self.Right.nice == True:
                            self.exe = False
                            money+=10000 + (total_idle_power*60)
                            
                            
                            
    def reset(self):
            if self.Right.alpha == 0:
                self.Up = Event_gui(self.position[1], random.choice(self.different))#1
                self.Down = Event_gui(self.position[2], random.choice(self.different))#2
                self.Left = Event_gui(self.position[3], random.choice(self.different))#3
                self.Right = Event_gui(self.position[4], random.choice(self.different))
                self.key()
                self.update()

        
    def update(self):
        if self.exe == True:
            moving_image.add(self.Up)
            moving_image.add(self.Down)
            moving_image.add(self.Left)
            moving_image.add(self.Right)
          
            
            
        
        
    def fadeout(self):
        self.Up.fadeout()
        self.Down.fadeout()
        self.Left.fadeout()
        self.Right.fadeout()
        

def collect_bonus():
    global total_idle_power
    global click_power
    global gold
    with open("Bonus.txt","r") as f:
        spl = f.read()
        m = spl.replace('S','')
        bonus = m.split(" ")
        for i in range(0,len(bonus),2):
            time = int(bonus[i])
            idl = bonus[i+1]
            if idl == "IDLE":
                gold = gold+(total_idle_power * time)
            else:
                click_power = click_power + time
                    
    print(gold)    
    return gold
    


Test = QTE()



menu_settings = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0, 0), (500, 200)), 
                                            anchors={'center': 'center'},
                                            starting_height=10)

text_settings = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 0), (420, 80)),
                                            container=menu_settings,
                                            text="SETTINGS",
                                            object_id=ObjectID(class_id="@text_settings"))

text_saved = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((0, 80), (500, 50)),
                                            container=menu_settings,
                                            text="",
                                            object_id=ObjectID(class_id="@text_saved"))

button_settings_close = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((425, 15), (50, 50)),
                                                     container=menu_settings,
                                                     text="x")

button_save = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((25, 135), (200, 50)),
                                           container=menu_settings,
                                           text="Save Game")

button_reset = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((275, 135), (200, 50)),
                                           container=menu_settings,
                                           text="Reset Save",
                                           object_id=ObjectID(class_id="@button_reset"))

menu_settings.hide()
menu_settings.disable()



# Game loop \o/
running = True
while running:
    screen.fill(white)
    time_delta = clock.tick(60)/1000.0
    randomiser_x = random.randint(10000000,50000000)
    randomiser_y = random.randint(80,screen_height-50)
        
    for i in range(0, sections + 1):  
     screen.blit(background, (i * backgroundwidth + scroll, backgroundheight))
    
    
    #scrolling background
     scroll -= 1
    
    if abs(scroll) > backgroundwidth:
      scroll = 0


    # Event handling
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
            save_game_state()
            running = False

        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA I FINALLY FIXED THE TOOLTIP
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            for upgrade in list_upgrades:
                if event.ui_element == upgrade.button:
                    tooltip_upgrade.set_text(f"{upgrade.name} - Price: {upgrade.price}\n{upgrade.tooltip}")

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    prestige_show_price.set_text(f"Cost: {upgrade.price}")
                    prestige_show_tooltip.set_text(f"{upgrade.tooltip}")

        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            for upgrade in list_upgrades:
                if event.ui_element == upgrade.button:
                    tooltip_upgrade.set_text("")

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    prestige_show_price.set_text("")
                    prestige_show_tooltip.set_text("")

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:

            # The Prestige Button. yes. that one
            if event.ui_element == button_prestige:
                credits_total += 1
                credits_onhand += 1
                show_credits.set_text(f"Credits: {credits_onhand}/{credits_total}")
                progress_prestige.maximum_progress = 1000000 + (1000000 * credits_total)
                # Close everything in the main screen
                tab_openclose()
                if area_tabs_status == False:
                    button_tab.disable()
                    button_tab.hide()
                    current_tab = 1
                    paused = True
                    container_info_bars.hide()
                    container_info_bars.disable()
                    area_prestige.show()
                    #button_prestige_respec.enable()
                    button_prestige_continue.enable()

                # prestige title effect wahoo
                text_prestige.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

                for champion in champions:
                    champion.isUnlocked = False
                    champion.forHire = False
                    hero.forHire = True
                    champion.level = 0
                    champion.idle_power = 0
                    champion.up_mult = 1
                    champion.showChamp()
                    champion.price_hire_display.set_text(f"{champion.price_hire}")
                    champion.text_level.set_text(f"{champion.level}")
                    champion.text_idle.set_text(f"{champion.idle_power}/s")

                bought_champs.clear()
                print(bought_champs)

                for upgrade in list_upgrades:
                    upgrade.isUnlocked = False
                    upgrade.shown = False
                    list_available.clear()
                    list_bought.clear()
                    upgrade.available()
                    
                # reset all the things !
                money = 0
                hero_up_status = 0
                click_power = base_click_power + (math.floor(hero.idle_power * hero_up_status)) * prestige_2a_status
                total_idle_power = sum(champion.idle_power for champion in champions)
                

            elif event.ui_element == button_prestige_continue:
                paused = False
                button_tab.enable()
                button_tab.show()
                container_info_bars.show()
                container_info_bars.enable()
                area_prestige.hide()
                area_prestige.disable()

            elif event.ui_element == button_settings:
                paused = True
                menu_settings.show()
                menu_settings.enable()

            elif event.ui_element == button_settings_close:
                paused = False
                menu_settings.hide()
                menu_settings.disable()
                
                text_saved.set_text("")

            elif event.ui_element == button_save:
                save_game_state()
                text_saved.set_text("Game saved!")

            elif event.ui_element == button_reset:
                reset_game_state()
                running = False

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    if credits_onhand >= upgrade.price and upgrade.canBuy:
                        credits_onhand = credits_onhand - upgrade.price
                        upgrade.isUnlocked = True
                        print(f"{upgrade.name} bought")
                        show_credits.set_text(f"Credits: {credits_onhand}/{credits_total}")

                        if event.ui_element == prestige1.button:
                            if prestige1.canBuy:
                                prestige1.canBuy = False
                                prestige2a.button.enable()
                                prestige2b.button.enable()
                                prestige2a.canBuy = True
                                prestige2b.canBuy = True

                                prestige1.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige2a.button:
                            if prestige2a.canBuy:
                                prestige2a.action()
                                # upgrades of the same tier get disabled
                                prestige2a.canBuy = False
                                prestige2b.canBuy = False
                                prestige2b.not_chosen = True
                                # enable next tier upgrades
                                prestige3.button.enable()
                                prestige3a.button.enable()
                                prestige3b.button.enable()
                                # make them purchasable
                                prestige3.canBuy = True
                                prestige3a.canBuy = True
                                prestige3b.not_chosen = True
                                
                                prestige2b.button.change_object_id("@prestige_not_chosen")
                                prestige3b.button.change_object_id("@prestige_not_chosen")

                                prestige2a.button.change_object_id("@prestige_bought")
                    
                        elif event.ui_element == prestige2b.button:
                            if prestige2b.canBuy:
                                prestige2b.action()

                                prestige2a.canBuy = False
                                prestige2a.not_chosen = True
                                prestige2b.canBuy = False
                                prestige3.button.enable()
                                prestige3a.button.enable()
                                prestige3b.button.enable()
                                prestige3.canBuy = True
                                prestige3b.canBuy = True
                                prestige3a.not_chosen = True

                                prestige2a.button.change_object_id("@prestige_not_chosen")
                                prestige3a.button.change_object_id("@prestige_not_chosen")

                                prestige2b.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige3.button:
                            if prestige3.canBuy:
                                prestige3.canBuy = False

                                prestige3.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige3a.button:
                            if prestige3a.canBuy:
                                prestige3a.canBuy = False
                                prestige3b.canBuy = False
                                prestige3b.not_chosen = True
                                prestige4a.button.enable()
                                prestige4b.button.enable()
                                prestige4a.canBuy = True

                                prestige3b.button.change_object_id("@prestige_not_chosen")
                                prestige4b.button.change_object_id("@prestige_not_chosen")

                                prestige3a.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige3b.button:
                            if prestige3b.canBuy:
                                prestige3a.canBuy = False
                                prestige3a.not_chosen = True
                                prestige3b.canBuy = False
                                prestige4a.button.enable()
                                prestige4b.button.enable()
                                prestige4b.canBuy = True

                                prestige3a.button.change_object_id("@prestige_not_chosen")
                                prestige4a.button.change_object_id("@prestige_not_chosen")

                                prestige3b.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige4a.button:
                            if prestige4a.canBuy:
                                prestige4a.canBuy = False
                                prestige4b.canBuy = False
                                prestige4b.not_chosen = True
                                
                                prestige5.button.enable()
                                prestige5.canBuy = True

                                prestige4b.button.change_object_id("@prestige_not_chosen")

                                prestige4a.button.change_object_id("@prestige_bought")
                    
                        elif event.ui_element == prestige4b.button:
                            if prestige4b.canBuy:
                                prestige4a.canBuy = False
                                prestige4a.not_chosen = True
                                prestige4b.canBuy = False

                                prestige5.button.enable()
                                prestige5.canBuy = True

                                prestige4a.button.change_object_id("@prestige_not_chosen")

                                prestige4b.button.change_object_id("@prestige_bought")
                        
                        elif event.ui_element == prestige5.button:
                            if prestige5.canBuy:
                                prestige5.canBuy = False

                                prestige5.button.change_object_id("@prestige_bought")

                        


            if not paused:
                if event.ui_element == button_next_tab:
                    current_tab = 2

                elif event.ui_element == button_prev_tab:
                    current_tab = 1

                # Tab buttons
                elif event.ui_element == button_tab:
                    # if open, close tab
                    if area_tabs_status:
                        tab_openclose()
                    # if closed, open tab
                    elif not area_tabs_status:
                        tab_openclose()

                

                # Champion buttons
                for champion in champions:
                    # Level up button
                    if event.ui_element == champion.button_level:
                        if money >= champion.price_level and champion.isUnlocked:
                            champion.level_up()
                            total_idle_power = sum(champion.idle_power for champion in champions)


                    # Hire button
                    if champion.button_hire.is_enabled:
                        if event.ui_element == champion.button_hire:
                            if money >= champion.price_hire and not champion.isUnlocked:
                                champion.hire()
                                total_idle_power = sum(champion.idle_power for champion in champions)

                

                # Upgrade buttons
                for upgrade in list_available:
                    if event.ui_element == upgrade.button:
                        if money >= upgrade.price and not upgrade.isUnlocked and upgrade.shown:
                            # Buy upgrade
                            upgrade.purchase()
                            # Move bought upgrade from available to bought                     lists make me wanna commit a crime
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

        if not paused:
            if event.type == pygame.MOUSEBUTTONDOWN:
                        if event.button == 1:
                            mouse_pos = pygame.mouse.get_pos()
                            QTE_Button_Rect = QTE_Button.frames[QTE_Button.index].get_rect(topleft=(QTE_Button.x,QTE_Button.y))

                            if generatable_area.rect.collidepoint(mouse_pos):
                                money += click_power
                                        
                            if QTE_Button_Rect.collidepoint(mouse_pos):
                                QTE_Button.x = randomiser_x
                                Test.exe = True 
                                Test.reset()

        #    if event.ui_element == button_game_start:
         #       game_start()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                QTE_Button_Rect = QTE_Button.frames[QTE_Button.index].get_rect(topleft=(QTE_Button.x,QTE_Button.y))
                
                if not paused:
                    if generatable_area.rect.collidepoint(mouse_pos):
                        gold += click_power
                        
                    if QTE_Button_Rect.collidepoint(mouse_pos):
                        QTE_Button.x = randomiser_x
                        k = random.randint(1,2)
        
                        
                        if k == 1:
                            Test.exe = True 
                        else:
                            if Spinning_Wheel.run()== False:
                                collect_bonus()
        
        Test.key()               
        window.process_events(event)

   
            
    # Tab
    if current_tab == 1 and not paused:
        # enable tab 1 stuff
        button_next_tab.show()
        button_next_tab.enable()
        area_tab_champ.set_relative_position((7, 32))
        container_champ.set_relative_position((5, 90))
        area_tab_upgrade.set_relative_position((450, 32))
        container_upgrade.set_relative_position((450, 90))

        # disable tab 2 stuff
        button_prev_tab.hide()
        button_prev_tab.disable()
        area_tab2.hide()
        area_tab2.disable()

    elif current_tab == 2 and not paused:
        # enable tab 2 stuff
        button_prev_tab.show()
        button_prev_tab.enable()
        area_tab2.show()
        area_tab2.enable()

        # disable tab 1 stuff
        button_next_tab.hide()
        button_next_tab.disable()
        area_tab_champ.set_relative_position((1000, 1000))
        container_champ.set_relative_position((1000, 1000))
        area_tab_upgrade.set_relative_position((1000, 1000))
        container_upgrade.set_relative_position((1000, 1000))
        # i hate that this works LOL
        # its so botched but at least its technically fixed??


    # Champions
    for champion in champions:
        # Grey out button if unable to afford
        if champion.forHire and money >= champion.price_hire:
            champion.button_hire.enable()
        else:
            champion.button_hire.disable()

        if champion.isUnlocked and money >= champion.price_level:
            champion.button_level.enable()
        else:
            champion.button_level.disable()

        # Keep stats updated
        if champion.isUnlocked:
            champion.price_level_display.set_text(f"{champion.price_level}")
            champion.text_level.set_text(f"{champion.level}")
            champion.text_idle.set_text(f"{champion.idle_power}/s")


    # Upgrade button gray-out
    for upgrade in list_upgrades:
        if upgrade not in list_available and upgrade not in list_bought and upgrade.shown and upgrade.isUnlocked: # God I feel like a genius figuring this out after 3 #$*&ing days
            list_bought.append(upgrade)
            upgrade.sort()

        if upgrade not in list_available and upgrade not in list_bought and upgrade.shown and not upgrade.isUnlocked: # God I feel like a genius figuring this out after 3 #$*&ing days
            list_available.append(upgrade)
            upgrade.available()

        
        
        if upgrade.origin.level >= upgrade.requirement and not upgrade.shown:
            upgrade.shown = True


    # Prestige progress bar
    progress_prestige.set_current_progress(money)
    progress_prestige.percent_full = min(progress_prestige.current_progress/progress_prestige.maximum_progress, 1.0)

    if money >= progress_prestige.maximum_progress:
        button_prestige.enable()
    else:
        button_prestige.disable()

#    if main_menu_status == True:
#       init_main_menu()
   
    
    QTE_Button.move(random.randint(5,10))
    QTE_Button.check(randomiser_x,randomiser_y)
    screen.blit(QTE_Button.frames[QTE_Button.index], (QTE_Button.x, QTE_Button.y))
    QTE_Button.index = (QTE_Button.index + 1) % len(QTE_Button.frames)
    
    info_num_click.set_text(f"{format_num(click_power)}")
    info_num_idle.set_text(f"{format_num(total_idle_power)}")
    info_num_money.set_text(f"{format_money(money)}")

    
    
    
    Test.update()
    Test.fadeout()
    moving_image.draw(screen)
    moving_image.update()
    window.update(time_delta)
    window.draw_ui(screen)
    pygame.display.update()
    pygame.display.flip()

print(time_delta)
print(clock)
pygame.quit()
sys.exit()
