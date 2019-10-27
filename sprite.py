import pygame
import os


class Sprite:

    def __init__(self, file_name, width=20, height=20):
        path = os.path.join(os.getcwd(), 'assets')
        
        self.original_image = pygame.image.load(os.path.join(path, file_name))
        self.original_image = pygame.transform.scale(self.original_image, (width, height))

        self.original_rect = self.original_image.get_rect()

        self.rotated_image = self.original_image
    
    def draw(self, surface, x, y):
        surface.blit(self.rotated_image, (x, y))
        
    def rotate(self, angle):
        angle -= 180

        self.rotated_image = pygame.transform.rotate(self.original_image, angle)

        rotated_rect = self.original_rect.copy()
        rotated_rect.center = self.rotated_image.get_rect().center

        self.rotated_image = self.rotated_image.subsurface(rotated_rect).copy()
        
    def update_rotation(self):
        self.sprite.rotate(self.rotation)

        radians = self.rotation * (math.pi / 180)

        self.dx = round(self.speed*math.sin(radians), 2)
        self.dy = round(self.speed*math.cos(radians), 2)