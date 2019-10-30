import pygame
import time
import math
from random import uniform, randrange, randint
import os, sys
import ast
import json

from TankAssets import *
import TankOptions
from TankOptions import *


pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

clock = pygame.time.Clock() 
done = False

cs_pellets = 12
ps_pellets = 10

gl_shrapnel = 82
c4_shrapnel = 73
g_shrapnel = 47
sds_shrapnel = 37
hrpg_shrapnel = 23

br_burst = 3
bp_burst = 2

r_speed = uniform(4, 7)
r_health = randint(65, 135)

weapon_grenade_count = {
    'smg': 2,
    'mg': 2,
    'hmg': 1,
    't': 3,
    'n': 0,
    'ss': 1,
    's': 3,
    'cs': 3,
    'ps': 2,
    'r': randint(0, 4),
    'br': 2,
    'bp': 5,
    'ft': 2,
    'D': 7,
    'td': 3,
    'gl': 0,
    'mng': 4,
    'ml': 0,
    'mar': 3,
    'sap': 4,
    'mp': 3,
    'hrpg': 0
}

weapon_cooldowns = {
    'smg': 0.065,
    'mg': 0.1,
    'hmg': 0.2,
    't': 0.01,
    'n': 0.095,
    'ss': 1.5,
    's': 0.65,
    'cs': 0.25,
    'ps': 0.85,
    'r': uniform(0.001, 1),
    'br': 0.35,
    'bp': 0.325,
    'ft': 0.0000001,
    'D': 0.0005,
    'td': 5,
    'gl': 1,
    'mng': 0.0035,
    'g': 2,
    'ml': 0.2,
    'mar': 0.3,
    'sap': 0.075,
    'mp': 0.065,
    'st': 0.3,
    'rft': 0.075,
    'hrpg': 0.35
}

weapon_magazines = {
    'smg': 25,
    'mg': 35,
    'hmg': 65,
    't': 60,
    'n': 100,
    'ss': 6,
    's': 10,
    'cs': 14,
    'ps': 8,
    'r': randint(7, 65),
    'br': 10 * br_burst,
    'bp': 7 * bp_burst,
    'ft': 900,
    'D': 500,
    'td': 3,
    'gl': 4,
    'gls': 20,
    'mng': 250,
    'ml': 10,
    'mar': 20,
    'sap': 19,
    'mp': 21,
    'st': 60,
    'rft': 120,
    'hrpg': 3
}

weapon_reloads = {
    'smg': 2,
    'mg': 2.5,
    'hmg': 3.5,
    't': 0,
    'n': 0,
    'ss': 4,
    's': 3,
    'cs': 3,
    'ps': 3,
    'r': uniform(1.5, 8),
    'br': 3,
    'bp': 1.4,
    'ft': 4,
    'D': 4,
    'td': 3,
    'gl': 4,
    'mng': 5,
    'ml': 0,
    'mar': 2.7,
    'sap': 1.2,
    'mp': 1.6,
    'st': 7,
    'rft': 8,
    'hrpg': 3
}

player_speeds = {
    'smg': 6.5,
    'smg-low': 7,
    
    's': 6,
    's-low': 6.5,
    
    't': 6.5,
    't-low': 7,
    
    'n': 5,
    'n-low': 5.5,
    
    'mg': 6.25,
    'mg-low': 6.75,
    
    'ss': 4.75,
    'ss-low': 5.25,
    
    'hmg': 4.5,
    'hmg-low': 5.5,

    'cs': 6.25,
    'cs-low': 6.75,

    'ps': 6,
    'ps-low': 6.5,

    'r': r_speed,
    'r-low': r_speed + 0.5,

    'br': 6,
    'br-low': 6.5,

    'bp': 7,
    'bp-low':7.5,

    'ft': 5.5,
    'ft-low': 6,
    
    'D': 7,
    'D-low': 7.5,

    'td': 4.5,
    'td-low':5.5,

    'gl': 5.5,
    'gl-low': 4.5,

    'mng': 2.2,
    'mng-low': 1.8,

    'ml': 5.25,
    'ml-low': 5,
    
    'mar': 5.5,
    'mar-low': 6,

    'sap': 6.5,
    'sap-low': 7,

    'mp': 6.25,
    'mp-low': 6.85,

    'hrpg': 4,
    'hrpg-low': 4.25
    
}

bullet_speeds = {
    'smg': 16,
    'mg': 14,
    'hmg': 15,
    'mar': 19,
    't': 0,
    'n': 6,
    'ss': 33,
    's': 22.5,
    'cs': 18,
    'ps': 19,
    'r': randint(5, 19),
    'br': 19,
    'bp': 19,
    'ft': 10,
    'D': 23,
    'td': 13,
    'gl': 14.5,
    'gls': 5,
    'mng': 14.5,
    'g': 6,
    'c4': 0,
    'sap': 16,
    'mp': 15,
    'st': 13,
    'rft': 12,
    'sds': 0,
    'hrpg': 8
}

bullet_damages = {
    'smg': 2.5,
    'mg': 5,
    'hmg': 12,
    'mar': 28,
    't': 1,
    'n': 2,
    'ss': 65,
    's': 35,
    'cs': 3,
    'ps': 10.5,
    'r': uniform(0.01, randint(10, 90)),
    'br': 12.5,
    'bp': 7.5,
    'ft': uniform(1, 1.75),
    'D': 4.5,
    'td': 100,
    'mng': 2,
    'gl': 5,
    'gls': 1.5,
    'g': 3,
    'c4': 5,
    'c4s': 0.25,
    'sap': 8,
    'mp': 6,
    'st': 3,
    'rft': 0.5,
    'sds': 1,
    'hrpg': 5
}

bullet_penetration_factors = {
    'smg': 1.5,
    'mg': 7,
    'hmg': 43,
    'mar': 43,
    't': 20,
    'n': 0,
    'ss': 125,
    's': 85,
    'cs': 4,
    'ps': 10.5,
    'r': uniform(0.01, randint(10, 90)),
    'br': 12.5,
    'bp': 3.5,
    'ft': uniform(1, 1.75),
    'D': 1,
    'td': 400,
    'gl': 70,
    'gls': 7,
    'mng': 2.5,
    'g': 6,
    'c4': 0,
    'sap': 12,
    'mp': 3,
    'st': 2,
    'rft': 1,
    'sds': 2,
    'hrpg': 97
}

