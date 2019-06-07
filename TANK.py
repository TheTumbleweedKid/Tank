import pygame
import time
import math
from random import uniform, randrange, randint
import os, sys

from TankAssets import *

import TankOptions


pygame.init()
pygame.font.init()

SCREEN_WIDTH = 1500
SCREEN_HEIGHT = 1000

clock = pygame.time.Clock() 
done = False

cs_pellets = 10
ps_pellets = 14

r_burst = 3
p_burst = 2

rSpeed = uniform(4, 7)

weapon_cooldowns = {
    "smg": 0.065,
    "mg": 0.1125,
    "hmg": 0.2,
    "t": 0.01,
    "n": 0.095,
    "ss": 1.5,
    "s": 0.65,
    "cs":0.25,
    "ps": 0.75,
    "r": uniform(0.01, 0.5),
    "br": 0.35,
    "bp": 0.325,
    "ft": 0.0000001,
    "D": 0.0005,
    "td": 5
}

weapon_magazines = {
    "smg": 25,
    "mg": 35,
    "hmg": 65,
    "t": 130,
    "n": 100,
    "ss": 6,
    "s": 10,
    "cs": 14,
    "ps": 8,
    "r": randint(15, 65),
    "br": 10,
    "bp": 7,
    "ft": 900,
    "D": 1000,
    "td": 3
}

weapon_reloads = {
    "smg": 2,
    "mg": 2.5,
    "hmg": 3.5,
    "t": 0,
    "n": 0,
    "ss": 4,
    "s": 3,
    "cs": 3,
    "ps": 3,
    "r": uniform(1.5, 8),
    "br": 3,
    "bp": 1.4,
    "ft": 4,
    "D": 4,
    "td": 3
}

player_speeds = {
    "smg": 6.5,
    "smg-low": 7,
    
    "s": 6,
    "s-low": 6.5,
    
    "t": 6.5,
    "t-low": 7,
    
    "n": 5,
    "n-low": 5.5,
    
    "mg": 6.25,
    "mg-low": 6.75,
    
    "ss": 4.75,
    "ss-low": 5.25,
    
    "hmg": 4.5,
    "hmg-low": 5.5,

    "cs": 6.25,
    "cs-low": 6.75,

    "ps": 6.5,
    "ps-low": 7,

    "r": rSpeed,
    "r-low": rSpeed + 0.5,

    "br": 6,
    "br-low": 6.5,

    "bp": 7,
    "bp-low":7.5,

    "ft": 5.5,
    "ft-low": 6,
    
    "D": 7,
    "D-low": 7.5,

    "td": 4.5,
    "td-low":5.5,
}

bullet_speeds = {
    "smg": 11,
    "mg": 12,
    "hmg": 10,
    "t": 0,
    "n": 6,
    "ss": 19,
    "s": 16.5,
    "cs": 18,
    "ps": 19,
    "r": randint(5, 19),
    "br": 16,
    "bp": 15,
    "ft": 8,
    "D": 21,
    "td": 17
}

bullet_damages = {
    "smg": 3.5,
    "mg": 5,
    "hmg": 8,
    "t": 1,
    "n": 1,
    "ss": 65,
    "s": 35,
    "cs": 3,
    "ps": 4.75,
    "r": uniform(0.01, randint(40, 60)),
    "br": 5,
    "bp": 4.5,
    "ft": uniform(1, 1.75),
    "D": 4.5,
    "td": 100
}

obstacle_numbers = {
    "m": [12, 17],
    "l": [7, 12],
    "h": [18, 23],
    "c": [42, 60],
    "b": [56, 65],
    "n": [0, 1],
    "i": [97, 125]
}

