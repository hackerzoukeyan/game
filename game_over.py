from settings import Settings
import pygame.font


class GameOver:
    def __init__(self, game):
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.font = pygame.font.SysFont(None, 100)

    def blit(self):
        text = self.font.render(f'Game Over(press Q to quit.)', True, self.settings.sb_color)
        rect = text.get_rect()
        rect.center = self.screen_rect.center
        self.screen.blit(text, rect)
