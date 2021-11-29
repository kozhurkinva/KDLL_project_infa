import pygame
from game_constants import *
import pygame.draw as dr
from game_visualisation import *
from game_objects_creatures import *
from game_objects_towers import *
from game_objects_projectiles import *


class Game:
    def __init__(self):
        pygame.init()
        # screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        clock = pygame.time.Clock()
        self.level = 0
        self.tower_types = [0] * 999
        self.towers = []
        self.opponents = []
        self.bullets = []
        self.start_button = Button(x=50, y=400, image=pygame.image.load("Textures/StartButton.png").convert_alpha(),
                                   scale=0.5)
        self.stop_button = Button(x=600, y=400, image=pygame.image.load("Textures/StopButton.png").convert_alpha(),
                                  scale=0.5)
        self.start_flag = False
        self.is_config = True
        finished = False

        while not finished:

            if not self.start_flag:
                if self.start_button.is_pressed(screen):
                    print("Game starts!")
                    self.level += 1  # FIXME: тестовая штука, потом изменится обязательно!
                    self.opponents += [Warrior("alpha"), Warrior("beta")]
                    self.towers += [ArrowTower(200, 200, self.opponents)]
                    self.start_flag = True

            if self.start_flag:
                if self.is_config:
                    cur_level = Level(level=self.level, screen=screen)
                    self.is_config = False
                else:
                    cur_level.draw()

            for our_event in pygame.event.get():
                if our_event.type == pygame.QUIT:
                    finished = True
                elif our_event.type == pygame.MOUSEBUTTONDOWN:
                    pass
                else:
                    pass  # FIXME: self.level выбирается на пользовательском интерфейсе

            if self.stop_button.is_pressed(screen):
                finished = True

            for tower in self.towers:
                tower.check_cause()

            for opp in self.opponents:
                if not opp.alive:
                    self.opponents.pop(self.opponents.index(opp))
                opp.move_opponent("level" + str(self.level))
                for projectile in opp.projectiles:
                    projectile.move()
                    projectile.draw(screen)
                opp.draw(screen)    # FIXME временно, для тестов
            pygame.display.update()
            draw_map(screen, self.level, self.tower_types)
            clock.tick(FPS)
        pygame.quit()


gggg = Game()
