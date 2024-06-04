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


# Colours
white = (255, 255, 255)
black = (0, 0, 0)

font = pygame.font.Font("assets/Chava-Regular.ttf", 26)
window.add_font_paths("canva", "assets/Chava-Regular.ttf")
window.preload_fonts([{'name': 'canva', 'point-size': 14, 'style': 'regular'}])

# Game Variables
paused = False
click_power = 100000
money = 0

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
container_upgrade = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((450, 90), (440, 230)),
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
area_upgrade_available = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0), (422, 500)),
                                                     container=container_upgrade)
area_upgrade_bought = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,504), (422, 500)),
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

# the thing that makes prestige prestige-able
total_prestige_points = 0

class MyProgressBar(pygame_gui.elements.UIProgressBar):
    def __init__(self, x, y, w, h, ui_container):
        super().__init__(relative_rect=pygame.Rect((x, y), (w, h)), container=ui_container)
        global money, total_prestige_points
        self.current_progress = money
        self.maximum_progress = 1000000

    def status_text(self):
        return f"{self.current_progress:,}/{self.maximum_progress:,}"
    
    def set_current_progress(self, progress: float):
        return super().set_current_progress(progress)
    
progress_prestige = MyProgressBar(5, 62, 875, 25, area_tab2)


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
button_prestige_respec = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((10, 11), (200, 60)),
                                                      text="RESPEC",
                                                      container=area_prestige)
button_prestige_continue = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((750, 11), (200, 60)),
                                                        text="Back to\n campus\n ",
                                                        container=area_prestige,
                                                        object_id=ObjectID(class_id="@prestige_continue"))


# Champions
class Champion():
    def __init__(self, index, name, title, base_idle_power, forHire, price_hire, price_level, image="assets/images.png"):
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
        global money

        # Deduct money
        money = money - self.price_hire
        # Update champion variables and total champion
        self.level = 1
        self.isUnlocked = True
        bought_champs.append(self)
        self.idle_power = self.base_idle_power * self.level * self.up_mult
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
            

        return self.idle_power
        

    # Level Up Function
    def level_up(self):
        global money
        money = money - self.price_level
        self.level += 1
        self.price_level *= 2
        
        self.idle_power = self.base_idle_power * self.level * self.up_mult
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

    # Champ upgrades
    def upgrade1(self, mult):
        self.up_mult = self.up_mult * mult
        self.idle_power = self.base_idle_power * self.level * self.up_mult
        return self.idle_power



# Champions List 
# (index, name, title, base_idle_power, forHire, price_hire, price_level, image)
hero = Champion(0, "hero", "The Protagonist", 1, True, 15, 20, "assets/images.png")
reliable = Champion(1, "reliable", "The Reliable", 10, False, 1000, 1200, "assets/images.png")
incon = Champion(2, "incon", "The Inconsistent", 100, False, 2500, 3000, "assets/images.png")
leader = Champion(3, "leader", "The Group Leader", 1000, False, 5000, 6000, "assets/images.png")
perfect = Champion(4, "perfect", "The Perfectionist", 10000, False, 10000, 10000, "assets/images.png")
president = Champion(5, "president", "The Club President", 10000, False, 10000, 10000, "assets/images.png")
lect = Champion(6, "lect", "The Lecturer", 10000, False, 10000, 10000, "assets/images.png")
gpt = Champion(7, "gpt", "ChatGGEZ", 10000, False, 10000, 10000, "assets/images.png")

