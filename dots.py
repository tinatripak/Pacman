import pygame


class Dots(pygame.sprite.Sprite):
    def __init__(self, width, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect()
