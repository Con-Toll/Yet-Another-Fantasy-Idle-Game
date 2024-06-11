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


class Event_gui(pygame.sprite.Sprite):
    def __init__(self,pos,direc,name="none") -> None:
        super().__init__()
        self.name = name
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
            if self.fade == True:
                self.alpha=max(0,self.alpha-5)
                self.image.fill((255,255,255,self.alpha),special_flags=pygame.BLEND_RGBA_MULT)
                if self.alpha <= 0:
                    self.kill()
                    
                
             
           
    
        
moving_image = pygame.sprite.Group()

class QTE(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.position = {
            1: (350, 3),
            2: (450, 3),
            3: (550, 3),
            4: (650, 3)
        }
        self.different = ["UP","DOWN","LEFT","RIGHT"]
        self.Up = Event_gui(self.position[1], random.choice(self.different))#1
        self.Down = Event_gui(self.position[2], random.choice(self.different))#2
        self.Left = Event_gui(self.position[3], random.choice(self.different))#3
        self.Right = Event_gui(self.position[4],random.choice(self.different))
        self.current_key = 0
        self.prev_key = None
        self.exe =True
        self.randomise = False
        
        
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
                            self.randomise =True
                            self.reset()
                            
                            
    def reset(self):
        if self.randomise ==  True:
            if self.Right.alpha <= 0:
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
        y   = self.center_x + self.radius * math.sin(math.radians(self.angle))
        angle_center = math.atan2(self.center_y - y,self.center_x - x)
        angle_center = math.degrees(angle_center)
        
        triangle_width = 2* self.radius * math.sin(math.radians(360 / num_triangles ))
        
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
        """
        Check if the given point is inside the bounding rectangle of the triangle.
        """
        x, y = point
        x_min = min(p[0] for p in self.rotated_points)
        x_max = max(p[0] for p in self.rotated_points)
        y_min = min(p[1] for p in self.rotated_points)
        y_max = max(p[1] for p in self.rotated_points)
        return x_min <= x <= x_max and y_min <= y <= y_max

        