def specialRound(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1

    return 0

bulletcolour = (255, 180, 180)
ft_bulletcolour = (255, 180, 180)

myfont = pygame.font.SysFont("Impact", 80)
myfont2 = pygame.font.SysFont("Bahnscrift", 5)
myfont3 = pygame.font.SysFont("Bahnscrift", 40)

p1victorytext = myfont.render("GREEN WINS!", False, (0, 100, 0))
p2victorytext = myfont.render("RED WINS!", False, (100, 0, 0))

p1ammocount = 0
p2ammocount = 0

p1ammocountstr = str()
p2ammocountstr = str()

screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

SCREEN_WIDTH = screen.get_width()
SCREEN_HEIGHT = screen.get_height()

def getx():
    x = randrange(25, (SCREEN_WIDTH - 40))
    return x
def gety():
    y = randrange(25, (SCREEN_HEIGHT - 40))
    return y

class BloodSpatter:
    def __init__(self, colour, x, y):
        self.x = x
        self.y = y
        self.width = randint(11, 15)
        self.height = randint(11, 15)
        self.colour = colour

    def draw(self):
        pygame.draw.ellipse(screen, self.colour, pygame.Rect(self.x, self.y, self.width, self.height))

class Obstacle:
    def __init__(self, colour, x, y):
        self.x = x
        self.y = y
        self.width = 60
        self.height = 60
        self.colour = colour
        
    def create_obstacle(self):
        pygame.draw.ellipse(screen, self.colour, pygame.Rect(self.x, self.y, 60, 60))

    def isTouching(self, other):
        dist = math.sqrt(((other.x + 20) - (self.x + 30)) ** 2 + ((other.y + 20) - (self.y + 30)) ** 2)

        if type(other) == Bullet:
            return dist <= 34
        elif type(other) == Obstacle:
            return dist <= self.width
        else:
            return dist <= self.width*0.8

class Obstacles:
    def __init__(self, num_of_obs):
        self.obstacles = []
        self.num_of_obs = num_of_obs


        range_1 = obstacle_numbers[num_of_obs][0]
        range_2 = obstacle_numbers[num_of_obs][1]
        
        for i in range(randrange(range_1, range_2)):
            while True:
                newObstacle = Obstacle((119, 49, 19), getx(), gety())
                if not self.isTouching(newObstacle) and not newObstacle.isTouching(p1) and not newObstacle.isTouching(p2):
                    self.obstacles.append(newObstacle)
                    break
 
    def isTouching(self, object):
        for obstacle in self.obstacles:
            
            if obstacle.isTouching(object):
                return True

        return False

    def draw(self):
        for obstacle in self.obstacles:
            obstacle.create_obstacle()

class Bullet:
    def __init__(self, x, y, dx, dy, weaponclass, x_origin, y_origin):
        self.csbullet_range = 300
        self.psbullet_range = 560
        self.bpbullet_range = 800
        self.ftfire_range = uniform(160, 280)
        self.ftbullet_colour = (uniform(253, 255), uniform(110, 150), uniform(35, 55))
        self.x = x
        self.y = y
        
        self.x_origin = x_origin
        self.y_origin = y_origin
        
        self.weaponclass = weaponclass

        self.dx = self.bulletSpeed(specialRound(dx))
        self.dy = self.bulletSpeed(specialRound(dy))
        
        if weaponclass == "cs":
            self.dx += uniform(-6, 6)
            self.dy += uniform(-6, 6)
            
        if weaponclass == "ps":
            self.dx += uniform(-2.5, 2.5)
            self.dy += uniform(-2.5, 2.5)
            
        if weaponclass == "smg":
            self.dx += uniform(-0.65, 0.65)
            self.dy += uniform(-0.65, 0.65)
            
        if weaponclass == "mg":
            self.dx += uniform(-0.19, 0.19)
            self.dy += uniform(-0.19, 0.19)
            
        if weaponclass == "br":
            self.dx += uniform(-0.05, 0.05)
            self.dy += uniform(-0.05, 0.05)
            
        if weaponclass == "s":
            self.dx += uniform(-0.05, 0.05)
            self.dy += uniform(-0.05, 0.05)
            
        if weaponclass == "ft":
            self.dx += uniform(-2, 2)
            self.dy += uniform(-2, 2)

        if weaponclass == "r":
            self.dx += uniform(-uniform(0, 3), uniform(0, 3))
            self.dy += uniform(-uniform(0, 3), uniform(0, 3))

        if weaponclass == "D":
            self.dx += uniform(-uniform(0, 1.25), uniform(0, 1.25))
            self.dy += uniform(-uniform(0, 1.25), uniform(0, 1.25))
            
        if self.weaponclass == "ft":
            self.damage = uniform(1, 1.75)
            
        else:
            self.damage = bullet_damages[weaponclass]
        
        self.width = 14
        self.height = 14
    
    def move(self):
        self.x += self.dx
        self.y += self.dy
        
        if self.weaponclass == "ft":
            pygame.draw.ellipse(screen, self.ftbullet_colour, pygame.Rect(self.x, self.y, 14, 14))
            
        elif self.weaponclass == "ps" or self.weaponclass == "cs":
            pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 7, 7))   
        else:
            pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 8, 8))

    def customMove(self, dx, dy):
        self.x += self.bulletSpeed(specialRound(dx))
        self.y += self.bulletSpeed(specialRound(dy))

        pygame.draw.ellipse(screen, bulletcolour, pygame.Rect(self.x, self.y, 8, 8))

    def isColliding(self, player):
        if player.isTouchingBullet(self):
            global blood_splatters            
            blood_splatters.append(BloodSpatter((randint(227, 250), 51, 51), player.x + uniform(-33.5, 33.5), player.y + uniform(-33.5, 33.5)))
            
            player.health -= self.damage
            return True

        if obstacles.isTouching(self):
            return True

    def ps_range(self):
        dx = (self.x - self.x_origin)
        dy = (self.y - self.y_origin)
        if math.sqrt(dx**2 + dy**2) >= self.psbullet_range:
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
        
        
    def bulletSpeed(self, x):
        return x * bullet_speeds[self.weaponclass]

    def isOutOfBounds(self):
        return ((self.x < 0 or self.x + self.width > SCREEN_WIDTH) or (self.y < 0 or self.y + self.height > SCREEN_HEIGHT))
    
