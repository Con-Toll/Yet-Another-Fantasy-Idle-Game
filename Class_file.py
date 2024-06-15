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

class LW_button:
    def __init__(self, text, position, size, color=(173,217,230)):
        self.text = text
        self.rect = pygame.Rect(position, size)
        self.color = color
        self.destination = (0, 0) 
        self.clicked = False

    def draw(self, surface,font):
        pygame.draw.rect(surface, self.color, self.rect)
        text_surface = font.render(self.text, True, (0,0,0))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)

    
            
    
    

    
        
        