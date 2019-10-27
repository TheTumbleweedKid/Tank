import pygame


def getx():
    x = randrange(20, (SCREEN_WIDTH - 40))
    return x

def gety():
    y = randrange(20, (SCREEN_HEIGHT - 40))
    return y


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

        if use_maps == "n":
            range_1 = obstacle_numbers[num_of_obs][0]
            range_2 = obstacle_numbers[num_of_obs][1]
            for i in range(randrange(range_1, range_2)):
                while True:
                    new_obstacle = Obstacle((87, 55, 41), getx(), gety(), uniform(20, uniform(32, 40)))
                    if not self.isTouching(new_obstacle) and not new_obstacle.isTouching(p1) and not new_obstacle.isTouching(p2):
                        self.obstacles.append(new_obstacle)
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

    def isTouching(self, object):
        for obstacle in self.obstacles:
            if obstacle.isTouching(object):
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