champions = [hero, reliable, incon, leader, perfect, president, lect, gpt]
bought_champs = []
total_champion = len(bought_champs)

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
                                                   container=area_upgrade_available,
                                                   manager=window)
    
        self.button_tooltip = None

    def create_tooltip(self):
        self.button_tooltip = pygame_gui.elements.UITooltip(html_text="<font face=canva>"
                                                            f"{self.name}\n{self.tooltip}\nPrice: {self.price}"
                                                            "</font>",
                                                            hover_distance=(0, 0),
                                                            manager=window)
        return self.button_tooltip


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
            if index >= 64:
                self.x = 10 + ((index-64) * 49) + ((index-64) * 2)
                self.y = 60 + (8 * 51)
            elif index >= 56:
                self.x = 10 + ((index-56) * 49) + ((index-56) * 2)
                self.y = 60 + (7 * 51)
            elif index >= 48:
                self.x = 10 + ((index-48) * 49) + ((index-48) * 2)
                self.y = 60 + (6 * 51)
            elif index >= 40:
                self.x = 10 + ((index-40) * 49) + ((index-40) * 2)
                self.y = 60 + (5 * 51)
            elif index >= 32:
                self.x = 10 + ((index-32) * 49) + ((index-32) * 2)
                self.y = 60 + (4 * 51)
            elif index >= 24:
                self.x = 10 + ((index-24) * 49) + ((index-24) * 2)
                self.y = 60 + (3 * 51)
            elif index >= 16:
                self.x = 10 + ((index-16) * 49) + ((index-16) * 2)
                self.y = 60 + (2 * 51)
            elif index >= 8:
                self.x = 10 + ((index-8) * 49) + ((index-8) * 2)
                self.y = 60 + (1 * 51)
            elif index >= 0:
                self.x = 10 + (index * 49) + (index * 2)
                self.y = 60
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
        self.action(self.mult)

        print("bought")


    def sort(self):
        if self.isUnlocked == True:
            index = list_bought.index(self)
            
            if index >= 64:
                self.x = 10 + ((index-64) * 49) + ((index-64) * 2)
                self.y = 60 + (8 * 51)
            elif index >= 56:
                self.x = 10 + ((index-56) * 49) + ((index-56) * 2)
                self.y = 60 + (7 * 51)
            elif index >= 48:
                self.x = 10 + ((index-48) * 49) + ((index-48) * 2)
                self.y = 60 + (6 * 51)
            elif index >= 40:
                self.x = 10 + ((index-40) * 49) + ((index-40) * 2)
                self.y = 60 + (5 * 51)
            elif index >= 32:
                self.x = 10 + ((index-32) * 49) + ((index-32) * 2)
                self.y = 60 + (4 * 51)
            elif index >= 24:
                self.x = 10 + ((index-24) * 49) + ((index-24) * 2)
                self.y = 60 + (3 * 51)
            elif index >= 16:
                self.x = 10 + ((index-16) * 49) + ((index-16) * 2)
                self.y = 60 + (2 * 51)
            elif index >= 8:
                self.x = 10 + ((index-8) * 49) + ((index-8) * 2)
                self.y = 60 + (1 * 51)
            elif index >= 0:
                self.x = 10 + (index * 49) + (index * 2)
                self.y = 60

            self.button.set_relative_position((self.x, self.y))


# Upgrades
# num_id, requirement, price, name, origin, tooltip, mult, action

# Hero
up_hero1 = Upgrade(1, 2, 100000, "Freshman", hero, "This is hero upgrade 1", 2, action=(hero.upgrade1))
up_hero2 = Upgrade(2, 3, 100000, "Sophomore", hero, "This is hero upgrade 2", 2, action=(hero.upgrade1))
up_hero3 = Upgrade(3, 4, 100000, "Junior", hero, "This is hero upgrade 3", 2, action=(hero.upgrade1))
up_hero4 = Upgrade(4, 5, 100000, "Senior", hero, "This is hero upgrade 4", 2, action=(hero.upgrade1))
up_hero5 = Upgrade(5, 6, 100000, "Graduate", hero, "This is hero upgrade 5", 2, action=(hero.upgrade1))

# reliable
up_reliable1 = Upgrade(6, 2, 100000, "reliable 1", reliable, "This is reliable upgrade 1", 2, action=(reliable.upgrade1))
up_reliable2 = Upgrade(7, 3, 100000, "reliable 2", reliable, "This is reliable upgrade 2", 2, action=(reliable.upgrade1))
up_reliable3 = Upgrade(8, 4, 100000, "reliable 3", reliable, "This is reliable upgrade 3", 2, action=(reliable.upgrade1))
up_reliable4 = Upgrade(9, 5, 100000, "reliable 4", reliable, "This is reliable upgrade 4", 2, action=(reliable.upgrade1))
up_reliable5 = Upgrade(10, 6, 100000, "reliable 5", reliable, "This is reliable upgrade 5", 2, action=(reliable.upgrade1))

