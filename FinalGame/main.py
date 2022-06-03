#from email.mime import audio
import pygame,sys
from settings import *
from level import Level

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH,HEIGTH))
        pygame.display.set_caption('Final Game')
        self.clock = pygame.time.Clock()

        self.level = Level()
        self.kind_pause = 'Normal'
        self.boss_moment = False

        pygame.mixer.music.load('./audio/main_2.wav')
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(loops=-1)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        #print('se presiono')
                        self.kind_pause='EXP'
                        self.level.toggle_menu(self.kind_pause)
                    if event.key == pygame.K_ESCAPE:
                        #print('se presiono')
                        self.kind_pause = 'Normal'
                        self.level.toggle_menu(self.kind_pause)

            if self.level.game_paused:
                pygame.mixer.music.pause()
            else:
                pygame.mixer.music.unpause()

            if self.level.boss_alert and not self.boss_moment:
                pygame.mixer.music.pause()
                pygame.mixer.music.unload()
                pygame.mixer.music.load('./audio/boss_theme.wav')
                pygame.mixer.music.set_volume(0.4)
                pygame.mixer.music.play(loops=-1)
                self.boss_moment = True
                #pygame.mixer.unpause()

            self.screen.fill('black')
            self.level.run()
            pygame.display.update()
            self.clock.tick(FPS)

if __name__ == '__main__':
    game = Game()
    game.run()