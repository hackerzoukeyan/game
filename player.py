from settings import Settings
import pygame.font


class Player:
    def __init__(self, game):
        self.game = game
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.image = pygame.image.load(self.settings.player_right_image)
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
        self.moving_right = False
        self.moving_left = False
        self.jumping = False
        self.jump_up_value = 0
        self.falling = False
        self.life_count = LifeCount(self.game)

    def to_left(self):
        self.image = pygame.image.load(self.settings.player_left_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def to_right(self):
        self.image = pygame.image.load(self.settings.player_right_image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = self.x, self.y

    def check_fall(self):
        if self.falling:
            self.jumping = False
        if self.jumping:
            self.falling = False
        else:
            self.falling = True
            if self.rect.bottom == self.screen_rect.bottom:
                self.falling = False
            if self.rect.top == self.screen_rect.top:
                self.falling = True
            for x in self.game.bricks:
                if self.rect.bottom == x.rect.top:
                    if x.rect.left <= self.rect.centerx <= x.rect.right:
                        self.falling = False

    def update(self):
        self.check_fall()
        if self.jumping:
            if self.jump_up_value < self.settings.player_jump_high:
                self.jump_up_value += self.settings.player_jump_speed
                self.y -= self.settings.player_jump_speed
            else:
                self.jumping = False
        elif self.falling:
            self.y += self.settings.player_jump_speed
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.to_right()
            self.x += self.settings.player_speed
        if self.moving_left and self.rect.left > 0:
            self.to_left()
            self.x -= self.settings.player_speed
        self.rect.x = self.x
        self.rect.y = self.y

    def blit(self):
        self.screen.blit(self.image, self.rect)
        self.life_count.blit()


class LifeCount:
    def __init__(self, game):
        self.game = game
        self.count = 0
        self.screen: pygame.surface.Surface = self.game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = Settings()
        self.font = pygame.font.SysFont(None, 100)
        self.colors = (255, 0, 0), (255, 120, 0), (0, 255, 0), (0, 0, 0)

    def blit(self):
        text = self.font.render(str(self.count), True, self.colors[self.count - 1])
        rect = text.get_rect()
        rect.topleft = self.screen_rect.topleft
        self.screen.blit(text, rect)
