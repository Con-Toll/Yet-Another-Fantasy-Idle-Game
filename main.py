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

#background image 
background = pygame.image.load("assets/background.png").convert()
backgroundwidth = background.get_width()
background_area = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0 , 0),(screen_width, screen_height)),
                                              visible=0, manager=window)

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
click_power = 100000

# Currency
gold = 0

# Champions
total_champion = 0


# Main tab button
area_tabs = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((-3, screen_height/2.5), (969, screen_height/3*2)))
button_tab = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((0, 0), (966, 30)), 
                                          text="",
                                          container=area_tabs)



#Container
container_champ = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((4, 30), (440, 290)),
                                                                container=area_tabs,
                                                                allow_scroll_x=False)
container_upgrade = pygame_gui.elements.UIScrollingContainer(relative_rect=pygame.Rect((445, 30), (440, 290)),
                                                                  container=area_tabs,
                                                                  allow_scroll_x=False)


#Upgrade Area
area_up_buyall = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,0),(422, 56)),
                                          container=container_upgrade)
area_upgrade_available = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,56),(422,400)),
                                                     container=container_upgrade)
area_upgrade_bought = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((0,456),(422,400)),
                                                  container=container_upgrade)


#Upgrade Button
button_up_buyall = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((5,2), (422, 56)),
                                             text="Buy All",
                                             container=area_up_buyall,
                                             )



#Upgrade "Available Text"
Available_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,50)),
                                             text="Available:",
                                             container=area_upgrade_available,
                                            )

Bought_text = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((5,5),(422,50)),
                                          text="Bought:",
                                          container=area_upgrade_bought,
                                         )


# Champions
class Champion():
    def __init__(self, name, title, level, base_idle_power, shown, position, price_hire, price_level, image="assets/images.png"):
        self.name = name
        self.title = title
        self.level = level
        self.base_idle_power = base_idle_power
        self.idle_power = 0
        self.isUnlocked = False
        self.shown = shown
        self.pos = position
        self.image = image
        self.price_hire = price_hire
        self.price_level = price_level
        self.up_mult = 1

        # Champion container
        self.container = pygame_gui.elements.UIPanel(relative_rect=pygame.Rect((2, self.pos),(420, 200)),
                                                     container=container_champ)

        # Champion info
        self.image_level_load = pygame.image.load("assets/images.png")
        self.image_level = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((108, 30), (35, 35)),
                                                       image_surface=self.image_level_load,
                                                       container=self.container)
        
        self.text_level = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((143, 30), (140, 35)),
                                                                     text=f"{self.level}",
                                                                     container=self.container,
                                                                     object_id=ObjectID(class_id="@champ_info"))


        self.image_idle_load = pygame.image.load("assets/images.png")
        self.image_idle = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((108, 65), (35, 35)),
                                                       image_surface=self.image_idle_load,
                                                       container=self.container)

        self.text_idle = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((143, 65), (140, 35)),
                                                                     text=f"{self.idle_power} /s",
                                                                     container=self.container,
                                                                     object_id=ObjectID(class_id="@champ_info"))

        # Champion image
        self.image_load = pygame.image.load(image)
        self.image = pygame_gui.elements.UIImage(relative_rect=pygame.Rect((5, 0), (80, 80)),
                                                 image_surface=self.image_load,
                                                 container=self.container)

        # Champion title
        self.title = pygame_gui.elements.UILabel(relative_rect=pygame.Rect((110, 5),(310, 25)),
                                                 text=f"{self.title}",
                                                 container=self.container,
                                                 object_id=ObjectID(class_id="@champ_title"))

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

    def upgrade1(self, mult):
        self.up_mult = self.up_mult * mult
        self.idle_power = self.base_idle_power * self.level * self.up_mult
        self.update_stats()
        return self.idle_power