obstacle_numbers = {
    'n': [0, 1],
    'l': [7, 12],
    'm': [23, 27],
    'h': [30, 43],
    'c': [54, 66],
    'b': [69, 93],
    'i': [97, 125]
}

def specialRound(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1

    return 0

bulletcolour = (255, 180, 180)
ft_bulletcolour = (255, 180, 180)

turrets = []
turret_sds = [] # NB: sds mean Self Destruct System(s)
turret_bullets = []

myfont = pygame.font.SysFont('Impact', 80)
myfont2 = pygame.font.SysFont('Bahnscrift', 40)
myfont3 = pygame.font.SysFont('Bahnscrift', 25)

p1victorytext = myfont.render('GREEN WINS!', False, (0, 100, 0))
p2victorytext = myfont.render('RED WINS!', False, (100, 0, 0))

p1ammocount = 0
p2ammocount = 0

p1ammocountstr = str()
p2ammocountstr = str()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

def getx():
    x = randrange(20, (SCREEN_WIDTH - 40))
    return x

def gety():
    y = randrange(20, (SCREEN_HEIGHT - 40))
    return y

def recentlyShot(subject, last_hit, wait_time):
    if time.time() - subject.last_hit <= subject.wait_time:
        return True

def healthBar(subject, colour, x, y, health, width, adjustment_factor):
    if recentlyShot(subject, subject.last_hit, subject.wait_time):
        if type(subject) == Player:
            pygame.draw.rect(screen, colour, pygame.Rect(x + (width / 2) - ((health / adjustment_factor) / 2), y - 10, health / adjustment_factor, 3)) 

        else:
            if subject.width <= 56:
                pygame.draw.rect(screen, colour, pygame.Rect(x + (width / 2) - ((health / (adjustment_factor * 0.6)) / 2), y - 12, health / adjustment_factor, 5)) 

            elif subject.width <= 64:
                pygame.draw.rect(screen, colour, pygame.Rect(x + (width / 2) - ((health / (adjustment_factor)) / 2), y - 12, health / adjustment_factor, 5))

            else:
                pygame.draw.rect(screen, colour, pygame.Rect(x + (width / 2) - ((health / (adjustment_factor * 1.2)) / 2), y - 12, health / adjustment_factor, 5))

class BloodSpatter:
    def __init__(self, colour, x, y):
        self.x = x
        self.y = y
        self.width = randint(13, 19)
        self.height = randint(13, 19)
        self.colour = colour

    def draw(self):
        pygame.draw.ellipse(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))


class Turret:
    def __init__(self, x, y, obstacle, weaponclass='st'):
        self.x = x
        self.y = y
        
        self.width = 20
        self.height = 20
        self.radius = 10

        self.weaponclass = weaponclass

        if self.weaponclass == 'rft':
            self.colour = (0, 0, 0)
            
        else:
            self.colour = (70, 70, 255)
            
        self.obstacle = obstacle


        self.last_fire = 0
        self.fired_bullets = 0
        self.mag_size = weapon_magazines[self.weaponclass]
        
        self.is_reloading = False
        self.reload_start = 0

        self.health = 162
        self.last_hit = 0
        self.wait_time = 3

        
    def range_finder(self, player):
        dist = math.sqrt(((player.x + 20) - (self.x + self.radius)) ** 2 + ((player.y + 20) - (self.y + self.radius)) ** 2)
        return dist

    def get_bullet_velocity(self, player):
        horizontal = -(self.x - player.x)
        vertical = -(self.y - player.y)
        distance = ((vertical**2) + (horizontal**2)) ** 0.5
        dx = horizontal / distance
        dy = vertical / distance
        return (dx, dy)

    def target(self, player1, player2):
        if (time.time() - self.last_fire >= weapon_cooldowns[self.weaponclass]) and (self.fired_bullets < self.mag_size):
            if self.range_finder(player1) < self.range_finder(player2):
                if self.range_finder(player1) <= 525:
                    (dx, dy) = self.get_bullet_velocity(player1)
                    new_bullet = Bullet(self.x + 6, self.y + 6, float(dx), float(dy), self.weaponclass, self.x + 6, self.y + 6, round_values=False, turret=self)
                    global turret_bullets
                    turret_bullets.append(new_bullet)
                    
                    self.fired_bullets += 1
                    self.last_fire = time.time()

            else:
                if self.range_finder(player2) <= 525:
                    (dx, dy) = self.get_bullet_velocity(player2)
                    new_bullet = Bullet(self.x + 10, self.y + 10, float(dx), float(dy), self.weaponclass, self.x + 10, self.y + 10, round_values=False, turret=self)
                    turret_bullets.append(new_bullet)
                    
                    self.fired_bullets += 1
                    self.last_fire = time.time()

            self.reload()
            
    def out_of_ammo(self):
        ammo_left = self.mag_size - self.fired_bullets
        return ammo_left <= 0

    def reload(self):
        if self.out_of_ammo:
            if not self.is_reloading:
                self.is_reloading = True
                self.reload_start = time.time()

            if time.time() - self.reload_start >= weapon_reloads[self.weaponclass]:
                self.is_reloading = False
                self.fired_bullets = 0

    def isTouching(self, bullet):
        dist = math.sqrt(((bullet.x + (bullet.width / 2)) - (self.x + self.radius)) ** 2 + ((bullet.y + (bullet.height / 2)) - (self.y + self.radius)) ** 2)
        return dist <= (self.radius + 4)
    

    def draw(self):
        pygame.draw.ellipse(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))


