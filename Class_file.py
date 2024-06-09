import pygame
import random
import json
import math




class moving_button():
    def __init__(self):
        self.frames = []
        self.frame = 0
        self.x = 0
        self.index = 0
        self.y = 200
      
    def move(self,speed):
        for i in range(0,6):
            self.frame =  pygame.image.load(f"assets\pixilart-frames\pixil-frame-{i}.png")  
            self.frames.append(self.frame)
     
        self.x -= speed
    
    def check(self,random_x,random_y):
        if self.x + self.frames[self.index].get_width() < 0:
            self.x =  random_x
            self.y = random_y
            
            
    
class Event_gui(pygame.sprite.Sprite):
    def __init__(self,pos,direc) -> None:
        super().__init__()
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
            for event in pygame.event.get():
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
            global point
            if self.fade == True:
                self.alpha=max(0,self.alpha-5)
                self.image.fill((255,255,255,self.alpha),special_flags=pygame.BLEND_RGBA_MULT)
                if self.alpha <= 0:
                    self.kill()
                    self.is_animating = False
                
             
           
    
        
moving_image = pygame.sprite.Group()


class QTE(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = {
            1: (350, 200),
            2: (450, 200),
            3: (550, 200),
            4: (650, 200)
        }
        self.different = ["UP", "DOWN", "LEFT", "RIGHT"]
        self.Up = Event_gui(self.position[1], random.choice(self.different))#1
        self.Down = Event_gui(self.position[2], random.choice(self.different))#2
        self.Left = Event_gui(self.position[3], random.choice(self.different))#3
        self.Right = Event_gui(self.position[4], random.choice(self.different))
        self.exe = False
        
        
    def key(self):
        global gold
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
                            gold+=10000
                            self.exe = False
                            self.reset()
                            
    def reset(self):
        self.Down.direc = random.choice(self.different)
        self.Up.direc = random.choice(self.different)
        self.Left.direc = random.choice(self.different)
        self.Right.direc = random.choice(self.different)
        self.key()
                    
        
    def update(self,screen):
        moving_image.update()
        moving_image.draw(screen)
        if self.exe == True:
            moving_image.add(self.Up)
            moving_image.add(self.Down)
            moving_image.add(self.Left)
            moving_image.add(self.Right)
            self.Down.alpha = 255
            self.Up.alpha = 255
            self.Left.alpha = 255
            self.Right.alpha = 255
        self.fadeout()
            
        
    def fadeout(self):
        self.Up.fadeout()
        self.Down.fadeout()
        self.Left.fadeout()
        self.Right.fadeout()