# Champions List 
# (name, title, level, base_idle_power, shown, position, price_hire, price_level, image)
hero = Champion("hero", "You, the Hero", 0, 1, True, 0, 15, 20, "assets/images.png")
pyr = Champion("pyr", "Pyr, the Apprentice", 0, 10, False, 200, 1000, 1200, "assets/images.png")
avani = Champion("avani", "Avani, the Bright", 0, 100, False, 400, 2500, 3000, "assets/images.png")
obek = Champion("obek", "Obek, the Scavenger", 0, 1000, False, 600, 5000, 6000, "assets/images.png")
azura = Champion("azura", "Azura, the Something", 0, 10000, False, 800, 10000, 10000, "assets/images.png")

champions = [hero, pyr, avani, obek, azura]


# Champion initialization
for champion in champions:
    champion.showChamp()



# Upgrades
class Upgrade():
    def __init__(self, num_id, price, name, origin, tooltip, mult, action=None):
        self.x = 10
        self.y = 60
        self.num_id = num_id
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
                                                   container=area_upgrade_available)
        

    def available(self):
        if self.shown:
            self.button.enable()
            self.button.show()

        if not self.isUnlocked:
            index = list_available.index(self)
            self.x = 10 + (index * 45)
            if self.x > 250:
                self.x = 10

        self.button.set_relative_position((self.x, self.y))

        print(self.num_id, self.x)

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
            self.x = 10 + (index * 45)
            if self.x > 250:
                self.x = 10

            self.button.set_relative_position((self.x, self.y))


# Upgrades
# num_id, price, name, origin, tooltip, mult, action

up_hero1 = Upgrade(1, 100000, "Hero 1", "Hero", "This is hero upgrade 1", 2, action=(hero.upgrade1))
up_hero2 = Upgrade(2, 100000, "Hero 1", "Hero", "This is hero upgrade 1", 2, action=(hero.upgrade1))
up_hero3 = Upgrade(3, 100000, "Hero 1", "Hero", "This is hero upgrade 1", 2, action=(hero.upgrade1))
up_pyr1 = Upgrade(4, 100000, "Pyr 1", "Pyr", "This is pyr upgrade 1", 2, action=(pyr.upgrade1))

list_upgrades = [up_hero1, up_hero2, up_hero3, up_pyr1]
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


champion_y = 490
upgrade_y = 490


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
#                if champ_button.rect.collidepoint(mouse_pos):
 #                   if champion_y == 490:
  #                      champion_y = 0
   #                     upgrade_y = 490
    #                else:
     #                   champion_y = 490
      #              area_champ.set_position(position=(0, champion_y))
       #             area_upgrade.set_position(position=(320, upgrade_y))
        #        elif upgrade_button.rect.collidepoint(mouse_pos):
         #           if upgrade_y == 490:
          #              champion_y = 490
           #             upgrade_y = 0
            #        else:
             #           upgrade_y = 490
              #      area_champ.set_position(position=(0, champion_y))
               #     area_upgrade.set_position(position=(320, upgrade_y))
                #    print("Upgrade button pressed")

                        
                # Champion buttons
                for champion in champions:
                    # Level up button
                    if champion.button_level.rect.collidepoint(mouse_pos):
                        if gold >= champion.price_level and champion.isUnlocked:
                            champion.level_up()
                            total_idle_power = sum(champion.idle_power for champion in champions)

                    # Hire button
                    if champion.button_hire.is_enabled:
                        if champion.button_hire.rect.collidepoint(mouse_pos):
                            if gold >= champion.price_hire and not champion.isUnlocked:
                                champion.hire()
                                total_idle_power = sum(champion.idle_power for champion in champions)


                # Upgrade buttons
                for upgrade in list_available:
                    if upgrade.button.rect.collidepoint(mouse_pos):
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


                if background_area.rect.collidepoint(mouse_pos):
                    gold += click_power

        window.process_events(event)


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

    if hero.level >= 5 and not up_hero1.shown:
        up_hero1.shown = True
        
    if hero.level >= 10 and not up_hero2.shown:
        up_hero2.shown = True

    if hero.level >= 15 and not up_hero3.shown:
        up_hero3.shown = True

    if pyr.level >= 5 and not up_pyr1.shown:
        up_pyr1.shown = True
    
    click_power_display()
    idle_power_display()
    gold_display(gold)


    window.update(time_delta)
    window.draw_ui(screen)
    pygame.display.update
    pygame.display.flip()

pygame.quit()
sys.exit()
