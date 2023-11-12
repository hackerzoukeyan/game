from settings import Settings
import pygame


class Brick(pygame.sprite.Sprite):
    def __init__(self, game, x, y):
        super().__init__()
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.rect = pygame.Rect(0, 0, self.settings.brick_width, self.settings.brick_height)
        self.rect.x = x
        self.rect.y = y

    def blit(self):
        pygame.draw.rect(self.screen, self.settings.brick_color, self.rect)