# incon
up_incon1 = Upgrade(11, 2, 100000, "incon 1", incon, "This is incon upgrade 1", 2, action=(incon.upgrade1))
up_incon2 = Upgrade(12, 3, 100000, "incon 2", incon, "This is incon upgrade 2", 2, action=(incon.upgrade1))
up_incon3 = Upgrade(13, 4, 100000, "incon 3", incon, "This is incon upgrade 3", 2, action=(incon.upgrade1))
up_incon4 = Upgrade(14, 5, 100000, "incon 4", incon, "This is incon upgrade 4", 2, action=(incon.upgrade1))
up_incon5 = Upgrade(15, 6, 100000, "incon 5", incon, "This is incon upgrade 5", 2, action=(incon.upgrade1))

# leader
up_leader1 = Upgrade(16, 2, 100000, "leader 1", leader, "This is leader upgrade 1", 2, action=(leader.upgrade1))
up_leader2 = Upgrade(17, 3, 100000, "leader 2", leader, "This is leader upgrade 2", 2, action=(leader.upgrade1))
up_leader3 = Upgrade(18, 4, 100000, "leader 3", leader, "This is leader upgrade 3", 2, action=(leader.upgrade1))
up_leader4 = Upgrade(19, 5, 100000, "leader 4", leader, "This is leader upgrade 4", 2, action=(leader.upgrade1))
up_leader5 = Upgrade(20, 6, 100000, "leader 5", leader, "This is leader upgrade 5", 2, action=(leader.upgrade1))

# perfect
up_perfect1 = Upgrade(26, 2, 100000, "perfect 1", perfect, "This is perfect upgrade 1", 2, action=(perfect.upgrade1))
up_perfect2 = Upgrade(27, 3, 100000, "perfect 2", perfect, "This is perfect upgrade 2", 2, action=(perfect.upgrade1))
up_perfect3 = Upgrade(28, 4, 100000, "perfect 3", perfect, "This is perfect upgrade 3", 2, action=(perfect.upgrade1))
up_perfect4 = Upgrade(29, 5, 100000, "perfect 4", perfect, "This is perfect upgrade 4", 2, action=(perfect.upgrade1))
up_perfect5 = Upgrade(30, 6, 100000, "perfect 5", perfect, "This is perfect upgrade 5", 2, action=(perfect.upgrade1))

# Champ 6
up_president_1 = Upgrade(6, 2, 100000, "president 1", president, "This is president upgrade 1", 2, action=(president.upgrade1))
up_president_2 = Upgrade(7, 3, 100000, "president 2", president, "This is president upgrade 2", 2, action=(president.upgrade1))
up_president_3 = Upgrade(8, 4, 100000, "president 3", president, "This is president upgrade 3", 2, action=(president.upgrade1))
up_president_4 = Upgrade(9, 5, 100000, "president 4", president, "This is president upgrade 4", 2, action=(president.upgrade1))
up_president_5 = Upgrade(10, 6, 100000, "president 5", president, "This is president upgrade 5", 2, action=(president.upgrade1))

# Champ 7
up_lect_1 = Upgrade(6, 2, 100000, "lect 1", lect, "This is lect upgrade 1", 2, action=(lect.upgrade1))
up_lect_2 = Upgrade(7, 3, 100000, "lect 2", lect, "This is lect upgrade 2", 2, action=(lect.upgrade1))
up_lect_3 = Upgrade(8, 4, 100000, "lect 3", lect, "This is lect upgrade 3", 2, action=(lect.upgrade1))
up_lect_4 = Upgrade(9, 5, 100000, "lect 4", lect, "This is lect upgrade 4", 2, action=(lect.upgrade1))
up_lect_5 = Upgrade(10, 6, 100000, "lect 5", lect, "This is lect upgrade 5", 2, action=(lect.upgrade1))

