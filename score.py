from settings import Settings
import pygame


class Score(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.image = pygame.image.load(self.settings.score_image)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def blit(self):
        self.screen.blit(self.image, self.rect)