class Obstacle:
    def __init__(self, colour, x, y, radius):
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
        pygame.draw.ellipse(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

    def isTouching(self, other):
        if type(other) == Bullet:
            dist = math.sqrt(((other.x + (other.width / 2)) - (self.x + self.radius)) ** 2 + ((other.y + (other.height / 2)) - (self.y + self.radius)) ** 2)
            return dist <= (self.radius + 4)
        
        elif type(other) == Obstacle:
            dist = math.sqrt(((other.x + other.radius) - (self.x + self.radius)) ** 2 + ((other.y + other.radius) - (self.y + self.radius)) ** 2)
            return dist <= self.width
        
        else:
            dist = math.sqrt(((other.x + 20) - (self.x + self.radius)) ** 2 + ((other.y + 20) - (self.y + self.radius)) ** 2)
            return dist <= self.width*0.8


class Obstacles:
    def __init__(self, num_of_obs, use_maps):
        self.obstacles = []
        self.num_of_obs = num_of_obs

        if use_maps == 'n':
            range_1 = obstacle_numbers[num_of_obs][0]
            range_2 = obstacle_numbers[num_of_obs][1]
            for i in range(randrange(range_1, range_2)):
                while True:
                    has_turret = randint(0, 20)
                    rf_turret = randint(1, 3)
                    new_obs_x = getx()
                    new_obs_y = gety()
                    new_obs_radius = uniform(20, uniform(32, 40))

                    if (150 >= new_obs_x <= SCREEN_WIDTH - 150) or (150 >= new_obs_y <= SCREEN_HEIGHT - 150):
                        has_turret = randint(0, 35)
                    
                    new_obstacle = Obstacle((87, 55, 41), new_obs_x, new_obs_y, new_obs_radius)
                    if rf_turret == 1:
                        new_turret = Turret(new_obs_x + new_obs_radius - 10, new_obs_y + new_obs_radius - 10, new_obstacle, weaponclass='rft')

                    else:
                        new_turret = Turret(new_obs_x + new_obs_radius - 10, new_obs_y + new_obs_radius - 10, new_obstacle)
                    
                    if not self.isTouching(new_obstacle) and not new_obstacle.isTouching(p1) and not new_obstacle.isTouching(p2):
                        self.obstacles.append(new_obstacle)

                        if num_of_obs != 'i':
                            if has_turret == 3:
                                print('A new baby turret has been born!')
                                global turrets
                                turrets.append(new_turret)

                        elif num_of_obs == 'i' and has_turret <= 3:
                            print('Oh, God! Not another one!')
                            turrets.append(new_turret)
                            
                        break
                    
        else:
            with open('TANKMaps.json', 'r') as map_file:
                map_file_contents = map_file.read()
            map_dict = json.loads(map_file_contents)
            selected_map = map_dict[num_of_obs]
            print(len(selected_map))
            
            for obstacle in selected_map:
                new_obstacle = Obstacle((87, 55, 41), obstacle[0], obstacle[1], obstacle[2])
                self.obstacles.append(new_obstacle)
                
                if obstacle[3] == 1:
                    new_turret = Turret(obstacle[0] + obstacle[2] - 10, obstacle[1] + obstacle[2] - 10, new_obstacle)
                    turrets.append(new_turret)
                    
                if obstacle[3] == 2:
                    new_turret = Turret(obstacle[0] + obstacle[2] - 10, obstacle[1] + obstacle[2] - 10, new_obstacle, weaponclass='rft')
                    turrets.append(new_turret)

    def isTouching(self, object, exclusion=None):
        for obstacle in self.obstacles:
            if obstacle.isTouching(object) and obstacle != exclusion:
                if type(object) == Bullet:
                    obstacle.health -= 1 * bullet_penetration_factors[object.weaponclass]
                    obstacle.last_hit = time.time()
                    
                if obstacle.health <= 0:
                    self.obstacles.remove(obstacle)
                    
                return True

        return False

    def draw(self):
        for obstacle in self.obstacles:
            obstacle.create_obstacle()
            

class Bullet:
    def __init__(self, x, y, dx, dy, weaponclass, x_origin, y_origin, grenade_type='not gl',  round_values=True, turret=None):
        self.csbullet_range = 300
        self.psbullet_range = 360
        self.bpbullet_range = 800
        self.sapbullet_range = 1000
        self.mpbullet_range = 750
        self.stbullet_range = randint(410, 490)
        
        self.ftfire_range = uniform(130, 310)
        self.ftbullet_colour = (uniform(253, 255), uniform(110, 150), uniform(35, 55))

        self.gls_colour = (uniform(235, 255), uniform(140, 190), uniform(0, 25))

        self.x = x
        self.y = y
        
        self.x_origin = x_origin
        self.y_origin = y_origin
        
        self.weaponclass = weaponclass

        self.grenade_type = grenade_type

        self.turret = turret

        if self.grenade_type == 'gl':
            self.gls_range_value = uniform(85, uniform(87, uniform(90, uniform(92, uniform(106, 210)))))

        elif self.grenade_type == 'c4':
            self.gls_range_value = uniform(73, uniform(75, uniform(77, uniform(79, uniform(85, 310)))))

        elif self.grenade_type == 'sds':
            self.gls_range_value = uniform(43, uniform(63, uniform(64, uniform(66, uniform(67, 185)))))
            
        else:
            self.gls_range_value = uniform(60, uniform(79, uniform(90, uniform(106, uniform(120, 160)))))


        if round_values:
            self.dx = self.bulletSpeed(specialRound(dx))
            self.dy = self.bulletSpeed(specialRound(dy))
            
        else:
            self.dx = self.bulletSpeed(dx)
            self.dy = self.bulletSpeed(dy)

        
        if weaponclass == 'cs':
            self.dx += uniform(-6, 6)
            self.dy += uniform(-6, 6)
            
        elif weaponclass == 'ps':
            self.dx += uniform(-3.5, 3.5)
            self.dy += uniform(-3.5, 3.5)
            
        if weaponclass == 'smg':
            self.dx += uniform(-0.65, 0.65)
            self.dy += uniform(-0.65, 0.65)
            
        elif weaponclass == 'mg':
            self.dx += uniform(-0.19, 0.19)
            self.dy += uniform(-0.19, 0.19)

        elif weaponclass == 'mng':
            self.dx += uniform(-0.45, 0.45)
            self.dy += uniform(-0.45, 0.45)
            
        elif weaponclass == 'br':
            self.dx += uniform(-0.1, 0.1)
            self.dy += uniform(-0.1, 0.1)
            
        elif weaponclass == 's':
            self.dx += uniform(-0.05, 0.05)
            self.dy += uniform(-0.05, 0.05)
            
        elif weaponclass == 'ft':
            self.dx += uniform(-2, 2)
            self.dy += uniform(-2, 2)
            
        elif weaponclass == 'r':
            self.dx += uniform(-uniform(0, 3), uniform(0, 3))
            self.dy += uniform(-uniform(0, 3), uniform(0, 3))

        elif weaponclass == 'D':
            self.dx += uniform(-uniform(0, 1.25), uniform(0, 1.25))
            self.dy += uniform(-uniform(0, 1.25), uniform(0, 1.25))

        elif weaponclass == 'sap':
            self.dx += uniform(-uniform(0, 0.25), uniform(0, 0.25))
            self.dy += uniform(-uniform(0, 0.25), uniform(0, 0.25))

        elif weaponclass == 'mp':
            self.dx += uniform(-uniform(0, 0.75), uniform(0, 0.75))
            self.dy += uniform(-uniform(0, 0.75), uniform(0, 0.75))

        elif weaponclass == 'st':
            self.dx += uniform(-uniform(0, 0.25), uniform(0, 0.25))
            self.dy += uniform(-uniform(0, 0.25), uniform(0, 0.25))

        elif weaponclass == 'rft':
            self.dx += uniform(-uniform(0, 0.75), uniform(0, 0.75))
            self.dy += uniform(-uniform(0, 0.75), uniform(0, 0.75))
            


        if weaponclass == 'ft':
            self.damage = uniform(2.25, 4.75)
            
        else:
            self.damage = bullet_damages[weaponclass]
        
        self.width = 14
        self.height = 14
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.weaponclass == 'ft':
            pygame.draw.ellipse(screen, self.ftbullet_colour, pygame.Rect(self.x, self.y, 14, 14))
            
        elif self.weaponclass == 'ps' or self.weaponclass == 'cs':
            pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 7, 7))

        elif self.weaponclass == 'gls':
            pygame.draw.ellipse(screen, self.gls_colour, pygame.Rect(self.x, self.y, 8, 8))

        else:
            pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 8, 8))

    def customMove(self, dx, dy):
        self.x += self.bulletSpeed(specialRound(dx))
        self.y += self.bulletSpeed(specialRound(dy))

        pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 8, 8))

    def isColliding(self, player):
        if player.isTouchingBullet(self):
            global blood_splatters
            for i in range(0, randint(1, 3)):
                blood_splatters.append(BloodSpatter((randint(177, 200), 11, 11), player.x + 10 + uniform(-24, 24), player.y + 10 + uniform(-24, 24)))
            
            player.health -= self.damage
            player.last_hit = time.time()
            return True

        if self.weaponclass == 'st' or self.weaponclass == 'rft':
            if obstacles.isTouching(self, self.turret.obstacle):
                return True
            
        else:
            if obstacles.isTouching(self) and not (self.weaponclass == 'c4'):
                return True

    def ps_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.psbullet_range:
            return True
        return False
    
    def gls_range(self):
        if self.weaponclass == 'gls':
            dx = (self.x - self.x_origin)
            dy = (self.y - self.y_origin)
            if math.sqrt(dx**2 + dy**2) >= self.gls_range_value:
                return True
        return False
    
    def bp_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.bpbullet_range:
            return True
        return False
    
    def cs_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.csbullet_range:
            return True
        return False
    
    def ft_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.ftfire_range:
            return True
        return False

    def sap_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.sapbullet_range:
            return True
        return False
    
    def mp_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.mpbullet_range:
            return True
        return False

    def st_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.stbullet_range:
            return True
        return False     
        
    def bulletSpeed(self, x):
        return x * bullet_speeds[self.weaponclass]

    def isOutOfBounds(self):
        return ((self.x < 0 or self.x + self.width > SCREEN_WIDTH) or (self.y < 0 or self.y + self.height > SCREEN_HEIGHT))


