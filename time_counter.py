from settings import Settings
import pygame.font
import time


class TimeCounter:
    def __init__(self, game):
        self.time = int(time.time())
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.font = pygame.font.SysFont(None, 100)

    def zero(self):
        self.time = int(time.time())

    def timeout(self):
        now = int(time.time())
        if now - self.time == self.settings.time:
            return True

    def blit(self):
        now = int(time.time())
        text = self.font.render(str(self.settings.time - (now - self.time)), True, self.settings.sb_color)
        rect = text.get_rect()
        rect.topright = self.screen_rect.topright
        self.screen.blit(text, rect)
