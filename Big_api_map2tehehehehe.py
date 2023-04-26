import pygame
import requests

if __name__ == '__main__':
    pygame.init()
    pygame.display.set_caption('Большая задача по Maps API. Часть №3')
    size = width, height = 500, 400
    screen = pygame.display.set_mode(size)
    screen.fill((255, 255, 255))


    class Map:
        def __init__(self):
            self.api_server = "http://static-maps.yandex.ru/1.x/"
            self.lon = "37.530887"
            self.lat = "55.703118"
            self.delta = "0.005"

            self.params = {"ll": ",".join([self.lon, self.lat]),
                           "spn": ",".join([self.delta, self.delta]),
                           "l": "map"}
            self.response = requests.get(self.api_server, params=self.params)

            self.map_file = "map.png"
            self.pos_change = [0, 0]

        def move(self, x, y):
            print(self.delta, x, y, self.lon, self.lat)
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
            print(self.delta, x, y, self.lon, self.lat)
            self.params = {"ll": ",".join([self.lon, self.lat]),
                           "spn": ",".join([self.delta, self.delta]),
                           "l": "map"}
            self.response = requests.get(self.api_server, params=self.params)

        def show(self):
            with open(self.map_file, "wb") as file:
                file.write(self.response.content)
            screen.blit(pygame.image.load(self.map_file), (0, 0))

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
            self.params = {"ll": ",".join([self.lon, self.lat]),
                           "spn": ",".join([self.delta, self.delta]),
                           "l": "map"}
            self.response = requests.get(self.api_server, params=self.params)


    running = True
    map_object = Map()
    map_object.show()
    move = 0.001
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    map_object.zoom_change(-1)  # zoom
                    map_object.show()
                if event.key == pygame.K_PAGEDOWN:
                    map_object.zoom_change(1)  # unzoom
                    map_object.show()
                if event.key == pygame.K_UP:  # up arrow
                    map_object.move(0, move)
                    map_object.show()
                if event.key == pygame.K_DOWN:  # down arrow
                    map_object.move(0, -move)
                    map_object.show()
                if event.key == pygame.K_LEFT:  # left arrow
                    map_object.move(-move, 0)
                    map_object.show()
                if event.key == pygame.K_RIGHT:  # right arrow
                    map_object.move(move, 0)
                    map_object.show()
        pygame.display.flip()
    pygame.quit()