class Grenade(Bullet):
    def __init__(self, x, y, dx, dy, player, straight_aim_hrpg=False):
        self.grenade_range = 20

        self.player = player
        
        self.x = x
        self.y = y

        self.dx = dx * 0.8
        self.dy = dy * 0.8

        self.radius = 7
        self.width = 14
        self.height = 14

        self.straight_aim_hrpg = straight_aim_hrpg

        if self.player.weaponclass == 'st' or self.player.weaponclass == 'rft':
            self.weaponclass = 'sds'

        elif self.player.weaponclass == 'gl':
            self.weaponclass = 'gl'

        elif self.player.weaponclass == 'hmg' or self.player.weaponclass == 'ml':
            self.weaponclass = 'c4'

        elif self.player.weaponclass == 'hrpg':
            self.weaponclass = 'hrpg'
            self.grenade_range = 320
            self.radius = 5.5
            self.width = 11
            self.height = 11

        else:
            self.weaponclass = 'g'  
    
        self.damage = bullet_damages[self.weaponclass]
        
        self.grenade_movement_rate = bullet_speeds[self.weaponclass]
        
        self.has_detonated = False

    def get_bullet_velocity(self, otherPlayer):
        horizontal = -(self.x - otherPlayer.x)
        vertical = -(self.y - otherPlayer.y)
        distance = ((vertical**2) + (horizontal**2)) ** 0.5
        dx = horizontal / distance
        dy = vertical / distance
        return (dx, dy)

    def interpolate(self, value, destination, increment):
        if value < destination:
            return increment

        elif value > destination:
            return -increment

        else:
            return 0

    def lock(self, value, max):
        if value < -max:
            return -max

        elif value > max:
            return max

        return value
        
    
    def move(self, otherPlayer):
        if self.weaponclass == 'hrpg' and not self.straight_aim_hrpg:
            (des_dx, des_dy) = (self.get_bullet_velocity(otherPlayer))
            
            self.dx += self.interpolate(self.dx, des_dx, 0.08)
            self.dx = self.lock(self.dx, 4)

            self.dy +=  self.interpolate(self.dy, des_dy, 0.08)
            self.dy = self.lock(self.dy, 4)

            self.x += self.dx * bullet_speeds['hrpg']
            self.y += self.dy * bullet_speeds['hrpg']

        else:
            self.dx = self.grenade_speed(specialRound(self.dx))
            self.dy = self.grenade_speed(specialRound(self.dy))
        
        self.x += self.dx
        self.y += self.dy

        self.grenade_range -= 1
    
        if self.weaponclass == 'g':
            self.grenade_movement_rate -= 0.075
    
        if ((self.weaponclass == 'gl' or self.weaponclass == 'hrpg') and (self.grenade_range <= 0)) or ((self.weaponclass == 'g') and (self.grenade_movement_rate <= 0)) or self.isColliding(otherPlayer) or self.isOutOfBounds():
            self.detonate()


        if self.weaponclass == 'gl':
            pygame.draw.ellipse(screen, (96, 96, 96), pygame.Rect(self.x, self.y, self.width, self.height))

        elif self.weaponclass == 'c4':
            pygame.draw.ellipse(screen, (115, 127, 115), pygame.Rect(self.x, self.y, self.width, self.height))

        elif self.weaponclass == 'hrpg':
            pygame.draw.ellipse(screen, (100, 100, 100), pygame.Rect(self.x, self.y, self.width, self.height))

        else:
            pygame.draw.ellipse(screen, (106, 122, 90), pygame.Rect(self.x, self.y, self.width, self.height))

    def detonate(self):
        if not self.has_detonated:
            self.has_detonated = True
        else:
            return
        
        self.dx = 0
        self.dy = 0
    
        if self.weaponclass == 'gl':
            for shrapnel in range(gl_shrapnel):
                self.dx = uniform(-4, 4)
                self.dy = uniform(-4, 4)

                newBullet = Bullet(self.x + 3, self.y + 3, self.dx, self.dy, 'gls', self.x + 3, self.y + 3, 'gl', round_values=False)
                self.player.bullets.append(newBullet)

        elif self.weaponclass == 'c4':
            for shrapnel in range(c4_shrapnel):
                self.dx = uniform(-4, 4)
                self.dy = uniform(-4, 4)

                newBullet = Bullet(self.x + 3 + uniform(-17, 17), self.y + 3 + uniform(-17, 17), self.dx, self.dy, 'gls', self.x + 3, self.y + 3, 'c4', round_values=False)
                self.player.bullets.append(newBullet)

        elif self.weaponclass == 'hrpg':
            for shrapnel in range(hrpg_shrapnel):
                self.dx = uniform(-4, 4)
                self.dy = uniform(-4, 4)

                newBullet = Bullet(self.x + 3 + uniform(-17, 17), self.y + 3 + uniform(-17, 17), self.dx, self.dy, 'gls', self.x + 3, self.y + 3, 'hrpg', round_values=False)
                self.player.bullets.append(newBullet)

        elif self.weaponclass == 'sds':
            for shrapnel in range(sds_shrapnel):
                self.dx = uniform(-4, 4)
                self.dy = uniform(-4, 4)

                newBullet = Bullet(self.x + 3 + uniform(-17, 17), self.y + 3 + uniform(-17, 17), self.dx, self.dy, 'gls', self.x + 3, self.y + 3, 'sds', round_values=False)
                global turret_bullets
                turret_bullets.append(newBullet)
                
        else:
            for shrapnel in range(g_shrapnel):
                self.dx = uniform(-4, 4)
                self.dy = uniform(-4, 4)

                newBullet = Bullet(self.x + 3, self.y + 3, self.dx, self.dy, 'gls', self.x + 3, self.y + 3, round_values=False)
                self.player.bullets.append(newBullet)
    
        if self.weaponclass == 'sds':
            global turret_sds
            turret_sds.remove(self)
            
        else:
            self.player.grenades.remove(self)
            
    def grenade_speed(self, x):
        return x * self.grenade_movement_rate

    
