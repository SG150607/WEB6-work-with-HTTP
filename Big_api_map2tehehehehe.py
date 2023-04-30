import pygame
import requests
from get_coordinates import get_coordinates

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Большая задача по Maps API')
    size = width, height = 650, 450
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))
    COLOR_INACTIVE = pygame.Color('lightskyblue3')
    COLOR_ACTIVE = pygame.Color('dodgerblue2')
    FONT = pygame.font.Font(None, 28)


    class Button:
        def __init__(self, x, y, w, h, text="' '"):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.text_surface = FONT.render(text, True, self.color)

        def get_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos):
                if "pt" in map_object.params.keys():
                    map_object.params.pop("pt")
                # следующие 2 строчки удаляют содержимое запроса (избавьтесь от них по желаиню:3)
                input_box.text = ''
                input_box.text_surface = FONT.render(input_box.text, True, input_box.color)
                info_pole.text = ''
                info_pole.text_surface = FONT.render(info_pole.text, True, info_pole.color)

        def draw(self, screen):
            screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)


    class InputBox:
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.text_surface = FONT.render(text, True, self.color)
            self.active = False

        def get_event(self, event):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.rect.collidepoint(event.pos):
                    self.active = not self.active
                else:
                    self.active = False
                if self.active:
                    self.color = COLOR_ACTIVE
                else:
                    self.color = COLOR_INACTIVE
            if event.type == pygame.KEYDOWN:
                if self.active:
                    if event.key == pygame.K_RETURN:
                        # Передаем координаты указанного объекта
                        new_coords = get_coordinates(self.text)
                        if new_coords:
                            map_object.lon, map_object.lat = new_coords[0], new_coords[1]
                            map_object.params["ll"] = ",".join(new_coords)
                            map_object.params["pt"] = f"{map_object.params['ll']},pm2rdl"
                            map_object.find_object = True

                            search_api_server = "https://search-maps.yandex.ru/v1/"
                            api_key = "dda3ddba-c9ea-4ead-9010-f43fbc15c6e3"
                            search_params = {
                                "apikey": api_key,
                                "text": input_box.text,
                                "lang": "ru_RU",
                                "ll": map_object.params["ll"],
                                "spn": map_object.params["spn"]
                            }
                            the_response = requests.get(search_api_server, params=search_params)
                            the_place = the_response.json()["features"][0]["properties"]

                            if "GeocoderMetaData" not in the_place:  # организация
                                info_pole.text = the_place["CompanyMetaData"]["address"]
                            else:
                                info_pole.text = the_place["GeocoderMetaData"]["text"]
                            info_pole.text_surface = FONT.render(info_pole.text, True, info_pole.color)
                        else:
                            info_pole.text = "ХЗ хде ето ¯\_(0-0)_/¯"
                            info_pole.text_surface = FONT.render(info_pole.text, True, info_pole.color)
                    elif event.key == pygame.K_BACKSPACE:
                        self.text = self.text[:-1]
                    else:
                        self.text += event.unicode
                    self.text_surface = FONT.render(self.text, True, self.color)

        def update(self):
            # удлиняем поле если текст слишком длинный
            width = max(200, self.text_surface.get_width() + 10)
            self.rect.w = width

        def draw(self, screen):
            screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)


    class InfoPole:
        def __init__(self, x, y, w, h, text=''):
            self.rect = pygame.Rect(x, y, w, h)
            self.color = COLOR_INACTIVE
            self.text = text
            self.text_surface = FONT.render(text, True, self.color)

        def update(self):
            # удлиняем поле если текст слишком длинный
            width = max(200, self.text_surface.get_width() + 10)
            self.rect.w = width

        def draw(self, screen):
            screen.blit(self.text_surface, (self.rect.x + 5, self.rect.y + 5))
            pygame.draw.rect(screen, self.color, self.rect, 2)


    class Map:
        def __init__(self):
            self.api_server = "http://static-maps.yandex.ru/1.x/"
            self.lon = "37.530887"
            self.lat = "55.703118"
            self.delta = "0.005"

            self.params = {"ll": ",".join([self.lon, self.lat]),
                           "spn": ",".join([self.delta, self.delta]),
                           "l": "map",
                           "size": f"{width},{height}"}
            self.response = requests.get(self.api_server, params=self.params)

            self.map_file = "map.png"
            self.pos_change = [0, 0]

            self.find_object = False

        def move(self, x, y):
            if x:
                self.lon = str(float(self.lon) + x)
                if float(self.lon) > 179:
                    self.lon = "179"
                elif float(self.lon) < -180:
                    self.lon = "-180"
            if y:
                self.lat = str(float(self.lat) + y)
                if float(self.lat) > 80:
                    self.lat = "80"
                elif float(self.lat) < -80:
                    self.lat = "-80"
            self.params["ll"] = ",".join([self.lon, self.lat])
            self.params["spn"] = ",".join([self.delta, self.delta])

        def zoom_change(self, value):
            global move
            if value == -1:  # zoom
                self.delta = str(round(float(self.delta) / 2, 4))
                move /= 2
            else:  # unzoom
                self.delta = str(round(float(self.delta) * 2, 4))
                move *= 2
            if move < 0.001:
                move = 0.001
            elif move > 10:
                move = 10
            if float(self.delta) > 50:
                self.delta = "50"
            elif float(self.delta) < 0.0001:
                self.delta = "0.0001"
            self.params["ll"] = ",".join([self.lon, self.lat])
            self.params["spn"] = ",".join([self.delta, self.delta])

        def show(self):
            map_object.response = requests.get(map_object.api_server, params=map_object.params)
            with open(self.map_file, "wb") as file:
                file.write(self.response.content)
            screen.blit(pygame.image.load(self.map_file), (0, 0))


    running = True
    map_object = Map()
    map_object.show()
    input_box = InputBox(52, 20, 200, 30)
    info_pole = InfoPole(15, height - 45, 200, 30)
    button = Button(15, 20, 30, 30)
    move = 0.001
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    map_object.zoom_change(-1)  # zoom
                if event.key == pygame.K_PAGEDOWN:
                    map_object.zoom_change(1)  # unzoom
                if event.key == pygame.K_UP:  # up arrow
                    map_object.move(0, move)
                if event.key == pygame.K_DOWN:  # down arrow
                    map_object.move(0, -move)
                if event.key == pygame.K_LEFT:  # left arrow
                    map_object.move(-move, 0)
                if event.key == pygame.K_RIGHT:  # right arrow
                    map_object.move(move, 0)
                if event.key == pygame.K_m:  # m - map
                    map_object.params['l'] = 'map'
                    map_object.response = requests.get(map_object.api_server, params=map_object.params)
                if event.key == pygame.K_s:  # s - sat
                    map_object.params['l'] = 'sat'
                    map_object.response = requests.get(map_object.api_server, params=map_object.params)
                if event.key == pygame.K_b:  # b - both
                    map_object.params['l'] = 'sat,skl'
                    map_object.response = requests.get(map_object.api_server, params=map_object.params)
            map_object.show()
            input_box.get_event(event)
            input_box.update()
            input_box.draw(screen)
            button.get_event(event)
            button.draw(screen)
            info_pole.update()
            info_pole.draw(screen)
        pygame.display.flip()
    pygame.quit()
