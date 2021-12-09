import pygame
import os

clock = pygame.time.Clock()
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
WIDTH = 800
HEIGHT = 600

# проверка существования папки new
if not os.path.exists("new"):
    os.mkdir("new")

# ввод
size = list(map(int, input("размер в клетках в формате AxB: ").split("x")))
file_name = input("класс: ") + "_"
file_name += input("группа: ") + "_move_map.txt"
color = list(map(int, input("цвет(R G B): ").split()))
width = int(input("ширина: "))

pygame.init()

# первичная обработка данных, создание пустых массивов
screen = pygame.display.set_mode((WIDTH, HEIGHT))
rect_size = [WIDTH / size[0], HEIGHT / size[1]]
map_info = []
for i in range(size[0]):
    map_info += [["-"] * size[1]]
finished = False
move_trajectory = []
trajectory_length = 0

# цикл создания карты перемещений
while not finished:

    # визуализация процесса
    screen.fill(WHITE)

    # сетка
    for i in range(1, size[0]):
        pygame.draw.line(screen, BLACK, (i * rect_size[0], 0), (i * rect_size[0], HEIGHT))
    for j in range(1, size[1]):
        pygame.draw.line(screen, BLACK, (0, j * rect_size[1]), (WIDTH, j * rect_size[1]))

    # траектория
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
            if event.button == 1:   # установка следующей точки
                if len(move_trajectory) != 0:
                    trajectory_length += ((event.pos[0] / rect_size[0] - move_trajectory[-1][0]) ** 2 + (
                        (event.pos[1] / rect_size[1] - move_trajectory[-1][1])) ** 2) ** (1 / 2)
                move_trajectory += [(int(event.pos[0] / rect_size[0]), int(event.pos[1] / rect_size[1]))]
            elif event.button == 3:     # удаление предыдущей точки
                move_trajectory = move_trajectory[0:-1]
    pygame.display.update()
    clock.tick(30)

# сохранение траектории в виде изображения
image = pygame.surface.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
for i in range(len(move_trajectory) - 1):
    pygame.draw.line(image, color,
                     ((move_trajectory[i][0] + 0.5) * rect_size[0],
                      (move_trajectory[i][1] + 0.5) * rect_size[1]),
                     ((move_trajectory[i + 1][0] + 0.5) * rect_size[0],
                      (move_trajectory[i + 1][1] + 0.5) * rect_size[1]), width)
pygame.image.save(image, "new/image_" + file_name[0:-4] + ".png")

# перенос данных из массива координат в двухмерный конечный массив
if len(move_trajectory) >= 2:
    for i in range(len(move_trajectory[0:-1])):
        x = move_trajectory[i][0]
        y = move_trajectory[i][1]
        nx = move_trajectory[i + 1][0]
        ny = move_trajectory[i + 1][1]
        map_info[x][y] = str((nx + 0.5) * rect_size[0]) + ";" + str((ny + 0.5) * rect_size[1])
if len(move_trajectory) >= 1:
    map_info[move_trajectory[-1][0]][move_trajectory[-1][1]] = "stop"
    map_info += [[(move_trajectory[0][0] + 0.5) * rect_size[0], (move_trajectory[0][1] + 0.5) * rect_size[1]]]

# сохранение текстовых данных
with open("new/" + file_name, "w") as file:
    file.write(str(trajectory_length) + " ")
    file.write("\n")
    for line in map_info:
        for an in line:
            file.write(str(an) + " ")
        file.write("\n")

# сохранение копии изображения в окне
pygame.image.save(screen, "new/" + file_name + "_plan.png")
