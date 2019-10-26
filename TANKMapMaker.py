import pygame
import time
from random import uniform
import json

maps = []
map_obstacles = []
obstacles = []


map_name = input('Name your map: ')

with open('TANKMaps.json', 'r') as map_file:
    map_file_contents = map_file.read()
    
map_dict = {}
map_dict = json.loads(map_file_contents)


pygame.init()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

screenfill = (140, 140, 140)
done = False
clock = pygame.time.Clock()

class Obstacle:
    def __init__(self, colour, radius, x, y):
        self.x = x
        self.y = y
        
        self.radius = radius 
        self.width = 2 * self.radius
        self.height = 2 * self.radius
                         
        self.colour = colour
        self.health = (self.radius / 30) * 400
                         
        self.last_hit = 0
        self.wait_time = 7
    
    def create_obstacle(self):
        pygame.draw.ellipse(
            screen,
            self.colour,
            pygame.Rect(self.x, self.y, self.width, self.height)
        )




while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()

            obstacle_radius = uniform(20, uniform(32, 40))
            new_obstacle = Obstacle((87, 55, 41), obstacle_radius, mouse_x - obstacle_radius, mouse_y - obstacle_radius)

            map_obstacles.append([mouse_x - obstacle_radius, mouse_y - obstacle_radius, obstacle_radius])
            obstacles.append(new_obstacle)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            done = True

    screen.fill(screenfill) 

    for obstacle in obstacles:
        obstacle.create_obstacle()

    pygame.display.flip()
    clock.tick(60)


map_dict[map_name] = map_obstacles
new_contents = json.dumps(map_dict)

with open('TANKMaps.json', 'w') as map_file:
    map_file.write(new_contents)

print('Your map has been saved as ' + map_name)

pygame.quit()

