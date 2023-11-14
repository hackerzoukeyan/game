from settings import Settings
import pygame.font


class ScoreBoard:
    def __init__(self, game):
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.font = pygame.font.SysFont(None, 50)
        self.high_score = int(open('high_score.txt', encoding='utf-8').read())
        self.level = int(open('level.txt', encoding='utf-8').read())

    def check_high_score(self):
        if self.game.score > self.high_score:
            self.high_score = self.game.score

    def save_high_score(self):
        open('high_score.txt', 'w', encoding='utf-8').write(str(self.high_score))

    def save_level(self):
        if self.level < self.settings.max_level:
            open('level.txt', 'w', encoding='utf-8').write(str(self.level))
        if self.level == self.settings.max_level and self.game.msg.msg == 'You win!(Press Q to quit.)':
            open('level.txt', 'w', encoding='utf-8').write('1')

    def blit(self):
        text = self.font.render(
            f'Level: {self.level} Score: {self.game.score} High Score: {self.high_score}', True, self.settings.sb_color
        )
        rect = text.get_rect()
        rect.midtop = self.screen_rect.midtop
        self.screen.blit(text, rect)
