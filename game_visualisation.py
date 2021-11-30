import pygame
from game_objects_creatures import *
from game_objects_towers import *


class Menu:
    def __init__(self, game):
        self.game = game
        self.mid_h, self.mid_w = self.game.HEIGHT / 2, self.game.WIDTH / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)  # для того, чтобы можно было кастомизировать курсоры
        self.offset = 100

    def draw_cursor(self):
        self.game.draw_text('--', 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()


class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Start Game"
        self.startx, self.starty = self.mid_w, self.mid_h + 20
        self.optionsx, self.optionsy = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.exitx, self.exity = self.mid_w, self.mid_h + 110
        self.cursor_rect.midtop = (self.startx + self.offset, self.starty)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Main Menu", 50, self.mid_w, self.mid_h - 50)
            self.game.draw_text("Start Game", 20, self.startx, self.starty)
            self.game.draw_text("Options", 20, self.optionsx, self.optionsy)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)
            self.game.draw_text("Exit", 40, self.exitx, self.exity)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == "Start Game":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start Game"
        elif self.game.UP_KEY:
            if self.state == "Start Game":
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
                self.state = "Exit"
            elif self.state == "Options":
                self.cursor_rect.midtop = (self.startx + self.offset, self.starty)
                self.state = "Start Game"
            elif self.state == "Credits":
                self.cursor_rect.midtop = (self.optionsx + self.offset, self.optionsy)
                self.state = "Options"
            elif self.state == "Exit":
                self.cursor_rect.midtop = (self.creditsx + self.offset, self.creditsy)
                self.state = "Credits"

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == "Start Game":
                self.game.curr_menu = self.game.levels
            elif self.state == "Options":
                self.game.curr_menu = self.game.options
            elif self.state == "Credits":
                self.game.curr_menu = self.game.credits
            elif self.state == "Exit":
                self.game.running, self.game.playing = False, False
            self.run_display = False


class LevelsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Level 1"
        self.lvl1_x, self.lvl1_y = self.mid_w, self.mid_h + 20
        self.lvl2_x, self.lvl2_y = self.mid_w, self.mid_h + 40
        self.lvl3_x, self.lvl3_y = self.mid_w, self.mid_h + 60
        self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Levels", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 30)
            self.game.draw_text("Level 1", 15, self.lvl1_x, self.lvl1_y)
            self.game.draw_text("Level 2", 15, self.lvl2_x, self.lvl2_y)
            self.game.draw_text("Level 3", 15, self.lvl3_x, self.lvl3_y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == "Level 1":
                self.cursor_rect.midtop = (self.lvl2_x + self.offset, self.lvl2_y)
                self.state = "Level 2"
            elif self.state == "Level 2":
                self.cursor_rect.midtop = (self.lvl3_x + self.offset, self.lvl3_y)
                self.state = "Level 3"
            elif self.state == "Level 3":
                self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)
                self.state = "Level 1"
        elif self.game.UP_KEY:
            if self.state == "Level 1":
                self.cursor_rect.midtop = (self.lvl3_x + self.offset, self.lvl3_y)
                self.state = "Level 3"
            elif self.state == "Level 3":
                self.cursor_rect.midtop = (self.lvl2_x + self.offset, self.lvl2_y)
                self.state = "Level 2"
            elif self.state == "Level 2":
                self.cursor_rect.midtop = (self.lvl1_x + self.offset, self.lvl1_y)
                self.state = "Level 1"
        elif self.game.START_KEY:
            self.game.level_name = self.state
            self.game.level = Level(self.game.level_name, self.game.display)
            self.run_display = False
            self.game.playing = True


class IngameMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.pausex, self.pausey = self.mid_w, self.mid_h + 20


class OptionsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Volume"
        self.volx, self.voly = self.mid_w, self.mid_h + 20
        self.controlsx, self.controlsy = self.mid_w, self.mid_h + 40
        self.cursor_rect.midtop = (self.volx + self.offset, self.voly)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill((0, 0, 0))
            self.game.draw_text("Options", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 30)
            self.game.draw_text("Volume", 15, self.volx, self.voly)
            self.game.draw_text("Controls", 15, self.controlsx, self.controlsy)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.main_menu
            self.run_display = False
        elif self.game.UP_KEY or self.game.DOWN_KEY:
            if self.state == "Volume":
                self.state = "Controls"
                self.cursor_rect.midtop = (self.controlsx + self.offset, self.controlsy)
            elif self.state == "Controls":
                self.state = "Volume"
                self.cursor_rect.midtop = (self.volx + self.offset, self.voly)
        elif self.game.START_KEY:
            # FIXME: сделать меню для Controls и Volume
            pass


class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.curr_menu = self.game.main_menu
                self.run_display = False
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text("Credits", 20, self.game.WIDTH / 2, self.game.HEIGHT / 2 - 20)
            self.game.draw_text("Made bi me", 15, self.game.WIDTH / 2, self.game.HEIGHT / 2 + 10)
            self.blit_screen()


class Level:
    def __init__(self, level, screen):
        self.opponents = []
        self.level = level[-1]
        self.screen = screen

        self.ingame_towers = []

        self.background_img = pygame.image.load("Textures/Background" + self.level + ".png").convert_alpha()

        self.towerspot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
        self.towerspot_rect = self.towerspot_img.get_rect()

        self.archertower_img = pygame.image.load("Textures/ArcherTower.png").convert_alpha()
        self.archertower_rect = self.archertower_img.get_rect()

        self.images = [self.towerspot_img, self.archertower_img]
        self.opponents += [Warrior("alpha"), Warrior("beta")]

        with open("level_designs.txt", "r") as level_design:
            design = level_design.readlines()[int(self.level)].split()
            for i in range(int(design[1])):
                x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
                click = Button(x, y, self.images[0], 1)
                self.ingame_towers.append(click)

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        for tower in self.ingame_towers:
            if tower.is_pressed(self.screen):
                tower.image = self.images[1]




# def draw_map(screen, level, towers):
#     towers_pos = []
#
#     background_img = pygame.image.load("Textures/Background" + str(level) + ".png").convert_alpha()
#     screen.blit(background_img, (0, 0))
#
#     towerspot_img = pygame.image.load("Textures/TowerSpot.png").convert_alpha()
#     towerspot_rect = towerspot_img.get_rect()
#
#     archertower_img = pygame.image.load("Textures/ArcherTower.png").convert_alpha()
#     archertower_rect = archertower_img.get_rect()
#
#     images = [towerspot_img, archertower_img]
#
#     with open("level_designs.txt", "r") as level_design:
#         design = level_design.readlines()[level].split()
#         for i in range(int(design[1])):
#             x, y = int(design[2 * i + 2]), int(design[2 * i + 3])
#             towers_pos.append([x, y])
#
#     for tower in towers_pos:
#         screen.blit(images[towers[i]], tower)


class Button:
    def __init__(self, x, y, image, scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image, (int(width * scale), int(height * scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    def is_pressed(self, surface):
        action = False
        pos = pygame.mouse.get_pos()

        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] and not self.clicked:
                self.clicked = True
                action = True

        if not pygame.mouse.get_pressed()[0]:
            self.clicked = False

        surface.blit(self.image, (self.rect.x, self.rect.y))

        return action
