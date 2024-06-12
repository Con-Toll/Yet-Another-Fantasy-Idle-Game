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

    
            
    
    
class Triangle():
    def __init__(self,center_x,center_y,radius,angle,length,height,color):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = angle
        self.angular_velocity = 0
        self.length = length
        self.height = height
        self.color = color
        self.rotated_points = []
        self.fallen_word = ["ADD 100000","ADD CHAMPION","ADD BOY","ADD 5223","ADD 566O2","ADD 23211","ADD 2321","ADD 23133","NONE","NONE"] #Add the bonus thing that you want
        
    def update(self):
        self.angle +=self.angular_velocity
        
    def draw(self,screen):
        x = self.center_x + self.radius * math.cos(math.radians(self.angle))
        y   = self.center_y + self.radius * math.sin(math.radians(self.angle))
        angle_center = math.atan2(self.center_y - y,self.center_x - x)
        angle_center = math.degrees(angle_center)
        
        triangle_width = 2* self.radius * math.sin(math.radians(360 / 10 ))
        
        self.rotated_points = [
            (
                point[0] * math.cos(math.radians(angle_center + 90)) - point[1] * math.sin(math.radians(angle_center + 90)) + x,
                point[0] * math.sin(math.radians(angle_center + 90)) + point[1] * math.cos(math.radians(angle_center + 90)) + y
            )
            for point in [
                (-triangle_width / 2, self.length / 2),
                (triangle_width / 2, self.length / 2),
                (0, -self.height / 2)
            ]
        ]

        # Draw the triangle with the bottom corner always pointing towards the center
        pygame.draw.polygon(screen, self.color, self.rotated_points)

    def collidepoint(self, point):
       # for further operation where lucky wheel need to check which one is hit
        x, y = point
        x_min = min(p[0] for p in self.rotated_points)
        x_max = max(p[0] for p in self.rotated_points)
        y_min = min(p[1] for p in self.rotated_points)
        y_max = max(p[1] for p in self.rotated_points)
        return x_min <= x <= x_max and y_min <= y <= y_max

color =  [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0)]




   
    
    
        
        