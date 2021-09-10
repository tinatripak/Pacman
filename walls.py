import pygame


class Walls(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, colour):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(colour)
        # rectangle
        self.rect = self.image.get_rect()
        self.rect.left = x
        self.rect.top = y
