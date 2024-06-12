import pygame
import math
import random



def run():
    pygame.init()

    WIDTH = 960
    HEIGHT =  540
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Lucky Wheel")

  
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)

    
    original_vertices = [(WIDTH//2,HEIGHT//2 + 200),(WIDTH//2-10,520),(WIDTH//2+10,520)]

    
    def invert_vertices(vertices):
        inverted_vertices = []
        for vertex in vertices:
            inverted_vertices.append((vertex[0], HEIGHT - vertex[1]))  
        return inverted_vertices

    
    inverted_vertices = invert_vertices(original_vertices)

    def calculate_centroid(vertices):
        centroid_x = sum(vertex[0] for vertex in vertices) / len(vertices)
        centroid_y = sum(vertex[1] for vertex in vertices) / len(vertices)
        return centroid_x, centroid_y

    class Triangle:
        def __init__(self, center_x, center_y, radius, angle, length, height, color):
            self.center_x = center_x
            self.center_y = center_y
            self.radius = radius
            self.angle = angle
            self.angular_velocity = 0
            self.length = length
            self.height = height
            self.color = color
            self.rotated_points = []  
            self.fallen_word = ["ADD 100000","ADD CHAMPION","ADD BOY","ADD 5223","ADD 566O2","ADD 23211","ADD 2321","ADD 23133","NONE","NONE"]  

        def update(self):
            self.angle += self.angular_velocity

        def draw(self, screen):
            x = self.center_x + self.radius * math.cos(math.radians(self.angle))
            y = self.center_y + self.radius * math.sin(math.radians(self.angle))

            
            angle_to_center = math.atan2(self.center_y - y, self.center_x - x)
            angle_to_center = math.degrees(angle_to_center)

            
            triangle_width = 2 * self.radius * math.sin(math.radians(360 / num_triangles //2))

            
            self.rotated_points = [
                (
                    point[0] * math.cos(math.radians(angle_to_center + 90)) - point[1] * math.sin(math.radians(angle_to_center + 90)) + x,
                    point[0] * math.sin(math.radians(angle_to_center + 90)) + point[1] * math.cos(math.radians(angle_to_center + 90)) + y
                )
                for point in [
                    (-triangle_width / 2, self.length / 2),
                    (triangle_width / 2, self.length / 2),
                    (0, -self.height / 2)
                ]
            ]

            
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


    
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    radius = 200

    
    num_triangles = 10

    
    clock = pygame.time.Clock()

    triangles = []
    colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255), (0, 255, 255), (128, 0, 0), (0, 128, 0), (0, 0, 128), (128, 128, 0)]

    
    for i in range(num_triangles):
        angle = pygame.time.get_ticks() / 10 + (360 / num_triangles * i)
        color = random.choice(colors)
        triangle = Triangle(center_x, center_y, radius, angle, 0, 400, color)
        triangle.angular_velocity = 0  
        triangles.append(triangle)

    
    button_x = 50
    button_y = 50
    button_width = 100
    button_height = 40
    button_color = BLACK
    button_text = "Spin"

    button_clicked = False

    
    spinning = False

    
    spin_start_time = 0

    
    spin_duration = 3000

    
    spin_force = random.uniform(5, 20)

    
    fallen_triangle = None

    runnings = True

    while runnings:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  
                    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)
                    if button_rect.collidepoint(event.pos):
                        button_clicked = True
                        spinning = True
                        spin_start_time = pygame.time.get_ticks()  
                        spin_force = random.uniform(5, 20)  
                        for triangle in triangles:
                            triangle.angular_velocity = spin_force  
                            fallen_triangle = None  

       
        screen.fill(WHITE)

        
        pygame.draw.rect(screen, button_color, (button_x, button_y, button_width, button_height))
        font = pygame.font.Font(None, 32)
        text = font.render(button_text, True, WHITE)
        text_rect = text.get_rect(center=(button_x + button_width // 2, button_y + button_height // 2))
        screen.blit(text, text_rect)

      
        pygame.draw.circle(screen, (255, 0, 0), (center_x, center_y), radius, 2)

        
        for triangle in triangles:
            triangle.draw(screen)

        if button_clicked and spinning:
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - spin_start_time
            if elapsed_time < spin_duration:
                for triangle in triangles:
                    triangle.angular_velocity -= spin_force / spin_duration  
                    triangle.update()  
                 
            else:
                spinning = False
                for triangle in triangles:
                    triangle.update()
                    if triangle.collidepoint(inverted_vertices[0]) and not fallen_triangle:
                        fallen_triangle = triangle  
                        print("Pussei {} has fallen on the inverted triangle area and says '{}'".format(
                            triangles.index(triangle) + 1, triangle.fallen_word[triangles.index(triangle)]))
                button_clicked = False  
                runnings = False
        
        checker = pygame.draw.polygon(screen, BLACK, inverted_vertices)
       
        pygame.display.flip()

        
        clock.tick(60)

    