class Player:
    def __init__(self, player, x, y, bodycolour, left, right, up, down, fire, throw, weaponclass, x_origin, y_origin):
        self.player = player                 
        self.isReloading = False
                         
        self.last_hit = time.time()
        self.wait_time = 1000
        
        if self.player == 'p1':
            self.playerImg = pygame.image.load('.\TankAssets\GreenSoldier Paint\GreenSoldierRight(Paint).png')
            
        else:
            self.playerImg = pygame.image.load('.\TankAssets\RedSoldier Paint\RedSoldierRight(Paint).png')
        
        self.x = x
        self.y = y

        self.x_origin = x_origin
        self.y_origin = y_origin
        self.dx = 0
        self.dy = 0
        self.lastDx = 1
        self.lastDy = 0

        self.width = 40
        self.height = 40
        
        self.bulletfired = 0
        self.bodycolour = bodycolour
        
        self.bullets = []
        self.grenades = []
        
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.fire = fire
        self.throw = throw

        self.fire_key_up = 0

        self.oldX = 0
        self.oldY = 0
        
        self.weaponclass = weaponclass

        self.weaponImg = pygame.image.load(r'.\\TankAssets\Weapon Paint\\' + str(self.weaponclass).upper() + '\\' + str(self.weaponclass) + ' Right.png')
        

        if self.weaponclass == 'ps':
            self.health = 92.5

        elif self.weaponclass == 'cs':
            self.health = 110

        elif self.weaponclass == 's':
            self.health = 75

        elif self.weaponclass == 'br':
            self.health = 95
            
        elif self.weaponclass == 'bp':
            self.health = 131

        elif self.weaponclass == 'ft':
            self.health = 105

        elif self.weaponclass == 'hmg':
            self.health = 120
            
        elif self.weaponclass == 'td':
            self.health = 325

        elif self.weaponclass == 'r':
            self.health = r_health

        elif self.weaponclass == 'mng':
            self.health = 142

        elif self.weaponclass == 'ml':
            self.health = 116

        elif self.weaponclass == 'hrpg':
            self.health = 135
            
        else:
            self.health = 100
        
        self.lastFire = 0
        self.lastThrow = 0
        self.isFiring = False
    
        self.startReload = 0
    
        self.firedBullets = 0
        self.thrownGrenades = 0
    
        self.speed = player_speeds[weaponclass]
        
    def damage(self, health):
        self.health -= health
        
    def move(self, player):
        self.oldX = self.x
        self.oldY = self.y
        if self.health <= 30:
            self.speed = player_speeds[self.weaponclass + '-low']

        if pressed[self.up]:
            self.dy = -self.speed
            self.lastDy = self.dy
            
        elif pressed[self.down]:
            self.dy = self.speed
            self.lastDy = self.dy
            
        else:
            if self.lastDx != 0:
                self.lastDy = 0
            self.dy = 0
            
        if pressed[self.left]:
            self.dx = -self.speed
            self.lastDx = self.dx
            
        elif pressed[self.right]:
            self.dx = self.speed
            self.lastDx = self.dx
            
        else:
            if self.lastDy != 0:
                self.lastDx = 0
            self.dx = 0


        self.x += self.dx
        if self.isOutOfBounds():
            self.x -= self.dx

        self.y += self.dy
        if self.isOutOfBounds():
            self.y -= self.dy

        if obstacles.isTouching(self):
            global blood_splatters            
            blood_splatters.append(BloodSpatter((randint(177, 200), 11, 11), self.x + 13.5, self.y + 13.5))
            
            self.last_hit = time.time()
            self.damage(0.25)
            self.x = self.oldX
            self.y = self.oldY

        if self.player == 'p1':
            if (self.dy / self.speed) == 1:
                self.playerImg = pygame.image.load('.\TankAssets\GreenSoldier Paint\GreenSoldierDown(Paint).png')
                
            elif (self.dy / self.speed) == -1:
                self.playerImg = pygame.image.load('.\TankAssets\GreenSoldier Paint\GreenSoldierUp(Paint).png')

            elif (self.dx / self.speed) == 1:
                self.playerImg = pygame.image.load('.\TankAssets\GreenSoldier Paint\GreenSoldierRight(Paint).png')
                
            elif (self.dx / self.speed) == -1:
                self.playerImg = pygame.image.load('.\TankAssets\GreenSoldier Paint\GreenSoldierLeft(Paint).png')

        else:
            if (self.dy / self.speed) == 1:
                self.playerImg = pygame.image.load('.\TankAssets\RedSoldier Paint\RedSoldierDown(Paint).png')

            elif (self.dy / self.speed) == -1:
                self.playerImg = pygame.image.load('.\TankAssets\RedSoldier Paint\RedSoldierUp(Paint).png')

            elif (self.dx / self.speed) == 1:
                self.playerImg = pygame.image.load('.\TankAssets\RedSoldier Paint\RedSoldierRight(Paint).png')
                
            elif (self.dx / self.speed) == -1:
                self.playerImg = pygame.image.load('.\TankAssets\RedSoldier Paint\RedSoldierLeft(Paint).png')

        if (self.dy / self.speed) == 1:
            self.weaponImg = pygame.image.load(r'.\\TankAssets\Weapon Paint\\' + str(self.weaponclass).upper() + '\\' + str(self.weaponclass) + ' Down.png')

        elif (self.dy / self.speed) == -1:
            self.weaponImg = pygame.image.load(r'.\\TankAssets\Weapon Paint\\' + str(self.weaponclass).upper() + '\\' + str(self.weaponclass) + ' Up.png')
            
        elif (self.dx / self.speed) == 1:
            self.weaponImg = pygame.image.load(r'.\\TankAssets\Weapon Paint\\' + str(self.weaponclass).upper() + '\\' + str(self.weaponclass) + ' Right.png')
                
        elif (self.dx / self.speed) == -1:
            self.weaponImg = pygame.image.load(r'.\\TankAssets\Weapon Paint\\' + str(self.weaponclass).upper() + '\\' + str(self.weaponclass) + ' Left.png')
            
        screen.blit(self.playerImg, (self.x, self.y))
        screen.blit(self.weaponImg, (self.x, self.y))

    def get_bullet_velocity(self, otherPlayer):
        horizontal = -(self.x - otherPlayer.x)
        vertical = -(self.y - otherPlayer.y)
        distance = ((vertical**2) + (horizontal**2)) ** 0.5
        dx = horizontal / distance
        dy = vertical / distance
        return (dx, dy)

    def isOutOfBounds(self):
        return (self.x <= 0 or self.x + self.width >= SCREEN_WIDTH) or (self.y <= 0 or self.y + self.height >= SCREEN_HEIGHT)
    
    def getReloadTime(self):
        return time.time() - self.startReload
    
    def outOfAmmo(self, weaponclass):
        if self.firedBullets == weapon_magazines[weaponclass]:
            self.isReloading = True
            self.firedBullets = 0
            return True
    
    def outOfGrenades(self):
        if self.thrownGrenades == weapon_grenade_count[self.weaponclass]:
            return True

    def reloaded(self, weaponclass):
        if self.getReloadTime() >= weapon_reloads[weaponclass]:
            self.isReloading = False
            return True

    def nested_fire_function(self):
        dx = self.dx
        dy = self.dy

        if dx == 0:
            dx = self.lastDx
        if dy == 0:
            dy = self.lastDy


        if dy >= 1:
            self.bulletspawn_x = self.x + 30
            self.bulletspawn_y = self.y + 30
            
        elif dy <= -1:
            self.bulletspawn_x = self.x
            self.bulletspawn_y = self.y
            
        elif dx >= 1:
            self.bulletspawn_x = self.x + 30
            self.bulletspawn_y = self.y
            
        elif dx <= -1:
            self.bulletspawn_x = self.x
            self.bulletspawn_y = self.y + 30
        
        if self.weaponclass == 'cs':
            self.firedBullets += 1
            for i in range(cs_pellets):
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                
                
        elif self.weaponclass == 'ps':
            self.firedBullets += 1
            for i in range(ps_pellets):
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                
                
        elif self.weaponclass == 'br':
            for i in range(br_burst):
                if dy == 0:
                    newBullet = Bullet(self.bulletspawn_x - 19 * (i - 1), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                    self.bullets.append(newBullet)
                    self.firedBullets += 1
                    
                elif dx == 0:
                    newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - 19 * (i - 1), dx, dy, self.weaponclass, self.x, self.y)
                    self.bullets.append(newBullet)
                    self.firedBullets += 1

        elif self.weaponclass == 'bp':
            for i in range(bp_burst):
                if dy == 0:
                    newBullet = Bullet(self.bulletspawn_x - 16 * (i - 1), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                    self.bullets.append(newBullet)
                    self.firedBullets += 1
                    
                elif dx == 0:
                    newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - 16 * (i - 1), dx, dy, self.weaponclass, self.x, self.y)
                    self.bullets.append(newBullet)
                    self.firedBullets += 1

        elif self.weaponclass == 'mar':
            if (time.time() - self.lastFire) - (time.time()- self.fire_key_up) >= 0:
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                self.firedBullets += 1

                    
        elif self.weaponclass == 'hmg':
            if dx == 0:
                newBullet = Bullet(self.bulletspawn_x - uniform(-10, 10), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                self.firedBullets += 1
                
            elif dy == 0:
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - uniform(-10, 10), dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                self.firedBullets += 1

        elif self.weaponclass == 'n':
            if len(self.bullets) < 100:
                newBullet = Bullet(self.x, self.y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                self.firedBullets += 1

        elif self.weaponclass == 't':
            if len(self.bullets) > (weapon_magazines['t'] - 1):
                del self.bullets[0]
                
            if len(self.bullets) < weapon_magazines['t']:
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                
        elif self.weaponclass == 'gl':
            newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self)
            self.grenades.append(newGrenade)
            self.firedBullets += 1

        elif self.weaponclass == 'ml':
            if len(self.grenades) > (weapon_magazines['ml'] - 1):
                self.grenades[0].detonate()
                
            if len(self.grenades) < weapon_magazines['ml']:
                newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self)
                self.grenades.append(newGrenade)

        elif self.weaponclass == 'sap':
            if (time.time() - self.lastFire) - (time.time()- self.fire_key_up) >= 0:
                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                self.bullets.append(newBullet)
                self.firedBullets += 1                       

        elif self.weaponclass == 'hrpg':
            if self.firedBullets == 0:
                if pressed[self.throw]:
                    newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self, straight_aim_hrpg=True)
                    self.grenades.append(newGrenade)
                    self.firedBullets += 1
                    self.isFiring = True

                else:
                    newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self)
                    self.grenades.append(newGrenade)
                    self.firedBullets += 1
                    self.isFiring = True
            else:
                return
            
        else:
            newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
            self.bullets.append(newBullet)
            self.firedBullets += 1
            
        self.lastFire = time.time()

    def bullet(self, weaponclass):
        if self.outOfAmmo(self.weaponclass):
            self.startReload = time.time()
            self.isReloading = True

        if (not self.outOfAmmo(self.weaponclass)) and self.reloaded(self.weaponclass):
            self.isReloading = False

        if pressed[self.fire]:
            if (self.getCooldown() > weapon_cooldowns[self.weaponclass]) and (not self.outOfAmmo(self.weaponclass)) and self.reloaded(self.weaponclass):
                self.nested_fire_function()

        if self.weaponclass == 'hrpg' and (time.time() - self.lastFire >= weapon_cooldowns['hrpg']) and self.isFiring and (not self.outOfAmmo('hrpg')) and (self.reloaded('hrpg')): 
            dx = self.dx
            dy = self.dy

            if dx == 0:
                dx = self.lastDx
            if dy == 0:
                dy = self.lastDy

            if dy >= 1:
                self.bulletspawn_x = self.x + 30
                self.bulletspawn_y = self.y + 30
            
            elif dy <= -1:
                self.bulletspawn_x = self.x
                self.bulletspawn_y = self.y
            
            elif dx >= 1:
                self.bulletspawn_x = self.x + 30
                self.bulletspawn_y = self.y

            elif dx <= -1:
                self.bulletspawn_x = self.x
                self.bulletspawn_y = self.y + 30
                    
            newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self)
            self.grenades.append(newGrenade)
            self.firedBullets += 1
            self.lastFire = time.time()
            if self.firedBullets == weapon_magazines['hrpg']:
                self.isFiring = False


        if pressed[self.throw]:
            if (self.getGrenadeCooldown() > weapon_cooldowns['g']) and (not self.outOfGrenades()):
                    self.lastThrow = time.time()
    
                    dx = self.dx
                    dy = self.dy
    
                    if dx == 0:
                        dx = self.lastDx
                    if dy == 0:
                        dy = self.lastDy
                        
                    if dy >= 1:
                        self.bulletspawn_x = self.x + 30
                        self.bulletspawn_y = self.y + 30
                        
                    elif dy <= -1:
                        self.bulletspawn_x = self.x
                        self.bulletspawn_y = self.y
                        
                    elif dx >= 1:
                        self.bulletspawn_x = self.x + 30
                        self.bulletspawn_y = self.y
                        
                    elif dx <= -1:
                        self.bulletspawn_x = self.x
                        self.bulletspawn_y = self.y + 30
    
                    newGrenade = Grenade(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self)
                    self.grenades.append(newGrenade)
                    self.thrownGrenades += 1

            elif self.weaponclass == 'hmg' and (len(self.grenades) == 1) and ((time.time() - self.lastThrow) > 0.5):
                self.grenades[0].detonate()
                    
    def moveBullet(self, otherPlayer):
        for bullet in self.bullets:
            if self.weaponclass == 'n':
                dx = self.dx
                dy = self.dy
                
                if dx == 0:
                    dx = self.lastDx
                if dy == 0:
                    dy = self.lastDy

                bullet.customMove(dx, dy)

            else:
                bullet.move()
            
            if bullet.isColliding(otherPlayer) or bullet.isOutOfBounds() or (self.weaponclass == 'cs' and bullet.cs_range()) or (self.weaponclass == 'ps' and bullet.ps_range()) or (self.weaponclass == 'bp' and bullet.bp_range()) or (self.weaponclass == 'ft' and bullet.ft_range()) or (self.weaponclass == 'sap' and bullet.sap_range()) or (self.weaponclass == 'mp' and bullet.mp_range()) or bullet.gls_range():
                self.bullets.remove(bullet)
                
        for grenade in self.grenades:
            grenade.move(otherPlayer)
            if grenade.isColliding(otherPlayer) or grenade.isOutOfBounds():
                grenade.detonate()
                
    def getCooldown(self):
        return time.time() - self.lastFire
    
    def getGrenadeCooldown(self):
        return time.time() - self.lastThrow

    def isDead(self):
        return self.health <= 0
    
    def isTouchingBullet(self, bullet):
        if self.weaponclass == 'ft':
            dist = math.sqrt(((bullet.x + 14) - (self.x + 20)) ** 2 + ((bullet.y + 14) - (self.y + 20)) ** 2)
            return dist <= 20

        elif self.weaponclass == 'ps' or self.weaponclass == 'cs':
            dist = math.sqrt(((bullet.x + 7) - (self.x + 20)) ** 2 + ((bullet.y + 7) - (self.y + 20)) ** 2)
            return dist <= 20
        
        else:
            dist = math.sqrt(((bullet.x + 8) - (self.x + 20)) ** 2 + ((bullet.y + 8) - (self.y + 20)) ** 2)
            return dist <= 20

