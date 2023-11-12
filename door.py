from settings import Settings
import pygame


class Door(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.x, self.y = x, y
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.image = pygame.image.load(self.settings.door_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
        self.opened = False

    def open(self):
        self.opened = True
        self.image = pygame.image.load(self.settings.door_opened_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def blit(self):
        self.screen.blit(self.image, self.rect)
