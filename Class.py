import pygame
import random
import json
import math



class button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__
        self.filename = "assets\Button_sprite.png"
        self.sprite_sheet = pygame.image.load(self.filename).convert()
        self.meta_data =self.filename.replace('png','json')
        with open(self.meta_data)as f:
            self.data = json.load(f)
        f.close
        
    def get_sprite(self,x,y,w,h):
        sprite = pygame.Surface((w,h))
        sprite.set_colorkey((0,0,0))
        sprite.blit(self.sprite_sheet,(0,0),(x,y,w,h))
        return sprite
    
    def parse_sprite(self,name):
        sprite = self.data["frames"][name]['frame']
        x,y,w,h = sprite["x"],sprite['y'],sprite['w'],sprite['h']
        image = self.get_sprite(x,y,w,h)
        return image 
    
class moving_button(button):
    def __init__(self):
        super().__init__
        self.button = button()
        self.sprite = [self.button.parse_sprite('f_button1.png'),self.button.parse_sprite('f_button2.png'),self.button.parse_sprite('f_button3.png'),self.button.parse_sprite('f_button4.png'),self.button.parse_sprite('f_button5.png'),self.button.parse_sprite('f_button6.png')]
        self.current_sprite = 0
        self.image = self.sprite
        self.image = self.sprite[self.current_sprite]
        self.animate = True
        self.index = 0
    
    
        
        