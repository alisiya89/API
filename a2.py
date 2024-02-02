import os
import sys

import pygame
import requests

map_file = ''


def create(lon="37.530887", lat="55.703118"):
    global map_file
    lon = lon
    lat = lat
    delta = "0.002"

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


create()

# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(map_file), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
mouse_position = 0
enter = False
text = ''
run = True
shrift = pygame.font.SysFont('arial', 20)
while run:
    screen.blit(pygame.image.load(map_file), (0, 0))
    pygame.draw.rect(screen, (0, 0, 0), (10, 20, 400, 60), 4)
    screen.blit(shrift.render(text, 1, (0, 0, 0)), (20, 35))
    pygame.draw.rect(screen, (0, 0, 0), (420, 20, 170, 60), 4)
    screen.blit(shrift.render('Искать', 1, (0, 0, 0)), (470, 34))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if 10 <= mouse_position[0] <= 410 and 20 <= mouse_position[1] <= 80:
                enter = True
            elif 420 <= mouse_position[0] <= 590 and 20 <= mouse_position[1] <= 80:
                enter = False
                geocoder_request = f"http://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-98ba-98533de7710b&geocode={text}" \
                                   "&format=json"
                response = requests.get(geocoder_request)
                json_response = response.json()
                print(json_response)
                toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]["Point"][
                    "pos"]
                print(toponym)
                coords = toponym.split()
                create(coords[0], coords[1])
                text=''
            else:
                enter = False
        if event.type == pygame.MOUSEMOTION:
            mouse_position = event.pos
        if event.type == pygame.KEYDOWN and enter:
            if event.key == pygame.K_BACKSPACE:
                text = text[:-1]
            else:
                if len(text) != 33:
                    text += event.unicode
    pygame.display.flip()

# Удаляем за собой файл с изображением.
os.remove(map_file)