# Champ 8
up_gpt_1 = Upgrade(6, 2, 100000, "Legally Distinct AI Model", gpt, "Increases ChatGGEZ's idle power by 100%.", 2, action=(gpt.upgrade1))
up_gpt_2 = Upgrade(7, 3, 100000, "As an AI language model", gpt, "This is gpt upgrade 2", 2, action=(gpt.upgrade1))
up_gpt_3 = Upgrade(8, 4, 100000, "gpt 3", gpt, "This is gpt upgrade 3", 2, action=(gpt.upgrade1))
up_gpt_4 = Upgrade(9, 5, 100000, "gpt 4", gpt, "This is gpt upgrade 4", 2, action=(gpt.upgrade1))
up_gpt_5 = Upgrade(10, 6, 100000, "gpt 5", gpt, "This is gpt upgrade 5", 2, action=(gpt.upgrade1))



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

        self.button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((self.x, self.y), (150, 75)),
                                                   text=f"{self.name}",
                                                   anchors={"center": "center"},
                                                   container=area_prestige,
                                                   object_id=ObjectID(class_id="@prestige_available"))
    


# x, y, price, name, tooltip, mult, action
# requirement is for prestige branches
prestige1 = Prestige(-380, -55, 0, "Foundation", "The end of your first year!", 1)
prestige2a = Prestige(-190, -115, 0, "Become FCM", "Live a life of never-ending deadlines. (This is the \"Active\" path, for art students can never catch a break.) \n(+100% Click Power)", 1)
prestige2b = Prestige(-190, 5, 0, "Turn to FCI", "Learn to make computers do your work for you! (This is the \"Passive\" path, 'cause screw manual labour!) \n(+100% Idle Power)", 1)
prestige3 = Prestige(0, -55, 0, "Electives", "To hold my places, y'know. (+Takes up space)", 1)
prestige3a = Prestige(0, -140, 0, "Placeholder", "To hold my places, y'know. (+Takes up space)", 1)
prestige3b = Prestige(0, 30, 0, "Placeholder", "To hold my places, y'know. (+Takes up space)", 1)
prestige4a = Prestige(190, -115, 0, "Placeholder", "To hold my places, y'know. (+Takes up space)", 1)
prestige4b = Prestige(190, 5, 0, "Placeholder", "To hold my places, y'know. (+Takes up space)", 1)
prestige5 = Prestige(380, -55, 0, "Graduation", "Congratulations, it's finally over! (+The End)", 1)

list_prestige = [prestige1, prestige2a, prestige2b, prestige3, prestige3a, prestige3b, prestige4a, prestige4b, prestige5]

for upgrade in list_prestige:
    upgrade.button.disable()
    
prestige1.button.enable()
prestige1.canBuy = True

total_credits = 0
show_credits = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((480, 350), (480, 60)),
                                           text=f"Credits: {total_credits}",
                                           container=area_prestige,
                                           object_id=ObjectID(class_id="@prestige_credits"))

clock = pygame.time.Clock()


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
icon_click_power_load = pygame.image.load("assets/images.png")
icon_click_power = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((1, 1), (47, 47)),
                                              image_surface=icon_click_power_load,
                                              container=container_info_click)
info_num_click = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((49, 1), (163, 47)),
                                             text=f"{click_power}",
                                             container=container_info_click)


container_info_idle = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((211, 51), (210, 49)),
                                                  container=container_info_bars)
