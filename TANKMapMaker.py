import pygame
import time
from random import randint
import json
import math

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
    def __init__(self, colour, radius, x, y, turret, obs_number):
        self.x = x
        self.y = y
        
        self.radius = radius 
        self.width = 2 * self.radius
        self.height = 2 * self.radius
                         
        self.colour = colour
        self.obs_number = obs_number

        self.turret = turret
    
    def create_obstacle(self):
        pygame.draw.ellipse(
            screen,
            self.colour,
            pygame.Rect(self.x, self.y, self.width, self.height)
        )

        if self.turret == 1:
            pygame.draw.ellipse(
                screen,
                (70, 70, 255),
                pygame.Rect(self.x + self.radius - 10, self.y + self.radius - 10, 20, 20)
        )

        if self.turret == 2:
            pygame.draw.ellipse(
                screen,
                (0, 0, 0),
                pygame.Rect(self.x + self.radius - 10, self.y + self.radius - 10, 20, 20)
        )


while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break

        if event.type == pygame.KEYDOWN and event.key == pygame.KMOD_LCTRL:
            max_radius1 = 23
            max_radius2 = 26

        else:
            max_radius1 = 32
            max_radius2 = 40

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            turret = 0
            obstacle_radius = randint(20, randint(max_radius1, max_radius2))
            obs_number = len(map_obstacles)
            new_obstacle = Obstacle((87, 55, 41), obstacle_radius, mouse_x - obstacle_radius, mouse_y - obstacle_radius, turret, obs_number)
            
            map_obstacles.append([mouse_x - obstacle_radius, mouse_y - obstacle_radius, obstacle_radius, turret])
            
            obstacles.append(new_obstacle)

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()

            
            for deleted_obstacle in obstacles:
                if math.sqrt((mouse_x - (deleted_obstacle.x + deleted_obstacle.radius)) ** 2 + (mouse_y - (deleted_obstacle.y + deleted_obstacle.radius)) ** 2) <= deleted_obstacle.radius:
                    map_obstacles.remove(map_obstacles[deleted_obstacle.obs_number])
                    
                    for obstacle in obstacles:
                        if obstacle.obs_number > deleted_obstacle.obs_number:
                            obstacle.obs_number -= 1
                            
                    obstacles.remove(deleted_obstacle)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            turret = 1
            obstacle_radius = randint(20, randint(max_radius1, max_radius2))
            obs_number = len(map_obstacles)
            new_obstacle = Obstacle((87, 55, 41), obstacle_radius, mouse_x - obstacle_radius, mouse_y - obstacle_radius, turret, obs_number)

            map_obstacles.append([mouse_x - obstacle_radius, mouse_y - obstacle_radius, obstacle_radius, turret])
            obstacles.append(new_obstacle)

        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
            (mouse_x, mouse_y) = pygame.mouse.get_pos()
            turret = 2
            obs_number = len(map_obstacles)
            obstacle_radius = randint(20, randint(max_radius1, max_radius2))
            new_obstacle = Obstacle((87, 55, 41), obstacle_radius, mouse_x - obstacle_radius, mouse_y - obstacle_radius, turret, obs_number)

            map_obstacles.append([mouse_x - obstacle_radius, mouse_y - obstacle_radius, obstacle_radius, turret])
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

num_of_obs = str(len(map_obstacles))

print('Your map, containing ' + num_of_obs + ' obstacles, has been saved as ' + map_name + '.')

pygame.quit()