p1 = Player('p1', 40, 40, (0, 100, 0), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SLASH, pygame.K_PERIOD, TankOptions.player1_weapon, 0, 0)
p2 = Player('p2', SCREEN_WIDTH - 80, SCREEN_HEIGHT - 80, (100, 0, 0), pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_q, pygame.K_e, TankOptions.player2_weapon, 0, 0)
obstacles = Obstacles(TankOptions.obstacles_frame_answer, TankOptions.maps_frame_answer)
blood_splatters = []

if p1.weaponclass == 'r':
    print('p1 dmg: ' + str(bullet_damages['r']))
    print('p1 fd: ' + str(weapon_cooldowns['r']))
    p1_dps = (1 / weapon_cooldowns['r']) * bullet_damages['r']
    print('p1 dps: ' + str(p1_dps))
    print('p1 health: ' + str(p1.health))
    print('p1 bpf: ' + str(bullet_penetration_factors['r']))
    

if p2.weaponclass == 'r':
    print('p2 dmg: ' + str(bullet_damages['r']))
    print('p2 fd: ' + str(weapon_cooldowns['r']))
    p2_dps = (1 / weapon_cooldowns['r']) * bullet_damages['r']
    print('p2 dps: ' + str(p2_dps))
    print('p2 health: ' + str(p2.health))
    print('p2 bpf: ' + str(bullet_penetration_factors['r']))
    
    
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SLASH:
                if time.time() - p1.fire_key_up > weapon_cooldowns[p1.weaponclass]:
                    p1.fire_key_up = time.time()

            if event.key == pygame.K_q: 
                if time.time() - p2.fire_key_up > weapon_cooldowns[p2.weaponclass]:
                    p2.fire_key_up = time.time()
    
    if p1.isDead():
        screenfill = (200, 200, 200)
        screen.fill(screenfill)
        screen.blit(p2victorytext, ((SCREEN_WIDTH / 2) - 180, (SCREEN_HEIGHT / 2) - 40))
        pygame.display.flip()
        clock.tick(1.53846153846)
        done = True
        
    elif p2.isDead():
        screenfill = (200, 200, 200)
        screen.fill(screenfill)
        screen.blit(p1victorytext, ((SCREEN_WIDTH / 2) - 200, (SCREEN_HEIGHT / 2) - 40))
        pygame.display.flip()
        clock.tick(1.53846153846)
        done = True
        
    else:
        if p1.health <= 30 and p2.health <= 30:
            screenfill = (214, 72, 72)
        else:
            screenfill = (140, 140, 140)

        screen.fill(screenfill)
        
        obstacles.draw()
        
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            done = True

        
        if p1.isReloading:
            p1ammocount = 'RELOADING...'
        else:
            p1ammocount = weapon_magazines[p1.weaponclass] - p1.firedBullets

        if p2.isReloading:
            p2ammocount = 'RELOADING...'
        else:
            p2ammocount = weapon_magazines[p2.weaponclass] - p2.firedBullets

        
        if (weapon_grenade_count[p1.weaponclass] - p1.thrownGrenades) == 0:
            p1_grenade_count = 'OUT OF GRENADES'
        else:
            p1_grenade_count = weapon_grenade_count[p1.weaponclass] - p1.thrownGrenades

        if (weapon_grenade_count[p2.weaponclass] - p2.thrownGrenades) == 0:
            p2_grenade_count = 'OUT OF GRENADES'
        else:
            p2_grenade_count = weapon_grenade_count[p2.weaponclass] - p2.thrownGrenades
            
            

        p1ammocountstr = str('GREEN AMMO: ' + str(p1ammocount))
        p2ammocountstr = str('RED AMMO: ' + str(p2ammocount))

        p1_grenade_count_str = str('GREEN GRENADES: ' + str(p1_grenade_count))
        p2_grenade_count_str = str('RED GRENADES: ' + str(p2_grenade_count))
                           

        p1ammotext = myfont2.render(p1ammocountstr, False, (0, 90, 0))
        p2ammotext = myfont2.render(p2ammocountstr, False, (90, 0, 0))

        p1_grenade_text = myfont3.render(p1_grenade_count_str, False, (0, 70, 0))
        p2_grenade_text = myfont3.render(p2_grenade_count_str, False, (70, 0, 0))

        
        screen.blit(p1ammotext, (SCREEN_WIDTH - 400, 20))
        screen.blit(p2ammotext, (SCREEN_WIDTH - 400, 85))
        
        screen.blit(p1_grenade_text, (SCREEN_WIDTH - 400, 50))
        screen.blit(p2_grenade_text, (SCREEN_WIDTH - 400, 115))

        
        p1.move('p1')
        p2.move('p2')
        
        p1.bullet(p1.weaponclass)
        p2.bullet(p2.weaponclass)
        
        p1.moveBullet(p2)
        p2.moveBullet(p1)


        for turret in turrets:
            for bullet in p1.bullets:
                if turret.isTouching(bullet):
                    turret.health -= 1 * bullet_penetration_factors[bullet.weaponclass]
                    turret.last_hit = time.time()
                    
            for bullet in p2.bullets:
                if turret.isTouching(bullet):
                    print('The baby turret was shot')
                    turret.health -= 1 * bullet_penetration_factors[bullet.weaponclass]
                    turret.last_hit = time.time()
                    
            if turret.health <= 0:
                new_sds = Grenade(turret.x + 3, turret.y + 3, 0, 0, turret)
                turret_sds.append(new_sds)
                new_sds = Grenade(turret.x + 3, turret.y + 3, 0, 0, turret)
                turret_sds.append(new_sds)

                turret_sds[-1].detonate()
                turret_sds[-1].detonate()
                
                turrets.remove(turret)
                
                

            turret.target(p1, p2)
            turret.draw()
            healthBar(turret, (0, 0, 150), turret.x, turret.y, turret.health, turret.radius, 6) 
            
            
        for bullet in turret_bullets:
            bullet.move()
            if bullet.isColliding(p1) or bullet.isColliding(p2) or bullet.st_range() or bullet.isOutOfBounds() or bullet.gls_range():
                turret_bullets.remove(bullet)
                    
        
        for splatter in blood_splatters:
            splatter.draw()
                         
        for obstacle in obstacles.obstacles:
            healthBar(obstacle, (0, 0, 150), obstacle.x, obstacle.y, obstacle.health, obstacle.radius, 12)  

        for player in [p1, p2]:
            if player.health <= 30:
                healthBar(player, (0, 0, 150), player.x, player.y, player.health, 40, 4)
                
            else:
                healthBar(player, player.bodycolour, player.x, player.y, player.health, 40, 4)

                      
                         
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