class Player:
    def __init__(self, player, x, y, bodycolour, left, right, up, down, fire, weaponclass, x_origin, y_origin):
        self.player = player
        self.isReloading = False
        if self.player == "player1":
            self.playerImg = pygame.image.load(".\TankAssets\GreenSoldier Paint\GreenSoldierDown(Paint).png")
        else:
            self.playerImg = pygame.image.load(".\TankAssets\RedSoldier Paint\RedSoldierDown(Paint).png")
            
        
        self.psbullet_range = 560
        self.csbullet_range = 300
        self.bpbullet_range = 800
        self.ftfire_range = uniform(140, 160)
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
        
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.fire = fire

        self.oldX = 0
        self.oldY = 0
        
        self.weaponclass = weaponclass

        self.weaponImg = pygame.image.load(r".\\TankAssets\Weapon Paint\\" + str(self.weaponclass).upper() + "\\" + str(self.weaponclass) + " Down.png")
        

        if self.weaponclass == "ps":
            self.health = 115

        elif self.weaponclass == "cs":
            self.health = 115

        elif self.weaponclass == "s":
            self.health = 85

        elif self.weaponclass == "bp":
            self.health = 120

        elif self.weaponclass == "ft":
            self.health = 105

        elif self.weaponclass == "hmg":
            self.health = 120
            
        elif self.weaponclass == "td":
            self.health = 325
            
        else:
            self.health = 100
        
        self.lastFire = 0
        self.startReload = 0
        self.firedBullets = 0
        self.speed = player_speeds[weaponclass]
        
    def damage(self, health):
        self.health -= health
        
    def move(self, player):
        self.oldX = self.x
        self.oldY = self.y
        if self.health <= 3:
            self.speed = player_speeds[self.weaponclass + "-low"]

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
            blood_splatters.append(BloodSpatter((randint(227, 250), 51, 51), self.x + 13.5, self.y + 13.5))
            
            self.damage(0.25)
            self.x = self.oldX
            self.y = self.oldY

        if self.player == "player1":
            if (self.dy / self.speed) == 1:
                self.playerImg = pygame.image.load(".\TankAssets\GreenSoldier Paint\GreenSoldierDown(Paint).png")
                
            elif (self.dy / self.speed) == -1:
                self.playerImg = pygame.image.load(".\TankAssets\GreenSoldier Paint\GreenSoldierUp(Paint).png")

            elif (self.dx / self.speed) == 1:
                self.playerImg = pygame.image.load(".\TankAssets\GreenSoldier Paint\GreenSoldierRight(Paint).png")
                
            elif (self.dx / self.speed) == -1:
                self.playerImg = pygame.image.load(".\TankAssets\GreenSoldier Paint\GreenSoldierLeft(Paint).png")

        else:
            if (self.dy / self.speed) == 1:
                self.playerImg = pygame.image.load(".\TankAssets\RedSoldier Paint\RedSoldierDown(Paint).png")

            elif (self.dy / self.speed) == -1:
                self.playerImg = pygame.image.load(".\TankAssets\RedSoldier Paint\RedSoldierUp(Paint).png")

            elif (self.dx / self.speed) == 1:
                self.playerImg = pygame.image.load(".\TankAssets\RedSoldier Paint\RedSoldierRight(Paint).png")
                
            elif (self.dx / self.speed) == -1:
                self.playerImg = pygame.image.load(".\TankAssets\RedSoldier Paint\RedSoldierLeft(Paint).png")

        if (self.dy / self.speed) == 1:
            self.weaponImg = pygame.image.load(r".\\TankAssets\Weapon Paint\\" + str(self.weaponclass).upper() + "\\" + str(self.weaponclass) + " Down.png")

        elif (self.dy / self.speed) == -1:
            self.weaponImg = pygame.image.load(r".\\TankAssets\Weapon Paint\\" + str(self.weaponclass).upper() + "\\" + str(self.weaponclass) + " Up.png")
            
        elif (self.dx / self.speed) == 1:
            self.weaponImg = pygame.image.load(r".\\TankAssets\Weapon Paint\\" + str(self.weaponclass).upper() + "\\" + str(self.weaponclass) + " Right.png")
                
        elif (self.dx / self.speed) == -1:
            self.weaponImg = pygame.image.load(r".\\TankAssets\Weapon Paint\\" + str(self.weaponclass).upper() + "\\" + str(self.weaponclass) + " Left.png")
            
        screen.blit(self.playerImg, (self.x, self.y))
        screen.blit(self.weaponImg, (self.x, self.y))
        
    def isOutOfBounds(self):
        return (self.x <= 0 or self.x + self.width >= SCREEN_WIDTH) or (self.y <= 0 or self.y + self.height >= SCREEN_HEIGHT)
    
    def getReloadTime(self):
        return time.time() - self.startReload
    
    def outOfAmmo(self, weaponclass):
        if self.firedBullets == weapon_magazines[weaponclass]:
            self.isReloading = True
            self.firedBullets = 0
            return True

    def reloaded(self, weaponclass):
        if self.getReloadTime() >= weapon_reloads[weaponclass]:
            self.isReloading = False
            return True

    def bullet(self, weaponclass):
        if self.outOfAmmo(self.weaponclass):
            self.startReload = time.time()
            self.isReloading = True

        if (not self.outOfAmmo(self.weaponclass)) and self.reloaded(self.weaponclass):
            self.isReloading = False

              
        if pressed[self.fire]:
            if (self.getCooldown() > weapon_cooldowns[self.weaponclass]) and (not self.outOfAmmo(self.weaponclass)) and self.reloaded(self.weaponclass):
                    self.lastFire = time.time()
                    self.firedBullets += 1
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
                    
                    if self.weaponclass == "cs":
                        for i in range(cs_pellets):
                            newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)
                            
                    elif self.weaponclass == "ps":
                        for i in range(ps_pellets):
                            newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)

                            
                    elif self.weaponclass == "br":
                        for i in range(r_burst):
                            if dy == 0:
                                newBullet = Bullet(self.bulletspawn_x - 14 * (i - 1), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                                self.bullets.append(newBullet)
                            elif dx == 0:
                                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - 14 * (i - 1), dx, dy, self.weaponclass, self.x, self.y)
                                self.bullets.append(newBullet)

                    elif self.weaponclass == "bp":
                        for i in range(p_burst):
                            if dy == 0:
                                newBullet = Bullet(self.bulletspawn_x - 16 * (i - 1), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                                self.bullets.append(newBullet)
                            elif dx == 0:
                                newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - 16 * (i - 1), dx, dy, self.weaponclass, self.x, self.y)
                                self.bullets.append(newBullet)
                                
                    elif self.weaponclass == "hmg":
                        if dx == 0:
                            newBullet = Bullet(self.bulletspawn_x - uniform(-8, 8), self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)
                        elif dy == 0:
                            newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y - uniform(-8, 8), dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)

                    elif self.weaponclass == "n":
                        if len(self.bullets) < 100:
                            newBullet = Bullet(self.x, self.y, dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)

                    elif self.weaponclass == "t":
                        if len(self.bullets)>= 129:
                            del self.bullets[0]
                            
                        if len(self.bullets) < 130:
                            newBullet = Bullet(self.x, self.y, dx, dy, self.weaponclass, self.x, self.y)
                            self.bullets.append(newBullet)
                            
                    else:
                        newBullet = Bullet(self.bulletspawn_x, self.bulletspawn_y, dx, dy, self.weaponclass, self.x, self.y)
                        self.bullets.append(newBullet)
                        
    def moveBullet(self, otherPlayer):
        for bullet in self.bullets:
            if self.weaponclass == "n":
                dx = self.dx
                dy = self.dy
                
                if dx == 0:
                    dx = self.lastDx
                if dy == 0:
                    dy = self.lastDy

                bullet.customMove(dx, dy)
            else:
                bullet.move()

            if bullet.isColliding(otherPlayer) or bullet.isOutOfBounds() or (self.weaponclass == "cs" and bullet.cs_range()) or (self.weaponclass == "ps" and bullet.ps_range()) or (self.weaponclass == "bp" and bullet.bp_range()) or (self.weaponclass == "ft" and bullet.ft_range()):
                self.bullets.remove(bullet)

    def getCooldown(self):
        return time.time() - self.lastFire

    def isDead(self):
        return self.health <= 0
    
    def isTouchingBullet(self, bullet):
        if self.weaponclass == "ft":
            dist = math.sqrt(((bullet.x + 14) - (self.x + 20)) ** 2 + ((bullet.y + 14) - (self.y + 20)) ** 2)
            return dist <= 20

        elif self.weaponclass == "ps" or self.weaponclass == "cs":
            dist = math.sqrt(((bullet.x + 7) - (self.x + 20)) ** 2 + ((bullet.y + 7) - (self.y + 20)) ** 2)
            return dist <= 20
        
        else:
            dist = math.sqrt(((bullet.x + 8) - (self.x + 20)) ** 2 + ((bullet.y + 8) - (self.y + 20)) ** 2)
            return dist <= 20

