from settings import Settings
import pygame
import time


class Monster(pygame.sprite.Sprite):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.image = pygame.image.load(self.settings.monster_image)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midtop
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = True
        self.moving_left = False
        self.falling = False
        self.start_time = int(time.time())

    def check_fall(self):
        self.falling = True
        for x in self.game.bricks:
            if self.rect.bottom == x.rect.top:
                if x.rect.left <= self.rect.centerx <= x.rect.right:
                    self.falling = False

    def change_direction(self):
        if self.moving_right is True:
            self.moving_left = True
            self.moving_right = False
        else:
            self.moving_right = True
            self.moving_left = False

    def update(self):
        end_time = int(time.time())
        if end_time - self.start_time == self.settings.monster_time:
            self.change_direction()
            self.start_time = int(time.time())
        self.check_fall()
        if self.falling:
            self.y += self.settings.monster_jump_speed
        if self.moving_right:
            self.x += self.settings.monster_speed
        if self.moving_left:
            self.x -= self.settings.monster_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blit(self):
        self.screen.blit(self.image, self.rect)
