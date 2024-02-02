import sys


import pygame
import requests


delta = "0.002"
lon = "37.530887"
lat = "55.703118"
pygame.init()
screen = pygame.display.set_mode((600, 450))


def update():
    params = {
        "ll": ",".join([lon, lat]),
        "spn": ",".join([delta, delta]),
        "l": "map"
    }
    map_request = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(map_request, params=params)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

        # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    screen.blit(pygame.image.load(map_file), (0, 0))



# Инициализируем pygame

# Рисуем картинку, загружаемую из только что созданного файла.
update()
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        key = pygame.key.get_pressed()
        if key[pygame.K_PAGEDOWN]:
            delta = str(float(delta) + 0.001)

            update()
        elif key[pygame.K_PAGEUP]:
            delta = str(float(delta) - 0.001)
            if float(delta) < 0:
                delta = '0'

            update()
    pygame.display.flip()
pygame.quit()