p1 = Player("player1", 40, 40, (0, 100, 0), pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN, pygame.K_SLASH, TankOptions.player1_weapon.value, 0, 0)
p2 = Player("player2", 1460, 960, (100, 0, 0), pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s, pygame.K_q, TankOptions.player2_weapon.value, 0, 0)
obstacles = Obstacles(TankOptions.obstacles_frame.value)
blood_splatters = []

if p1.weaponclass == "r":
    print("p1 dmg: " + str(bullet_damages["r"]))

if p2.weaponclass == "r":
    print("p2 dmg: " + str(bullet_damages["r"]))

if p1.weaponclass == "r":
    print("p1 fd: " + str(weapon_cooldowns["r"]))

if p2.weaponclass == "r":
    print("p2 fd: " + str(weapon_cooldowns["r"]))
    
    
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
            break
    
    if p1.isDead():
        screenfill = (200, 200, 200)
        screen.fill(screenfill)
        screen.blit(p2victorytext, ((SCREEN_WIDTH / 2) - 180, (SCREEN_HEIGHT / 2) - 40))
        print("gg 2fez u thot")
        pygame.display.flip()
        clock.tick(1.53846153846)
        done = True
        
    elif p2.isDead():
        screenfill = (200, 200, 200)
        screen.fill(screenfill)
        screen.blit(p1victorytext, ((SCREEN_WIDTH / 2) - 200, (SCREEN_HEIGHT / 2) - 40))
        print("gg 2fez u thot")
        pygame.display.flip()
        clock.tick(1.53846153846)
        done = True
        
    else:
        if p1.health <= 30 and p2.health <= 30:
            screenfill = (200, 40, 40)
        else:
            screenfill = (140, 140, 140)

        screen.fill(screenfill)

        
        obstacles.draw()
        
        pressed = pygame.key.get_pressed()

        if pressed[pygame.K_ESCAPE]:
            done = True
        
        if p1.isReloading:
            p1ammocount = "RELOADING..."

        else:
            p1ammocount = weapon_magazines[p1.weaponclass] - p1.firedBullets

            
        if p2.isReloading:
            p2ammocount = "RELOADING..."

        else:
            p2ammocount = weapon_magazines[p2.weaponclass] - p2.firedBullets

        p1ammocountstr = str("GREEN AMMO: " + str(p1ammocount))
        p2ammocountstr = str("RED AMMO: " + str(p2ammocount))

        p1healthstr = str()
        p2healthstr = str()
        
        p1healthint = int(p1.health / 1.65)
        p2healthint = int(p2.health / 1.65)
        
        for i in range(0, p1healthint):
            p1healthstr = str(p1healthstr + "|")
            
        for i in range(0, p2healthint):
            p2healthstr = str(p2healthstr + "|")
            
        p1healthtext = myfont2.render(p1healthstr, False, (0, 100, 0))
        p2healthtext = myfont2.render(p2healthstr, False, (100, 0, 0))
        
        p1ammotext = myfont3.render(p1ammocountstr, False, (0, 100, 0))
        p2ammotext = myfont3.render(p2ammocountstr, False, (100, 0, 0))

        if p1.health <= 30 and not p2.health <= 30:
            p1healthtext = myfont2.render(p1healthstr, False, (0, 0, 150))
        
        if p2.health <= 30 and not p1.health <= 30:
            p2healthtext = myfont2.render(p2healthstr, False, (0, 0, 150))
        
        screen.blit(p1healthtext, (p1.x - (p1healthint / 6.5), p1.y - 5))
        screen.blit(p2healthtext, (p2.x - (p2healthint / 6.5), p2.y - 5))

        screen.blit(p1ammotext, (SCREEN_WIDTH - 400, 20))
        screen.blit(p2ammotext, (SCREEN_WIDTH - 400, 80))

        
        p1.move("player1")
        p2.move("player2")
        
        p1.bullet(p1.weaponclass)
        p2.bullet(p2.weaponclass)
        
        p1.moveBullet(p2)
        p2.moveBullet(p1)
        
        for splatter in blood_splatters:
            splatter.draw()
        
    pygame.display.flip()
    clock.tick(60)
    
pygame.quit()