icon_idle_power_load = pygame.image.load("assets/images.png")
icon_idle_power = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((1, 1), (47, 47)),
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
                                               container=container_info_bars)

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

        # AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA I FINALLY FIXED THE TOOLTIP
        if event.type == pygame_gui.UI_BUTTON_ON_HOVERED:
            for upgrade in list_available:
                if event.ui_element == upgrade.button:
                    if upgrade.button_tooltip is None:
                        upgrade.button_tooltip = upgrade.create_tooltip()

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    prestige_show_price.set_text(f"Cost: {upgrade.price}")
                    prestige_show_tooltip.set_text(f"{upgrade.tooltip}")

        if event.type == pygame_gui.UI_BUTTON_ON_UNHOVERED:
            for upgrade in list_available:
                if event.ui_element == upgrade.button:
                    if upgrade.button_tooltip is not None:
                        upgrade.button_tooltip.kill()
                        upgrade.button_tooltip = None

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    prestige_show_price.set_text("")
                    prestige_show_tooltip.set_text("")

        elif event.type == pygame_gui.UI_BUTTON_PRESSED:

            # The Prestige Button. yes. that one
            if event.ui_element == button_prestige:
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
                    button_prestige_respec.enable()
                    button_prestige_continue.enable()

                # prestige title effect wahoo
                text_prestige.set_active_effect(pygame_gui.TEXT_EFFECT_TYPING_APPEAR)

                # reset all the things !
                money = 0
                #click_power = 1
                total_idle_power = sum(champion.idle_power for champion in champions)

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


            elif event.ui_element == button_prestige_continue:
                paused = False
                button_tab.enable()
                button_tab.show()
                container_info_bars.show()
                container_info_bars.enable()
                area_prestige.hide()
                area_prestige.disable()

            for upgrade in list_prestige:
                if event.ui_element == upgrade.button:
                    if total_credits >= upgrade.price and upgrade.canBuy:
                        total_credits = total_credits - upgrade.price
                        upgrade.isUnlocked = True
                        print(f"{upgrade.name} bought")

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
                                # upgrades of the same tier get disabled
                                prestige2a.canBuy = False
                                prestige2b.canBuy = False
                                # enable next tier upgrades
                                prestige3.button.enable()
                                prestige3a.button.enable()
                                prestige3b.button.enable()
                                # make them purchasable
                                prestige3.canBuy = True
                                prestige3a.canBuy = True
                                
                                prestige2b.button.change_object_id("@prestige_not_chosen")
                                prestige3b.button.change_object_id("@prestige_not_chosen")

                                prestige2a.button.change_object_id("@prestige_bought")
                    
                        elif event.ui_element == prestige2b.button:
                            if prestige2b.canBuy:
                                prestige2a.canBuy = False
                                prestige2b.canBuy = False
                                prestige3.button.enable()
                                prestige3a.button.enable()
                                prestige3b.button.enable()
                                prestige3.canBuy = True
                                prestige3b.canBuy = True

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
                                prestige4a.button.enable()
                                prestige4b.button.enable()
                                prestige4a.canBuy = True

                                prestige3b.button.change_object_id("@prestige_not_chosen")
                                prestige4b.button.change_object_id("@prestige_not_chosen")

                                prestige3a.button.change_object_id("@prestige_bought")

                        elif event.ui_element == prestige3b.button:
                            if prestige3b.canBuy:
                                prestige3a.canBuy = False
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
                                
                                prestige5.button.enable()
                                prestige5.canBuy = True

                                prestige4b.button.change_object_id("@prestige_not_chosen")

                                prestige4a.button.change_object_id("@prestige_bought")
                    
                        elif event.ui_element == prestige4b.button:
                            if prestige4b.canBuy:
                                prestige4a.canBuy = False
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




        #    if event.ui_element == button_game_start:
         #       game_start()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = pygame.mouse.get_pos()
                
                if not paused:
                    if generatable_area.rect.collidepoint(mouse_pos):
                        money += click_power

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
        if upgrade not in list_available and upgrade not in list_bought and upgrade.shown: # God I feel like a genius figuring this out after 3 #$*&ing days
            list_available.append(upgrade)
            upgrade.available()

        
        if upgrade.origin.level >= upgrade.requirement and not upgrade.shown:
            upgrade.shown = True


    for upgrade in list_available:
        if upgrade.button_tooltip is not None:
            mouse_pos = pygame.mouse.get_pos()
            adjusted_mouse_pos = (mouse_pos[0] - 75, mouse_pos[1] - 108)
            upgrade.button_tooltip.find_valid_position((adjusted_mouse_pos))


    # Prestige progress bar
    progress_prestige.set_current_progress(money)
    progress_prestige.percent_full = progress_prestige.current_progress/progress_prestige.maximum_progress*100

    if money >= progress_prestige.maximum_progress:
        button_prestige.enable()
    else:
        button_prestige.disable()

#    if main_menu_status == True:
 #       init_main_menu()

    info_num_click.set_text(f"{format_num(click_power)}")
    info_num_idle.set_text(f"{format_num(total_idle_power)}")
    info_num_money.set_text(f"{format_money(money)}")

    if not status_thread:
        thread_start()


    window.update(time_delta)
    window.draw_ui(screen)
    pygame.display.update()
    pygame.display.flip()

pygame.quit()
sys.exit()