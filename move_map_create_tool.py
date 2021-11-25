import math
import pygame
import game_constants as g_c

pygame.init()
clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# ввод
size = list(map(int, input("размер в клетках в формате AxB: ").split("x")))
file_name = input("класс: ") + "_"
file_name += input("группа: ") + "_move_map.txt"

# первичная обработка данных, создание пустых массивов
screen = pygame.display.set_mode((g_c.WIDTH, g_c.HEIGHT))
rect_size = [g_c.WIDTH / size[0], g_c.HEIGHT / size[1]]
map_info = []
for i in range(size[1]):
    map_info += [["-"] * size[0]]
finished = False
move_trajectory = []
trajectory_length = 0

# цикл создания карты перемещений
while not finished:

    # визуализация процесса
    screen.fill(WHITE)
    for i in range(1, size[0]):
        pygame.draw.line(screen, BLACK, (i * rect_size[0], 0), (i * rect_size[0], g_c.HEIGHT))
    for j in range(1, size[1]):
        pygame.draw.line(screen, BLACK, (0, j * rect_size[1]), (g_c.WIDTH, j * rect_size[1]))
    if len(move_trajectory) >= 2:
        for i in range(len(move_trajectory) - 1):
            pygame.draw.line(screen, RED,
                             ((move_trajectory[i][0] + 0.5) * rect_size[0],
                              (move_trajectory[i][1] + 0.5) * rect_size[1]),
                             ((move_trajectory[i + 1][0] + 0.5) * rect_size[0],
                              (move_trajectory[i + 1][1] + 0.5) * rect_size[1]))

    # обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if len(move_trajectory) != 0:
                    trajectory_length += ((event.pos[0] / rect_size[0] - move_trajectory[-1][0]) ** 2 + (
                        (event.pos[1] / rect_size[1] - move_trajectory[-1][1])) ** 2) ** (1 / 2)
                move_trajectory += [(int(event.pos[0] / rect_size[0]), int(event.pos[1] / rect_size[1]))]
            elif event.button == 3:
                move_trajectory = move_trajectory[0:-1]
    pygame.display.update()
    clock.tick(30)

image = pygame.surface.Surface((g_c.WIDTH, g_c.HEIGHT), pygame.SRCALPHA)
color = list(map(int, input("цвет: ").split()))
width = int(input("ширина: "))
for i in range(len(move_trajectory) - 1):
    pygame.draw.line(image, color,
                     ((move_trajectory[i][0] + 0.5) * rect_size[0],
                      (move_trajectory[i][1] + 0.5) * rect_size[1]),
                     ((move_trajectory[i + 1][0] + 0.5) * rect_size[0],
                      (move_trajectory[i + 1][1] + 0.5) * rect_size[1]), width)
pygame.image.save(image, "maps/new/image_" + file_name[0:-4] + ".png")

# перенос данных из массива координат в двухмерный конечный массив
if len(move_trajectory) >= 2:
    for i in range(len(move_trajectory[0:-1])):
        x = move_trajectory[i][0]
        y = move_trajectory[i][1]
        dx = move_trajectory[i + 1][0] - x
        dy = move_trajectory[i + 1][1] - y
        if dx != 0:
            map_info[y][x] = math.atan(dy / dx) + math.pi / 2 * int(dx < 0)
        else:
            map_info[y][x] = math.pi / 2 * (int(dy > 0) - int(dy < 0))
map_info[move_trajectory[-1][1]][move_trajectory[-1][0]] = "stop"
map_info += [move_trajectory[0]]
# сохранение данных
with open("maps/new/" + file_name, "w") as file:
    file.write(str(trajectory_length) + " ")
    file.write("\n")
    for line in map_info:
        for an in line:
            file.write(str(an) + " ")
        file.write("\n")
pygame.image.save(screen, "maps/new/" + file_name + "_plan.png")  # FIXME нужно сохранять этот файл?
