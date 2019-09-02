# Jacob Meadows
# Practicum IT, 7th - 8th Period
# 30 August 2019
"""
Basic Python review.

Copyright (C) 2018 Jacob Meadows

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""
import pygame
import string
import random
import socket


class App:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Review")
        pygame.key.set_repeat(500, 20)
        self.window = pygame.display.set_mode((640, 480))
        self.clock = pygame.time.Clock()
        self.texts = dict()
        self.buttons = dict()
        self.text_inputs = dict()
        self.menu()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.KEYDOWN:
                    self.key_callback(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_button_callback(event)

            self.window.fill((0, 0, 0))
            for text_object in self.texts:
                self.texts[text_object].render(self.window)
            for button in self.buttons:
                self.buttons[button].render(self.window)
            for text_input in self.text_inputs:
                self.text_inputs[text_input].render(self.window)

            pygame.display.flip()
            self.clock.tick()

    def menu(self):
        self.texts.clear()
        self.buttons.clear()
        self.text_inputs.clear()
        self.texts["title"] = TextObject(text="Python Review", rect=(160, 50, 320, 100), fg_color=(0, 255, 0),
                                         font=("Times New Roman", 50))
        self.buttons["program_1"] = Button(text="1. 10 Random Numbers", rect=(220, 150, 200, 30), fg_color=(0, 255, 0),
                                           command=self.program_1)
        self.buttons["program_2"] = Button(text="2. Car Class", rect=(220, 200, 200, 30), fg_color=(0, 255, 0),
                                           command=self.program_2)
        self.buttons["program_3"] = Button(text="3. Ping 10 IPs", rect=(220, 250, 200, 30), fg_color=(0, 255, 0),
                                           command=self.program_3)
        self.buttons["quit"] = Button(text="Quit", rect=(290, 350, 60, 30), fg_color=(0, 255, 0), justify="center",
                                      command=lambda: [pygame.quit(), quit()])

    def program_1(self):
        self.texts.clear()
        self.buttons.clear()
        self.text_inputs.clear()
        random_numbers = ""
        while len(random_numbers.split()) < 10:
            random_number = random.randint(1, 50)
            if str(random_number) not in random_numbers:
                if len(random_numbers) == 0:
                    random_numbers += f"{random_number}"
                else:
                    random_numbers += f" {random_number}"
        self.texts["random_numbers"] = TextObject(text=random_numbers, rect=(190, 50, 260, 30), justify="center",
                                                  fg_color=(0, 255, 0))
        self.buttons["randomize"] = Button(text="Randomize Again", rect=(240, 150, 160, 30), fg_color=(0, 255, 0),
                                           justify="center", command=self.program_1)
        self.buttons["menu"] = Button(text="Back to Menu", rect=(260, 350, 120, 30), fg_color=(0, 255, 0),
                                      command=self.menu)

    def program_2(self):
        self.texts.clear()
        self.buttons.clear()
        self.text_inputs.clear()
        self.texts["car_color"] = TextObject(text="What color is the car?", rect=(60, 100, 240, 30),
                                             justify="center", fg_color=(0, 255, 0))
        self.text_inputs["car_color"] = TextInput(self, text="", rect=(300, 100, 200, 30), fg_color=(0, 255, 0),
                                                  restriction=string.ascii_letters, limit=12)
        self.texts["car_year"] = TextObject(text="What year is the car?\n(1886 - 2020)", rect=(60, 150, 240, 30),
                                            fg_color=(0, 255, 0), justify="center")
        self.text_inputs["car_year"] = TextInput(self, text="", rect=(300, 150, 200, 30), fg_color=(0, 255, 0),
                                                 restriction=string.digits, limit=12)
        self.texts["car_speed"] = TextObject(text="What is the car's top speed?\n(0 - 278)", rect=(60, 200, 240, 30),
                                             fg_color=(0, 255, 0), justify="center")
        self.text_inputs["car_speed"] = TextInput(self, text="", rect=(300, 200, 200, 30), fg_color=(0, 255, 0),
                                                  restriction=string.digits, limit=12)
        self.texts["car_sentence"] = TextObject(text="", rect=(20, 250, 600, 30), fg_color=(0, 255, 0),
                                                justify="center")

        def submit_command():
            colors = [color.lower() for color in open("colors.txt", "r").read().split("\n")]
            self.text_inputs['car_color'].text = self.text_inputs['car_color'].text.lower()
            if (len(self.text_inputs['car_color'].text) > 0 and self.text_inputs['car_color'].text in colors) and \
                    (len(self.text_inputs['car_year'].text) > 0 and
                     1886 <= int(self.text_inputs['car_year'].text) <= 2020) and \
                    (len(self.text_inputs['car_speed'].text) > 0 and
                     0 <= int(self.text_inputs['car_speed'].text) <= 278):
                user_car = Car(self.text_inputs['car_color'].text.strip(), self.text_inputs['car_year'].text.strip(),
                               self.text_inputs['car_speed'].text.strip())
                vowels = ['a', 'e', 'i', 'o', 'u']
                self.texts["car_sentence"].text = \
                    f"You have {'a ' + user_car.color if user_car.color[0] not in vowels else 'an ' + user_car.color}" \
                    f" car from {user_car.year} that can go {user_car.top_speed} miles per hour."

        self.buttons["submit"] = Button(text="Submit", rect=(280, 300, 80, 30), fg_color=(0, 255, 0), justify="center",
                                        command=submit_command)
        self.buttons["menu"] = Button(text="Back to Menu", rect=(260, 350, 120, 30), fg_color=(0, 255, 0),
                                      command=self.menu)

    def program_3(self):
        self.texts.clear()
        self.buttons.clear()
        self.text_inputs.clear()
        self.texts["port"] = TextObject(text="Port:", rect=(200, 100, 200, 30), fg_color=(0, 255, 0))
        self.text_inputs["port"] = TextInput(self, text="", rect=(250, 100, 200, 30), fg_color=(0, 255, 0), limit=5,
                                             restriction=string.digits)
        program_socket = socket.socket()

        def submit_command():
            if len(self.text_inputs["port"].text) > 0:
                self.texts["ping_chat"] = TextObject(text="", rect=(20, 300, 600, 30), fg_color=(0, 255, 0), width=1)
                random_ip_addresses = []
                while len(random_ip_addresses) < 10:
                    random_ip = f"172.17.2.{random.randint(101, 254)}"
                    if random_ip not in random_ip_addresses:
                        random_ip_addresses.append(random_ip)
                for ip_address in random_ip_addresses:
                    self.texts["ping_chat"].text += f"Connecting to {ip_address}:{self.text_inputs['port'].text}...\n"
                    self.window.fill((0, 0, 0))
                    self.texts["ping_chat"].render(self.window)
                    self.buttons["menu"].render(self.window)
                    pygame.display.flip()
                    try:
                        program_socket.connect((ip_address, int(self.text_inputs["port"].text)))
                        test = True
                    except TimeoutError:
                        test = False
                    if test:
                        self.texts["ping_chat"].text += "Success!\n"
                    else:
                        self.texts["ping_chat"].text += "No response.\n"
                    self.texts["ping_chat"].text_rect[1] -= 47
                    self.texts["ping_chat"].rect[1] -= 47
                    self.texts["ping_chat"].text_rect[3] += 45
                    self.texts["ping_chat"].rect[3] += 47
                self.texts["ping_chat"].text += "Done!"
                del self.buttons["submit"]
                del self.text_inputs["port"]
                del self.texts["port"]

        self.buttons["submit"] = Button(text="Submit", rect=(280, 300, 80, 30), fg_color=(0, 255, 0), justify="center",
                                        command=submit_command)
        self.buttons["menu"] = Button(text="Back to Menu", rect=(260, 350, 120, 30), fg_color=(0, 255, 0),
                                      command=self.menu)

    def key_callback(self, event):
        mods = pygame.key.get_mods()
        for text_input in self.text_inputs:
            self.text_inputs[text_input].key_input(event, mods)

    def mouse_button_callback(self, event):
        for button in self.buttons:
            if self.buttons[button].rect.collidepoint(event.pos):
                self.buttons[button].activate(self)
                break
        for text_input in self.text_inputs:
            if self.text_inputs[text_input].rect.collidepoint(event.pos):
                self.text_inputs[text_input].focus_state = True
            else:
                self.text_inputs[text_input].focus_state = False


class Car:
    def __init__(self, color, year, top_speed):
        self.color = color
        self.year = year
        self.top_speed = top_speed


class Entity(pygame.sprite.Sprite):
    def __init__(self, image=None, rect=None):
        super().__init__()
        if image:
            if isinstance(image, str):
                self.image = pygame.image.load(image).convert()
            else:
                self.image = image
            if rect:
                self.rect = pygame.Rect(*rect[:2], *self.image.get_size())
            else:
                self.rect = self.image.get_rect()
        else:
            self.image = None
            if rect:
                self.rect = pygame.Rect(rect)
            else:
                self.rect = pygame.Rect(0, 0, 0, 0)
        self.dirty = True

    def render(self, screen):
        if self.image:
            screen.blit(self.image, self.rect)
        return self.rect


class TextObject(Entity):
    def __init__(self, bg_color=(0, 0, 0), fg_color=(0, 0, 0), text=None, font=("Times New Roman", 20, False, False),
                 justify="left", width=0, enclosed=True, bg=True, **kwargs):
        super().__init__(**kwargs)
        self.font = pygame.font.SysFont(*font)
        self.bg_color = bg_color
        self.bg = bg
        self.fg_color = fg_color
        self.text = text
        self.text_rect = self.rect[:]
        self.justify = justify
        self.width = width
        self.enclosed = enclosed
        self.cached_text = dict()
        self.formatted_text = list()

    def render(self, screen):
        if self.text is not None:
            if f"{self.text}{self.fg_color}" not in self.cached_text:
                self.formatted_text = self.text.split("\n")
                text_line = 0
                while len(self.formatted_text) > text_line:
                    text_size = self.font.size(self.formatted_text[text_line])
                    new_line = " ".join(self.formatted_text[text_line].split()[:-1])
                    if self.enclosed:
                        while text_size[0] >= self.rect.width - 5:
                            new_line = " ".join(new_line.split()[:-1])
                            text_size = self.font.size(new_line)
                    if new_line != " ".join(self.formatted_text[text_line].split()[:-1]):
                        self.formatted_text.insert(text_line + 1, self.formatted_text[text_line][len(new_line) + 1:])
                        self.formatted_text[text_line] = self.font.render(
                            new_line, True, self.fg_color
                        )
                    else:
                        self.formatted_text[text_line] = self.font.render(
                            self.formatted_text[text_line], True, self.fg_color
                        )
                    text_line += 1
                self.cached_text[f"{self.text}{self.fg_color}"] = self.formatted_text[:]
            elif f"{self.text}{self.fg_color}" in self.cached_text:
                self.formatted_text = self.cached_text[f"{self.text}{self.fg_color}"][:]
        if self.bg:
            pygame.draw.rect(screen, self.bg_color, self.rect)
        if self.width > 0:
            pygame.draw.rect(screen, self.fg_color, self.rect, 1)
        if self.justify == "left":
            self.text_rect[0] += 5
        original_y = self.text_rect[1]
        self.text_rect[1] += 2
        if self.formatted_text:
            for text_line in range(len(self.formatted_text)):
                text_x = 0
                if self.justify == "center":
                    text_x = (self.text_rect[2] - self.formatted_text[text_line].get_width()) / 2
                self.text_rect[0] += text_x
                screen.blit(self.formatted_text[text_line], self.text_rect)
                self.text_rect[0] += self.formatted_text[text_line].get_width()
                if len(self.formatted_text) > text_line + 1:
                    self.text_rect[1] += self.formatted_text[text_line].get_height()
                self.text_rect[0] -= text_x + self.formatted_text[text_line].get_width()
            if self.justify == "left":
                self.text_rect[0] -= 5
            self.text_rect[1] = original_y
        super().update(screen)


class Button(TextObject):
    def __init__(self, command=None, focus_command=None, width=1, **kwargs):
        super().__init__(width=width, **kwargs)
        self.command = command
        self.focus_state_command = focus_command
        self.focus_state = False
        self.active_state = True

    def activate(self, given_object):
        if self.command is not None:
            try:
                self.command(given_object)
            except TypeError:
                self.command()

    def focus(self, pos):
        if self.focus_state_command is not None:
            self.focus_state_command(self, pos)


class TextInput(TextObject):
    def __init__(self, app, limit=0, restriction=None, width=1, **kwargs):
        super().__init__(width=width, **kwargs)
        self.app = app
        self.limit = limit
        self.restriction = restriction
        self.focus_state = False
        self.key_dict = {
            "`": "~", "1": "!", "2": "@", "3": "#", "4": "$", "5": "%", "6": "^", "7": "&", "8": "*", "9": "(",
            "0": ")", "-": "_", "=": "+", "[": "{", "]": "}", ";": ":", "'": '"', "\\": "|", ",": "<", ".": ">",
            "/": "?"
        }
        self.active_ticks = 0
        self.active_state = True

    def render(self, given_screen):
        super().render(given_screen)
        if self.focus_state:
            self.active_ticks += self.app.clock.get_time()
            if self.active_ticks / 1000 > 1:
                self.active_state = not self.active_state
                self.active_ticks %= 1000
            if self.active_state:
                given_screen.blit(
                    self.font.render("|", True, self.fg_color),
                    (self.text_rect[0] + sum([text_line.get_width() for text_line in self.formatted_text], 3),
                     self.text_rect[1])
                )
        else:
            self.active_state = False

    def key_input(self, event, mods):
        if self.focus_state:
            key_name = pygame.key.name(event.key)
            if len(self.text) < self.limit or self.limit == 0:
                if (self.restriction is not None and key_name in self.restriction) or self.restriction is None:
                    if key_name in string.ascii_letters:
                        if not mods & pygame.KMOD_LSHIFT:
                            self.text += key_name
                        elif mods & pygame.KMOD_LSHIFT:
                            self.text += key_name.upper()
                    elif key_name in self.key_dict:
                        if not mods & pygame.KMOD_LSHIFT:
                            self.text += key_name
                        elif mods & pygame.KMOD_LSHIFT:
                            self.text += self.key_dict[key_name]
                    elif key_name == "space":
                        self.text += " "
            if key_name == "backspace":
                self.text = self.text[:-1]


if __name__ == "__main__":
    App()
    