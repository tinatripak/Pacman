import pygame


class Player(pygame.sprite.Sprite):
    change_x = 0
    change_y = 0
    playerLives = 3

    def __init__(self, x, y, filename):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename)
        self.rect = self.image.get_rect()
        self.rect.top = y
        self.rect.left = x
        self.prev_x = x
        self.prev_y = y

    def change_speed_player(self, x, y):
        if self.rect.x > 587:
            self.rect.x = 17
        if self.rect.x < 17:
            self.rect.x = 587
        self.change_x += x
        self.change_y += y

    def clear_speed_player(self):
        self.prev_x = self.change_x
        self.prev_y = self.change_y

    def new_position_player(self, walls, spawn):
        old_x = self.rect.left
        new_x = old_x + self.change_x
        self.rect.left = new_x
        old_y = self.rect.top
        new_y = old_y + self.change_y

        x_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
        if x_sprite_collide:
            self.rect.left = old_x
        else:
            self.rect.top = new_y
            y_sprite_collide = pygame.sprite.spritecollide(self, walls, False)
            if y_sprite_collide:
                self.rect.top = old_y

        if spawn:
            spawn_sprite_collide = pygame.sprite.spritecollide(self, spawn, False)
            if spawn_sprite_collide:
                self.rect.left = old_x
                self.rect.top = old_y
