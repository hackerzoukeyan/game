from time_counter import TimeCounter
from score_board import ScoreBoard
from settings import Settings
from monster import Monster
from player import Player
from brick import Brick
from score import Score
from door import Door
from msg import Msg
import pygame
import json
import sys


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.display.set_caption('Game')
        pygame.mouse.set_visible(False)
        self.settings = Settings()
        self.score = None
        self.player = Player(self)
        self.bricks = pygame.sprite.Group()
        self.scores = pygame.sprite.Group()
        self.monsters = pygame.sprite.Group()
        self.door = None
        self.json = None
        self.game_finished = False
        self.sb = ScoreBoard(self)
        self.msg = Msg(self, 'None')
        self.prepare_world()
        self.game_over_sound = pygame.mixer.Sound(self.settings.game_over_sound)
        self.score_sound = pygame.mixer.Sound(self.settings.score_sound)
        self.win_sound = pygame.mixer.Sound(self.settings.win_sound)
        self.tc = TimeCounter(self)

    def prepare_world(self):
        self.score = 0
        self.json = json.load(open(f'levels/{self.sb.level}.json', encoding='utf-8'))
        self.add_bricks()
        self.add_scores()
        self.door = Door(self, self.json['door']['x'], self.json['door']['y'])
        
    def add_bricks(self):
        brick_positions = zip(self.json['bricks']['x'], self.json['bricks']['y'])
        for x, y in brick_positions:
            brick = Brick(self, x, y)
            self.bricks.add(brick)

    def add_monster(self):
        monster = Monster(self)
        self.monsters.add(monster)

    def add_scores(self):
        score_positions = zip(self.json['scores']['x'], self.json['scores']['y'])
        for x, y in score_positions:
            score = Score(self, x, y)
            self.scores.add(score)

    def check_scores(self):
        c = pygame.sprite.spritecollide(self.player, self.scores, True)
        if c:
            self.score += len(c)
            self.score_sound.play()
            self.add_monster()
        if not len(self.scores):
            self.add_scores()
        if self.score == self.settings.max_score:
            self.door.open()

    def check_monsters(self):
        for x in self.monsters.sprites():
            if x.rect.top >= self.screen.get_rect().bottom:
                self.monsters.remove(x)

    def check_lose(self):
        if pygame.sprite.spritecollide(self.player, self.monsters, True):
            self.score -= 5
        if self.tc.timeout():
            self.timeout()

    def timeout(self):
        self.game_finished = True
        self.msg.msg = 'Time Out(press Q to quit.)'
        pygame.mixer.music.stop()
        self.game_over_sound.play()

    def check_quit(self, event: pygame.event.Event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            self.sb.save_high_score()
            self.sb.save_level()
            sys.exit()

    def check_events(self):
        for event in pygame.event.get():
            self.check_quit(event)
            if event.type == pygame.KEYDOWN:
                self.check_keydown_event(event)
            if event.type == pygame.KEYUP:
                self.check_keyup_event(event)

    def check_keydown_event(self, event: pygame.event.Event):
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = True
        elif event.key == pygame.K_UP and not self.player.jumping:
            self.player.jumping = True
            self.player.jump_up_value = 0

    def check_keyup_event(self, event: pygame.event.Event):
        if event.key == pygame.K_RIGHT:
            self.player.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.player.moving_left = False
    
    def check_win(self):
        if self.door.opened and self.player.rect.colliderect(self.door.rect):
            self.win()
    
    def win(self):
        if self.sb.level == self.settings.max_level:
            self.game_finished = True
            self.msg.msg = 'You win!(Press Q tu quit.)'
            pygame.mixer.music.stop()
            self.win_sound.play()
            return
        self.tc.zero()
        self.win_sound.play()
        self.sb.level += 1
        self.monsters.empty()
        self.bricks.empty()
        self.scores.empty()
        self.prepare_world()

    def update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.door.blit()
        self.player.blit()
        for x in self.bricks.sprites():
            x.blit()
        for x in self.scores.sprites():
            x.blit()
        for x in self.monsters.sprites():
            x.blit()
        self.sb.blit()
        if self.game_finished:
            self.msg.blit()
        else:
            self.tc.blit()
        pygame.display.flip()

    def run(self):
        pygame.mixer.music.load(self.settings.bg_mp3)
        pygame.mixer.music.play(-1)
        while 1:
            if not self.game_finished:
                self.check_lose()
                self.check_monsters()
                self.check_scores()
                self.sb.check_high_score()
                self.check_win()
                self.player.update()
                self.bricks.update()
                self.monsters.update()
            self.check_events()
            self.update_screen()


if __name__ == '__main__':
    game = Game()
    game.run()
